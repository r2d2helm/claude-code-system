# Commande: /obs-orphans

Détecter les notes orphelines (sans liens entrants ni sortants).

## Syntaxe

```
/obs-orphans [options]
```

## Comportement

Analyse toutes les notes du vault et identifie celles qui ne sont liées à aucune autre note (ni via `[[wikilinks]]` entrants, ni sortants). Les notes système (`_Templates/`, `_Index/`, `README`) sont exclues.

## Script bash

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

declare -A all_backlinks
declare -A all_outlinks

# Collecter tous les liens
while IFS= read -r note; do
    name=$(basename "$note" .md)
    links=$(grep -oP '\[\[\K[^\]|]+(?=[\]|])' "$note" 2>/dev/null || true)
    all_outlinks["$name"]="$links"
    while IFS= read -r target; do
        [ -n "$target" ] && all_backlinks["$target"]+=" $name"
    done <<< "$links"
done < <(find "$VAULT" -name "*.md" -type f)

# Trouver les orphelins
orphans=()
no_backlinks=()

while IFS= read -r note; do
    name=$(basename "$note" .md)
    rel="${note#$VAULT/}"

    # Exclure notes systeme
    echo "$note" | grep -qE '(_Templates|_Index|_Attachments|\.obsidian)' && continue
    echo "$name" | grep -qE '^(README|INDEX)' && continue

    has_backlinks=false
    [ -n "${all_backlinks[$name]:-}" ] && has_backlinks=true
    has_outlinks=false
    [ -n "${all_outlinks[$name]:-}" ] && has_outlinks=true

    if [ "$has_backlinks" = false ] && [ "$has_outlinks" = false ]; then
        orphans+=("$rel")
    elif [ "$has_backlinks" = false ] && [ "$has_outlinks" = true ]; then
        no_backlinks+=("$rel")
    fi
done < <(find "$VAULT" -name "*.md" -type f)

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     NOTES ORPHELINES                         ║"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"
printf "║  Totalement isolees: %4d                  ║\n" "${#orphans[@]}"
printf "║  Sans backlinks:     %4d                  ║\n" "${#no_backlinks[@]}"
echo "║                                              ║"

if [ "${#orphans[@]}" -gt 0 ]; then
    echo "║  ISOLEES (aucun lien):                       ║"
    count=0
    for o in "${orphans[@]}"; do
        [ "$count" -ge 15 ] && break
        printf "║    - %-38s║\n" "$o"
        count=$((count + 1))
    done
    remaining=$((${#orphans[@]} - 15))
    [ "$remaining" -gt 0 ] && printf "║    ... et %d de plus                         ║\n" "$remaining"
fi

echo "║                                              ║"
echo "║  Actions suggérees:                          ║"
echo "║  1. Ajouter des [[liens]] vers ces notes     ║"
echo "║  2. Deplacer vers _Inbox/ pour tri           ║"
echo "║  3. Supprimer si obsoletes                   ║"
echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
```

## Exemples

```bash
# Lister toutes les notes orphelines du vault
/obs-orphans

# Obtenir des suggestions de liens pour les notes isolees
/obs-orphans --suggest

# Deplacer automatiquement les orphelins vers _Inbox/ pour tri
/obs-orphans --move-inbox

# Exporter la liste des orphelins en JSON pour traitement
/obs-orphans --json

# Combiner : suggerer des liens et exporter en JSON
/obs-orphans --suggest --json
```

## Options

| Option | Description |
|--------|-------------|
| `--suggest` | Suggérer des liens possibles |
| `--move-inbox` | Déplacer les orphelins vers _Inbox/ |
| `--json` | Sortie JSON |
