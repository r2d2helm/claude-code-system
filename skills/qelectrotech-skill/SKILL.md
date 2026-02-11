---
name: qelectrotech-skill
description: "Plans electriques QElectroTech : schemas unifilaires, multifilaires, nomenclatures, elements, folios. Normes NF C 15-100 et IEC 60617."
---

# Agent QElectroTech - Plans Electriques Professionnels

Agent specialise dans la creation, administration et manipulation de plans electriques avec QElectroTech (QET) 0.100.x. Competences en schemas unifilaires residentiels, tableaux electriques, normes IEC 60617 et NF C 15-100.

## Environnement

| Composant | Valeur |
|-----------|--------|
| QElectroTech | 0.100.1 (git8595) |
| Chemin | `C:\Program Files\QElectroTech\qelectrotech-0.100.1+git8595-x86-win64-readytouse\` |
| Executable | `bin\qelectrotech.exe` |
| Elements | `elements\` (bibliotheque systeme) |
| Titleblocks | `titleblocks\` (cartouches) |
| Exemples | `examples\` (projets de reference) |
| Format | `.qet` (XML, UTF-8) |
| Elements | `.elmt` (XML, definitions graphiques) |
| Cartouches | `.titleblock` (XML, templates) |

> Voir `references/collections-paths.md` pour les types de collections (common://, custom://, embed://) et flags CLI.

## Commandes Slash

### Gestion de Projets

| Commande | Description |
|----------|-------------|
| `/qet-create` | Creer un nouveau projet QET multi-folios |
| `/qet-open` | Ouvrir un projet dans QElectroTech |
| `/qet-merge` | Fusionner plusieurs fichiers QET en un seul projet |
| `/qet-info` | Analyser un fichier QET (folios, elements, stats) |
| `/qet-export` | Exporter un projet (PDF via GUI, CSV nomenclature) |
| `/qet-backup` | Sauvegarder un projet avec versioning |

### Folios / Diagrammes

| Commande | Description |
|----------|-------------|
| `/qet-folio-add` | Ajouter un folio a un projet existant |
| `/qet-folio-list` | Lister les folios d'un projet |
| `/qet-folio-reorder` | Reorganiser l'ordre des folios |
| `/qet-folio-rename` | Renommer les titres des folios |
| `/qet-folio-extract` | Extraire un folio en fichier separe |

### Elements et Symboles

| Commande | Description |
|----------|-------------|
| `/qet-element-create` | Creer un element personnalise (.elmt) |
| `/qet-element-search` | Chercher un element dans la bibliotheque |
| `/qet-element-list` | Lister les elements utilises dans un projet |
| `/qet-element-import` | Importer un element dans la collection d'un projet |
| `/qet-element-catalog` | Catalogue complet des elements disponibles |

### Nomenclature et Devis

| Commande | Description |
|----------|-------------|
| `/qet-bom` | Generer un Bill of Materials (nomenclature) |
| `/qet-conductors` | Lister et analyser les conducteurs |
| `/qet-devis` | Generer un devis a partir du projet |
| `/qet-materials` | Calculer les materiaux necessaires |

### Conception Electrique

| Commande | Description |
|----------|-------------|
| `/qet-circuit` | Concevoir un circuit electrique (guide) |
| `/qet-panel` | Concevoir un tableau electrique |
| `/qet-nfc15100` | Verifier la conformite NF C 15-100 |
| `/qet-sizing` | Dimensionner cables et protections |

### Fonctions Avancees

| Commande | Description |
|----------|-------------|
| `/qet-titleblock` | Creer/gerer les cartouches personnalises |
| `/qet-autonumber` | Configurer l'auto-numerotation (elements, conducteurs, folios) |
| `/qet-crossref` | Gerer les references croisees Master/Slave |
| `/qet-terminal-strip` | Generer et gerer les borniers |
| `/qet-validate` | Valider l'integrite XML et les references |
| `/qet-variables` | Gerer les variables projet/folio |
| `/qet-diff` | Comparer deux versions d'un projet |
| `/qet-stats` | Statistiques avancees du projet |
| `/qet-dxf-import` | Importer un DXF comme element .elmt |
| `/qet-element-transform` | Redimensionner/pivoter/inverser/exporter un element |

### Wizards Interactifs

| Commande | Description |
|----------|-------------|
| `/qet-wizard` | Assistant interactif general |

## Syntaxe

```
/qet-<commande> [action] [options]
```

### Exemples

```
/qet-create maison 8 folios           # Creer projet maison 8 folios
/qet-info "C:\path\projet.qet"        # Analyser un projet
/qet-merge "C:\dir\*.qet"             # Fusionner des fichiers QET
/qet-bom "C:\path\projet.qet"         # Generer nomenclature
/qet-element-search "prise"           # Chercher un element
/qet-nfc15100 check                   # Verifier conformite
/qet-wizard residential               # Assistant maison complete
/qet-wizard panel                      # Assistant tableau electrique
```

## Wizards Disponibles

| Wizard | Etapes | Description |
|--------|--------|-------------|
| Residential | 8 | Projet electrique maison complete (pieces, circuits, plan) |
| Panel | 6 | Tableau electrique (TGBT, rangees, disjoncteurs, differentiel) |
| Renovation | 5 | Mise aux normes installation existante |
| Extension | 4 | Ajout circuit a un projet existant |
| Tertiaire | 7 | Installation bureau/commerce |
| Outdoor | 4 | Eclairage et prises exterieur/jardin |
| Industrial | 7 | Installation industrielle (moteurs, VFD, automate, borniers) |
| Photovoltaic | 6 | Installation solaire (autoconso, revente, hybride, batterie) |
| EV Charger | 5 | Borne de recharge IRVE (domestique, copropriete, professionnel) |

## Structure Fichiers

```
qelectrotech-skill/
  SKILL.md                    # Ce fichier (35 cmd, 9 wizards, 4 templates)
  commands/                   # Commandes slash (35 fichiers)
    create.md                 # /qet-create
    open.md                   # /qet-open
    merge.md                  # /qet-merge
    info.md                   # /qet-info
    export.md                 # /qet-export
    backup.md                 # /qet-backup
    folio-add.md              # /qet-folio-add
    folio-list.md             # /qet-folio-list
    folio-reorder.md          # /qet-folio-reorder
    folio-rename.md           # /qet-folio-rename
    folio-extract.md          # /qet-folio-extract
    element-create.md         # /qet-element-create
    element-search.md         # /qet-element-search
    element-list.md           # /qet-element-list
    element-import.md         # /qet-element-import
    element-catalog.md        # /qet-element-catalog
    element-transform.md      # /qet-element-transform
    bom.md                    # /qet-bom
    conductors.md             # /qet-conductors
    devis.md                  # /qet-devis
    materials.md              # /qet-materials
    circuit.md                # /qet-circuit
    panel.md                  # /qet-panel
    nfc15100.md               # /qet-nfc15100
    sizing.md                 # /qet-sizing
    titleblock.md             # /qet-titleblock
    autonumber.md             # /qet-autonumber
    crossref.md               # /qet-crossref
    terminal-strip.md         # /qet-terminal-strip
    validate.md               # /qet-validate
    variables.md              # /qet-variables
    diff.md                   # /qet-diff
    stats.md                  # /qet-stats
    dxf-import.md             # /qet-dxf-import
    wizard.md                 # /qet-wizard
  wizards/                    # Assistants interactifs (9 fichiers)
    wizard-residential.md
    wizard-panel.md
    wizard-renovation.md
    wizard-extension.md
    wizard-tertiaire.md
    wizard-outdoor.md
    wizard-industrial.md
    wizard-photovoltaic.md
    wizard-ev-charger.md
  templates/                  # Templates XML (5 fichiers)
    project-template.xml
    element-template.xml
    titleblock-template.xml
    terminal-strip-template.xml
    titleblock-nelu.xml
  references/                 # Documentation technique (11 fichiers)
    field-definitions.md      # Champs element et conducteur, orientation
    collections-paths.md      # Types de collections, flags CLI
    variables-autonumber.md   # Variables projet/folio, auto-numerotation, UUID
    iec-designations.md       # IEC 81346 prefixes, nommage bornes, tags
    electrical-standards.md   # NF C 15-100, NF EN 12464-1, IEC 60617
    manufacturers-tools.md    # Fabricants references, outils GitHub
    grid-coordinates.md       # Grille, dimensions folio A4, references croisees
    xml-schema.md             # Structure XML projet/element/cartouche, styles
    elements-catalog.md       # Bibliotheque, elements archi/VDI/protection
    powershell-snippets.md    # Scripts PS pour manipuler .qet/.elmt
    gui-reference.md          # Raccourcis GUI, limitations, exemples inclus
```

## References Externes

- [QElectroTech Official](https://qelectrotech.org)
- [QET Wiki](https://qelectrotech.org/wiki_new/)
- [Element Collection](https://qelectrotech.org/elementsFixture/)
- [Source Code](https://github.com/qelectrotech/qelectrotech-source-mirror)
- [NF C 15-100 Guide](https://www.schneider-electric.fr/fr/work/support/green-premium/nfc15100.jsp)
- [IEC 60617 Symbols](https://std.iec.ch/iec60617)
