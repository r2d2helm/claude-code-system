# Commande: /know-report

Générer un rapport périodique de la base de connaissances.

## Syntaxe

```
/know-report [options]
```

## Description

Génère un rapport hebdomadaire du vault : statistiques globales, notes créées et modifiées sur la période, tags les plus utilisés, notes orphelines et recommandations d'actions. Le rapport est sauvegardé dans _Index/ et lié à la Daily Note du jour.

## Options

| Option | Description |
|--------|-------------|
| `--period=PERIOD` | Période: `week` (défaut), `month`, `all` |
| `--since=DATE` | Date de début personnalisée (YYYY-MM-DD) |
| `--output=FILE` | Chemin du rapport (défaut: _Index/Report_DATE.md) |
| `--format=FMT` | Format: `md` (défaut), `json` |
| `--no-save` | Afficher sans sauvegarder |

## Exemples

### Rapport hebdomadaire complet

```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
DATE=$(date +%Y-%m-%d)
SINCE=$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)
REPORT="$KNOWLEDGE_PATH/_Index/Report_${DATE}.md"

# Statistiques globales
TOTAL=$(find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/.git/*' -not -path '*/_Templates/*' | wc -l)
CONVS=$(find "$KNOWLEDGE_PATH/Conversations" -name '*.md' 2>/dev/null | wc -l)
CONCEPTS=$(find "$KNOWLEDGE_PATH/Concepts" -name '*.md' 2>/dev/null | wc -l)
CODE=$(find "$KNOWLEDGE_PATH/Code" -name '*.md' 2>/dev/null | wc -l)
INBOX=$(find "$KNOWLEDGE_PATH/_Inbox" -name '*.md' 2>/dev/null | wc -l)

# Notes de la semaine
NEW_NOTES=$(find "$KNOWLEDGE_PATH" -name '*.md' -newermt "$SINCE" \
    -not -path '*/.git/*' -not -path '*/_Templates/*' 2>/dev/null | wc -l)
MODIFIED=$(find "$KNOWLEDGE_PATH" -name '*.md' -newermt "$SINCE" \
    -not -path '*/.git/*' 2>/dev/null | wc -l)

# Notes orphelines (sans backlinks)
ORPHANS=0
while IFS= read -r filepath; do
    name=$(basename "$filepath" .md)
    refs=$(grep -rl "\[\[$name\]\]" "$KNOWLEDGE_PATH" --include='*.md' 2>/dev/null | \
           grep -v "$filepath" | wc -l)
    [ "$refs" -eq 0 ] && ORPHANS=$((ORPHANS + 1))
done < <(find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/_Index/*' \
    -not -path '*/.git/*' -not -path '*/_Templates/*' 2>/dev/null)

# Top 10 tags
TOP_TAGS=$(grep -roh '#[a-zA-Z][a-zA-Z0-9_/-]*' "$KNOWLEDGE_PATH" --include='*.md' \
    --exclude-dir='.git' 2>/dev/null | sort | uniq -c | sort -rn | head -10)

# Générer le rapport
cat > "$REPORT" << EOF
---
date: $DATE
type: report
tags: [report, weekly]
---

# Rapport Hebdomadaire - $DATE

> Période: $SINCE -> $DATE

## Statistiques Globales

| Métrique | Valeur |
|----------|--------|
| Total notes | $TOTAL |
| Conversations | $CONVS |
| Concepts | $CONCEPTS |
| Code snippets | $CODE |
| Inbox (à traiter) | $INBOX |
| Orphelines | $ORPHANS |

## Activité de la Semaine

- Notes créées/modifiées: **$MODIFIED**
- Nouvelles notes: **$NEW_NOTES**

### Notes Récentes
EOF

# Ajouter la liste des notes récentes
find "$KNOWLEDGE_PATH" -name '*.md' -newermt "$SINCE" \
    -not -path '*/.git/*' -not -path '*/_Index/*' \
    -printf '%TY-%Tm-%Td  %p\n' 2>/dev/null | sort -rn | head -20 | \
    while read -r d filepath; do
        echo "- $d [[$(basename "$filepath" .md)]]"
    done >> "$REPORT"

cat >> "$REPORT" << EOF

## Top Tags

\`\`\`
$TOP_TAGS
\`\`\`

## Recommandations

EOF

# Recommandations dynamiques
[ "$INBOX" -gt 5 ] && echo "- **Inbox saturée** ($INBOX notes) : trier avec \`/know-wizard review daily\`" >> "$REPORT"
[ "$ORPHANS" -gt 10 ] && echo "- **Notes orphelines** ($ORPHANS) : lier avec \`/know-link --all\`" >> "$REPORT"
[ "$NEW_NOTES" -eq 0 ] && echo "- **Aucune nouvelle note** cette semaine : capturer davantage" >> "$REPORT"

echo "" >> "$REPORT"
echo "---" >> "$REPORT"
echo "*Rapport généré le $DATE*" >> "$REPORT"

echo "Rapport créé: $REPORT"
echo "  Total: $TOTAL notes | Semaine: +$NEW_NOTES | Inbox: $INBOX | Orphelines: $ORPHANS"
```

### Rapport en JSON

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"

jq -n \
  --arg date "$(date +%Y-%m-%d)" \
  --argjson total "$(find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/.git/*' | wc -l)" \
  --argjson inbox "$(find "$KNOWLEDGE_PATH/_Inbox" -name '*.md' 2>/dev/null | wc -l)" \
  --argjson week "$(find "$KNOWLEDGE_PATH" -name '*.md' -mtime -7 -not -path '*/.git/*' | wc -l)" \
  '{date: $date, total: $total, inbox: $inbox, modified_this_week: $week}'
```

### Statistiques rapides (sans sauvegarde)

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"

echo "=== Knowledge Vault Stats ==="
printf "%-20s %s\n" "Total notes:" "$(find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/.git/*' | wc -l)"
printf "%-20s %s\n" "Conversations:" "$(find "$KNOWLEDGE_PATH/Conversations" -name '*.md' 2>/dev/null | wc -l)"
printf "%-20s %s\n" "Concepts:" "$(find "$KNOWLEDGE_PATH/Concepts" -name '*.md' 2>/dev/null | wc -l)"
printf "%-20s %s\n" "Inbox:" "$(find "$KNOWLEDGE_PATH/_Inbox" -name '*.md' 2>/dev/null | wc -l)"
printf "%-20s %s\n" "Taille vault:" "$(du -sh "$KNOWLEDGE_PATH" --exclude='.git' 2>/dev/null | cut -f1)"
printf "%-20s %s\n" "Dernière modif:" "$(find "$KNOWLEDGE_PATH" -name '*.md' -printf '%T+ %p\n' 2>/dev/null | sort -r | head -1 | cut -d. -f1)"
```

## Notes

- Le rapport hebdomadaire est le meilleur outil pour la revue du dimanche.
- Les notes orphelines sont celles sans aucun wikilink entrant depuis une autre note.
- Combiner avec `/know-index --full` pour reconstruire l'index après la revue.
- Le format JSON est utile pour intégrer les stats dans des dashboards externes.
- L'historique des rapports dans _Index/ permet de suivre l'évolution du vault.
