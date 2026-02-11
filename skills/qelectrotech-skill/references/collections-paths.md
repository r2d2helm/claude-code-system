# Collections et Chemins QET

> Reference extraite du skill QElectroTech - types de collections et flags CLI

## Types de collections

| Prefixe | Description | Emplacement |
|---------|-------------|-------------|
| `common://` | Collection systeme (lecture seule) | `<install>/elements/` |
| `custom://` | Collection utilisateur | `C:\Users\<user>\Application Data\qet\elements\` |
| `embed://` | Collection embarquee dans le projet | `<project>/collection/` |

## Flags CLI

| Flag | Description |
|------|-------------|
| `--common-elements-dir` | Chemin vers la collection systeme |
| `--config-dir` | Repertoire de configuration utilisateur |
| `--lang-dir` | Repertoire des fichiers de langue |

> **Note** : QET n'a pas d'export CLI natif (Issues GitHub #162, #309). L'export PDF/SVG/DXF se fait uniquement via la GUI.
