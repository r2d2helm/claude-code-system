# Commande: /obs-links

Gérer les liens internes du vault Obsidian.

## Syntaxe

```
/obs-links [action] [options]
```

## Actions

### /obs-links broken

Trouver tous les liens cassés (pointant vers des notes inexistantes) :

```
╔══════════════════════════════════════════════════════════════╗
║                   LIENS CASSES                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Trouves: 5 liens casses dans 3 notes                        ║
║                                                              ║
║  Projets/MultiPass/Architecture.md                           ║
║  │                                                           ║
║  ├─ [[API-Design]]                                           ║
║  │  └─ Note n'existe pas                                     ║
║  │  └─ Similaire: "API-Documentation" (85%)                  ║
║  │                                                           ║
║  └─ [[Database-Schema]]                                      ║
║     └─ Note n'existe pas                                     ║
║     └─ Aucune suggestion                                     ║
║                                                              ║
║  [1] Creer notes manquantes                                  ║
║  [2] Remplacer par suggestions                               ║
║  [3] Supprimer liens casses                                  ║
║  [4] Exporter liste                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-links fix

Réparer automatiquement les liens cassés :

```
╔══════════════════════════════════════════════════════════════╗
║                   REPARATION LIENS                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Mode: Interactif                                            ║
║                                                              ║
║  Projets/MultiPass/Architecture.md                           ║
║  Lien casse: [[API-Design]]                                  ║
║                                                              ║
║  Options:                                                    ║
║  [1] Creer note "API-Design.md"                              ║
║  [2] Remplacer par "API-Documentation" (85% similaire)       ║
║  [3] Supprimer le lien                                       ║
║  [4] Ignorer                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-links unlinked

Notes sans aucun lien (ni entrant ni sortant) - voir `/obs-links-unlinked`

### /obs-links suggest

Suggérer des connexions basées sur le contenu - voir `/obs-links-suggest`

### /obs-links stats

Statistiques sur les liens du vault :

```
╔══════════════════════════════════════════════════════════════╗
║                   STATISTIQUES LIENS                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RESUME:                                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Liens totaux         : 1,234                            │ ║
║  │ Liens uniques        : 456                              │ ║
║  │ Liens casses         : 5                                │ ║
║  │ Liens externes       : 89                               │ ║
║  │ Moyenne liens/note   : 2.7                              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  TOP 10 NOTES LES PLUS LIEES (backlinks):                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. INDEX.md                        (45 backlinks)       │ ║
║  │ 2. C_Proxmox-Administration.md     (23 backlinks)       │ ║
║  │ 3. Conv_2026-02-03_Setup.md        (15 backlinks)       │ ║
║  │ 4. C_Docker-Basics.md              (12 backlinks)       │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Script bash

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

find_broken_links() {
    local vault="$1"
    mapfile -t note_names < <(find "$vault" -name "*.md" -type f | xargs -I{} basename {} .md)

    find "$vault" -name "*.md" -type f | while IFS= read -r note; do
        content=$(< "$note" 2>/dev/null) || continue
        [ -z "$content" ] && continue

        while IFS= read -r target; do
            [ -z "$target" ] && continue
            # Ignorer liens externes
            echo "$target" | grep -qE '^https?://' && continue

            # Verifier si la note existe
            found=false
            for n in "${note_names[@]}"; do
                [ "$n" = "$target" ] && found=true && break
            done

            if [ "$found" = false ]; then
                # Chercher note similaire
                similar=$(printf '%s\n' "${note_names[@]}" | grep -iF "$target" | head -1 || true)
                line=$(grep -n "\[\[$target" "$note" | head -1 | cut -d: -f1)
                echo "source=$note target=$target line=$line suggestion=${similar:-(aucune)}"
            fi
        done < <(grep -oP '\[\[\K[^\]|#]+' "$note" 2>/dev/null | sed 's/[[:space:]]*$//' || true)
    done
}

repair_link() {
    local file="$1"
    local old_link="$2"
    local new_link="$3"
    local create_note="$4"

    if [ "$create_note" = true ]; then
        vault=$(dirname "$(dirname "$file")")
        new_note="${vault}/_Inbox/${new_link}.md"
        cat > "$new_note" << EOF
---
title: $new_link
date: $(date '+%Y-%m-%d')
type: note
tags: []
---

# $new_link

<!-- Note creee automatiquement -->
EOF
        echo "Note creee: $new_note"
    else
        sed -i "s/\[\[$old_link\]\]/[[$new_link]]/g" "$file"
        sed -i "s/\[\[$old_link|/[[$new_link|/g" "$file"
        echo "Lien remplace: [[$old_link]] -> [[$new_link]]"
    fi
}

get_link_stats() {
    local vault="$1"
    local total_links=0
    local external_links=0

    while IFS= read -r note; do
        out=$(grep -cP '\[\[' "$note" 2>/dev/null || echo 0)
        total_links=$((total_links + out))
        ext=$(grep -coP 'https?://[^\s\)\]>]+' "$note" 2>/dev/null || echo 0)
        external_links=$((external_links + ext))
    done < <(find "$vault" -name "*.md" -type f)

    note_count=$(find "$vault" -name "*.md" -type f | wc -l)
    avg=$(awk "BEGIN {printf \"%.1f\", $total_links / ($note_count > 0 ? $note_count : 1)}")

    echo "Liens totaux: $total_links"
    echo "Liens externes: $external_links"
    echo "Moyenne: $avg liens/note"

    echo ""
    echo "Top 10 backlinks:"
    find "$vault" -name "*.md" -type f | xargs grep -hoP '\[\[\K[^\]|#]+' 2>/dev/null | \
        sort | uniq -c | sort -rn | head -10
}
```

## Options

| Option | Description |
|--------|-------------|
| `--auto` | Mode automatique (pas d'interaction) |
| `--dry-run` | Prévisualiser sans modifier |
| `--backup` | Créer backup avant modification |
| `--export=file` | Exporter résultats |
| `--vault=path` | Vault spécifique |

## Exemples

```bash
# Trouver liens cassés
/obs-links broken

# Réparer automatiquement
/obs-links fix --auto

# Statistiques
/obs-links stats

# Suggestions pour une note
/obs-links suggest --note="C_Microservices.md"

# Exporter liste des liens cassés
/obs-links broken --export="broken-links.csv"
```
