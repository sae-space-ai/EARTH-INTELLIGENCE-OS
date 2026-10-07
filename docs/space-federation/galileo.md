# Galileo & EGNOS

## Galileo
**Status**: REGISTERED ONLY

### Services
| Service | Access | Description |
|---------|--------|-------------|
| Open Service | OPEN_ANONYMOUS | Free positioning |
| High Accuracy Service (HAS) | FREE_REGISTRATION_REQUIRED | cm-level accuracy |
| OSNMA | OPEN_ANONYMOUS | Authentication |
| Search & Rescue | RESTRICTED | COSPAS-SARSAT |
| PRS | RESTRICTED | Public Regulated Service |

### Capabilities
- POSITIONING
- NAVIGATION
- TIMING
- HIGH_ACCURACY_CORRECTIONS
- NAVIGATION_AUTHENTICATION
- SEARCH_AND_RESCUE

## EGNOS
**Status**: REGISTERED ONLY

### Services
| Service | Access | Description |
|---------|--------|-------------|
| EGNOS Open | OPEN_ANONYMOUS | Augmentation |
| EGNOS Data | OPEN_ANONYMOUS | Integrity metadata |

### Capabilities
- GNSS_AUGMENTATION
- POSITIONING
- INTEGRITY_METADATA

## Important Notes
- PRS access is RESTRICTED — no unauthorized access attempted
- Safety-critical operational usage not represented as ordinary API
- Authentication status tracking: VERIFIED, UNVERIFIED, FAILED, UNKNOWN
