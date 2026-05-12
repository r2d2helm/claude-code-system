# Commande: /obs-clean

Nettoyer et optimiser le vault Obsidian.

## Syntaxe

```
/obs-clean [action] [options]
```

## Actions

### /obs-clean (analyse)

Analyser ce qui peut être nettoyé :

```
╔══════════════════════════════════════════════════════════════╗
║                    ANALYSE NETTOYAGE                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ELEMENTS DETECTES:                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Type                      Nombre    Taille   Action     │ ║
║  │ ─────────────────────────────────────────────────────── │ ║
║  │ Notes vides                 5       2 KB     Supprimer  │ ║
║  │ Attachments orphelins      12      45 MB     Supprimer  │ ║
║  │ Dossiers vides              3       0 KB     Supprimer  │ ║
║  │ Fichiers temporaires        8      12 KB     Supprimer  │ ║
║  │ Doublons potentiels         2      89 KB     Examiner   │ ║
║  │ Cache Obsidian             --      234 MB    Nettoyer   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ESPACE RECUPERABLE: ~280 MB                                 ║
║                                                              ║
║  AVERTISSEMENTS:                                             ║
║  - 12 attachments non references seront supprimes           ║
║  - Le cache Obsidian sera reconstruit au prochain lancement  ║
║                                                              ║
║  [1] Nettoyer tout  [2] Selectionner  [3] Annuler            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean --all

Nettoyage complet automatique :

```
╔══════════════════════════════════════════════════════════════╗
║                    NETTOYAGE EN COURS                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [████████████████████████████████████████] 100%             ║
║                                                              ║
║  Notes vides supprimees          : 5                         ║
║  Attachments orphelins supprimes : 12 (45 MB)                ║
║  Dossiers vides supprimes        : 3                         ║
║  Fichiers temporaires supprimes  : 8                         ║
║  Cache Obsidian nettoye          : 234 MB                    ║
║                                                              ║
║  RESUME:                                                     ║
║  - Fichiers supprimes : 28                                   ║
║  - Espace libere      : 279 MB                               ║
║                                                              ║
║  Redemarrez Obsidian pour reconstruire le cache              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean empty

Supprimer notes vides :

```
╔══════════════════════════════════════════════════════════════╗
║                    NOTES VIDES                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Trouvees: 5 notes vides ou quasi-vides                      ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Fichier                          Taille    Contenu      │ ║
║  │ ─────────────────────────────────────────────────────── │ ║
║  │ _Inbox/Untitled.md               0 KB      (vide)       │ ║
║  │ _Inbox/New-Note.md               0.1 KB    "# "         │ ║
║  │ Conversations/Draft.md           0.2 KB    frontmatter  │ ║
║  │ Code/test.md                     0 KB      (vide)       │ ║
║  │ Projets/temp.md                  0.1 KB    "---"        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Supprimer toutes  [2] Selectionner  [3] Annuler         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean attachments

Gérer les attachments (images, PDF, etc.) :

```
╔══════════════════════════════════════════════════════════════╗
║                    ATTACHMENTS                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STATISTIQUES:                                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Type          Fichiers    Taille    References          │ ║
║  │ ─────────────────────────────────────────────────────── │ ║
║  │ Images PNG       45       23 MB        42               │ ║
║  │ Images JPG       38       45 MB        35               │ ║
║  │ PDF              34      156 MB        32               │ ║
║  │ Autres           12        8 MB        10               │ ║
║  │ ─────────────────────────────────────────────────────── │ ║
║  │ TOTAL           129      232 MB       119               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ORPHELINS (non references): 10 fichiers (45 MB)             ║
║                                                              ║
║  [1] Supprimer orphelins  [2] Deplacer vers archive          ║
║  [3] Exporter liste       [4] Annuler                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean cache

Nettoyer le cache Obsidian :

```bash
/obs-clean cache
```

Supprime :
- `.obsidian/cache`
- `.obsidian/workspace.json` (optionnel)
- Index de recherche corrompu

## Script bash

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
DRY_RUN=false

echo "Analyse du vault: $VAULT"
echo ""

# === NOTES VIDES ===
empty_notes=()
while IFS= read -r note; do
    content=$(< "$note" 2>/dev/null || true)
    body=$(echo "$content" | sed '/^---$/,/^---$/d' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    body_len=${#body}
    if [ "$body_len" -lt 10 ]; then
        empty_notes+=("$note")
    fi
done < <(find "$VAULT" -name "*.md" -type f)
echo "  Notes vides: ${#empty_notes[@]}"

# === ATTACHMENTS ORPHELINS ===
all_content=$(find "$VAULT" -name "*.md" -type f | xargs cat 2>/dev/null)
orphan_atts=()
while IFS= read -r att; do
    name=$(basename "$att")
    if ! echo "$all_content" | grep -qF "$name"; then
        orphan_atts+=("$att")
    fi
done < <(find "$VAULT" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.pdf" -o -name "*.webp" -o -name "*.svg" \))
echo "  Attachments orphelins: ${#orphan_atts[@]}"

# === DOSSIERS VIDES ===
empty_dirs=()
while IFS= read -r dir; do
    count=$(find "$dir" -maxdepth 1 | wc -l)
    [ "$count" -le 1 ] && empty_dirs+=("$dir")
done < <(find "$VAULT" -type d | grep -vE '\.obsidian|\.git')
echo "  Dossiers vides: ${#empty_dirs[@]}"

# === FICHIERS TEMPORAIRES ===
temp_files=()
while IFS= read -r tmp; do
    temp_files+=("$tmp")
done < <(find "$VAULT" -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*.swp" -o -name "*~" -o -name ".DS_Store" -o -name "Thumbs.db" \))
echo "  Fichiers temporaires: ${#temp_files[@]}"

# === NETTOYAGE ===
if [ "$DRY_RUN" = false ]; then
    read -p "Proceder au nettoyage? [O/N] " confirm
    if [[ "$confirm" =~ ^[OoYy]$ ]]; then
        for note in "${empty_notes[@]}"; do rm -f "$note"; done
        for att in "${orphan_atts[@]}"; do rm -f "$att"; done
        for dir in "${empty_dirs[@]}"; do rmdir "$dir" 2>/dev/null || true; done
        for tmp in "${temp_files[@]}"; do rm -f "$tmp"; done
        echo "Nettoyage termine!"
    fi
fi

vault_clean_cache() {
    local vault="$1"
    local cache_path="${vault}/.obsidian/cache"
    if [ -d "$cache_path" ]; then
        size=$(du -sm "$cache_path" | awk '{print $1}')
        rm -rf "$cache_path"
        echo "Cache supprime: ${size} MB"
    fi
}
```

## Options

| Option | Description |
|--------|-------------|
| `--all` | Nettoyer tout automatiquement |
| `--dry-run` | Prévisualiser sans supprimer |
| `--backup` | Backup avant nettoyage |
| `--force` | Pas de confirmation |
| `--exclude=pattern` | Exclure fichiers/dossiers |

## Exemples

```bash
# Analyser
/obs-clean

# Nettoyer tout
/obs-clean --all

# Supprimer notes vides uniquement
/obs-clean empty

# Nettoyer attachments orphelins
/obs-clean attachments --delete

# Previsualiser
/obs-clean --dry-run

# Nettoyer cache Obsidian
/obs-clean cache
```
