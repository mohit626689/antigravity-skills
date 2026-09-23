---
name: agent-skills
description: Standardized authoring, validation, and optimization of Agent Skills following the open agentskills.io specification. Use when creating new agent skills, validating existing SKILL.md files, optimizing skill descriptions, or structuring agent runbooks, tools, and scripts.
compatibility: Compatible with all agentskills.io clients (Antigravity, Claude Code, Cursor, Copilot, Codex)
metadata:
  standard: "agentskills.io"
  version: "1.0.0"
---

# Agent Skills Specialist (agentskills.io)

This skill equips the agent to author, structure, audit, and validate skills according to the open **Agent Skills specification** ([agentskills.io](https://agentskills.io)).

---

## ⚡ Triggers & Capabilities

Activate this skill when:
- Creating a new skill (`/skill-create`, "create a skill for ...", "turn this into an agent skill")
- Validating an existing skill against the official specification (`/skill-validate`, "validate skill ...")
- Optimizing a skill's description for reliable activation
- Auditing skill token footprints and implementing progressive disclosure

---

## 🏗️ Core Specification Rules

All skills must adhere to the official directory structure and frontmatter constraints:

```
<skill-name>/
├── SKILL.md                  # Mandatory entry point
├── scripts/                  # Executable helpers (Python, Bash, Node)
├── references/               # Detailed documentation, schemas, domain manuals
└── assets/                   # Templates, configuration files, static resources
```

### 1. `SKILL.md` Frontmatter Requirements
- **`name`** (required): 1–64 characters, lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`).
  - Must **not** start or end with a hyphen.
  - Must **not** contain consecutive hyphens (`--`).
  - Must **match the parent directory name exactly**.
- **`description`** (required): 1–1024 characters. Must state **what** the skill does AND **when** the agent should trigger it.
- **`compatibility`** (optional): 1–500 characters describing environment dependencies.
- **`metadata`** (optional): Key-value string pairs (author, version, tags).

### 2. Progressive Disclosure Budget
- **Discovery**: ~100 tokens (frontmatter name + description loaded at startup).
- **Activation**: `< 5,000` tokens (keep `SKILL.md` under **500 lines**).
- **On-Demand**: Move large tables, extensive API docs, and bulky schemas into `references/`.

For complete specification details, see [Specification Reference](references/specification.md).  
For authoring philosophy, see [Best Practices Guide](references/best-practices.md).

---

## 🛠️ Step-by-Step Skill Authoring Workflow

### Step 1: Scoping and Name Definition
1. Identify a coherent, modular workflow or domain procedure.
2. Select a concise, hyphenated lowercase name (e.g. `data-pipeline`, `code-review`).
3. Create the directory: `.agents/skills/<skill-name>/` (workspace) or `~/.gemini/config/skills/<skill-name>/` (global).

### Step 2: Crafting the Description
A high-converting description answers both questions:
- *What does this skill do?* (e.g., "Generates client proposals with 3 pricing tiers...")
- *When should the agent trigger it?* (e.g., "Use when the user asks for a proposal, quote, or sales pitch...")

### Step 3: Writing Prescriptive & Flexible Instructions
1. **Gotchas First**: List non-obvious traps and environment quirks at the top.
2. **Defaults over Menus**: State the primary recommended tool/approach first; mention fallbacks briefly.
3. **Templates**: Include concrete output markdown or JSON formats.
4. **Validation Loop**: Always include instructions for the agent to verify its work before finalizing.

### Step 4: Extracting Bulky Resources
If documentation exceeds 500 lines:
- Move reference docs to `references/<topic>.md`.
- Link using relative paths, for example: `references/<topic>.md`.

---

## 🧪 Validation

Run the bundled validator script to check any skill folder:

```bash
python3 scripts/validate_skill.py <path-to-skill-directory>
```

The script checks:
- Directory name formatting & length
- Frontmatter YAML validity
- Name match with parent directory
- Description length (≤ 1024 chars) and quality
- Line count against progressive disclosure guidelines
- Existence of referenced relative files
