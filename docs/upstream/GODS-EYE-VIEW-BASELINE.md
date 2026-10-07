# God's Eye View — Upstream Baseline

## Repository Information
- **URL**: https://github.com/bilawalsidhu/gods-eye-view
- **Branch**: main
- **Latest Commit**: e685449a52550775a5279cef1b9090ef24d507a2
- **Commit Date**: October 6, 2026
- **Retrieval Date**: October 6, 2026
- **Version**: v0.2.1
- **License**: MIT (code only — third-party data has separate licenses)

## Technology Stack
- **Frontend**: Vanilla JavaScript + CesiumJS + Vite
- **Backend**: Node.js server with provider proxies
- **Voice**: OpenAI Realtime API
- **3D**: CesiumJS + Google Photorealistic 3D Tiles
- **Total Commits**: 667
- **Contributors**: 67

## Key Capabilities Discovered
- Live aircraft tracking (OpenSky, adsb.lol)
- Military ADS-B visualization
- Live vessel tracking (AISStream)
- Satellite tracking with SGP4 propagation (CelesTrak)
- Earthquake visualization (USGS)
- Active fire detection (NASA FIRMS)
- Fire perimeters (NIFC WFIGS)
- Weather: wind (NOAA GFS, ECMWF IFS), radar, clouds, lightning, cyclones
- Public CCTV cameras (~3,900 cameras worldwide)
- Mapped ALPR infrastructure (OpenStreetMap)
- Traffic simulation + live flow (TomTom)
- Public transit (GTFS-Realtime)
- Bikeshare (GBFS)
- Radio stations (Radio Browser)
- Routing (OSRM)
- Search (Google, Photon, Nominatim)
- Space missions/launches (Launch Library 2)
- Infrastructure: datacenters, dams, submarine cables
- Visual styles: CRT, NVG, FLIR, Noir, Snow, etc.
- HUD modes: standard, tactical, military
- Scene director for cinematic camera tours
- Share links with state serialization
- Voice control with 29 tools
- MCP server support
- Cockpit view for tracked aircraft
- Detection overlay
- Draw/annotate on map
- Measurement tools

## Data Sources
See DATA_SOURCES.md in upstream repository for complete attribution.

## Security Model
- Server-side credential brokering
- SSRF protection on all proxies
- No client-side secret exposure
- Privacy boundaries enforced (no face/person recognition)
- See SECURITY.md in upstream repository

## Integration Decision
Earth Intelligence OS will integrate these capabilities through:
1. Provider-neutral adapter architecture
2. European Space Federation integration
3. Provenance tracking for all data
4. Security boundaries maintained
5. Original Earth Intelligence OS branding (no GEV branding copied)
