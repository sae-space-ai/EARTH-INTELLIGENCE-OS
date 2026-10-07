-- PostgreSQL initialization for Earth Intelligence OS
-- Enables PostGIS and pgvector extensions

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify extensions
SELECT PostGIS_Version();
SELECT extname FROM pg_extension WHERE extname IN ('postgis', 'vector');
