name: "PRP Base Template - Système r2d2"
description: |

## Purpose
Template optimisé pour que Claude Code implémente des features avec suffisamment
de contexte et de capacité d'auto-validation pour produire du code fonctionnel.

## Core Principles
1. **Context is King**: Inclure TOUTE la documentation, exemples et gotchas nécessaires
2. **Validation Loops**: Fournir des tests/vérifications exécutables
3. **Information Dense**: Utiliser les patterns et conventions du système existant
4. **Progressive Success**: Simple d'abord, valider, puis enrichir
5. **Règles globales**: Toujours respecter CLAUDE.md et les conventions du vault

---

## Goal
[Objectif précis - décrire l'état final souhaité]

## Why
- [Valeur ajoutée et impact sur le système]
- [Intégration avec les skills/fonctionnalités existants]
- [Problèmes que cela résout]

## What
[Comportement attendu et exigences techniques]

### Success Criteria
- [ ] [Résultat mesurable et spécifique]

## Contexte nécessaire

### Documentation & Références
```yaml
# MUST READ - Contexte à charger
- file: [chemin/vers/fichier]
  why: [Pattern à suivre, gotchas à éviter]

- skill: [nom-du-skill]
  why: [Conventions ou commandes à réutiliser]

- url: [URL documentation]
  why: [Sections spécifiques nécessaires]

- vault: [[[Nom-Note]]]
  why: [Contexte ou décisions antérieures]
```

### Arbre actuel du système
```
~/.claude/
├── skills/         # [décrire l'état actuel pertinent]
├── commands/       # [commandes existantes]
├── mcp-servers/    # [serveurs MCP]
└── CLAUDE.md       # [instructions globales]
```

### Arbre souhaité avec nouveaux fichiers
```
~/.claude/
├── [nouveaux fichiers avec responsabilité de chacun]
```

### Gotchas connus du système
```
# CRITICAL: Encodage UTF-8 sans BOM pour .md/.json
# CRITICAL: UTF-8 avec BOM pour .ps1/.psm1 (PS 5.1)
# CRITICAL: Wikilinks [[Nom]] dans les notes Obsidian
# CRITICAL: Frontmatter YAML obligatoire dans les notes vault
# CRITICAL: Pas de `??` ni `UTF8BOM` dans les scripts PowerShell (PS 5.1)
```

## Implementation Blueprint

### Structure des fichiers à créer
```yaml
Fichier 1:
  path: [chemin]
  rôle: [responsabilité]
  pattern: [skill/fichier existant à suivre comme modèle]

Fichier 2:
  ...
```

### Liste des tâches ordonnées
```yaml
Task 1:
  action: CREATE | MODIFY | CONFIGURE
  path: [chemin du fichier]
  description: [ce qui doit être fait]
  pattern: [fichier existant à utiliser comme référence]

Task 2:
  ...
```

### Pseudocode par tâche (si nécessaire)
```
# Task 1 - Détails critiques uniquement
# PATTERN: Suivre la structure de [skill existant]
# GOTCHA: [piège spécifique à éviter]
```

### Points d'intégration
```yaml
ROUTER:
  - Ajouter keywords dans skills/SKILL.md
  - Pattern: section du meta-router existant

VAULT:
  - Créer note dans Knowledge/[dossier]/
  - Template: _Templates/Template-[type].md
  - Tags: [tags hiérarchiques]

MCP:
  - Impacte le serveur knowledge-assistant: [oui/non]

CLAUDE.MD:
  - Mise à jour nécessaire: [sections à modifier]
```

## Validation Loop

### Niveau 1 : Structure & Syntax
```powershell
# Vérifier que les fichiers existent
Test-Path [chemin-fichier]

# Vérifier l'encodage (UTF-8 sans BOM pour .md)
$bytes = [System.IO.File]::ReadAllBytes("[chemin]")
if ($bytes[0] -eq 0xEF) { Write-Warning "BOM détecté" }

# Vérifier le frontmatter YAML (pour notes vault)
Select-String -Path [chemin] -Pattern "^---" | Measure-Object
```

### Niveau 2 : Fonctionnel
```powershell
# Tester les commandes du skill
# Vérifier que les scripts s'exécutent
# Valider les réponses MCP
```

### Niveau 3 : Intégration
```powershell
# Vérifier le routage
# /router test [skill-name]
# Vérifier l'indexation vault
# /know-search [terme]
# Vérifier le health score
# /guardian-health --quick
```

## Checklist de validation finale
- [ ] Tous les fichiers créés avec le bon encodage
- [ ] Frontmatter YAML valide (notes vault)
- [ ] Commandes fonctionnelles
- [ ] Router mis à jour et détecte le skill
- [ ] Vault indexé (si applicable)
- [ ] CLAUDE.md mis à jour (si applicable)
- [ ] Aucun skill existant cassé

---

## Anti-Patterns à éviter
- Ne pas créer de nouveaux patterns quand les existants fonctionnent
- Ne pas sauter la validation
- Ne pas ignorer les tests qui échouent
- Ne pas hardcoder des chemins (utiliser les variables du système)
- Ne pas modifier les _Templates/ sauf demande explicite
- Ne pas oublier les wikilinks dans les notes vault
