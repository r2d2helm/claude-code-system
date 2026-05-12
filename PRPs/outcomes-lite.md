name: "PRP — Outcomes-lite (grader isolé + rubrique + retry borné)"
description: |
  Adapte le principe "Outcomes" d'Anthropic (Claude Managed Agents, mai 2026) au système r2d2 :
  un grader qui évalue un artefact contre une rubrique dans son propre contexte, plus une boucle
  de retry bornée (1 passe max) dans le workflow d'orchestration Contract-First.
  100 % markdown/prompts — aucun nouveau code Python. Additif et rétro-compatible.

## Purpose
Donner à r2d2 une "porte de sortie" pilotée par rubrique : on écrit ce qu'est "réussi", un grader
isolé le vérifie, et si ça échoue l'agent producteur retente UNE fois avec le feedback du grader,
puis on remonte à Mike. C'est `gaia-correctrice` opérationnalisée et la doctrine `review-surface`
appliquée à l'orchestration.

## Core Principles
1. **Context is King** — tout le contexte est dans ce PRP ou référencé par chemin.
2. **Validation Loops** — vérifications exécutables fournies (niveau 1/2/3).
3. **Information Dense** — réutilise les patterns existants (`commands/validate.md`, `agents/validation-gates.md`, `PRPs/templates/`).
4. **Progressive Success** — d'abord le template + le mode rubrique du grader, puis le flag `/validate`, puis le pattern de retry documenté.
5. **Règles globales** — respecter CLAUDE.md et le vault.

---

## Goal
À la fin :
- `~/.claude/PRPs/templates/rubric.md` existe — canevas de rubrique réutilisable.
- `~/.claude/agents/validation-gates.md` a une section **"Mode rubrique"** : entrée = rubrique + artefact ; sortie = verdict `PASS|FAIL` + liste numérotée de corrections demandées ; **l'agent ne modifie/applique RIEN sur l'artefact évalué** (override explicite de la section "Corrections autorisées" pour ce mode).
- `~/.claude/commands/validate.md` accepte `--rubric <chemin>` (avec une cible optionnelle) : invoque le grader en mode rubrique et restitue son rapport. Sans `--rubric` → comportement actuel **strictement inchangé**.
- `~/.claude/CLAUDE.md` § "Orchestration multi-agents (Contract-First)" décrit le **pattern de retry borné** (1 passe max, sinon escalade humaine) ; la table des Custom Commands mentionne `--rubric` ; la règle 14 est complétée.
- `Knowledge/Conversations/2026-05-11_Conv_Veille-AI-Dreaming-Manus-ClinicalAI.md` — Annexe A passe en statut "implémenté ✅" avec un pointeur vers le PRP.
- `/validate` (sans argument) sur le système après modif → toujours PASS, rien de cassé.

