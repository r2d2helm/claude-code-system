---
name: mon-wizard alert-rule
description: Creer une regle d'alerte Beszel
---

# Wizard : Creer une Regle d'Alerte

## Questions

1. **Quel systeme ?** (vm100, proxmox, windows, all)
2. **Quel type de metrique ?** (cpu, memory, disk, status)
3. **Quel seuil ?** (ex: >90%)
4. **Quelle duree ?** (ex: 5 min)
5. **Quelle severite ?** (warning, critical)
6. **Canaux de notification ?** (ntfy, telegram, both)

## Implementation via API Beszel

```bash
TOKEN=$(curl -s -X POST http://192.168.1.162:8091/api/collections/_superusers/auth-with-password \
  -H 'Content-Type: application/json' \
  -d '{"identity":"<email>","password":"<password>"}' | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

curl -X POST http://192.168.1.162:8091/api/collections/alerts/records \
  -H "Content-Type: application/json" \
  -H "Authorization: $TOKEN" \
  -d '{
    "system": "<system_id>",
    "name": "<alert_name>",
    "metric": "<cpu|memory|disk>",
    "threshold": <value>,
    "duration": <minutes>
  }'
```

## Regles recommandees

| Regle | Metrique | Seuil | Duree | Severite |
|-------|----------|-------|-------|----------|
| CPU High | cpu | >90% | 5 min | Warning |
| RAM High | memory | >85% | 5 min | Warning |
| Disk Full | disk | >80% | 0 | Warning |
| Disk Critical | disk | >90% | 0 | Critical |
| Host Down | status | down | 0 | Critical |
