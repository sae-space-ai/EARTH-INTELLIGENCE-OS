-- PostgreSQL initialization for Earth Intelligence OS
-- Enables PostGIS and pgvector extensions

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify extensions
SELECT PostGIS_Version();
SELECT extname, extversion FROM pg_extension WHERE extname IN ('postgis', 'vector');

-- Create federation tables
CREATE TABLE IF NOT EXISTS space_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    organization_type VARCHAR(100),
    country_or_region VARCHAR(100),
    base_url TEXT,
    documentation_url TEXT,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    capabilities JSONB DEFAULT '[]'::jsonb,
    access_policy JSONB,
    last_catalog_sync TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS external_missions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES space_providers(id),
    mission_code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    programme VARCHAR(255),
    operator VARCHAR(255),
    lifecycle_status VARCHAR(50) NOT NULL,
    launch_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    documentation_url TEXT,
    capabilities JSONB DEFAULT '[]'::jsonb,
    access_policy JSONB,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(provider_id, mission_code)
);

CREATE TABLE IF NOT EXISTS external_spacecraft (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES space_providers(id),
    mission_id UUID REFERENCES external_missions(id),
    external_id VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    norad_id INTEGER,
    cospar_id VARCHAR(50),
    lifecycle_status VARCHAR(50) NOT NULL,
    launch_date TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS external_instruments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES space_providers(id),
    mission_id UUID REFERENCES external_missions(id),
    spacecraft_id UUID REFERENCES external_spacecraft(id),
    external_id VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    capabilities JSONB DEFAULT '[]'::jsonb,
    spatial_resolution VARCHAR(100),
    swath VARCHAR(100),
    frequency VARCHAR(100),
    wavelength_metadata JSONB,
    polarizations JSONB,
    spectral_bands JSONB,
    product_levels JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS external_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES space_providers(id),
    external_collection_id VARCHAR(255) NOT NULL,
    mission_id UUID REFERENCES external_missions(id),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    sensor_types JSONB DEFAULT '[]'::jsonb,
    temporal_extent JSONB,
    spatial_extent JSONB,
    processing_level VARCHAR(50),
    license_metadata JSONB,
    access_policy JSONB,
    capabilities JSONB DEFAULT '[]'::jsonb,
    canonical_url TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(provider_id, external_collection_id)
);

CREATE TABLE IF NOT EXISTS external_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES space_providers(id),
    external_service_id VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    description TEXT,
    capabilities JSONB DEFAULT '[]'::jsonb,
    base_url TEXT,
    documentation_url TEXT,
    access_policy JSONB,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    metadata JSONB DEFAULT '{}'::jsonb,
    last_verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS space_environment_observations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES space_providers(id),
    observed_at TIMESTAMPTZ NOT NULL,
    valid_from TIMESTAMPTZ,
    valid_to TIMESTAMPTZ,
    knowledge_state VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    variable VARCHAR(255) NOT NULL,
    value DOUBLE PRECISION,
    unit VARCHAR(50),
    confidence DOUBLE PRECISION CHECK (confidence >= 0 AND confidence <= 1),
    source_asset TEXT,
    provenance_metadata JSONB,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS catalog_sync_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES space_providers(id),
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    status VARCHAR(50) NOT NULL,
    collections_discovered INTEGER DEFAULT 0,
    collections_updated INTEGER DEFAULT 0,
    missions_discovered INTEGER DEFAULT 0,
    spacecraft_discovered INTEGER DEFAULT 0,
    services_discovered INTEGER DEFAULT 0,
    errors JSONB DEFAULT '[]'::jsonb,
    provider_cursor TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for federation
CREATE INDEX IF NOT EXISTS idx_space_providers_code ON space_providers(code);
CREATE INDEX IF NOT EXISTS idx_external_missions_provider ON external_missions(provider_id);
CREATE INDEX IF NOT EXISTS idx_external_missions_status ON external_missions(lifecycle_status);
CREATE INDEX IF NOT EXISTS idx_external_spacecraft_mission ON external_spacecraft(mission_id);
CREATE INDEX IF NOT EXISTS idx_external_instruments_mission ON external_instruments(mission_id);
CREATE INDEX IF NOT EXISTS idx_external_instruments_spacecraft ON external_instruments(spacecraft_id);
CREATE INDEX IF NOT EXISTS idx_external_collections_provider ON external_collections(provider_id);
CREATE INDEX IF NOT EXISTS idx_external_collections_mission ON external_collections(mission_id);
CREATE INDEX IF NOT EXISTS idx_external_services_provider ON external_services(provider_id);
CREATE INDEX IF NOT EXISTS idx_space_env_obs_provider ON space_environment_observations(provider_id);
CREATE INDEX IF NOT EXISTS idx_space_env_obs_category ON space_environment_observations(category);
CREATE INDEX IF NOT EXISTS idx_space_env_obs_observed_at ON space_environment_observations(observed_at);
CREATE INDEX IF NOT EXISTS idx_catalog_sync_provider ON catalog_sync_runs(provider_id);
CREATE INDEX IF NOT EXISTS idx_catalog_sync_status ON catalog_sync_runs(status);
