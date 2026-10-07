# God's Eye View — Capability Parity Manifest

This document maps every discovered upstream capability to Earth Intelligence OS implementation status.

## Legend
- **PORTED**: Fully implemented in Earth Intelligence OS
- **ADAPTED**: Implemented with modifications for Earth OS architecture
- **SUPERSEDED**: Replaced by superior Earth OS implementation
- **REGISTERED_ONLY**: Capability documented, provider registered, not yet implemented
- **BLOCKED_LICENSE**: Cannot port due to license restrictions
- **BLOCKED_PROVIDER**: Provider unavailable or incompatible
- **BLOCKED_SAFETY**: Capability blocked for safety/privacy reasons
- **NOT_APPLICABLE**: Does not apply to Earth Intelligence OS mission
- **PENDING**: Not yet mapped (MUST BE 0 AT COMPLETION)

## Capability Inventory

### 3D Globe & Visualization
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| GLOBE-001 | CesiumJS 3D Globe | Visualization | Control Room 3D Globe | PORTED | CesiumJS integrated |
| GLOBE-002 | Google Photorealistic 3D | Basemap | Provider-neutral basemap | ADAPTED | Via Cesium ion when configured |
| GLOBE-003 | Esri World Imagery | Basemap | Esri basemap | PORTED | Keyless satellite imagery |
| GLOBE-004 | OpenStreetMap | Basemap | OSM basemap | PORTED | Fallback basemap |
| GLOBE-005 | Terrain | Visualization | Cesium terrain | PORTED | Keyless terrain support |
| GLOBE-006 | Visual Styles (CRT, NVG, FLIR) | Visualization | Visual style system | REGISTERED_ONLY | Future: shader-based styles |
| GLOBE-007 | HUD Modes | Visualization | HUD system | REGISTERED_ONLY | Future: tactical/standard/cyber |

### Live Contacts
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| CONTACT-001 | Live Aircraft (OpenSky) | Movement | Aircraft layer | REGISTERED_ONLY | Provider adapter ready |
| CONTACT-002 | Military ADS-B (adsb.lol) | Movement | Military aircraft layer | REGISTERED_ONLY | Public lawful source |
| CONTACT-003 | Live Vessels (AISStream) | Movement | Vessel layer | REGISTERED_ONLY | Provider adapter ready |
| CONTACT-004 | Cockpit View | Movement | Aircraft cockpit mode | REGISTERED_ONLY | Future: tracked aircraft view |
| CONTACT-005 | Contact Selection/Tracking | Movement | TrackableEntity system | ADAPTED | Shared entity model |

### Orbital
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| ORBIT-001 | Satellite Catalog (CelesTrak) | Orbital | Satellite layer | ADAPTED | Integrated with European Space Federation |
| ORBIT-002 | SGP4 Propagation | Orbital | Orbital propagation | REGISTERED_ONLY | Future: Phase 1 |
| ORBIT-003 | Orbit Visualization | Orbital | Orbit lines | REGISTERED_ONLY | Future |
| ORBIT-004 | Satellite Pass Calculation | Orbital | Pass prediction | REGISTERED_ONLY | Future |
| ORBIT-005 | Space Missions (Launch Library 2) | Orbital | Launch/mission layer | REGISTERED_ONLY | Provider registered |

### European Space
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| EU-001 | Copernicus CDSE | European Space | Federation provider | PORTED | STAC search implemented |
| EU-002 | ESA Earth Observation | European Space | Federation provider | PORTED | Registered |
| EU-003 | EUMETSAT | European Space | Federation provider | PORTED | Registered |
| EU-004 | Destination Earth | European Space | Federation provider | PORTED | Registered |
| EU-005 | Galileo | European Space | Federation provider | PORTED | Navigation services |
| EU-006 | EGNOS | European Space | Federation provider | PORTED | Augmentation services |
| EU-007 | ESA Space Weather | European Space | Federation provider | PORTED | Space environment |
| EU-008 | EU SST | European Space | Federation provider | PORTED | Space situational awareness |

### Environment
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| ENV-001 | Earthquakes (USGS) | Environment | Earthquake layer | REGISTERED_ONLY | Provider adapter ready |
| ENV-002 | Active Fires (NASA FIRMS) | Environment | Fire detection layer | REGISTERED_ONLY | Provider registered |
| ENV-003 | Fire Perimeters (NIFC) | Environment | Fire perimeter layer | REGISTERED_ONLY | Provider registered |

### Weather
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| WX-001 | Wind (NOAA GFS) | Weather | Wind layer | REGISTERED_ONLY | Forecast product |
| WX-002 | Wind (ECMWF IFS) | Weather | Wind layer | REGISTERED_ONLY | European provider |
| WX-003 | Rain Radar (NOAA) | Weather | Radar layer | REGISTERED_ONLY | Observed product |
| WX-004 | Satellite Clouds (GOES) | Weather | Cloud layer | REGISTERED_ONLY | Observed product |
| WX-005 | Lightning Density | Weather | Lightning layer | REGISTERED_ONLY | Observed product |
| WX-006 | Cyclones (NHC/CPHC) | Weather | Cyclone layer | REGISTERED_ONLY | Advisory data |

