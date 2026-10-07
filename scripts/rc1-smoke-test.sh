#!/bin/bash
# RC1 Smoke Test Script
# Validates Earth Intelligence OS RC1 deployment

set -e  # Exit on error

echo "=========================================="
echo "Earth Intelligence OS RC1 Smoke Test"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=$3
    
    echo -n "Testing $name... "
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$status" = "$expected_status" ]; then
        echo -e "${GREEN}PASS${NC} (HTTP $status)"
        ((PASSED++))
    else
        echo -e "${RED}FAIL${NC} (HTTP $status, expected $expected_status)"
        ((FAILED++))
    fi
}

# Test JSON response
test_json_response() {
    local name=$1
    local url=$2
    local key=$3
    
    echo -n "Testing $name... "
    
    response=$(curl -s "$url" 2>/dev/null)
    
    if echo "$response" | grep -q "$key"; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}FAIL${NC} (key '$key' not found)"
        ((FAILED++))
    fi
}

echo "1. API Health Checks"
echo "--------------------"
test_endpoint "Health endpoint" "http://localhost:8000/health" "200"
test_endpoint "Ready endpoint" "http://localhost:8000/ready" "200"
test_endpoint "Version endpoint" "http://localhost:8000/version" "200"
echo ""

echo "2. Live Data Endpoints (Demo Mode)"
echo "-----------------------------------"
# Enable demo mode
curl -s -X POST http://localhost:8000/api/v1/live/demo/enable > /dev/null 2>&1

test_endpoint "Aircraft endpoint" "http://localhost:8000/api/v1/live/aircraft" "200"
test_endpoint "Military aircraft endpoint" "http://localhost:8000/api/v1/live/military-aircraft" "200"
test_endpoint "Vessels endpoint" "http://localhost:8000/api/v1/live/vessels" "200"
test_endpoint "Satellites endpoint" "http://localhost:8000/api/v1/live/satellites" "200"
test_endpoint "Earthquakes endpoint" "http://localhost:8000/api/v1/live/earthquakes" "200"
test_endpoint "Fires endpoint" "http://localhost:8000/api/v1/live/fires" "200"
test_endpoint "Provider health endpoint" "http://localhost:8000/api/v1/live/provider-health" "200"
echo ""

echo "3. Demo Data Validation"
echo "-----------------------"
test_json_response "Aircraft data present" "http://localhost:8000/api/v1/live/aircraft" "DEMO001"
test_json_response "Military aircraft present" "http://localhost:8000/api/v1/live/military-aircraft" "DUKE01"
test_json_response "Vessel data present" "http://localhost:8000/api/v1/live/vessels" "DEMO CONTAINER"
test_json_response "Satellite data present" "http://localhost:8000/api/v1/live/satellites" "ISS"
test_json_response "Earthquake data present" "http://localhost:8000/api/v1/live/earthquakes" "Tokyo"
test_json_response "Fire data present" "http://localhost:8000/api/v1/live/fires" "DEMO"
echo ""

echo "4. European Space Federation"
echo "-----------------------------"
test_endpoint "Space providers endpoint" "http://localhost:8000/api/v1/space/providers" "200"
test_endpoint "Space missions endpoint" "http://localhost:8000/api/v1/space/missions" "200"
test_json_response "Copernicus provider" "http://localhost:8000/api/v1/space/providers" "COPERNICUS_CDSE"
test_json_response "ESA provider" "http://localhost:8000/api/v1/space/providers" "ESA_EARTH_OBSERVATION"
echo ""

echo "5. Satellite Pass Prediction"
echo "-----------------------------"
echo -n "Testing pass prediction API... "
response=$(curl -s -X POST "http://localhost:8000/api/v1/live/satellites/pass?latitude=37.7749&longitude=-122.4194&altitude=10&norad_id=25544&hours=24&min_elevation=10" 2>/dev/null)

if echo "$response" | grep -q "norad_id"; then
    echo -e "${GREEN}PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    ((FAILED++))
fi
echo ""

echo "6. Demo Mode Controls"
echo "---------------------"
test_endpoint "Demo status endpoint" "http://localhost:8000/api/v1/live/demo/status" "200"
test_json_response "Demo mode enabled" "http://localhost:8000/api/v1/live/demo/status" "demo_mode"

# Disable demo mode
curl -s -X POST http://localhost:8000/api/v1/live/demo/disable > /dev/null 2>&1
test_json_response "Demo mode disabled" "http://localhost:8000/api/v1/live/demo/status" "demo_mode"
echo ""

echo "7. Frontend"
echo "-----------"
test_endpoint "Control Room frontend" "http://localhost:3000" "200"
echo ""

echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo ""
    echo "Earth Intelligence OS RC1 is ready for human testing."
    echo ""
    echo "Next steps:"
    echo "1. Open http://localhost:3000 in your browser"
    echo "2. Follow the testing guide: docs/runbooks/TRY-RC1.md"
    echo ""
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    echo ""
    echo "Please check the logs and ensure all services are running:"
    echo "  docker compose ps"
    echo "  docker compose logs"
    echo ""
    exit 1
fi
