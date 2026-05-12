# Integration Vault Obsidian

## Structure dans le vault

```
Knowledge/
└── References/
    └── Intel/
        ├── 2026-03-25_Intel_Migration-VMware-Broadcom.md   (finding)
        ├── 2026-03-25_Intel_Cheque-Cyber-Wallonie.md       (finding)
        ├── OPP-7_Pack-Migration-VMware-PME.md              (opportunity)
        ├── THR-3_OpenClaw-Variantes.md                     (threat)
        └── Briefs/
            ├── 2026-03-25_Brief_Hebdo.md                   (weekly brief)
            └── 2026-03-18_Brief_Hebdo.md
```

## Notes creees automatiquement

### Findings (score >= 3)

- **Chemin** : `Knowledge/References/Intel/YYYY-MM-DD_Intel_{title-slug}.md`
- **Template** : `templates/finding-note.md`
- **Frontmatter** : type=reference, tags=intel/finding + intel/{category}
- **Wikilinks** : vers `[[MOC-Intelligence]]` et findings connectes

### Opportunity Cards

- **Chemin** : `Knowledge/References/Intel/OPP-{id}_{title-slug}.md`
- **Template** : `templates/opportunity-card.md`
- **Frontmatter** : type=reference, tags=intel/opportunity + business/plan-seldon
- **Wikilinks** : vers `[[MOC-Intelligence]]`, findings sources, skills R2D2

### Threat Alerts

- **Chemin** : `Knowledge/References/Intel/THR-{id}_{title-slug}.md`
- **Template** : `templates/threat-alert.md`
- **Frontmatter** : type=reference, tags=intel/threat + business/plan-seldon

### Intelligence Briefs

- **Chemin** : `Knowledge/References/Intel/Briefs/YYYY-MM-DD_Brief_{title}.md`
- **Template** : `templates/intelligence-brief.md`
- **Frontmatter** : type=reference, tags=intel/brief + business/plan-seldon

## MOC Intelligence

Le skill s'attend a ce qu'une note `[[MOC-Intelligence]]` existe dans `Knowledge/_Index/`.
Si elle n'existe pas, le wizard setup la cree :

```markdown
---
title: "MOC - Intelligence Strategique"
date: 2026-03-25
type: reference
status: growing
tags:
  - moc
  - intel
  - business/plan-seldon
related:
  - "[[MOC-References]]"
---

# MOC - Intelligence Strategique

## Briefs hebdomadaires
<!-- Liens automatiques vers les briefs -->

## Opportunities actives
<!-- Liens automatiques vers les OPP -->

## Threats actifs
<!-- Liens automatiques vers les THR -->

## Findings recents
<!-- Top findings par score -->
```

## Integration avec press-review-skill

Le flux principal :

```
/press-review
    -> cree Knowledge/References/YYYY-MM-DD_Press-Review.md

/intel-ingest --from-press-review
    -> parse la note press-review
    -> extrait chaque article
    -> stocke dans SQLite
    -> detecte les connexions
    -> cree des notes Intel individuelles (score >= 3)
```

Les notes Press-Review restent dans `References/` (pas dans `References/Intel/`).
Les notes Intel individuelles sont dans `References/Intel/`.

## Integration avec knowledge-assistant MCP

Les notes Intel sont automatiquement indexees par le MCP knowledge-assistant.
Recherche possible via :
- `knowledge_search("intel opportunity VMware")`
- `knowledge_search("threat alert")`
- `knowledge_tags("intel/opportunity")`

## Conventions de nommage

| Prefixe | Type | Exemple |
|---------|------|---------|
| `YYYY-MM-DD_Intel_` | Finding | `2026-03-25_Intel_Migration-VMware.md` |
| `OPP-{id}_` | Opportunity | `OPP-7_Pack-Migration-VMware-PME.md` |
| `THR-{id}_` | Threat | `THR-3_OpenClaw-Variantes.md` |
| `YYYY-MM-DD_Brief_` | Brief | `2026-03-25_Brief_Hebdo.md` |

## Tags hierarchiques

- `intel/finding` : tout finding ingere
- `intel/opportunity` : Opportunity Card
- `intel/threat` : Threat Alert
- `intel/brief` : Intelligence Brief
- `intel/IT_Tech`, `intel/Business_Reglementaire`, etc. : par categorie
- `business/plan-seldon` : lie au Plan Seldon
