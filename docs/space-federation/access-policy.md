# Access Policy

## AccessPolicy Enum

| Value | Description |
|-------|-------------|
| OPEN_ANONYMOUS | No authentication required |
| OPEN_REGISTRATION_REQUIRED | Free, but must register |
| FREE_REGISTRATION_REQUIRED | Free with registration |
| FREE_ELIGIBLE_USERS | Free for specific user groups |
| RESTRICTED | Limited access, authorization required |
| COMMERCIAL | Paid/commercial license required |
| UNKNOWN | Policy not determined |

## Policy Metadata

Each provider/collection stores:
- license_name
- license_url
- terms_url
- registration_required
- authentication_type
- quota_information
- redistribution_allowed
- commercial_use_allowed
- access_notes
- last_verified_at

## Rules

1. Never bypass authentication
2. Never bypass eligibility checks
3. Never bypass rate limits
4. Never bypass licensing
5. Never bypass provider restrictions
6. Restricted data may be catalogued from public metadata
7. Restricted data must NOT be downloaded without authorization
