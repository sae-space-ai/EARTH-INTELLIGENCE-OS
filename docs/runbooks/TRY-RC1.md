# Try Earth Intelligence OS RC1

This guide walks you through testing Earth Intelligence OS Release Candidate 1.

---

## Prerequisites

- **Docker Desktop** installed and running
- **8GB RAM** available
- **10GB disk space** available
- **Web browser** (Chrome, Firefox, Safari, or Edge)

---

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd earth-intelligence-os

# Copy environment configuration
cp .env.example .env
```

### Optional: Add Provider API Keys

Edit `.env` and add any provider credentials you have:

```bash
# Aircraft tracking (optional - anonymous access available)
OPENSKY_USERNAME=your_username
OPENSKY_PASSWORD=your_password

# Vessel tracking (required for live data)
AISSTREAM_API_KEY=your_key

# Fire detection (required for live data)
FIRMS_MAP_KEY=your_key

# European Space (optional)
CDSE_CLIENT_ID=your_client_id
CDSE_CLIENT_SECRET=your_client_secret
```

**Note:** If you don't have API keys, you can still use **Demo Mode** (see Step 4).

---

## Step 2: Start the Application

```bash
# Start all services (this may take a few minutes on first run)
docker compose up --build
```

Wait for all services to be healthy. You should see:

```
✓ Container earth-intelligence-postgres-1    Healthy
✓ Container earth-intelligence-minio-1        Healthy
✓ Container earth-intelligence-redpanda-1     Healthy
✓ Container earth-intelligence-api-1          Healthy
✓ Container earth-intelligence-worker-1       Healthy
✓ Container earth-intelligence-control-room-1 Healthy
```

---

## Step 3: Open the Control Room

Open your web browser and navigate to:

**http://localhost:3000**

You should see the Earth Intelligence OS Control Room with a 3D globe.

---

## Step 4: Enable Demo Mode (If No API Keys)

If you don't have provider API keys, enable demo mode to see sample data:

### Option A: Via API

```bash
curl -X POST http://localhost:8000/api/v1/live/demo/enable
```

### Option B: Via UI

1. Look for a "Demo Mode" toggle in the Control Room UI
2. Click to enable demo mode
3. You should see "DEMO DATA" indicator

Demo mode provides:
- 3 aircraft
- 1 military aircraft
- 2 vessels
- 4 satellites (including ISS with real orbital data)
- 3 earthquakes
- 5 fire detections

---

## Step 5: Test Live Data Layers

### Test Aircraft Tracking

1. In the left panel, find **"Live Aircraft"** layer
2. Toggle it **ON**
3. You should see aircraft markers on the globe
4. **Click** on an aircraft to see details
5. Click **"Track"** to follow the aircraft
6. You should see a trail appear behind the aircraft

### Test Satellite Tracking

1. Find **"Satellites"** layer and toggle it **ON**
2. You should see satellite markers (these are propagated using real SGP4)
3. **Click** on a satellite to see orbital elements
4. Look for:
   - NORAD ID
   - Orbital period
   - Inclination
   - Element epoch
   - Propagation status

### Test Earthquakes

1. Find **"Earthquakes"** layer and toggle it **ON**
2. You should see earthquake markers (sized by magnitude)
3. **Click** on an earthquake to see:
   - Magnitude
   - Depth
   - Location
   - Time

### Test Active Fires

1. Find **"Active Fires"** layer and toggle it **ON**
2. You should see fire detection points
3. **Click** on a fire to see:
   - Satellite/instrument
   - Confidence level
   - Fire Radiative Power (FRP)

---

## Step 6: Test Satellite Pass Prediction

1. Select a satellite (e.g., ISS with NORAD ID 25544)
2. Look for **"Predict Pass"** button or use the API:

```bash
curl -X POST "http://localhost:8000/api/v1/live/satellites/pass?latitude=37.7749&longitude=-122.4194&altitude=10&norad_id=25544&hours=24&min_elevation=10"
```

You should see:
- Rise time and azimuth
- Culmination time and max elevation
- Set time and azimuth
- Pass duration

---

## Step 7: Test European Space Federation

1. Switch to **"European Space"** context (if available in UI)
2. Or use the API:

```bash
# List providers
curl http://localhost:8000/api/v1/space/providers

# List missions
curl http://localhost:8000/api/v1/space/missions

# Search for Sentinel-2 data
curl -X POST http://localhost:8000/api/v1/space/search \
  -H "Content-Type: application/json" \
  -d '{
    "bbox": [-10, 35, 10, 55],
    "datetime_range": {"start": "2024-01-01T00:00:00Z", "end": "2024-01-31T23:59:59Z"},
    "collections": ["sentinel-2-l2a"]
  }'
