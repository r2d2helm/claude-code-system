# /pai-customize — Personnaliser USER/

Personnaliser l'identite et les preferences dans USER/.

## Syntaxe

```
/pai-customize [section]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `section` | `identity`, `preferences`, `steering`, `all` | Interactif |

## Procedure

### identity — Identite DA et principal
1. Demander via AskUserQuestion :
   - Nom du DA (defaut: R2D2)
   - Nom du principal (utilisateur)
   - Fuseau horaire
   - Catchphrase de demarrage
2. Mettre a jour settings.json : daidentity et principal
3. Mettre a jour USER/DAIDENTITY.md si present

### preferences — Preferences techniques
1. Demander :
   - Terminal prefere
   - Navigateur prefere
   - Niveau de detail des reponses
2. Mettre a jour settings.json : techStack

### steering — Regles de pilotage
1. Lire USER/AISTEERINGRULES.md actuel
2. Proposer les modifications courantes :
   - Langue de reponse
   - Format de reponse
   - Domaines d'expertise prioritaires
3. Editer USER/AISTEERINGRULES.md

### all
1. Executer identity, preferences, steering dans l'ordre
