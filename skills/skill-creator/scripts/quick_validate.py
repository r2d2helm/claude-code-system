#!/usr/bin/env python3
"""
Quick validation script for r2d2 skills

Checks:
- SKILL.md exists with valid frontmatter
- commands/ directory exists with at least one command
- Naming conventions (hyphen-case)
- Description completeness
- Encoding (UTF-8)

Usage:
    python quick_validate.py <skill_directory>
"""

import sys
import os
import re
from pathlib import Path


def validate_skill(skill_path):
    """Validate a skill against r2d2 conventions."""
    skill_path = Path(skill_path)
    issues = []
    warnings = []

    # Check skill directory exists
    if not skill_path.exists():
        return False, f"Skill directory not found: {skill_path}", []

    if not skill_path.is_dir():
        return False, f"Path is not a directory: {skill_path}", []

    # Check skill name convention
    skill_name = skill_path.name
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', skill_name):
        issues.append(f"Skill name '{skill_name}' is not hyphen-case")

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found", []

    # Read and validate SKILL.md
    try:
        content = skill_md.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return False, "SKILL.md is not valid UTF-8", []

    # Check for BOM (should NOT have BOM for .md)
    raw = skill_md.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'):
        issues.append("SKILL.md has UTF-8 BOM (should be without BOM)")

    # Check frontmatter
    if not content.startswith('---'):
        issues.append("No YAML frontmatter found in SKILL.md")
    else:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            issues.append("Invalid frontmatter format in SKILL.md")
        else:
            frontmatter_text = match.group(1)
            # Simple YAML parsing without external dependency
            has_name = bool(re.search(r'^name:', frontmatter_text, re.MULTILINE))
            has_desc = bool(re.search(r'^description:', frontmatter_text, re.MULTILINE))

            if not has_name:
                issues.append("Missing 'name' in frontmatter")
            if not has_desc:
                issues.append("Missing 'description' in frontmatter")

            # Check for TODO in description
            if 'TODO' in frontmatter_text:
                warnings.append("Frontmatter still contains TODO placeholders")

    # Check SKILL.md line count
    line_count = len(content.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md has {line_count} lines (recommended max: 500)")

    # Check commands/ directory (REQUIRED for r2d2)
    commands_dir = skill_path / 'commands'
    if not commands_dir.exists():
        issues.append("commands/ directory is missing (required for r2d2 system)")
    else:
        cmd_files = list(commands_dir.glob('*.md'))
        if len(cmd_files) == 0:
            issues.append("commands/ directory has no .md files (need at least one)")

    # Check for wizards/ (recommended)
    wizards_dir = skill_path / 'wizards'
    if not wizards_dir.exists():
        warnings.append("wizards/ directory is missing (recommended)")

    # Check .ps1 files for BOM (REQUIRED for PS 5.1)
    for ps1_file in skill_path.rglob('*.ps1'):
        raw = ps1_file.read_bytes()
        if not raw.startswith(b'\xef\xbb\xbf'):
            issues.append(f"{ps1_file.name} missing UTF-8 BOM (required for PS 5.1)")

    # Check .md files for BOM (should NOT have)
    for md_file in skill_path.rglob('*.md'):
        if md_file == skill_md:
            continue  # already checked
        raw = md_file.read_bytes()
        if raw.startswith(b'\xef\xbb\xbf'):
            warnings.append(f"{md_file.relative_to(skill_path)} has unnecessary BOM")

    # Build result
    if issues:
        msg = "FAIL - Issues found:\n" + "\n".join(f"  [ERROR] {i}" for i in issues)
        if warnings:
            msg += "\n" + "\n".join(f"  [WARN]  {w}" for w in warnings)
        return False, msg, warnings

    msg = "PASS - Skill is valid!"
    if warnings:
        msg += "\n" + "\n".join(f"  [WARN]  {w}" for w in warnings)
    return True, msg, warnings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        print()
        print("Validates a skill against r2d2 system conventions:")
        print("  - SKILL.md with name/description frontmatter")
        print("  - commands/ directory with at least one command")
        print("  - Naming conventions (hyphen-case)")
        print("  - Encoding rules (UTF-8 BOM for .ps1, no BOM for .md)")
        sys.exit(1)

    skill_dir = os.path.expanduser(sys.argv[1])
    valid, message, _ = validate_skill(skill_dir)
    print(message)
    sys.exit(0 if valid else 1)