```

---

## Step 8: Test Provider Health

Check the status of all data providers:

```bash
curl http://localhost:8000/api/v1/live/provider-health
```

You should see health status for:
- OpenSky Network
- adsb.lol
- AISStream
- CelesTrak
- USGS Earthquakes
- NASA FIRMS

---

## Step 9: Test Demo/Live Mode Switching

### Switch to Live Mode

```bash
curl -X POST http://localhost:8000/api/v1/live/demo/disable
```

If you have API keys configured, you should now see real data.

### Switch Back to Demo Mode

```bash
curl -X POST http://localhost:8000/api/v1/live/demo/enable
```

You should see "DEMO DATA" indicator and sample fixtures.

---

## Step 10: Test Entity Selection and Tracking

1. **Select** any entity (aircraft, vessel, satellite, earthquake, fire)
2. Verify the details panel shows:
   - Entity type
   - Provider
   - Coordinates
   - Timestamp
   - Freshness status
   - Knowledge state (OBSERVED/INFERRED)
3. Click **"Track"** to follow the entity
4. Verify a trail appears
5. Click **"Untrack"** to stop following
6. Verify trail remains visible

---

## Step 11: Test Context Switching

If context switching is available in the UI:

1. Switch to **"Live Contacts"** context
   - Should enable aircraft, vessels, traffic layers
2. Switch to **"Space Missions"** context
   - Should enable satellites, space missions layers
3. Switch to **"Environmental"** context
   - Should enable earthquakes, fires, weather layers
4. Switch to **"European Space"** context
   - Should enable European federation layers

---

## Step 12: Verify API Health

```bash
# Health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/ready

# Version info
curl http://localhost:8000/version
```

All should return successful responses.

---

## Step 13: Check Database

Verify PostgreSQL is running with PostGIS and pgvector:

```bash
# Connect to database
docker compose exec postgres psql -U postgres -d earth_intelligence

# Check PostGIS
SELECT PostGIS_Version();

# Check pgvector
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';

# List tables
\dt

# Exit
\q
```

---

## Step 14: Check Event Bus

Verify Redpanda is running:

```bash
# Check Redpanda health
docker compose exec redpanda rpk cluster health

# List topics
docker compose exec redpanda rpk topic list
```

---

## Step 15: Check Object Storage

Verify MinIO is running:

```bash
# Open MinIO console
open http://localhost:9001

# Login with:
# Username: minioadmin
# Password: minioadmin

# Verify bucket exists
# You should see "earth-observations" bucket
```

---

## Step 16: Stop the Application

When done testing:

```bash
# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

---

## Troubleshooting

### Control Room Not Loading

```bash
# Check if control-room container is running
docker compose ps

# Check logs
docker compose logs control-room

# Restart
docker compose restart control-room
```

### API Not Responding

```bash
# Check if API container is running
docker compose ps

# Check logs
docker compose logs api

# Restart
docker compose restart api
```

### Database Connection Issues

```bash
# Check if postgres is healthy
docker compose ps postgres

# Check logs
docker compose logs postgres

# Restart
docker compose restart postgres
```

### Demo Mode Not Working

```bash
# Check demo status
curl http://localhost:8000/api/v1/live/demo/status

# Enable demo mode
curl -X POST http://localhost:8000/api/v1/live/demo/enable
```

### No Data Showing

1. Verify you're in demo mode or have API keys configured
2. Check provider health: `curl http://localhost:8000/api/v1/live/provider-health`
3. Check browser console for errors
4. Check API logs: `docker compose logs api`

---

## Expected Results

### In Demo Mode

You should see:
- ✅ 3 aircraft with callsigns DEMO001, DEMO002, DEMO003
- ✅ 1 military aircraft with callsign DUKE01
- ✅ 2 vessels (DEMO CONTAINER, DEMO TANKER)
- ✅ 4 satellites (including ISS with real TLE propagation)
- ✅ 3 earthquakes (Tokyo, Los Angeles, Santiago)
- ✅ 5 fire detections (San Francisco, Sydney, Moscow, São Paulo, Delhi)

### In Live Mode (With API Keys)

You should see:
- ✅ Real aircraft positions from OpenSky/adsb.lol
- ✅ Real vessel positions from AISStream
- ✅ Real satellite positions propagated from CelesTrak TLE
- ✅ Real earthquakes from USGS
- ✅ Real fire detections from NASA FIRMS

---

## Reporting Issues

If you encounter issues:

1. **Check the logs:**
   ```bash
   docker compose logs > logs.txt
   ```

2. **Note the steps to reproduce**

3. **Include:**
   - Docker version
   - Browser version
   - API keys configured (yes/no)
   - Demo mode (yes/no)
   - Error messages

---

## Next Steps

After testing RC1:

1. **Provide feedback** on functionality and usability
2. **Report bugs** with reproduction steps
3. **Suggest improvements** for future releases
4. **Test with live data** if you have API keys

---

## Additional Resources

- [RC1 Release Notes](../releases/RC1.md)
- [Architecture Documentation](../architecture/README.md)
- [API Documentation](http://localhost:8000/docs)
- [Security Threat Model](../security/threat-model.md)

---

**Happy Testing!** 🌍🛰️✈️🚢
