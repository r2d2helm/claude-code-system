# Commande: /obs-frontmatter

Gérer les métadonnées YAML frontmatter des notes.

## Syntaxe

```
/obs-frontmatter [action] [options]
```

## Actions

### /obs-frontmatter check

Vérifier quelles notes manquent de frontmatter :

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

valid=0
invalid=0
missing=0

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     ETAT FRONTMATTER                         ║"
echo "╠══════════════════════════════════════════════╣"

find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian' | while IFS= read -r note; do
    content=$(< "$note")
    [ -z "$content" ] && continue

    if echo "$content" | head -1 | grep -q '^---'; then
        has_title=$(echo "$content" | grep -c '^title:' || true)
        has_date=$(echo "$content" | grep -c '^date:' || true)
        has_type=$(echo "$content" | grep -c '^type:' || true)

        if [ "$has_title" -gt 0 ] && [ "$has_date" -gt 0 ] && [ "$has_type" -gt 0 ]; then
            echo "OK: $(basename "$note")"
        else
            echo "INCOMPLET: $(basename "$note") (manque: $([ "$has_title" -eq 0 ] && echo "title ")$([ "$has_date" -eq 0 ] && echo "date ")$([ "$has_type" -eq 0 ] && echo "type"))"
        fi
    else
        echo "MANQUANT: $(basename "$note")"
    fi
done | awk '
    /^OK/       { ok++ }
    /^INCOMPLET/ { inc++; print }
    /^MANQUANT/ { miss++; print }
    END { printf "\nResume: %d complets, %d incomplets, %d manquants\n", ok, inc, miss }
'

echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
```

### /obs-frontmatter add

Ajouter le frontmatter manquant aux notes qui n'en ont pas :

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
DRY_RUN=false
added=0

find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian' | while IFS= read -r note; do
    content=$(< "$note")
    # Skip si frontmatter deja present
    echo "$content" | head -1 | grep -q '^---' && continue

    # Extraire titre
    title=$(echo "$content" | grep -m1 '^# ' | sed 's/^# //' | sed "s/\"/'/g")
    [ -z "$title" ] && title=$(basename "$note" .md)

    # Determiner type
    type="reference"
    echo "$note" | grep -q 'Conversations' && type="conversation"
    echo "$note" | grep -q 'Concepts' && type="concept"
    echo "$note" | grep -q 'Formations' && type="formation"
    echo "$note" | grep -q 'Projets' && type="project"

    date=$(date -r "$note" '+%Y-%m-%d')

    fm="---
title: \"$title\"
date: $date
type: $type
tags:
  - $type
related: []
---

"

    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Ajout frontmatter: $(basename "$note")"
    else
        printf '%s%s' "$fm" "$content" > "$note"
        echo "Frontmatter ajoute: $(basename "$note")"
    fi
done
```

### /obs-frontmatter validate

Valider la cohérence du frontmatter existant (types valides, dates correctes, tags bien formés).

### /obs-frontmatter update-dates

Mettre à jour le champ `date` avec la date de dernière modification réelle du fichier.

## Exemples

```bash
# Verifier le frontmatter de tout le vault
/obs-frontmatter check

# Simuler l'ajout de frontmatter sans modifier les fichiers
/obs-frontmatter add --dry-run

# Ajouter le frontmatter manquant a toutes les notes
/obs-frontmatter add

# Verifier un vault alternatif
/obs-frontmatter check --vault=~/Documents/SecondVault

# Mettre a jour les dates selon la modification reelle des fichiers
/obs-frontmatter update-dates
```

## Options

| Option | Description |
|--------|-------------|
| `check` | Vérifier l'état du frontmatter |
| `add` | Ajouter frontmatter manquant |
| `validate` | Valider le frontmatter existant |
| `update-dates` | Mettre à jour les dates |
| `--dry-run` | Simuler sans modifier |
| `--vault=path` | Vault alternatif |
