# Commande: /obs-wizard reorganize

Reorganisation assistee de la structure du vault.

## Syntaxe

```
/obs-wizard reorganize [options]
```

## Etapes du Wizard

### Etape 1 : Analyse de la structure actuelle

```
Actions:
- Scanner la structure des dossiers (/obs-structure)
- Identifier les problemes : profondeur > 3, dossiers vides, desequilibre
- Afficher un rapport de la situation actuelle
```

### Etape 2 : Proposition de nouvelle structure

```
Actions:
- Proposer une structure optimisee basee sur les conventions r2d2 :
  _Index/    - MOCs et navigation
  _Daily/    - Notes quotidiennes
  _Inbox/    - Notes a traiter
  _Templates/ - Templates
  Concepts/  - Notes atomiques (C_*)
  Conversations/ - Sessions Claude
  Projets/   - Notes de projets
  Formations/ - Cours et formations
  References/ - Documentation

- Identifier les notes mal placees
- Proposer les deplacements
```

### Etape 3 : Execution des deplacements

```
Actions:
- Deplacer les notes selon le plan (/obs-move)
- Mettre a jour les backlinks si necessaire
- Creer les dossiers manquants
- Supprimer les dossiers vides
```

### Etape 4 : Verification

```
Actions:
- Re-scanner la structure (/obs-structure)
- Verifier qu'aucun lien n'est casse (/obs-links broken)
- Afficher le rapport avant/apres
```

## Resume

```
REORGANISATION TERMINEE
=======================
Notes deplacees: X
Dossiers crees: X
Dossiers supprimes: X
Liens mis a jour: X
Structure: profondeur max Y niveaux
```

## Options

| Option | Description |
|--------|-------------|
| `--preview` | Afficher le plan sans executer |
| `--auto` | Executer automatiquement |
| `--conservative` | Deplacements minimaux uniquement |

## Exemples

```bash
/obs-wizard reorganize                # Reorganisation guidee
/obs-wizard reorganize --preview      # Plan de reorganisation
/obs-wizard reorganize --conservative # Deplacements minimaux
```

## Voir Aussi

- `/obs-structure` - Analyse de la structure
- `/obs-move` - Deplacer une note
- `/obs-wizard audit` - Audit complet
