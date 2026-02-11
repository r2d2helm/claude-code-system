#!/usr/bin/env python3
"""
Skill Initializer for r2d2 system - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-new-skill --path ~/.claude/skills
    init_skill.py monitoring-skill --path ~/.claude/skills
"""

import sys
import os
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: "[TODO: What the skill does AND when to use it. Include specific trigger scenarios.]"
---

# {skill_title}

## Description

[TODO: 1-2 sentences explaining what this skill enables]

## Commandes

| Commande | Description |
|----------|-------------|
| `/{prefix}-[action]` | [TODO: Description] |

## Conventions

[TODO: Domain-specific rules and patterns]

## Workflows

[TODO: Main processes step by step]

## References

[TODO: Links to references/ files if applicable]
"""

COMMAND_TEMPLATE = """# {command_title}

## Cible : $ARGUMENTS

[TODO: Description of what this command does]

## Processus

1. [TODO: Step 1]
2. [TODO: Step 2]
3. [TODO: Step 3]

## Exemples

```
/{prefix}-{action} [example args]
```
"""

WIZARD_TEMPLATE = """# Wizard Setup - {skill_title}

## Description

Assistant interactif pour la configuration initiale de {skill_name}.

## Processus

### Etape 1 : Collecte d'informations

Poser les questions suivantes :
1. [TODO: Question 1]
2. [TODO: Question 2]

### Etape 2 : Configuration

[TODO: Steps based on answers]

### Etape 3 : Validation

[TODO: Verify everything works]

## Resultat attendu

[TODO: What the user gets at the end]
"""

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

[TODO: Add detailed reference documentation here]

## When to Load This File

Load this reference when:
- [TODO: Specific scenario 1]
- [TODO: Specific scenario 2]
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def extract_prefix(skill_name):
    """Extract a command prefix from skill name."""
    # Remove '-skill' suffix if present
    name = skill_name.replace('-skill', '')
    # Take first 2-4 chars as prefix
    parts = name.split('-')
    if len(parts) == 1:
        return parts[0][:4]
    return ''.join(p[0] for p in parts[:3])


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with r2d2 conventions.

    Args:
        skill_name: Name of the skill (hyphen-case)
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Expand ~ in path
    path = os.path.expanduser(path)
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    # Validate skill name
    import re
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', skill_name):
        print(f"Error: Invalid skill name '{skill_name}'. Use hyphen-case (lowercase, digits, hyphens).")
        return None

    if len(skill_name) > 40:
        print(f"Error: Skill name too long ({len(skill_name)} chars). Maximum is 40.")
        return None

    # Create skill directory structure
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        (skill_dir / 'commands').mkdir()
        (skill_dir / 'wizards').mkdir()
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    prefix = extract_prefix(skill_name)

    # Create SKILL.md
    try:
        skill_content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title,
            prefix=prefix
        )
        (skill_dir / 'SKILL.md').write_text(skill_content, encoding='utf-8')
        print("Created SKILL.md")
    except Exception as e:
        print(f"Error creating SKILL.md: {e}")
        return None

    # Create example command
    try:
        cmd_content = COMMAND_TEMPLATE.format(
            command_title=f"{skill_title} Status",
            prefix=prefix,
            action="status"
        )
        (skill_dir / 'commands' / 'status.md').write_text(cmd_content, encoding='utf-8')
        print("Created commands/status.md")
    except Exception as e:
        print(f"Error creating command: {e}")
        return None

    # Create wizard template
    try:
        wizard_content = WIZARD_TEMPLATE.format(
            skill_title=skill_title,
            skill_name=skill_name
        )
        (skill_dir / 'wizards' / 'wizard-setup.md').write_text(wizard_content, encoding='utf-8')
        print("Created wizards/wizard-setup.md")
    except Exception as e:
        print(f"Error creating wizard: {e}")
        return None

    # Print summary
    print(f"\nSkill '{skill_name}' initialized at {skill_dir}")
    print(f"  Prefix suggestion: /{prefix}-*")
    print()
    print("Structure:")
    print(f"  {skill_name}/")
    print(f"  +-- SKILL.md")
    print(f"  +-- commands/status.md")
    print(f"  +-- wizards/wizard-setup.md")
    print()
    print("Next steps:")
    print("  1. Edit SKILL.md (complete TODO items, update description)")
    print("  2. Create commands in commands/")
    print("  3. Add wizards, scripts, references as needed")
    print("  4. Run quick_validate.py to check structure")
    print("  5. Update meta-router and CLAUDE.md")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        print()
        print("Skill name requirements:")
        print("  - Hyphen-case (e.g., 'monitoring-skill')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 40 characters")
        print()
        print("Examples:")
        print("  init_skill.py monitoring-skill --path ~/.claude/skills")
        print("  init_skill.py backup-skill --path ~/.claude/skills")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"Initializing skill: {skill_name}")
    print(f"Location: {path}")
    print()

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
