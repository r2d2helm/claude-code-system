---
name: skill-creator
description: "Guide for creating effective Claude Code skills for the r2d2 system. Use when the user wants to create a new skill, update an existing skill, or extend Claude's capabilities with specialized knowledge, workflows, or tool integrations. Triggers on requests like 'create a skill for...', 'new skill', 'build a skill', or any skill development task."
---

# Skill Creator - r2d2 System

Guide for creating effective skills that integrate with the r2d2 ecosystem (meta-router, vault Obsidian, Contract-First Protocol).

## About Skills

Skills are modular packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized one equipped with procedural knowledge.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex tasks

## Core Principles

### Concise is Key

The context window is a public good. Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this?"

Prefer concise examples over verbose explanations.

### Progressive Disclosure (3 levels)

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<500 lines)
3. **Bundled resources** - As needed (references/, scripts/)

### r2d2 System Conventions

#### Structure obligatoire
```
~/.claude/skills/{nom-du-skill}/
├── SKILL.md              # Instructions principales (REQUIS)
├── commands/             # Commandes du skill (REQUIS)
│   └── {commande}.md    # Au moins une commande
├── wizards/              # Wizards interactifs (RECOMMANDE)
│   └── wizard-setup.md  # Setup initial
├── scripts/              # Scripts PowerShell/Python (OPTIONNEL)
├── references/           # Documentation detaillee (OPTIONNEL)
└── templates/            # Templates de fichiers (OPTIONNEL)
```

#### Nommage
- Nom du skill : `hyphen-case` (minuscules, chiffres, tirets)
- Prefixe de commandes : `/{prefixe}-{action}` (ex: `/dk-ps`, `/win-network`)
- Fichiers commandes : `{action}.md` (ex: `status.md`, `deploy.md`)
- Wizards : `wizard-{nom}.md`

#### Encodage
- Fichiers .md et .json : UTF-8 sans BOM
- Fichiers .ps1 et .psm1 : UTF-8 avec BOM (requis PS 5.1)
- Scripts PowerShell : compatibles PS 5.1 (pas de `??`, pas de `UTF8BOM`)

## Skill Creation Process

### Step 1: Understand the Skill

Clarify concrete examples of how the skill will be used:
- What functionality should it support?
- What would a user say that should trigger this skill?
- Which existing skills to consult as reference models?

Good reference models from the r2d2 system:
- `docker-skill/` : Compact skill (10 cmd, 3 wizards)
- `windows-skill/` : Complete skill (36 cmd, 10 wizards)
- `knowledge-skill/` : Skill with MCP integration

### Step 2: Plan Reusable Contents

Analyze each use case and identify what to include:
- `scripts/` : Code that gets rewritten repeatedly
- `references/` : Documentation Claude should reference while working
- `commands/` : User-invocable commands (REQUIRED)
- `wizards/` : Interactive guided workflows

### Step 3: Initialize the Skill

Run the initialization script:

```bash
python scripts/init_skill.py <skill-name> --path ~/.claude/skills
```

This creates the complete directory structure with SKILL.md template, commands/, wizards/, and example files.

### Step 4: Edit the Skill

#### SKILL.md Frontmatter
```yaml
---
name: skill-name
description: "What it does AND when to use it. Include specific triggers."
---
```

Only `name` and `description` in frontmatter. All "when to use" info goes in description (body is only loaded after triggering).

#### SKILL.md Body
- Keep under 500 lines
- Split detailed content into `references/`
- Include workflow overviews, command tables, conventions

#### Commands (`commands/`)
Each command file:
```markdown
# {Titre de la commande}

## Cible : $ARGUMENTS

[Description de ce que fait la commande]

## Processus
1. [Etape 1]
2. [Etape 2]

## Exemples
[Cas d'usage typiques]
```

### Step 5: Validate the Skill

Run the validation script:

```bash
python scripts/quick_validate.py ~/.claude/skills/<skill-name>
```

Checks: YAML frontmatter, naming conventions, directory structure, description quality.

### Step 6: Integrate with r2d2 System

After creating the skill, use the Contract-First Protocol:

1. **Publish contract** (for router-updater and knowledge-indexer):
```yaml
skill_name: "{nom}"
prefix: "/{prefixe}"
commands_count: N
wizards_count: N
keywords: ["mot1", "mot2", "mot3"]
description_router: "Description pour le meta-router"
description_claude_md: "Ligne pour le tableau CLAUDE.md"
```

2. **Update meta-router** (SKILL.md) with routing keywords
3. **Update CLAUDE.md** with skill in Skills Actifs table
4. **Index in vault** with concept note in `Knowledge/Concepts/`

Or use `/new-skill` command which orchestrates all of this automatically.

## Design Patterns

For detailed patterns, consult:
- **Multi-step processes**: See [references/workflows.md](references/workflows.md)
- **Output formats**: See [references/output-patterns.md](references/output-patterns.md)

## What NOT to Include

- README.md (SKILL.md suffices)
- INSTALLATION_GUIDE.md, CHANGELOG.md
- Duplicate commands from existing skills
- SKILL.md exceeding 500 lines
- Scripts without comments
