# Templates de Notes

Templates prêts à l'emploi pour différents types de notes.

## Template: Conversation

Fichier: `Template-Conversation.md`

```markdown
---
id: {{date:YYYYMMDD}}-{{time:HHmmss}}
title: {{title}}
date: {{date:YYYY-MM-DD}}
type: conversation
tags: []
source: Claude
status: captured
related: []
---

# {{title}}

## Résumé
<!-- Résumé en 2-3 phrases -->


## Points Clés
- 
- 
- 

## Décisions Prises
- [ ] 

## Code/Commandes
```
<!-- Code extrait -->
```

## Concepts Liés
- [[]]

## Actions Suivantes
- [ ] 

## Notes
<!-- Notes additionnelles -->


---
*Capturé le {{date:YYYY-MM-DD}} depuis conversation Claude*
```

---

## Template: Concept (Zettelkasten)

Fichier: `Template-Concept.md`

```markdown
---
id: {{id}}
title: {{title}}
date: {{date:YYYY-MM-DD}}
type: concept
tags: []
source: 
related: []
---

# {{title}}

<!-- Explication de l'idée principale -->


## Pourquoi c'est important
<!-- Contexte et pertinence -->


## Détails
<!-- Développement de l'idée -->


## Exemples
<!-- Exemples concrets -->


## Liens
- Découle de: [[]]
- Mène à: [[]]
- Voir aussi: [[]]

## Sources
- [[]]
```

---

## Template: Code Snippet

Fichier: `Template-Code.md`

```markdown
---
id: {{id}}
title: {{title}}
date: {{date:YYYY-MM-DD}}
type: code
language: {{language}}
tags: [code, {{language}}]
tested: false
source: 
---

# {{title}}

## Description
<!-- Que fait ce code -->


## Code
```{{language}}
<!-- Code ici -->
```

## Utilisation
```{{language}}
<!-- Exemple d'utilisation -->
```

## Paramètres
| Paramètre | Type | Description |
|-----------|------|-------------|
| | | |

## Notes
<!-- Notes sur l'implémentation -->


## Voir aussi
- [[]]
```

---

## Template: Daily Note

Fichier: `Template-Daily.md`

```markdown
---
date: {{date:YYYY-MM-DD}}
type: daily
tags: [daily, {{date:YYYY}}, {{date:MM}}]
---

# 📅 {{date:YYYY-MM-DD}}

## 🎯 Focus du Jour
<!-- Objectif principal -->


## 💬 Conversations
<!-- Liens vers conversations du jour -->


## 💡 Idées Capturées
<!-- Nouvelles idées -->


## 💻 Code Créé
<!-- Scripts ou snippets -->


## ✅ Accompli
- [ ] 

## 📝 Notes
<!-- Réflexions de la journée -->


## 🔗 Liens
<!-- Liens vers autres notes -->

```

---

## Template: Projet

Fichier: `Template-Projet.md`

```markdown
---
id: P-{{id}}
title: {{title}}
date: {{date:YYYY-MM-DD}}
type: projet
status: active
tags: [projet]
deadline: 
---

# 📁 {{title}}

## Description
<!-- Description du projet -->


## Objectifs
- [ ] Objectif 1
- [ ] Objectif 2

## Ressources
<!-- Liens vers ressources -->


## Notes de Travail
### {{date:YYYY-MM-DD}}
<!-- Notes du jour -->


## Décisions
| Date | Décision | Contexte |
|------|----------|----------|
| | | |

## Conversations Liées
- [[]]

## Archive
<!-- Anciennes notes -->

```

---

## Template: Référence

Fichier: `Template-Reference.md`

```markdown
---
id: R-{{id}}
title: {{title}}
date: {{date:YYYY-MM-DD}}
type: reference
source_type: article/documentation/video
url: 
author: 
tags: [reference]
---

# 📚 {{title}}

## Source
- **Type**: 
- **URL**: 
- **Auteur**: 
- **Date**: 

## Résumé
<!-- Résumé de la source -->


## Points Clés
- 
- 

## Citations
> Citation importante

## Idées Extraites
<!-- Concepts à explorer -->
- [[]]

## Application
<!-- Comment utiliser ces infos -->


## Voir aussi
- [[]]
```

---

## Template: Troubleshooting

Fichier: `Template-Troubleshooting.md`

```markdown
---
id: T-{{id}}
title: {{title}}
date: {{date:YYYY-MM-DD}}
type: troubleshooting
status: resolved
tags: [troubleshooting]
system: 
error_code: 
---

# 🔧 {{title}}

## Problème
<!-- Description du problème -->


## Environnement
- **OS**: 
- **Version**: 
- **Contexte**: 

## Symptômes
<!-- Ce qui se passe -->


## Message d'Erreur
```
<!-- Message exact -->
```

## Cause Identifiée
<!-- Pourquoi ça arrive -->


## Solution
<!-- Étapes pour résoudre -->

1. 
2. 
3. 

## Code de Résolution
```bash
<!-- Commandes utilisées -->
```

## Prévention
<!-- Comment éviter à l'avenir -->


## Références
- [[]]
```

---

## Utilisation des Templates

### Dans Claude Code
```
/know-save --template=conversation
/know-save --template=concept
/know-save --template=code
```

### Dans Obsidian
1. Placer templates dans `_Templates/`
2. Utiliser Ctrl+T pour insérer
3. Ou via Command Palette: "Templates: Insert"

### Variables Supportées
| Variable | Description | Exemple |
|----------|-------------|---------|
| `{{date:FORMAT}}` | Date formatée | `2026-02-04` |
| `{{time:FORMAT}}` | Heure formatée | `083045` |
| `{{title}}` | Titre de la note | `Mon Concept` |
| `{{id}}` | ID unique | `20260204-083045` |
| `{{language}}` | Langage de code | `bash` |
