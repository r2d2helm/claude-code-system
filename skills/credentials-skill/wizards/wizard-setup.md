---
name: wizard-setup
description: Migration initiale depuis vm100-credentials.md vers le registre structure
---

# Wizard Setup - Migration Initiale

## Prerequis
- Fichier source : `C:\Users\r2d2\Documents\claude-config-backup\vm100-credentials.md`
- Module CredentialRegistry.psm1 charge

## Questions

1. **Confirmer la source** : Utiliser `vm100-credentials.md` comme source principale ?
2. **Scope** : Migrer tous les credentials ou seulement certaines categories ?
3. **Rotation interval par defaut** : 90 jours pour tous, ou personnaliser par service ?

## Processus

### Etape 1 : Parser le fichier source
1. Lire `vm100-credentials.md` via Bash (pas Read tool, fichier sensible)
   ```
   powershell.exe -NoProfile -Command "Get-Content '$HOME\Documents\claude-config-backup\vm100-credentials.md'"
   ```
2. Identifier les blocs de credentials (sections par service)
3. Extraire : service, host, port, username, password, notes

### Etape 2 : Mapper vers le schema
Pour chaque credential trouve :
- Generer un slug (kebab-case du nom de service)
- Determiner la category (monitoring, database, api, ssh, web, bot, infra, oauth)
- Determiner le auth_type (password, apikey, token, ssh-key, oauth)
- Associer la VM
- Determiner la criticality

### Etape 3 : Creer les fichiers individuels
Pour chaque credential :
1. Creer `data/registry/{slug}.md` avec le frontmatter complet
2. Remplir le body (Access, Container, Rotation Notes)
3. Confirmer chaque creation

### Etape 4 : Generer l'index
```
powershell.exe -NoProfile -Command "
Import-Module '$HOME\.claude\skills\credentials-skill\scripts\CredentialRegistry.psm1' -Force
Update-CredentialIndex
"
```

### Etape 5 : Premier audit
- Executer `/cred-status` pour verifier la migration
- Executer `/cred-audit` pour le premier score de sante

## Validation
- Nombre de fichiers crees == nombre de credentials dans la source
- Index _index.json coherent
- Aucun doublon de slug
- Tous les champs obligatoires remplis

## Rollback
- Si la migration echoue, les fichiers individuels peuvent etre supprimes
- Le fichier source original n'est jamais modifie
