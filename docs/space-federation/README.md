# European Space Federation Layer

Earth Intelligence OS federates European space infrastructure to access external sensing and intelligence capabilities without owning them.

## Architecture

```
EUROPEAN SPACE ECOSYSTEM
        |
        v
SPACE FEDERATION LAYER
        |
        +-- Provider Registry
        +-- Mission Registry
        +-- Spacecraft Registry
        +-- Instrument Registry
        +-- Collection Registry
        +-- Service Registry
        +-- Capability Registry
        +-- Access Policy Registry
        +-- Connector Registry
        |
        v
EARTH INTELLIGENCE OS
```

## Status

| Component | Status |
|-----------|--------|
| Provider Registry | IMPLEMENTED |
| Connector Interface | IMPLEMENTED |
| CDSE Connector | IMPLEMENTED (STAC search) |
| ESA Connector | REGISTERED ONLY |
| EUMETSAT Connector | REGISTERED ONLY |
| DestinE Connector | REGISTERED ONLY |
| Galileo/EGNOS | REGISTERED ONLY |
| Space Weather | REGISTERED ONLY |
| SSA (EU SST) | REGISTERED ONLY |
| Capability Resolver | IMPLEMENTED |
| Federated Search API | IMPLEMENTED |

## Providers

See [providers.md](providers.md) for complete provider list.

## Access Policy

All external data access respects provider policies. See [access-policy.md](access-policy.md).

## API Endpoints

- `GET /api/v1/space/providers` — List providers
- `GET /api/v1/space/providers/{code}` — Get provider
- `GET /api/v1/space/missions` — List missions
- `GET /api/v1/space/provider-health` — Provider health
- `POST /api/v1/space/search` — Federated search
- `GET /api/v1/space/capabilities` — List capabilities
- `POST /api/v1/space/resolve-capability` — Resolve capability

## Documentation

- [providers.md](providers.md) — All registered providers
- [copernicus.md](copernicus.md) — Copernicus details
- [esa.md](esa.md) — ESA Earth Observation
- [eumetsat.md](eumetsat.md) — EUMETSAT meteorological
- [destination-earth.md](destination-earth.md) — DestinE digital twins
- [galileo.md](galileo.md) — Galileo navigation
- [egnos.md](egnos.md) — EGNOS augmentation
- [space-weather.md](space-weather.md) — Space weather
- [space-situational-awareness.md](space-situational-awareness.md) — SSA
- [access-policy.md](access-policy.md) — Access policies
