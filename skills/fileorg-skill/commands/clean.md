# Commande: /file-clean

Nettoyer fichiers temporaires, inutiles et liberer de l'espace disque.

## Syntaxe

```
/file-clean [mode] [options]
```

## Modes de Nettoyage

### /file-clean temp

Nettoyer fichiers temporaires Linux :

```
╔══════════════════════════════════════════════════════════════╗
║           NETTOYAGE FICHIERS TEMPORAIRES                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ANALYSE DES FICHIERS TEMPORAIRES:                           ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Emplacement              │ Fichiers │ Taille           │ ║
║  │ ─────────────────────────┼──────────┼────────────────  │ ║
║  │ /tmp                     │ 1,234    │ 2.3 GB           │ ║
║  │ ~/.cache                 │ 5,678    │ 1.8 GB           │ ║
║  │ ~/.local/share/Trash     │ 234      │ 890 MB           │ ║
║  │ ─────────────────────────┼──────────┼────────────────  │ ║
║  │ TOTAL                    │ 7,146    │ 5.0 GB           │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Nettoyer tout  [2] Selectionner  [3] Annuler            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
temp_locations=(
  "/tmp"
  "$HOME/.cache"
  "$HOME/.local/share/Trash/files"
)

total_size=0
total_files=0

for location in "${temp_locations[@]}"; do
  if [ -d "$location" ]; then
    count=$(find "$location" -type f 2>/dev/null | wc -l)
    size=$(du -sh "$location" 2>/dev/null | cut -f1)
    echo "Nettoyage $location..."
    echo "  $count fichiers, $size"

    # Supprimer fichiers > 7 jours
    find "$location" -type f -mtime +7 -delete 2>/dev/null

    total_files=$(( total_files + count ))
  fi
done

echo "Nettoye: $total_files fichiers"
```

### /file-clean downloads [jours]

Nettoyer anciens telechargements :

```
╔══════════════════════════════════════════════════════════════╗
║           NETTOYAGE DOWNLOADS                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Fichiers > 30 jours trouves:                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Categorie       │ Fichiers │ Taille    │ Action         │ ║
║  │ ────────────────┼──────────┼───────────┼──────────────  │ ║
║  │ Archives .zip   │ 23       │ 1.5 GB    │ Supprimer      │ ║
║  │ Documents .pdf  │ 12       │ 120 MB    │ Archiver       │ ║
║  │ Images          │ 34       │ 450 MB    │ Archiver       │ ║
║  │ Autres          │ 28       │ 890 MB    │ Reviser        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Espace recuperable: 3.0 GB                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
days="${1:-30}"
dry_run="${2:-}"
downloads=~/Downloads

old_files=$(find "$downloads" -type f -mtime +"$days")

# Categoriser
installers=$(echo "$old_files" | grep -iE '\.(deb|rpm|AppImage|run)$')
archives=$(echo "$old_files" | grep -iE '\.(zip|rar|7z|tar\.gz|tgz)$')
docs=$(echo "$old_files" | grep -iE '\.(pdf|doc|docx)$')

echo "Fichiers > $days jours dans Downloads:"
echo "  Archives: $(echo "$archives" | grep -c . || echo 0)"
echo "  Documents: $(echo "$docs" | grep -c . || echo 0)"

if [ -z "$dry_run" ]; then
  # Supprimer archives et paquets (generalement safe)
  echo "$installers" | grep -v '^$' | xargs -r rm -f
  echo "$archives" | grep -v '^$' | xargs -r rm -f
  echo "Archives et paquets supprimes"
fi
```

### /file-clean duplicates

Supprimer fichiers en double :

```
╔══════════════════════════════════════════════════════════════╗
║           SUPPRESSION DOUBLONS                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Doublons detectes: 234 groupes (567 fichiers)               ║
║  Espace recuperable: 4.5 GB                                  ║
║                                                              ║
║  Strategie de conservation:                                  ║
║  [1] Garder le plus recent                                   ║
║  [2] Garder le plus ancien                                   ║
║  [3] Garder celui avec le meilleur nom                       ║
║  [4] Choisir manuellement                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /file-clean empty

Supprimer dossiers vides :

```
╔══════════════════════════════════════════════════════════════╗
║           DOSSIERS VIDES                                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Dossiers vides trouves: 47                                  ║
║                                                              ║
║  [1] Supprimer tous  [2] Voir liste complete  [3] Annuler    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1:-$HOME}"
delete="${2:-}"

# Trouver tous les dossiers vides (recursivement, du plus profond)
empty_folders=$(find "$path" -type d -empty 2>/dev/null)
count=$(echo "$empty_folders" | grep -c . || echo 0)

echo "Dossiers vides: $count"
echo "$empty_folders" | head -20 | while read -r folder; do
  if [ "${delete}" = "--delete" ]; then
    rmdir "$folder" 2>/dev/null && echo "Supprime: $folder"
  else
    echo "  $folder"
  fi
done

if [ -z "$delete" ]; then
  echo "Utiliser --delete pour supprimer"
fi
```

### /file-clean trash

Gerer la corbeille :

```
╔══════════════════════════════════════════════════════════════╗
║           GESTION CORBEILLE                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Contenu de la corbeille:                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Elements        : 1,234                                 │ ║
║  │ Taille totale   : 8.5 GB                                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Vider completement                                      ║
║  [2] Supprimer elements > 30 jours                           ║
║  [3] Annuler                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
# Vider la corbeille (trash-cli)
trash-empty

# Ou supprimer directement
rm -rf ~/.local/share/Trash/files/*
rm -rf ~/.local/share/Trash/info/*

# Supprimer elements > 30 jours (trash-cli)
trash-empty 30
```

## Nettoyage Complet

### /file-clean full

Nettoyage complet du systeme :

```bash
# Execute toutes les operations de nettoyage
/file-clean full
```

Inclut:
- Fichiers temporaires /tmp et ~/.cache
- Anciens logs
- Corbeille (> 30 jours)
- Dossiers vides
- Paquets apt inutiles

## Planification

### /file-clean schedule

Configurer nettoyage automatique via cron :

```bash
# Nettoyage hebdomadaire (dimanche 03:00)
/file-clean schedule weekly

# Nettoyage mensuel (1er du mois 02:00)
/file-clean schedule monthly
```

**Script cron:**
```bash
# Ajouter au crontab : crontab -e
# Nettoyage hebdomadaire le dimanche a 03:00
0 3 * * 0 find /tmp -type f -mtime +7 -delete 2>/dev/null

# Nettoyage mensuel le 1er a 02:00
0 2 1 * * trash-empty 30 2>/dev/null
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Simuler sans supprimer |
| `--days=N` | Fichiers plus vieux que N jours |
| `--size=N` | Fichiers plus gros que N MB |
| `--force` | Pas de confirmation |
| `--verbose` | Afficher chaque fichier |
| `--log` | Enregistrer dans fichier log |
