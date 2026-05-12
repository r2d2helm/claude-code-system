---
service: "{SERVICE_NAME}"
slug: "{SLUG}"
category: "{CATEGORY}"
host: "{HOST}"
port: "{PORT}"
protocol: "{PROTOCOL}"
vm: "{VM}"
criticality: medium
auth_type: password
created: "{DATE}"
last_rotated: "{DATE}"
rotation_interval_days: 90
last_validated: null
validation_status: untested
tags: []
---

# {SERVICE_NAME}

## Access
- **URL**: {PROTOCOL}://{HOST}:{PORT}
- **Username**: {USERNAME}
- **Password**: {PASSWORD}

## Container
- **Compose**: {COMPOSE_PATH}

## Rotation Notes
- {ROTATION_NOTES}
