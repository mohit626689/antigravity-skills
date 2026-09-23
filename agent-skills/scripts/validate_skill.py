#!/usr/bin/env python3
"""
Agent Skills Validator (agentskills.io specification)
Validates that a skill directory and its SKILL.md comply with the open Agent Skills standard.
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Specification limits
MAX_NAME_LENGTH = 64
MAX_DESC_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
RECOMMENDED_MAX_LINES = 500

NAME_REGEX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_simple_yaml(yaml_text: str) -> dict:
    """Parse basic YAML key-value pairs without requiring external dependencies."""
    data = {}
    lines = yaml_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()

            # Handle multiline string indicator > or |
            if val in (">", "|", ">-", "|-"):
                multiline_val = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                    if lines[i].strip():
                        multiline_val.append(lines[i].strip())
                    i += 1
                data[key] = " ".join(multiline_val) if ">" in val else "\n".join(multiline_val)
                continue
            else:
                # Strip quotes if present
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                data[key] = val
        i += 1
    return data


def validate_skill(skill_dir: Path):
    """Validates the skill folder and returns (errors, warnings)."""
    errors = []
    warnings = []

    if not skill_dir.is_dir():
        return [f"Directory not found: {skill_dir}"], []

    folder_name = skill_dir.name

    # Check folder name constraints
    if not (1 <= len(folder_name) <= MAX_NAME_LENGTH):
        errors.append(f"Folder name '{folder_name}' length ({len(folder_name)}) must be between 1 and {MAX_NAME_LENGTH} characters.")

    if not NAME_REGEX.match(folder_name):
        errors.append(
            f"Folder name '{folder_name}' is invalid. It must contain only lowercase alphanumeric characters and hyphens, and cannot start/end with a hyphen or have consecutive hyphens."
        )

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        errors.append(f"Missing required SKILL.md at {skill_file}")
        return errors, warnings

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Failed to read SKILL.md: {e}"], warnings

    # Frontmatter check
    fm_match = FRONTMATTER_REGEX.match(content)
    if not fm_match:
        errors.append("SKILL.md must start with YAML frontmatter enclosed in '---' markers.")
        return errors, warnings

    yaml_block, markdown_body = fm_match.group(1), fm_match.group(2)
    meta = parse_simple_yaml(yaml_block)

    # 1. 'name' field
    if "name" not in meta or not meta["name"]:
        errors.append("Frontmatter is missing required 'name' field.")
    else:
        name = meta["name"]
        if name != folder_name:
            errors.append(f"'name' in frontmatter ('{name}') does not match directory name ('{folder_name}').")
        if not (1 <= len(name) <= MAX_NAME_LENGTH):
            errors.append(f"'name' length ({len(name)}) must be between 1 and {MAX_NAME_LENGTH} chars.")
        if not NAME_REGEX.match(name):
            errors.append(f"'name' ('{name}') format invalid. Only lowercase a-z, 0-9, and non-consecutive single hyphens allowed.")

    # 2. 'description' field
    if "description" not in meta or not meta["description"]:
        errors.append("Frontmatter is missing required 'description' field.")
    else:
        desc = meta["description"]
        if len(desc) > MAX_DESC_LENGTH:
            errors.append(f"'description' length ({len(desc)}) exceeds maximum allowed ({MAX_DESC_LENGTH} chars).")
        if len(desc.strip()) < 10:
            warnings.append("'description' is very short. Describe both what the skill does and when the agent should trigger it.")

    # 3. 'compatibility' field
    if "compatibility" in meta and len(meta["compatibility"]) > MAX_COMPATIBILITY_LENGTH:
        errors.append(f"'compatibility' exceeds {MAX_COMPATIBILITY_LENGTH} characters.")

    # 4. Check body length (progressive disclosure guideline)
    total_lines = len(content.splitlines())
    if total_lines > RECOMMENDED_MAX_LINES:
        warnings.append(
            f"SKILL.md has {total_lines} lines (recommended < {RECOMMENDED_MAX_LINES}). Consider moving large manuals/references into 'references/' directory to conserve agent context window."
        )

    # 5. Check local relative links in markdown
    local_links = re.findall(r"\[.*?\]\((?!(?:https?://|mailto:|#))([^)]+)\)", markdown_body)
    for link in local_links:
        target_path = link.split("#")[0]
        if target_path:
            resolved = (skill_dir / target_path).resolve()
            if not resolved.exists():
                warnings.append(f"Referenced relative file '{link}' does not exist on disk.")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate an Agent Skill folder against agentskills.io standard")
    parser.add_argument("skill_dir", type=str, help="Path to the skill directory")
    args = parser.parse_args()

    target_dir = Path(args.skill_dir).resolve()
    print(f"🔍 Validating skill at: {target_dir}")

    errors, warnings = validate_skill(target_dir)

    if warnings:
        for w in warnings:
            print(f"  ⚠️  Warning: {w}")

    if errors:
        print("\n❌ Validation FAILED with errors:")
        for err in errors:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ Skill is VALID according to agentskills.io specification!")
        sys.exit(0)


if __name__ == "__main__":
    main()
