# Commande: /know-search

Rechercher dans la base de connaissances.

## Syntaxe

```
/know-search "terme" [filtres]
```

## Modes de Recherche

### Recherche Simple

```
/know-search "proxmox"
```

```
╔══════════════════════════════════════════════════════════════╗
║           🔍 RECHERCHE: "proxmox"                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 RÉSULTATS: 12 notes trouvées                             ║
║                                                              ║
║  📁 CONVERSATIONS (5)                                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📄 2026-02-03_Conv_Proxmox-Skill-Creation.md           │ ║
║  │    "Création du super agent Proxmox avec 20 commandes"  │ ║
║  │    Tags: #proxmox #skill #claude-code                   │ ║
║  │                                                         │ ║
║  │ 📄 2026-01-28_Conv_Proxmox-Cluster-HA.md               │ ║
║  │    "Configuration haute disponibilité cluster PVE"      │ ║
║  │    Tags: #proxmox #ha #cluster                          │ ║
║  │                                                         │ ║
║  │ ... (+3 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💡 CONCEPTS (4)                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📝 C_Proxmox-API-Authentication.md                      │ ║
║  │    "Authentification API Proxmox avec tokens"           │ ║
║  │                                                         │ ║
║  │ 📝 C_Ceph-Integration-Proxmox.md                        │ ║
║  │    "Intégration Ceph dans cluster Proxmox"              │ ║
║  │                                                         │ ║
║  │ ... (+2 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💻 CODE (3)                                                 ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 🔧 Code_Proxmox-VM-Create.sh                            │ ║
║  │ 🔧 Code_Proxmox-Backup-Script.sh                        │ ║
║  │ 🔧 Code_Proxmox-API-Call.py                             │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Ouvrir note  [2] Filtrer  [3] Exporter résultats        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Recherche par Tag

```
/know-search tag:#proxmox/cluster
```

```
╔══════════════════════════════════════════════════════════════╗
║           🏷️ RECHERCHE TAG: #proxmox/cluster                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Notes avec ce tag: 8                                        ║
║                                                              ║
║  📄 2026-02-03_Conv_Proxmox-Cluster-Setup.md                 ║
║  📄 2026-01-28_Conv_Proxmox-HA-Config.md                     ║
║  📝 C_Corosync-Configuration.md                              ║
║  📝 C_Cluster-Quorum.md                                      ║
║  📝 C_Live-Migration.md                                      ║
║  🔧 Code_Cluster-Status-Check.sh                             ║
║  🔧 Code_HA-Failover-Test.sh                                 ║
║  📚 R_Proxmox-Cluster-Admin-Guide.md                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Recherche par Type

```
/know-search type:concept
```

Liste tous les concepts atomiques.

### Recherche par Date

```
/know-search date:2026-02
```

Notes de février 2026.

```
/know-search date:last-week
```

Notes de la dernière semaine.

### Recherche Combinée

```
/know-search "backup" tag:#proxmox type:code date:2026
```

```
╔══════════════════════════════════════════════════════════════╗
║           🔍 RECHERCHE AVANCÉE                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Filtres appliqués:                                          ║
║  • Terme: "backup"                                           ║
║  • Tag: #proxmox                                             ║
║  • Type: code                                                ║
║  • Date: 2026                                                ║
║                                                              ║
║  📊 RÉSULTATS: 3 notes                                       ║
║                                                              ║
║  🔧 2026-02-03_Proxmox-Backup-vzdump.sh                      ║
║     Relevance: ████████████████████ 95%                      ║
║                                                              ║
║  🔧 2026-01-15_Backup-PBS-Config.sh                          ║
║     Relevance: ████████████████░░░░ 80%                      ║
║                                                              ║
║  🔧 2026-01-10_Backup-Verification.sh                        ║
║     Relevance: ██████████████░░░░░░ 70%                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Script bash

```bash
#!/usr/bin/env bash
search_knowledge() {
    local query="$1"
    local tag="$2"
    local type="$3"
    local date_filter="$4"
    local knowledge_path="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"

    # Construire pattern de recherche
    local search_pattern="*.md"
    case "$type" in
        conversation) search_pattern="Conv_*.md" ;;
        concept)      search_pattern="C_*.md" ;;
        code)         search_pattern="Code_*.md" ;;
        reference)    search_pattern="R_*.md" ;;
    esac

    # Rechercher fichiers
    mapfile -t files < <(find "$knowledge_path" -name "$search_pattern" -type f)

    # Filtrer par contenu
    if [ -n "$query" ]; then
        mapfile -t files < <(printf '%s\n' "${files[@]}" | while read -r f; do
            grep -ql "$query" "$f" && echo "$f"
        done)
    fi

    # Filtrer par tag
    if [ -n "$tag" ]; then
        mapfile -t files < <(printf '%s\n' "${files[@]}" | while read -r f; do
            grep -ql "tags:.*$tag" "$f" && echo "$f"
        done)
    fi

    # Filtrer par date
    if [ -n "$date_filter" ]; then
        case "$date_filter" in
            last-week)
                mapfile -t files < <(printf '%s\n' "${files[@]}" | while read -r f; do
                    [ "$(find "$f" -mtime -7)" ] && echo "$f"
                done)
                ;;
            last-month)
                mapfile -t files < <(printf '%s\n' "${files[@]}" | while read -r f; do
                    [ "$(find "$f" -mtime -30)" ] && echo "$f"
                done)
                ;;
            *)
                mapfile -t files < <(printf '%s\n' "${files[@]}" | grep "/$date_filter")
                ;;
        esac
    fi

    echo ""
    echo "🔍 Résultats: ${#files[@]} notes trouvées"
    echo ""

    for f in "${files[@]}"; do
        local title
        title=$(grep -m1 'title:' "$f" | sed 's/title: *//')
        local tags
        tags=$(grep -m1 'tags:' "$f" | sed 's/tags: *//')
        local excerpt=""
        if [ -n "$query" ]; then
            excerpt=$(grep -m1 "$query" "$f" | head -c 100)
        fi
        echo "📄 $(basename "$f")"
        [ -n "$title" ] && echo "   $title"
        [ -n "$excerpt" ] && echo "   ...$excerpt..."
        [ -n "$tags" ] && echo "   Tags: $tags"
        echo ""
    done
}

# Alias
alias ks='search_knowledge'
```

## Options

| Option | Description |
|--------|-------------|
| `tag:#tag` | Filtrer par tag |
| `type:type` | Filtrer par type (conversation, concept, code) |
| `date:YYYY-MM` | Filtrer par date |
| `date:last-week` | Dernière semaine |
| `date:last-month` | Dernier mois |
| `--in=folder` | Chercher dans dossier spécifique |
| `--limit=N` | Limiter résultats |
| `--export=file` | Exporter résultats |

## Exemples

```bash
# Recherche simple
/know-search "docker"

# Par tag
/know-search tag:#infra/linux

# Par type
/know-search type:code "backup"

# Dernière semaine
/know-search date:last-week

# Combiné
/know-search "API" tag:#proxmox type:concept

# Exporter résultats
/know-search "bash" --export=results.md
```
