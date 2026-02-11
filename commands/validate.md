# Validation multi-niveaux

## Cible : $ARGUMENTS

Exécute une validation complète du système ou du composant spécifié.
Si aucun argument, valide l'ensemble du système Claude Code.

## Niveau 1 : Structure & Syntax

### Skills
```powershell
# Vérifier que chaque skill a un SKILL.md
Get-ChildItem "~/.claude/skills" -Directory | ForEach-Object {
    $skillMd = Join-Path $_.FullName "SKILL.md"
    if (-not (Test-Path $skillMd)) { Write-Warning "MISSING: $skillMd" }
}
```

### Encodage
- Fichiers .md et .json : UTF-8 sans BOM
- Fichiers .ps1 et .psm1 : UTF-8 avec BOM
- Vérifier avec : `[System.IO.File]::ReadAllBytes()` les 3 premiers octets

### Frontmatter (notes vault)
- Toutes les notes dans Knowledge/ doivent avoir un frontmatter YAML valide
- Champs requis : title, date, type, status, tags

## Niveau 2 : Fonctionnel

### Meta-Router
- Le SKILL.md principal liste tous les skills actifs
- Les keywords sont définis pour chaque skill
- Les commandes sont référencées

### Commandes
- Chaque skill a un dossier commands/ avec au moins une commande
- Les wizards sont fonctionnels

### MCP Server
- knowledge-assistant est accessible
- Les outils répondent (knowledge_search, knowledge_read)

## Niveau 3 : Intégration

### Router
- Tester le routage avec des mots-clés de chaque skill
- Vérifier qu'il n'y a pas de conflit de keywords entre skills

### Vault
- Exécuter un health check : cohérence des liens, orphelins, tags
- Vérifier l'index des notes

### Cohérence globale
- CLAUDE.md reflète l'état actuel (nombre de skills, commandes)
- Pas de références à des fichiers inexistants
- Pas de liens cassés dans les notes vault

## Rapport

Produire un rapport structuré :
```
VALIDATION REPORT - [date]
========================

Niveau 1 - Structure:  [PASS/FAIL] ([détails])
Niveau 2 - Fonctionnel: [PASS/FAIL] ([détails])
Niveau 3 - Intégration: [PASS/FAIL] ([détails])

Score global: [X/10]

Issues trouvées:
- [liste des problèmes]

Actions recommandées:
- [liste des corrections]
```