## Why
- **Valeur** : aujourd'hui `validation-gates` est un checker à 3 niveaux fixes ; il n'accepte pas de critères ad hoc et il n'y a pas de boucle de correction. Anthropic montre que "Outcomes" gagne jusqu'à +10 pts de succès (+8,4 % docx, +10,1 % pptx). On vole le principe, pas l'outil.
- **Intégration** : enrichit le dernier maillon du workflow Contract-First (skill-builder → router-updater + knowledge-indexer → **validation-gates**) sans toucher aux trois autres.
- **Résout** : pas de critères de succès paramétrables ; pas de retry ciblé (l'agent producteur ne reçoit jamais "voici précisément ce qui cloche, refais cette partie") ; doctrine `review-surface` non opérationnalisée dans l'orchestration.

## What
Comportement attendu :

1. **Rubrique** = fichier markdown : contexte de l'évaluation, table de critères (avec niveau `obligatoire|important|souhaitable`), seuil de réussite, format de sortie attendu du grader.
2. **Grader mode rubrique** = subagent `validation-gates` invoqué via Task tool (donc **contexte isolé** par construction) avec en entrée la rubrique + le chemin de l'artefact. Il lit, il évalue critère par critère, il produit :
   - `Verdict: PASS | FAIL`
   - Pour chaque critère en échec : `[#] <quoi> | <où — fichier:ligne si possible> | <pourquoi ça échoue le critère>`
   - **Il n'édite pas, ne supprime pas, ne réécrit pas l'artefact.** (Il peut, comme avant, lire/grepper.)
3. **`/validate --rubric <chemin> [cible]`** = la commande lit `$ARGUMENTS`, détecte `--rubric`, spawne le grader en mode rubrique, restitue son rapport tel quel. Pas de retry ici (la commande est une primitive de notation, pas un orchestrateur). Sans `--rubric` → la validation 3 niveaux actuelle, inchangée.
4. **Pattern de retry borné** (orchestration, documenté dans CLAUDE.md) : quand un agent producteur (ex. skill-builder) a produit un artefact et que `validation-gates` en mode rubrique renvoie `FAIL` → l'agent Lead re-spawne **une seule fois** l'agent producteur avec, injectée dans son prompt, la liste de corrections du grader. Si le 2ᵉ passage est encore `FAIL` → **stop**, on remonte le rapport à Mike. Jamais de 3ᵉ tentative, jamais de boucle.

### Success Criteria
- [ ] `~/.claude/PRPs/templates/rubric.md` créé, UTF-8 sans BOM, structure : Contexte / Critères (table avec niveau) / Seuil / Format de sortie du grader.
- [ ] `agents/validation-gates.md` : section "Mode rubrique" ajoutée ; frontmatter (`name`, `description`, `tools`) intact ; override explicite "en mode rubrique, NE PAS éditer l'artefact évalué — même pas le frontmatter, même pas un lien cassé".
- [ ] `commands/validate.md` : section "Mode rubrique (`--rubric`)" ajoutée ; parsing de `$ARGUMENTS` décrit ; comportement par défaut (sans `--rubric`) explicitement préservé.
- [ ] `CLAUDE.md` : sous-section "Boucle de retry bornée (Outcomes-lite)" dans § Orchestration ; table Custom Commands : ligne `/validate` mise à jour avec `--rubric` ; règle 14 complétée (mentionne le retry borné).
- [ ] Conv note : Annexe A → "implémenté ✅" + lien vers `PRPs/outcomes-lite.md`.
- [ ] `/validate` sans argument après modif → PASS (aucun skill/commande cassé).
- [ ] Démonstration fonctionnelle réussie (voir Validation Loop niveau 2).
- [ ] Aucun fichier Python créé ou modifié.

## Contexte nécessaire

### Documentation & Références
```yaml
- file: ~/.claude/PRPs/INITIAL-outcomes-lite.md
  why: La feature request d'origine (3+1 pièces, considérations, anti-moves).

- file: ~/.claude/commands/validate.md
  why: Commande à étendre. Syntaxe PowerShell dans les blocs de code. Structure "Cible : $ARGUMENTS" → "Niveau 1/2/3" → "Rapport". NE PAS casser le comportement par défaut.

- file: ~/.claude/agents/validation-gates.md
  why: Agent à étendre. Frontmatter YAML (name/description/tools: Bash, Read, Edit, Grep, Glob). Blocs bash. Sections : Périmètre / Processus 3 niveaux / Rapport / Processus itératif / Corrections autorisées / Principes. La section "Corrections autorisées" doit être explicitement neutralisée en mode rubrique.

- file: ~/.claude/PRPs/templates/prp_base.md
  why: Template PRP (déjà suivi par ce fichier). Le nouveau rubric.md s'en inspire pour le ton "canevas r2d2".

- file: ~/.claude/PRPs/templates/INITIAL.md
  why: Exemple de mini-template avec sections claires — modèle de simplicité pour rubric.md.

- file: ~/.claude/CLAUDE.md
  why: §"Orchestration multi-agents (Contract-First)" + règles 12-14 + table Custom Commands + table des hooks/Memory v2. C'est là que le pattern de retry et les màj de doc atterrissent.

- vault: "[[2026-05-11_Conv_Veille-AI-Dreaming-Manus-ClinicalAI]]"
  why: Roadmap complète + Annexe A = le plan détaillé de CE chantier. À mettre à jour en fin de course.

- vault: "[[review-surface-machine-propose-humain-land]]"   # dans C:\Users\r2d2\Documents\R2D2-Memory\principes\
  why: Doctrine encadrante. Le grader pointe / l'humain (ou l'auto opt-in) land / borne anti-boucle obligatoire. Le retry borné EST l'application de ce principe.

- url: https://claude.com/blog/new-in-claude-managed-agents
  why: Définition d'origine de "Outcomes" — grader séparé en contexte propre + retry. On ne dépend PAS de Claude Managed Agents : principe seulement.
```

### Arbre actuel du système (extrait pertinent)
```
~/.claude/
├── commands/
│   └── validate.md            # /validate — 3 niveaux fixes, PowerShell
├── agents/
│   ├── skill-builder.md        # producteur upstream (Contract-First)
│   ├── router-updater.md       # consommateur downstream
│   ├── knowledge-indexer.md    # consommateur downstream
│   └── validation-gates.md     # checker final — À ÉTENDRE
├── PRPs/
│   ├── templates/
│   │   ├── prp_base.md
│   │   └── INITIAL.md          # + rubric.md À CRÉER
│   ├── INITIAL-outcomes-lite.md
│   └── outcomes-lite.md        # ce PRP
└── CLAUDE.md                   # § Orchestration + règles + table commandes — À ÉTENDRE
```

### Arbre souhaité avec nouveaux fichiers
```
~/.claude/
├── PRPs/templates/rubric.md           # NOUVEAU — canevas de rubrique
├── agents/validation-gates.md         # MODIFIÉ — + section "Mode rubrique"
├── commands/validate.md               # MODIFIÉ — + section "--rubric"
└── CLAUDE.md                          # MODIFIÉ — + retry borné, table commandes, règle 14
~/Documents/Knowledge/Conversations/
└── 2026-05-11_Conv_Veille-AI-Dreaming-Manus-ClinicalAI.md   # MODIFIÉ — Annexe A → implémenté
```

### Gotchas connus du système
```
# CRITICAL: Aucun nouveau code Python. C'est de l'édition de prompts/markdown + 1 template.
# CRITICAL: Rétro-compatibilité absolue — /validate sans --rubric = comportement actuel inchangé.
# CRITICAL: En mode rubrique, validation-gates n'édite RIEN sur l'artefact évalué (override de "Corrections autorisées"). Séparation pointer / corriger / appliquer.
# CRITICAL: Retry borné — 1 passe max, jamais de boucle. 2e FAIL → escalade humaine (loi-de-la-membrane).
# CRITICAL: UTF-8 sans BOM pour .md ; ne pas casser le frontmatter YAML de validation-gates.md.
# CRITICAL: validate.md utilise PowerShell dans ses blocs ; validation-gates.md utilise bash. Garder chaque style.
# CRITICAL: /validate est une commande GLOBALE (~/.claude/commands/), pas un skill — pas (ou très peu) de màj meta-router nécessaire.
# CRITICAL: Ne pas migrer vers Claude Managed Agents ; aucune dépendance externe.
```

## Implementation Blueprint

### Structure des fichiers
```yaml
Fichier 1:
  path: ~/.claude/PRPs/templates/rubric.md
  rôle: Canevas de rubrique réutilisable (critères + niveaux + seuil + format de sortie attendu du grader)
  pattern: ~/.claude/PRPs/templates/INITIAL.md (simplicité), ton "canevas r2d2"

Fichier 2:
  path: ~/.claude/agents/validation-gates.md  (MODIFY)
  rôle: + section "Mode rubrique" ; override "Corrections autorisées" en mode rubrique
  pattern: ne pas toucher au reste ; même style bash/markdown

Fichier 3:
  path: ~/.claude/commands/validate.md  (MODIFY)
  rôle: + section "Mode rubrique (--rubric)" ; parsing $ARGUMENTS ; défaut préservé
  pattern: même style PowerShell/markdown ; ajouter après la ligne "Cible : $ARGUMENTS"

Fichier 4:
  path: ~/.claude/CLAUDE.md  (MODIFY)
  rôle: + sous-section retry borné dans § Orchestration ; table Custom Commands (/validate) ; règle 14
  pattern: respecter le formatage des tables/sections existantes

Fichier 5:
  path: ~/Documents/Knowledge/Conversations/2026-05-11_Conv_Veille-AI-Dreaming-Manus-ClinicalAI.md  (MODIFY)
  rôle: Annexe A → "implémenté ✅" + lien PRP ; (optionnel) status frontmatter growing→evergreen si jugé stable
```

### Liste des tâches ordonnées
```yaml
Task 1:
  action: CREATE
  path: ~/.claude/PRPs/templates/rubric.md
  description: |
    Canevas markdown. Sections :
    # Rubrique : <nom>
    ## Contexte           — qu'est-ce qui est évalué, produit par quel agent, dans quel but
    ## Critères           — table : | # | Critère (vérifiable) | Niveau (obligatoire/important/souhaitable) | Comment vérifier |
    ## Seuil de réussite  — règle explicite (ex: tous les "obligatoire" PASS + ≥ 70% des "important" PASS)
    ## Format de sortie attendu du grader  — Verdict PASS|FAIL ; pour chaque échec : [#] quoi | où (fichier:ligne) | pourquoi
    ## Notes              — (optionnel) hors-périmètre, hypothèses
  pattern: ~/.claude/PRPs/templates/INITIAL.md

Task 2:
  action: MODIFY
  path: ~/.claude/agents/validation-gates.md
  description: |
    Ajouter, APRÈS la section "Processus de validation à 3 niveaux" et AVANT "Rapport de validation",
    une section "## Mode rubrique (Outcomes-lite)" :
      - Déclencheur : invoqué avec une rubrique (chemin) + un artefact (chemin) au lieu / en plus du périmètre système.
      - Étapes : lire la rubrique → lire l'artefact → évaluer chaque critère → produire verdict + liste de corrections.
      - Sortie : bloc structuré (Verdict ; pour chaque critère FAIL : [#] quoi | où | pourquoi ; rappel du seuil).
      - INTERDICTION explicite : en mode rubrique, l'agent NE corrige RIEN (override de "Corrections autorisées" — pas de frontmatter, pas de BOM, pas de lien cassé sur l'artefact évalué). Il pointe, le producteur corrigera, l'humain landera.
      - Pas de retry depuis l'agent lui-même : le retry est piloté par le Lead (cf. CLAUDE.md § Orchestration).
    Compléter aussi la section "Corrections autorisées" avec une ligne : "⚠️ EXCEPTION : en Mode rubrique, AUCUNE correction n'est autorisée sur l'artefact évalué."
  pattern: style existant (bash + markdown), frontmatter intact

Task 3:
  action: MODIFY
  path: ~/.claude/commands/validate.md
  description: |
    Après "## Cible : $ARGUMENTS" et son paragraphe, ajouter "## Mode rubrique (`--rubric`)" :
      - Si $ARGUMENTS contient `--rubric <chemin-rubrique>` (et optionnellement une cible après) :
        → invoquer l'agent `validation-gates` en mode rubrique (Task tool) avec rubrique + cible (défaut cible = système / dernier artefact pertinent)
        → restituer SON rapport tel quel (verdict + liste de corrections)
        → NE PAS exécuter les 3 niveaux fixes dans ce mode
        → NE PAS lancer de retry ici (la commande est une primitive de notation)
      - Sinon (pas de `--rubric`) : comportement actuel inchangé (3 niveaux, ou système complet si pas d'argument).
    Ajouter un petit exemple : `/validate --rubric PRPs/rubrics/mon-skill.md ~/.claude/skills/mon-skill`
  pattern: style existant (PowerShell + markdown)

Task 4:
  action: MODIFY
  path: ~/.claude/CLAUDE.md
  description: |
    (a) Dans "### Orchestration multi-agents (Contract-First)", après le schéma et "Principes :", ajouter une sous-section :
        "#### Boucle de retry bornée (Outcomes-lite)
         - Après validation-gates en mode rubrique, si verdict = FAIL → le Lead re-spawne l'agent producteur UNE seule fois, avec la liste de corrections du grader injectée dans son prompt.
         - Si le 2e passage est encore FAIL → STOP. On remonte le rapport du grader à l'utilisateur. Jamais de 3e tentative, jamais de boucle (loi-de-la-membrane).
         - Le grader pointe, le producteur corrige, l'humain land — doctrine review-surface."
    (b) Table "### Custom Commands" : ligne /validate → Usage : "/validate, /validate mon-skill, /validate --rubric <rubrique> [cible]" ; Description : "... + mode rubrique (grader Outcomes-lite)".
    (c) Règle 14 (§ Orchestration multi-agents) : ajouter "; en cas d'échec sur rubrique, appliquer la boucle de retry bornée (1 passe max, sinon escalade humaine)".
  pattern: respecter strictement le formatage des tables/sections existantes ; ne PAS toucher au reste de CLAUDE.md

Task 5:
  action: MODIFY
  path: ~/Documents/Knowledge/Conversations/2026-05-11_Conv_Veille-AI-Dreaming-Manus-ClinicalAI.md
  description: |
    Dans "## Annexe A — Plan détaillé du chantier ① (Outcomes-lite)" : ajouter en tête "Statut : ✅ implémenté le {date} — voir `~/.claude/PRPs/outcomes-lite.md` et `PRPs/INITIAL-outcomes-lite.md`."
    Dans "## 4. Roadmap" : passer le statut de ① de "plan détaillé en annexe A, en attente de green-light" à "✅ implémenté {date}".
    (Optionnel) Ajouter un wikilink vers [[review-surface-machine-propose-humain-land]] s'il n'y est pas déjà.
  pattern: frontmatter/markdown du vault, wikilinks
```

### Points d'intégration
```yaml
ROUTER:
  - Optionnel / faible priorité : /validate est une commande globale, pas un skill. Si souhaité, ajouter dans skills/SKILL.md près de "validate skill -> si contexte verification" un rappel : "validate --rubric / rubrique / grader -> mode Outcomes-lite". Sinon, ne rien faire.

VAULT:
  - Mettre à jour la Conv note (Task 5). Pas de nouvelle note obligatoire — la Conv note + le principe R2D2-Memory couvrent déjà la doctrine. Si l'exécutant juge utile, une courte note Références/ "Outcomes-lite — mode rubrique" est acceptable mais non requise.
  - Pas de modification des _Templates/ du vault.

MCP:
  - Aucun impact sur knowledge-assistant.

CLAUDE.MD:
  - § Orchestration multi-agents (Contract-First) : + sous-section retry borné.
  - Table Custom Commands : ligne /validate.
  - Règle 14.
  - (Pas de changement au compte de skills/commandes : on n'ajoute pas de commande, on étend /validate.)

R2D2-Memory:
  - Aucun nouveau principe (review-surface déjà gravé). Ne pas y toucher.
```

## Validation Loop

### Niveau 1 : Structure & Syntax
```powershell
# Le template existe et est en UTF-8 sans BOM
Test-Path "~/.claude/PRPs/templates/rubric.md"
$b = [System.IO.File]::ReadAllBytes((Resolve-Path "~/.claude/PRPs/templates/rubric.md"))
if ($b[0] -eq 0xEF -and $b[1] -eq 0xBB) { Write-Warning "BOM détecté dans rubric.md" }

# Le frontmatter de validation-gates.md est intact (3 champs)
Select-String -Path "~/.claude/agents/validation-gates.md" -Pattern "^name:|^description:|^tools:" | Measure-Object  # attendu : 3

# Les fichiers modifiés contiennent les nouvelles sections
Select-String -Path "~/.claude/agents/validation-gates.md" -Pattern "Mode rubrique"        # >= 1
Select-String -Path "~/.claude/commands/validate.md"        -Pattern "--rubric"             # >= 1
Select-String -Path "~/.claude/CLAUDE.md"                   -Pattern "retry born|Outcomes-lite"  # >= 1

# Aucun .py touché
git -C "~" status --porcelain 2>$null | Select-String "\.py$"   # attendu : vide (ou: vérifier manuellement la liste des fichiers modifiés)
```

### Niveau 2 : Fonctionnel (démonstration manuelle)
```
1. Créer une rubrique de test à partir de PRPs/templates/rubric.md, ex. PRPs/rubrics/_test-demo.md
   avec 2 critères "obligatoire" simples et vérifiables (ex: "le fichier X contient une section Y").
2. Créer un artefact de test volontairement NON conforme (il manque la section Y).
3. /validate --rubric PRPs/rubrics/_test-demo.md <artefact-de-test>
   → attendu : le grader (validation-gates, contexte isolé) renvoie Verdict: FAIL + liste [1] ... [2] ...
   → vérifier qu'il n'a PAS modifié l'artefact.
4. Simuler le retry borné (à la main, dans le rôle du Lead) : re-donner l'artefact + la liste de corrections
   à "l'agent producteur" (ici, l'exécutant) → corriger → relancer /validate --rubric → attendu : PASS.
5. Vérifier qu'un 2e échec hypothétique ne déclenche PAS de 3e tour : la doc CLAUDE.md le dit, et l'agent
   validation-gates ne relance jamais lui-même.
6. Nettoyer : supprimer PRPs/rubrics/_test-demo.md et l'artefact de test.
```

### Niveau 3 : Intégration
```powershell
# Rien n'est cassé
/validate                       # attendu : PASS (3 niveaux), score stable
# Cohérence doc
Select-String -Path "~/.claude/CLAUDE.md" -Pattern "/validate"   # la ligne table mentionne --rubric
# Health vault stable
/guardian-health --quick        # attendu : pas de régression
```

## Checklist de validation finale
- [ ] `PRPs/templates/rubric.md` créé, UTF-8 sans BOM, sections complètes
- [ ] `validation-gates.md` : section "Mode rubrique" + override "Corrections autorisées" ; frontmatter intact
- [ ] `validate.md` : section `--rubric` ; défaut préservé ; exemple présent
- [ ] `CLAUDE.md` : sous-section retry borné + table /validate + règle 14
- [ ] Conv note : Annexe A "implémenté ✅" + lien PRP
- [ ] `/validate` sans argument → PASS
- [ ] Démonstration niveau 2 réussie (FAIL détecté, pas d'édition de l'artefact, retry → PASS, pas de 3e tour)
- [ ] Zéro fichier `.py` créé ou modifié
- [ ] Aucun skill / commande / agent existant cassé

---

## Anti-Patterns à éviter
- ❌ Écrire du Python / un script utilitaire. Ce chantier est 100 % markdown/prompts.
- ❌ Casser le comportement par défaut de `/validate` (sans `--rubric` ⇒ exactement comme avant).
- ❌ Laisser `validation-gates` éditer l'artefact évalué en mode rubrique (même un "petit fix" de frontmatter). Le grader pointe, il ne corrige pas.
- ❌ Boucle de retry > 1 passe. 2e FAIL ⇒ escalade humaine, point.
- ❌ Migrer vers Claude Managed Agents / introduire une dépendance externe.
- ❌ Toucher à `R2D2-Memory/` (la doctrine est déjà gravée), aux `_Templates/` du vault, ou au reste de CLAUDE.md hors des 3 points listés.
- ❌ Créer une nouvelle commande `/grade` ou `/outcomes` : c'est un flag sur `/validate`, comme spécifié.
- ❌ Hardcoder des chemins absolus là où `~/.claude/...` suffit.

---

## Score de confiance : 8/10
Implémentation quasi-mécanique (édition de 4 fichiers + 1 création + 1 màj vault), specs détaillées, patterns existants clairs, doctrine de référence gravée. Le -2 : (a) la "démonstration fonctionnelle" du retry est manuelle, pas un test automatisable ; (b) risque que l'exécutant sur-conçoive (Python, mode "both" rubrique+3-niveaux, nouvelle commande) — d'où la section Anti-Patterns insistante.
