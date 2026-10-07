# Third-Party Licenses & Attribution

Earth Intelligence OS integrates capabilities inspired by God's Eye View (MIT-licensed code). This document tracks all third-party data, assets, and their licenses.

## Code License
- **Earth Intelligence OS**: Proprietary (all rights reserved)
- **God's Eye View**: MIT License (code only)

## Data Sources & Licenses

### Live Data (Runtime Fetched)

| Source | License | Commercial Use | Attribution Required |
|--------|---------|----------------|---------------------|
| OpenSky Network | Non-commercial research/education | ❌ Contact OpenSky | Yes |
| adsb.lol | ODbL 1.0 | ✅ (share-alike) | Yes |
| AISStream | Free beta, no formal ToS | ✅ (courtesy) | Yes |
| CelesTrak | US government, no license | ✅ | Citation requested |
| USGS Earthquakes | US public domain | ✅ | Courtesy |
| NASA FIRMS | US public domain (CC0) | ✅ | Acknowledgement |
| NOAA GFS/ECMWF | US public domain / CC BY 4.0 | ✅ | Attribution |
| NOAA nowCOAST | NOAA disclaimer | ✅ | Attribution |
| NHC/CPHC Cyclones | NWS public-data terms | ✅ | Attribution |
| Launch Library 2 | The Space Devs ToS | ✅ | Courtesy |
| Esri World Imagery | Esri Master Agreement | ✅ (public apps) | Yes |
| OpenStreetMap | ODbL 1.0 | ✅ (share-alike) | Yes |
| Radio Browser | PDDL 1.0 | ✅ | Attribution |
| OSRM/FOSSGIS | FOSSGIS usage policy | ✅ (restrictions) | Attribution + link |
| Photon (komoot) | Fair use, ODbL 1.0 data | ✅ | Attribution |
| TomTom | Proprietary (BYOK) | ✅ (your key) | Yes |
| Google Maps | Proprietary (BYOK) | ✅ (your key) | Yes |
| Cesium ion | Proprietary (BYOK) | ✅ (your key) | Yes |

### CCTV Camera Sources

| Source | License | Notes |
|--------|---------|-------|
| City of Austin | Open Data Terms | Public cameras |
| TxDOT | Public traffic data | Texas cameras |
| TfL (London) | TfL Open Data terms | Attribution required |
| Ontario 511 | Open Gov Licence Ontario | Attribution required |
| Fintraffic (Finland) | CC BY 4.0 | Attribution required |
| DriveBC (Canada) | Open Gov Licence BC | Attribution required |
| DelDOT (Delaware) | Public traffic data | Includes HLS video |
| Live Traffic NSW | CC BY 4.0 | Attribution required |
| Caltrans (California) | Public traffic data | California cameras |
| Tallinn (Estonia) | Public traffic data | Intersection cameras |
| Tarktee (Estonia) | Public road data | Weather cameras |
| Calgary | Open Gov Licence Calgary | Attribution required |
| Statens vegvesen (Norway) | NLOD 2.0 | Attribution required |

### Bundled Datasets

| Dataset | License | Commercial Use | Notes |
|---------|---------|----------------|-------|
| Datacenters (OSM) | ODbL 1.0 | ✅ | Share-alike |
| Dams (OSM/OpenInfraMap) | ODbL 1.0 | ✅ | Share-alike |
| Military Area Names | ODbL 1.0 | ✅ | Overture/OSM |
| **Submarine Cables (TeleGeography)** | **CC BY-NC-SA 3.0** | **❌ NON-COMMERCIAL** | **Must remove for commercial use** |
| Natural Earth Regions | Public domain | ✅ | No restrictions |
| SF Neighborhoods (DataSF) | PDDL 1.0 | ✅ | Public domain |
| US Census Counties | Public domain | ✅ | No restrictions |

### European Space Federation Data

| Provider | Access Policy | Notes |
|----------|---------------|-------|
| Copernicus CDSE | FREE_REGISTRATION_REQUIRED | Sentinel data |
| ESA Earth Observation | FREE_REGISTRATION_REQUIRED | Various missions |
| EUMETSAT | FREE_REGISTRATION_REQUIRED | Meteorological |
| Destination Earth | FREE_REGISTRATION_REQUIRED | Digital twin |
| Galileo | OPEN_ANONYMOUS (OS) / RESTRICTED (PRS) | Navigation |
| EGNOS | OPEN_ANONYMOUS | Augmentation |
| ESA Space Weather | OPEN_ANONYMOUS | Space environment |
| EU SST | RESTRICTED | Space surveillance |

## Attribution Requirements

All attributions must be displayed in the application:
- On-globe credits (Cesium credit display)
- Data attribution popover
- Per-layer source badges
- Provider status panel

## License Compliance Actions

### For Commercial Deployment:
1. ❌ **DELETE** `telegeography_submarine_cables/` (CC BY-NC-SA)
2. ✅ Keep all ODbL datasets with attribution + share-alike
3. ✅ Keep all public domain datasets
4. ✅ Obtain OpenSky commercial license if using flight data
5. ✅ Configure your own API keys for metered services

### For Open Source / Non-Commercial:
1. ✅ All datasets can be used with proper attribution
2. ✅ Maintain share-alike obligations for ODbL data
3. ✅ Respect provider rate limits and terms

## Privacy Boundaries

Earth Intelligence OS enforces these privacy boundaries:
- ❌ No face recognition
- ❌ No person identification
- ❌ No private camera discovery
- ❌ No private license plate records
- ❌ No private surveillance access
- ❌ No weapon targeting
- ✅ Public aircraft/vessel/satellite data (lawful broadcast)
- ✅ Public camera infrastructure (published locations)
- ✅ Mapped ALPR infrastructure (OSM tags only, no plate data)

## God's Eye View Attribution

Earth Intelligence OS capability architecture was informed by analysis of:
- **God's Eye View** by Bilawal Sidhu & Sameh Khamis at Halfpixel
- License: MIT (code only)
- URL: https://github.com/bilawalsidhu/gods-eye-view
- Commit: e685449a52550775a5279cef1b9090ef24d507a2

No code, assets, or branding from God's Eye View was copied.
All functionality is independently implemented with original architecture.
