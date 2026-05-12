# Wizard: Audit Complet du Vault

Audit guidé et complet de la santé du vault Obsidian.

## Déclenchement

```
/obs-wizard audit
```

## Étapes du Wizard (6)

### Étape 1: Scan Initial

```
╔══════════════════════════════════════════════════════════════╗
║             AUDIT VAULT OBSIDIAN                             ║
║                Étape 1/6 : Scan Initial                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Vault: ~/Documents/Knowledge                                ║
║                                                              ║
║  Scan en cours...                                            ║
║  [████████████████████████████████████████] 100%             ║
║                                                              ║
║  RESULTATS DU SCAN:                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Notes totales         : 456                             │ ║
║  │ Attachments           : 156 (234 MB)                    │ ║
║  │ Dossiers              : 23                              │ ║
║  │ Taille totale         : 312 MB                          │ ║
║  │ Derniere modification : 2026-02-04 14:30                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [Continuer ->]                                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Analyse des Liens

```
╔══════════════════════════════════════════════════════════════╗
║             AUDIT VAULT OBSIDIAN                             ║
║               Étape 2/6 : Analyse Liens                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STATISTIQUES LIENS:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Liens internes totaux  : 1,234                          │ ║
║  │ Liens externes (URLs)  : 89                             │ ║
║  │ Moyenne liens/note     : 2.7                            │ ║
║  │ Notes sans liens       : 45                             │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  PROBLEMES DETECTES:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Liens casses        : 5                                 │ ║
║  │    -> Architecture.md: [[API-Design]]                   │ ║
║  │    -> Architecture.md: [[Database-Schema]]              │ ║
║  │    -> Zettelkasten.md: [[Luhmann-Bio]]                  │ ║
║  │                                                         │ ║
║  │ Notes orphelines   : 12                                 │ ║
║  │    (sans liens entrants ni sortants)                    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Reparer liens maintenant  [2] Continuer ->              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 3: Analyse des Tags

```
╔══════════════════════════════════════════════════════════════╗
║             AUDIT VAULT OBSIDIAN                             ║
║                Étape 3/6 : Analyse Tags                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STATISTIQUES TAGS:                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Tags uniques          : 89                              │ ║
║  │ Notes avec tags       : 412 / 456 (90%)                 │ ║
║  │ Moyenne tags/note     : 2.3                             │ ║
║  │ Tags hierarchiques    : 45 (51%)                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  PROBLEMES DETECTES:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Tags similaires (possibles doublons):                   │ ║
║  │ - #proxmox (45) <-> #Proxmox (3) <-> #pve (8)           │ ║
║  │ - #python (38) <-> #Python (5)                           │ ║
║  │ - #todo (32) <-> #TODO (2)                               │ ║
║  │                                                         │ ║
║  │ Tags utilises 1 seule fois: 8                           │ ║
║  │ Notes sans aucun tag: 44                                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Normaliser tags maintenant  [2] Continuer ->            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 4: Analyse du Contenu

```
╔══════════════════════════════════════════════════════════════╗
║             AUDIT VAULT OBSIDIAN                             ║
║              Étape 4/6 : Analyse Contenu                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STATISTIQUES CONTENU:                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Mots totaux           : 125,430                         │ ║
║  │ Moyenne mots/note     : 275                             │ ║
║  │ Note la plus longue   : 5,234 mots                      │ ║
║  │ Notes avec frontmatter: 389 / 456 (85%)                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Notes vides ou tres courtes: 8                              ║
║  Notes sans frontmatter: 67                                  ║
║                                                              ║
║  [Continuer ->]                                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 5: Analyse des Fichiers

```
╔══════════════════════════════════════════════════════════════╗
║             AUDIT VAULT OBSIDIAN                             ║
║              Étape 5/6 : Analyse Fichiers                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STRUCTURE:                                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Profondeur max        : 4 niveaux OK                    │ ║
║  │ Dossiers              : 23                              │ ║
║  │ Dossiers vides        : 2                               │ ║
║  │ Convention nommage    : 78% conforme                    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ATTACHMENTS:                                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Total                 : 156 fichiers (234 MB)           │ ║
║  │ Orphelins             : 12 (23 MB)                      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Nettoyer maintenant  [2] Continuer ->                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 6: Rapport Final

```
╔══════════════════════════════════════════════════════════════╗
║             AUDIT VAULT OBSIDIAN                             ║
║               Étape 6/6 : Rapport Final                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  SCORE DE SANTE GLOBAL: 72/100                               ║
║  ████████████████████████████████░░░░░░░░                    ║
║                                                              ║
║  RESUME PAR CATEGORIE:                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Structure          18/20    Bon                         │ ║
║  │ Liens              14/20    A ameliorer                 │ ║
║  │ Tags               12/15    A ameliorer                 │ ║
║  │ Contenu            13/15    Bon                         │ ║
║  │ Fichiers           8/15     A ameliorer                 │ ║
║  │ Maintenance        7/15     Action requise              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ACTIONS URGENTES:                                           ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. Reparer 5 liens casses                               │ ║
║  │ 2. Supprimer 12 attachments orphelins (23 MB)           │ ║
║  │ 3. Traiter 8 notes vides                                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  RAPPORT EXPORTE:                                            ║
║  ~/Documents/Knowledge/_Index/Audit-2026-02-04.md           ║
║                                                              ║
║  [1] Corriger tout automatiquement                           ║
║  [2] Corriger etape par etape                                ║
║  [3] Exporter rapport detaille                               ║
║  [4] Terminer                                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Rapport Généré

