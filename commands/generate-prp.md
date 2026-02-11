# Générer un PRP

## Fichier feature : $ARGUMENTS

Génère un PRP complet pour la feature décrite. Lis d'abord le fichier feature pour comprendre ce qui doit être créé.

L'agent qui exécutera ce PRP a accès au codebase et aux mêmes outils que toi. Inclus tout le contexte nécessaire directement dans le PRP ou sous forme de références (chemins de fichiers, URLs).

## Processus de recherche

1. **Analyse du système existant**
   - Chercher des skills/patterns similaires dans `~/.claude/skills/`
   - Identifier les fichiers à référencer dans le PRP
   - Noter les conventions existantes (nommage, structure, frontmatter)
   - Vérifier les commandes et wizards existants pour ne pas dupliquer
   - Consulter le vault via MCP (knowledge_search) pour le contexte antérieur

2. **Recherche externe** (si nécessaire)
   - Documentation des outils/APIs concernés
   - Exemples d'implémentation
   - Best practices et pièges courants

3. **Clarification utilisateur** (si nécessaire)
   - Patterns spécifiques à suivre ?
   - Contraintes d'intégration ?

## Génération du PRP

Utilise `~/.claude/PRPs/templates/prp_base.md` comme template.

### Contexte critique à inclure
- **Skills existants** : chemins et patterns à suivre
- **Conventions** : encodage, nommage, frontmatter YAML
- **Gotchas** : UTF-8 sans BOM (.md/.json), avec BOM (.ps1), PS 5.1 compatible
- **Router** : keywords à ajouter dans le meta-router
- **Vault** : notes liées, templates à utiliser

### Blueprint d'implémentation
- Commencer par le pseudocode montrant l'approche
- Référencer les fichiers existants comme modèles
- Lister les tâches dans l'ordre d'exécution
- Inclure les points d'intégration (router, vault, MCP, CLAUDE.md)

### Portes de validation
```powershell
# Niveau 1 : Structure
Test-Path [fichiers-créés]

# Niveau 2 : Fonctionnel
# Commandes du skill répondent

# Niveau 3 : Intégration
# Router détecte, vault indexé, health score stable
```

---

*** CRITICAL : Après la recherche et AVANT d'écrire le PRP ***
*** ULTRATHINK : Planifie ton approche, puis rédige le PRP ***

## Output
Sauvegarder dans : `~/.claude/PRPs/{feature-name}.md`

## Checklist qualité
- [ ] Tout le contexte nécessaire est inclus
- [ ] Les validations sont exécutables
- [ ] Référence les patterns existants
- [ ] Chemin d'implémentation clair
- [ ] Points d'intégration documentés
- [ ] Conventions d'encodage documentées

Note le PRP sur une échelle de 1-10 (confiance pour une implémentation réussie en un seul passage).

Objectif : succès en un seul passage grâce à un contexte exhaustif.
