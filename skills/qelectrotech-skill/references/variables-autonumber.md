# Variables et Auto-Numerotation QET

> Reference extraite du skill QElectroTech - variables de cartouche et systeme d'auto-numerotation

## Variables Projet

| Variable | Description |
|----------|-------------|
| `%{author}` | Auteur du projet |
| `%{projecttitle}` | Titre du projet |
| `%{plant}` | Installation / Usine |
| `%{machine}` | Machine |
| `%{locmach}` | Localisation machine |
| `%{indexrev}` | Indice de revision |
| `%{saveddate}` | Date de sauvegarde (format local) |
| `%{saveddate-eu}` | Date format europeen (DD/MM/YYYY) |
| `%{saveddate-us}` | Date format US (MM/DD/YYYY) |
| `%{savedtime}` | Heure de sauvegarde |
| `%{savedfilename}` | Nom du fichier |
| `%{savedfilepath}` | Chemin complet du fichier |
| `%{version}` | Version QET |

## Variables Folio

| Variable | Description |
|----------|-------------|
| `%{folio-id}` ou `%id` | Numero du folio courant |
| `%{folio-total}` ou `%total` | Nombre total de folios |
| `%{previous-folio-num}` | Numero du folio precedent |
| `%{next-folio-num}` | Numero du folio suivant |
| `%{title}` | Titre du folio |
| `%{filename}` | Nom du fichier |

## Variables Auto-Numerotation

| Variable | Description | Exemple |
|----------|-------------|---------|
| `%{F}` | Numero du folio (2 chiffres) | `01`, `02` |
| `%{f}` | Numero du folio (1 chiffre) | `1`, `2` |
| `%{M}` | Machine / Installation | `M1` |
| `%{LM}` | Localisation machine | `ARM1` |
| `%{l}` | Numero de ligne (row) | `A`, `B` |
| `%{c}` | Numero de colonne (col) | `1`, `2` |
| `%{id}` | Index auto-increment | `001`, `002` |

## Systeme UUID (v0.9+)

A partir de la version 0.9, chaque element et terminal possede un UUID :
- Format : `{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}`
- Generer en PowerShell : `[guid]::NewGuid().ToString()`
- Les UUIDs permettent le suivi des connexions entre terminaux et conducteurs
