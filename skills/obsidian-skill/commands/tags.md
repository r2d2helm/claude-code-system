# Commande: /obs-tags

Gérer les tags du vault Obsidian.

## Syntaxe

```
/obs-tags [action] [options]
```

## Actions

### /obs-tags list

Lister tous les tags avec statistiques :

```
╔══════════════════════════════════════════════════════════════╗
║                    LISTE DES TAGS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Total: 89 tags uniques dans 456 notes                       ║
║                                                              ║
║  TOP 20 TAGS (par utilisation):                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │  #  Tag                          Notes    Occurrences   │ ║
║  │ ─────────────────────────────────────────────────────── │ ║
║  │  1. #dev                           78          134      │ ║
║  │  2. #infra                         65          112      │ ║
║  │  3. #proxmox                       45           89      │ ║
║  │  4. #dev/python                    38           67      │ ║
║  │  5. #projet                        35           56      │ ║
║  │ ... (+79 autres)                                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Voir hierarchie  [2] Exporter  [3] Filtrer              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags hierarchy

Afficher la hiérarchie des tags :

```
╔══════════════════════════════════════════════════════════════╗
║                  HIERARCHIE DES TAGS                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  #dev (78 notes)                                             ║
║  ├── #dev/python (38)                                        ║
║  │   ├── #dev/python/flask (12)                              ║
║  │   └── #dev/python/automation (8)                          ║
║  ├── #dev/bash (42)                                          ║
║  └── #dev/api (15)                                           ║
║                                                              ║
║  #infra (65 notes)                                           ║
║  ├── #infra/proxmox (45)                                     ║
║  │   ├── #infra/proxmox/vm (20)                              ║
║  │   └── #infra/proxmox/backup (8)                           ║
║  ├── #infra/docker (25)                                      ║
║  └── #infra/linux (28)                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags unused

Tags utilisés une seule fois (potentiellement orphelins) :

```
╔══════════════════════════════════════════════════════════════╗
║                  TAGS PEU UTILISES                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Tags utilises 1 seule fois (12):                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ #old-project         -> Projets/Archive/OldApp.md       │ ║
║  │ #test123             -> _Inbox/Test-Note.md             │ ║
║  │ #temp                -> _Inbox/Temp-2026-01.md          │ ║
║  │ ... (+7 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Tags similaires (possibles doublons):                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ #proxmox (45) <-> #Proxmox (3) <-> #pve (8)              │ ║
║  │ #python (38) <-> #Python (5)                              │ ║
║  │ #todo (32) <-> #TODO (2)                                  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags rename

Renommer un tag dans tout le vault :

```bash
/obs-tags rename "#old-tag" "#new-tag"
```

### /obs-tags merge

Fusionner plusieurs tags en un seul :

```bash
/obs-tags merge "#Proxmox,#pve,#PVE" --into="#proxmox"
```

### /obs-tags add

Ajouter un tag à plusieurs notes :

```bash
/obs-tags add "#review" --folder="Conversations" --since="2026-01-01"
```

### /obs-tags remove

Retirer un tag de notes :

```bash
/obs-tags remove "#temp" --all
```

## Script bash

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

get_vault_tags() {
    local vault="$1"
    declare -A tag_stats
    declare -A tag_notes

    while IFS= read -r note; do
        content=$(< "$note" 2>/dev/null) || continue
        [ -z "$content" ] && continue

        while IFS= read -r tag; do
            [ -z "$tag" ] && continue
            tag_stats["$tag"]=$((${tag_stats["$tag"]:-0} + 1))
            echo "$tag $(basename "$note")"
        done < <(grep -oP '#[\w/-]+' "$note" 2>/dev/null || true)
    done < <(find "$vault" -name "*.md" -type f)

    # Afficher top tags
    for tag in "${!tag_stats[@]}"; do
        printf "%d %s\n" "${tag_stats[$tag]}" "$tag"
    done | sort -rn
}

find_similar_tags() {
    local tags=("$@")
    declare -A groups

    for tag in "${tags[@]}"; do
        normalized=$(echo "$tag" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')
        groups["$normalized"]+=" $tag"
    done

    # Retourner groupes avec plus d'un tag
    for key in "${!groups[@]}"; do
        count=$(echo "${groups[$key]}" | wc -w)
        [ "$count" -gt 1 ] && echo "${groups[$key]}"
    done
}

rename_tag() {
    local vault="$1" old_tag="$2" new_tag="$3" dry_run="${4:-false}"
    local modified=()

    while IFS= read -r note; do
        content=$(< "$note")
        if echo "$content" | grep -qF "$old_tag"; then
            if [ "$dry_run" = false ]; then
                new_content=$(echo "$content" | sed "s|$old_tag|$new_tag|g")
                printf '%s' "$new_content" > "$note"
            fi
            modified+=("$(basename "$note")")
        fi
    done < <(find "$vault" -name "*.md" -type f)

    echo "${modified[@]}"
}

add_tag_to_notes() {
    local vault="$1" tag="$2" folder="${3:-}" since="${4:-}"
    local path="${folder:+$vault/$folder}"
    path="${path:-$vault}"

    while IFS= read -r note; do
        # Filtre par date si specifie
        if [ -n "$since" ]; then
            mod_time=$(date -r "$note" '+%Y-%m-%d')
            [[ "$mod_time" < "$since" ]] && continue
        fi

        content=$(< "$note")
        echo "$content" | grep -qF "$tag" && continue

        # Ajouter dans frontmatter si present
        if echo "$content" | head -1 | grep -q '^---'; then
            new_content=$(echo "$content" | awk "
                /^tags:/ { print; print \"  - ${tag#'#'}\"; next }
                { print }
            ")
            printf '%s' "$new_content" > "$note"
        fi
    done < <(find "$path" -name "*.md" -type f)
}
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Prévisualiser sans modifier |
| `--backup` | Backup avant modification |
| `--folder=path` | Limiter à un dossier |
| `--since=date` | Notes depuis date |
| `--export=file` | Exporter résultats |

## Exemples

```bash
# Lister tous les tags
/obs-tags list

# Voir hierarchie
/obs-tags hierarchy

# Renommer tag
/obs-tags rename "#old" "#new"

# Fusionner tags similaires
/obs-tags merge "#Proxmox,#pve" --into="#proxmox"

# Ajouter tag aux notes recentes
/obs-tags add "#review" --since="2026-02-01"

# Exporter liste des tags
/obs-tags list --export="tags.csv"
```
