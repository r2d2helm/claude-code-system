---
name: cred-show
description: Afficher les details d un credential
---

# /cred-show - Details d'un Credential

## Comportement

1. **Lire le fichier** `data/registry/{slug}.md` via Bash + PowerShell :
   ```
   powershell.exe -NoProfile -Command "Import-Module scripts/CredentialRegistry.psm1; Get-CredentialEntry -Slug '{slug}'"
   ```

2. **Afficher le frontmatter** complet et le body

3. **Par defaut** : masquer le mot de passe avec `****`
   - `/cred-show beszel` : mot de passe masque
   - `/cred-show beszel --reveal` : afficher le mot de passe en clair

4. **Calculer les metriques** :
   - Age du credential (jours depuis created)
   - Jours depuis derniere rotation
   - Jours avant prochaine rotation (rotation_interval_days - age depuis last_rotated)
   - Statut validation

## Format de sortie

```
# Credential: {service}

| Propriete | Valeur |
|-----------|--------|
| Slug | {slug} |
| Category | {category} |
| Host | {host}:{port} |
| VM | {vm} |
| Protocol | {protocol} |
| Auth Type | {auth_type} |
| Criticality | {criticality} |
| URL | {protocol}://{host}:{port} |
| Username | {username} |
| Password | **** |
| Created | {created} (X jours) |
| Last Rotated | {last_rotated} (X jours) |
| Next Rotation | dans X jours |
| Validation | {validation_status} ({last_validated}) |

## Rotation Notes
{rotation_notes}

## Container
{container_info}
```