Le wizard génère un rapport Markdown dans `_Index/Audit-{date}.md` :

```markdown
---
title: Audit Vault - 2026-02-04
date: 2026-02-04
type: audit
tags: [audit, maintenance]
---

# Audit du Vault - 2026-02-04

## Score Global: 72/100

## Statistiques

| Métrique | Valeur |
|----------|--------|
| Notes totales | 456 |
| Mots totaux | 125,430 |
| Liens internes | 1,234 |
| Tags uniques | 89 |
| Attachments | 156 (234 MB) |
| Taille totale | 312 MB |

## Problèmes Détectés

### Urgents

- [ ] 5 liens cassés
- [ ] 12 attachments orphelins
- [ ] 8 notes vides

### À Améliorer

- [ ] 3 groupes de tags à normaliser
- [ ] 67 notes sans frontmatter
- [ ] 12 notes orphelines
- [ ] 2 doublons

---
*Généré par Obsidian Agent*
```

## Script Complet du Wizard

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
AUTO_FIX=false
score=100
issues=()

echo ""
echo "=== ETAPE 1/6: Scan Initial ==="

mapfile -t notes < <(find "$VAULT" -name "*.md" -type f 2>/dev/null)
mapfile -t attachments < <(find "$VAULT" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.pdf" \) 2>/dev/null)

note_count=${#notes[@]}
att_count=${#attachments[@]}
total_size=$(du -sm "$VAULT" | awk '{print $1}')

echo "  Notes: $note_count"
echo "  Attachments: $att_count"
echo "  Taille totale: ${total_size} MB"

echo ""
echo "=== ETAPE 2/6: Analyse Liens ==="

mapfile -t note_names < <(printf '%s\n' "${notes[@]}" | xargs -I{} basename {} .md)
broken_links=()
while IFS= read -r note; do
    while IFS= read -r target; do
        [ -z "$target" ] && continue
        echo "$target" | grep -qE '^https?://' && continue
        found=false
        for n in "${note_names[@]}"; do [ "$n" = "$target" ] && found=true && break; done
        [ "$found" = false ] && broken_links+=("$(basename "$note"):$target")
    done < <(grep -oP '\[\[\K[^\]|#]+' "$note" 2>/dev/null || true)
done < <(printf '%s\n' "${notes[@]}")

broken_count=${#broken_links[@]}
if [ "$broken_count" -gt 0 ]; then
    penalty=$((broken_count * 4 > 20 ? 20 : broken_count * 4))
    score=$((score - penalty))
    issues+=("Liens casses: $broken_count")
fi
echo "  Liens casses: $broken_count"

echo ""
echo "=== ETAPE 3/6: Analyse Tags ==="

all_tags=$(find "$VAULT" -name "*.md" -type f | xargs grep -hoP '#[\w/-]+' 2>/dev/null | sort -u)
similar_count=$(echo "$all_tags" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g' | sort | uniq -d | wc -l)
if [ "$similar_count" -gt 0 ]; then
    penalty=$((similar_count * 3 > 15 ? 15 : similar_count * 3))
    score=$((score - penalty))
    issues+=("Tags similaires: $similar_count groupes")
fi
echo "  Tags similaires: $similar_count groupes"

echo ""
echo "=== ETAPE 6/6: Rapport Final ==="
echo ""
echo "  SCORE FINAL: $score/100"

# Generer rapport MD
report_path="${VAULT}/_Index/Audit-$(date '+%Y-%m-%d').md"
cat > "$report_path" << EOF
---
title: "Audit Vault - $(date '+%Y-%m-%d')"
date: $(date '+%Y-%m-%d')
type: audit
tags: [audit, maintenance]
---

# Audit du Vault - $(date '+%Y-%m-%d')

## Score Global: $score/100

## Problèmes: ${issues[*]}
EOF

echo "  Rapport genere: $report_path"
```

## Options

| Option | Description |
|--------|-------------|
| `--auto-fix` | Corriger automatiquement les problèmes |
| `--report-only` | Générer rapport sans interaction |
| `--export=file` | Exporter rapport vers fichier |
| `--verbose` | Afficher détails complets |

## Exemples

```bash
# Audit interactif
/obs-wizard audit

# Audit avec correction automatique
/obs-wizard audit --auto-fix

# Rapport uniquement
/obs-wizard audit --report-only

# Exporter rapport
/obs-wizard audit --export="audit-report.md"
```
