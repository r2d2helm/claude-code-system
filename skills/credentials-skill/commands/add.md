---
name: cred-add
description: Ajouter un nouveau credential au registre
---

# /cred-add - Ajouter un Credential

## Comportement

1. **Collecter les informations** via questions interactives :
   - Service name (ex: "Beszel Hub")
   - Slug (auto-genere depuis le nom, ex: "beszel")
   - Category : monitoring | database | api | ssh | web | bot | infra | oauth
   - Host (IP ou hostname)
   - Port
   - Protocol : http | https | ssh | tcp | postgres | mysql
   - VM : vm100 | vm103 | vm104 | vm105 | proxmox | windows | other
   - Auth type : password | apikey | jwt | ssh-key | token | oauth | none
   - Criticality : critical | high | medium | low
   - Username
   - Password/Token/Key
   - Rotation interval (defaut: 90 jours)
   - Compose path (optionnel)
   - Rotation notes (optionnel)

2. **Verifier l'unicite** du slug dans le registre existant

3. **Creer le fichier** `data/registry/{slug}.md` avec le template rempli

4. **Mettre a jour l'index** via :
   ```
   powershell.exe -NoProfile -Command "Import-Module scripts/CredentialRegistry.psm1; Update-CredentialIndex"
   ```

5. **Confirmer** la creation avec un resume

## Format de sortie

```
# Credential ajoute

| Propriete | Valeur |
|-----------|--------|
| Service | {service} |
| Slug | {slug} |
| File | data/registry/{slug}.md |

Index mis a jour : X entries total.
```