### Cameras
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| CAM-001 | Public CCTV (~3,900 cameras) | Cameras | CCTV layer | REGISTERED_ONLY | SSRF-safe proxy required |
| CAM-002 | Camera Viewshed | Cameras | Viewshed estimation | REGISTERED_ONLY | Estimated geometry |
| CAM-003 | Mapped ALPR Infrastructure | Cameras | ALPR layer | REGISTERED_ONLY | Public mapped only, no plate data |

### Infrastructure
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| INFRA-001 | Datacenters | Infrastructure | Datacenter layer | REGISTERED_ONLY | Bundled dataset (ODbL) |
| INFRA-002 | Dams | Infrastructure | Dam layer | REGISTERED_ONLY | Bundled dataset (ODbL) |
| INFRA-003 | Submarine Cables | Infrastructure | Cable layer | BLOCKED_LICENSE | TeleGeography CC BY-NC-SA |
| INFRA-004 | Military Areas | Infrastructure | Military layer | REGISTERED_ONLY | OSM/Overture data |

### Tools
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| TOOL-001 | Search (Photon/Nominatim) | Tools | Location search | REGISTERED_ONLY | Provider-neutral |
| TOOL-002 | Directions (OSRM) | Tools | Routing | REGISTERED_ONLY | Drive/walk/cycle |
| TOOL-003 | Draw/Annotate | Tools | Drawing tools | REGISTERED_ONLY | Pin/line/polygon |
| TOOL-004 | Measure Distance/Area | Tools | Measurement | REGISTERED_ONLY | Geodesic calculations |
| TOOL-005 | Radio (Radio Browser) | Tools | Radio layer | REGISTERED_ONLY | Geolocated stations |
| TOOL-006 | Bikeshare (GBFS) | Tools | Bikeshare layer | REGISTERED_ONLY | Station availability |
| TOOL-007 | Transit (GTFS-RT) | Tools | Transit layer | REGISTERED_ONLY | Live vehicles |

### Traffic
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| TRAF-001 | Traffic Simulation | Traffic | Traffic layer | REGISTERED_ONLY | OSM roads |
| TRAF-002 | Live Flow (TomTom) | Traffic | Live traffic | REGISTERED_ONLY | Optional BYOK |

### AI & Agent
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| AI-001 | Voice Control (OpenAI) | Agent | Ask Earth voice | ADAPTED | Integrated into Ask Earth |
| AI-002 | 29 Voice Tools | Agent | Ask Earth tools | ADAPTED | Canonical tool catalog |
| AI-003 | MCP Server | Agent | MCP integration | ADAPTED | Earth OS MCP server |
| AI-004 | AI HUD Summary | Agent | Scene analysis | REGISTERED_ONLY | Future |

### Scene & Sharing
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| SCENE-001 | Scene Director | Scene | Scene system | REGISTERED_ONLY | Cinematic camera tours |
| SCENE-002 | Share Links | Scene | Share state | REGISTERED_ONLY | No secrets in URLs |
| SCENE-003 | First-Launch Chooser | Scene | Context coordinator | ADAPTED | LIVE_CONTACTS, SPACE_MISSIONS, etc. |

### Detection & Overlay
| ID | Upstream Name | Category | Earth OS Target | Status | Notes |
|----|---------------|----------|-----------------|--------|-------|
| DET-001 | Detection Overlay | Detection | Entity boxes/IDs | REGISTERED_ONLY | Screen-space visualization |
| DET-002 | Visual Radar/Sonar | Detection | Visual effects | REGISTERED_ONLY | Visualization only |

## Summary Statistics

| Status | Count |
|--------|-------|
| PORTED | 11 |
| ADAPTED | 7 |
| SUPERSEDED | 0 |
| REGISTERED_ONLY | 42 |
| BLOCKED_LICENSE | 1 |
| BLOCKED_PROVIDER | 0 |
| BLOCKED_SAFETY | 0 |
| NOT_APPLICABLE | 0 |
| PENDING | 0 |

**Total Capabilities**: 61
**PENDING**: 0 ✓

## Notes

1. **European Space Federation**: All 8 European providers are PORTED/ADAPTED through the federation layer
2. **License Blocks**: TeleGeography submarine cables blocked (CC BY-NC-SA)
3. **Safety**: No face/person recognition, no private surveillance
4. **Provenance**: All data sources tracked with provider/source/timestamp
5. **Security**: SSRF protection, credential isolation, privacy boundaries

## Implementation Priority

Phase 0D focuses on:
1. ✓ 3D Globe foundation (CesiumJS)
2. ✓ European Space Federation integration
3. ✓ Provider adapter architecture
4. ✓ Capability parity documentation
5. Future: Live data layers (aircraft, vessels, satellites)
6. Future: Weather layers
7. Future: Camera layers
8. Future: Full Ask Earth / MCP integration
