## FEATURE:

**Outcomes-lite** — adapter le principe "Outcomes" d'Anthropic (Claude Managed Agents, mai 2026) au système r2d2 : un grader isolé qui évalue contre une rubrique, plus une boucle de retry bornée dans le workflow d'orchestration Contract-First.

Trois pièces :

1. **Mode `--rubric <fichier>` pour `/validate`** — quand une rubrique est fournie, la validation se fait *contre la rubrique* (en plus, ou à la place, du check 3-niveaux fixe selon un flag). Sortie structurée : verdict `PASS` / `FAIL` + liste numérotée de points à corriger (chaque point = quoi + où + pourquoi ça échoue le critère).

2. **Mode "rubrique" pour l'agent `validation-gates`** — input = rubrique + artefact à évaluer ; output = verdict + diff de corrections demandées ; **l'agent grader pointe, il ne corrige pas et n'applique rien** (séparation pointer / corriger / appliquer — le grader évalue dans son propre contexte, pas pollué par le raisonnement de l'agent producteur).

3. **Boucle de retry bornée dans l'orchestration** — après `validation-gates`, si verdict = `FAIL`, l'agent Lead re-spawne l'agent d'origine **une seule fois** avec le diff du grader injecté. Si le 2ᵉ passage est encore `FAIL` → on s'arrête et on remonte à Mike (jamais de boucle infinie). À documenter dans `CLAUDE.md` § "Orchestration multi-agents (Contract-First)" et dans le SKILL.md / commande concernée.

4. **Template de rubrique** — `~/.claude/PRPs/templates/rubric.md` : un canevas réutilisable (critères, pondération optionnelle, seuil de réussite, format de sortie attendu du grader).

## CONTEXTE EXISTANT:

- `~/.claude/commands/validate.md` — commande `/validate` actuelle : validation 3 niveaux (structure/syntax, fonctionnel, intégration), syntaxe PowerShell. À étendre, **pas casser** : si aucune rubrique fournie → comportement actuel strictement inchangé (rétro-compatible).
- `~/.claude/agents/validation-gates.md` — subagent grader/checker existant (tools: Bash, Read, Edit, Grep, Glob). Périmètre : skills, commands, agents, meta-router, CLAUDE.md, MCP server, vault. À étendre avec le mode rubrique. Note : il a actuellement le tool `Edit` ("corrections autorisées") — en mode rubrique il ne doit PAS éditer l'artefact évalué.
- `~/.claude/CLAUDE.md` § "Orchestration multi-agents (Contract-First)" et règles 12-14 — c'est là que le pattern de retry borné doit être décrit.
- Workflow Contract-First : skill-builder (upstream) → router-updater + knowledge-indexer (downstream) → validation-gates (vérification finale). C'est ce dernier maillon qu'on enrichit.
- `~/.claude/PRPs/templates/` — `prp_base.md`, `INITIAL.md` : conventions PRP du système. Y ajouter `rubric.md`.
- Notes vault à consulter :
  - [[2026-05-11_Conv_Veille-AI-Dreaming-Manus-ClinicalAI]] — la roadmap complète + l'Annexe A (plan détaillé de ce chantier ①).
  - [[review-surface-machine-propose-humain-land]] *(dans R2D2-Memory/principes/)* — la doctrine encadrante : le grader pointe, l'humain (ou l'auto opt-in) land ; borne anti-boucle obligatoire.

## DOCUMENTATION:

- claude.com/blog/new-in-claude-managed-agents — feature "Outcomes" : *« A separate grader evaluates the output against your criteria in its own context window, so it isn't influenced by the agent's reasoning. When something isn't right, the grader pinpoints what needs to change and the agent takes another pass. »* (+10 pts de succès max ; +8,4 % docx, +10,1 % pptx). On vole le principe, pas l'outil — pas de dépendance à Claude Managed Agents.
- Convention r2d2 : commandes invocables `/<nom>`, fichiers `~/.claude/commands/`, agents `~/.claude/agents/`, PRPs `~/.claude/PRPs/`.

## CONSIDERATIONS:

- **Rétro-compatibilité absolue** : `/validate` sans rubrique = exactement le comportement actuel. Le mode rubrique est purement additif.
- **Borne anti-boucle** : max 1 retry. Jamais de boucle infinie (`loi-de-la-membrane`). Au 2ᵉ FAIL → stop + remontée humaine.
- **Séparation pointer/corriger/appliquer** : le grader (`validation-gates` en mode rubrique) ne modifie jamais l'artefact évalué. Il produit un diff de demandes. C'est l'agent producteur qui corrige (au retry), c'est l'humain (ou l'`--auto` opt-in, hors scope ici) qui land.
- **Encodage** : fichiers .md en UTF-8 sans BOM ; si des snippets .ps1 sont ajoutés, BOM + compat PS 5.1 (pas de `??`, pas de `UTF8BOM`).
- **Pas de nouveau code Python attendu** — c'est de l'édition de prompts/markdown (commands, agents, CLAUDE.md) + 1 template. Si l'analyse révèle qu'un script utilitaire est nécessaire, le signaler dans le PRP plutôt que de l'imposer.
- **Validation méta du chantier** : après implémentation, lancer `/validate` sur le système ; puis test fonctionnel — créer un artefact volontairement non conforme à une rubrique de test, vérifier que (a) `validation-gates` mode rubrique le détecte et liste les points, (b) le retry se déclenche une fois, (c) le 2ᵉ FAIL remonte à l'humain et ne reboucle pas.
- **Mettre à jour** : CLAUDE.md (§ orchestration + éventuellement la table des commandes si le comportement de `/validate` change visiblement), et le SKILL.md meta-router si pertinent (le `/validate` n'appartient pas à un skill spécifique — c'est une commande globale).
- **Ne PAS** : migrer quoi que ce soit vers Claude Managed Agents ; introduire une dépendance externe ; transformer `validation-gates` en agent qui édite les artefacts en mode rubrique.
