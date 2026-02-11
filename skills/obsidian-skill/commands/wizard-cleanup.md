# Commande: /obs-wizard cleanup

Nettoyage guide du vault en 4 etapes.

## Syntaxe

```
/obs-wizard cleanup [options]
```

## Etapes du Wizard

### Etape 1 : Notes orphelines et vides

```
Actions:
- Lister les notes sans liens (/obs-orphans)
- Lister les notes vides (/obs-empty)
- Proposer : lier, archiver ou supprimer
```

### Etape 2 : Liens casses

```
Actions:
- Detecter les liens casses (/obs-links broken)
- Proposer : creer la note cible, corriger le lien, ou supprimer
```

### Etape 3 : Doublons et attachments

```
Actions:
- Detecter les notes en double (/obs-duplicates)
- Detecter les attachments orphelins (/obs-attachments orphans)
- Proposer : fusionner les doublons, supprimer les orphelins
```

### Etape 4 : Tags et frontmatter

```
Actions:
- Normaliser les tags incohérents (/obs-tags unused)
- Ajouter le frontmatter manquant (/obs-frontmatter add)
- Proposer : renommer, fusionner ou supprimer les tags rares
```

## Resume

```
NETTOYAGE TERMINE
=================
Notes supprimees: X
Liens repares: X
Doublons fusionnes: X
Attachments supprimes: X
Tags normalises: X
Frontmatter ajoute: X
```

## Options

| Option | Description |
|--------|-------------|
| `--auto` | Mode automatique (corrections sans confirmation) |
| `--dry-run` | Preview sans modifications |
| `--step N` | Commencer a l'etape N |

## Exemples

```powershell
/obs-wizard cleanup               # Nettoyage guide complet
/obs-wizard cleanup --dry-run     # Preview
/obs-wizard cleanup --step 3      # Commencer aux doublons
```

## Voir Aussi

- `/obs-wizard audit` - Audit complet
- `/obs-clean` - Nettoyage rapide
- `/obs-health` - Diagnostic
