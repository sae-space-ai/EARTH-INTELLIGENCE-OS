# Security Threat Model — Earth Intelligence OS

## Threat Register

| Threat | Risk | Control | Status |
|--------|------|---------|--------|
| API Compromise | High | Rate limiting, WAF, input validation, auth tokens | Planned |
| Credential Theft | High | Secret rotation, vault, no hardcoded secrets | Planned |
| Malicious Ingestion | High | Schema validation, checksum verification, quarantine | Planned |
| Data Poisoning | Critical | Provenance tracking, anomaly detection, validation | Future |
| Model Poisoning | Critical | Checkpoint SHA-256, training data validation | Future |
| Event Bus Tampering | High | TLS, authentication, schema validation | Planned |
| Object Store Modification | Critical | Immutable raw data, SHA-256, access control | Active |
| Database Compromise | Critical | Encryption at rest, access control, audit | Planned |
| Prompt Injection | High | AI boundary enforcement, no direct actuator access | Designed |
| Tool Misuse | High | Tool sandboxing, output validation, human auth | Future |
| Unauthorized Mission | Critical | Policy engine, simulation, human approval | Designed |
| Unauthorized Command | Critical | Hard AI/command boundary, no direct path | Designed |
| Supply Chain | High | Dependency pinning, SBOM, vuln scanning | Planned |
| Secrets Exposure | Critical | Vault, no env in code, pre-commit detection | Active |
| Checkpoint Tampering | Critical | SHA-256 verification, signed checkpoints | Future |

## Active Controls (Phase 0)
- Immutable raw data policy with SHA-256 checksums
- No hardcoded secrets in codebase
- Pre-commit secret detection hooks
- Structured audit logging
- AI/command boundary documented and designed
- .env.example without real credentials
- Typed configuration validation

## Planned Controls
- Vault integration for secrets management
- mTLS between services
- RBAC/IAM system
- WAF / rate limiting
- Dependency vulnerability scanning (Dependabot/Snyk)
- SBOM generation
- Encryption at rest (database + object storage)

## Future Controls
- Model checkpoint signing and verification
- Prompt injection defenses for AI layer
- Tool sandboxing for generative AI
- Full supply chain verification (SLSA)
- Data poisoning detection algorithms

## AI/Command Boundary (Critical)
```
AI Layer → Mission Planner → Digital Twin → Policy Engine → Human Auth → Flight Ops → Uplink → Spacecraft
```
- NO direct network path between AI Layer and Flight Ops/Uplink/Spacecraft
- All proposals traverse full chain with human authorization
- Enforced at network, application, and policy levels
