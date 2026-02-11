# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** -> Follow "Creation workflow" below
   **Editing existing content?** -> Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## r2d2 System Workflows

### Contract-First Protocol

When a skill is created as part of multi-agent orchestration:

```
skill-builder (upstream)
    |  Builds skill + publishes contract
    |
    +---> router-updater (downstream)
    |       Updates SKILL.md + CLAUDE.md
    |
    +---> knowledge-indexer (downstream)
    |       Creates vault note + updates MOCs
    |
    +---> validation-gates (verification)
            Validates structure + functional + integration
```

### PRP-Driven Skill Creation

For complex skills, use the PRP Framework:

```
1. INITIAL.md (describe the skill need)
2. /generate-prp -> PRP blueprint
3. /execute-prp -> Implementation with validation
```
