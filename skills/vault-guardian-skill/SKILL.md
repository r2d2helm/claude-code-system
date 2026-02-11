---
name: vault-guardian-skill
description: "Maintenance proactive du vault : health checks, auto-fix, rapports. Utiliser pour diagnostiquer, corriger automatiquement, ou auditer le vault Obsidian."
---

# Vault Guardian Agent

Agent de maintenance proactive pour le vault Obsidian Knowledge. Surveille la sante, corrige les problemes courants automatiquement, et genere des rapports periodiques.

## Commandes

| Commande | Description |
|----------|-------------|
| `/guardian-health` | Rapport de sante complet du vault |
| `/guardian-fix` | Auto-correction des problemes detectes |
| `/guardian-report` | Generer rapport hebdomadaire |
| `/guardian-schedule` | Configurer maintenance planifiee |

## Fonctionnalites

### Health Check Complet
- Comptage notes, liens, tags
- Detection liens casses
- Detection notes orphelines (sans liens entrants/sortants)
- Verification frontmatter YAML
- Detection doublons
- Analyse taille et encodage
- Score de sante 0-10

### Auto-Fix
- Correction liens casses vers notes renommees
- Ajout frontmatter manquant avec inference type/tags
- Nettoyage notes vides
- Normalisation tags (flat -> hierarchique)
- Normalisation status (captured -> seedling)

### Rapport Hebdomadaire
- Evolution du score de sante
- Notes ajoutees/modifiees cette semaine
- Problemes detectes et corrections appliquees
- Recommandations d'amelioration
- Metriques : densite graphe, taux orphelins, couverture frontmatter

### Maintenance Planifiee
- Quick check quotidien (30s) : liens casses, notes vides
- Nettoyage hebdomadaire (2min) : orphelins, doublons, tags
- Audit mensuel complet (5min) : tout + rapport detaille

## Integration

- Utilise le MCP Server knowledge-assistant pour les recherches
- Appelle Build-NotesIndex.ps1 pour rafraichir l'index
- Interagit avec obsidian-skill pour les corrections
- Logs dans knowledge-watcher-skill/data/logs/

## Vault Path

```
C:\Users\r2d2\Documents\Knowledge
```

## Conventions

- UTF-8 sans BOM pour .md et .json
- Frontmatter YAML obligatoire : title, date, type, status, tags
- Status : seedling | growing | evergreen
- Tags hierarchiques : domaine/sous-domaine
- Nommage : C_ (concepts), YYYY-MM-DD_Conv_ (conversations), YYYY-MM-DD (daily)

## Scripts

### Windows (PowerShell)

```powershell
# Health check
.\scripts\Invoke-VaultGuardian.ps1 -Mode health

# Auto-fix
.\scripts\Invoke-VaultGuardian.ps1 -Mode fix

# Rapport complet
.\scripts\Invoke-VaultGuardian.ps1 -Mode report

# Check rapide
.\scripts\Invoke-VaultGuardian.ps1 -Mode quick
```

### Linux (Bash)

Equivalent bash disponible dans `scripts/invoke-vault-guardian.sh` :

```bash
# Health check
./scripts/invoke-vault-guardian.sh health

# Auto-fix
./scripts/invoke-vault-guardian.sh fix

# Rapport complet
./scripts/invoke-vault-guardian.sh report

# Check rapide
./scripts/invoke-vault-guardian.sh quick
```

#### Prerequis Linux

- jq (`sudo apt install jq`)
- bc (generalement pre-installe)
- Vault Obsidian accessible

#### Variable d'environnement

```bash
# Definir le chemin du vault (optionnel, sinon lit depuis config)
export VAULT_PATH="/chemin/vers/vault"
./scripts/invoke-vault-guardian.sh health
```
