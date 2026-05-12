---
name: cred-edit
description: Modifier un credential existant
---

# /cred-edit - Modifier un Credential

## Comportement

1. **Lire le credential** existant `data/registry/{slug}.md`

2. **Demander ce qui doit changer** :
   - `/cred-edit beszel` : menu interactif des champs modifiables
   - `/cred-edit beszel --password` : changer uniquement le mot de passe
   - `/cred-edit beszel --host 192.168.1.163` : changer un champ specifique

3. **Appliquer les modifications** au frontmatter et/ou body

4. **Logger le changement** via Add-RotationLog si le password a change

5. **Mettre a jour l'index** via Update-CredentialIndex

6. **Confirmer** avec diff avant/apres

## Format de sortie

```
# Credential modifie : {slug}

## Changements
| Champ | Avant | Apres |
|-------|-------|-------|
| host | 192.168.1.162 | 192.168.1.163 |

Index mis a jour.
```
