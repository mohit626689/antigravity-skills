# Agent Skills Specification Reference (agentskills.io)

This document mirrors and details the complete format specification from [agentskills.io](https://agentskills.io/specification).

---

## 1. Directory Structure

A skill must be a standalone directory containing a mandatory `SKILL.md` file at its root:

```
<skill-name>/
├── SKILL.md          # Required: YAML frontmatter + Markdown instructions
├── scripts/          # Optional: executable Python, Bash, or Node scripts
├── references/       # Optional: deep technical documentation, schemas, domain guides
├── assets/           # Optional: templates, images, data files
└── ...               # Any additional helper resources
```

---

## 2. SKILL.md Frontmatter

The `SKILL.md` file begins with a YAML frontmatter block enclosed between `---` markers:

| Field | Required | Constraints & Description |
| :--- | :--- | :--- |
| `name` | **Yes** | 1–64 characters. Unicode lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`). Must **not** start or end with a hyphen, must not contain consecutive hyphens (`--`), and must match the parent directory name exactly. |
| `description` | **Yes** | 1–1024 characters. Non-empty. Must clearly explain **what** the skill does and **when** the agent should activate it. |
| `license` | No | License name (e.g. `Apache-2.0`, `MIT`) or path to a bundled license file. |
| `compatibility` | No | 1–500 characters. Environment constraints (e.g., `Requires python 3.10+ and docker`). |
| `metadata` | No | Arbitrary string-to-string key-value mapping (e.g., author, version). |
| `allowed-tools` | No | Space-separated list of pre-approved tools (experimental). |

### Frontmatter Example
```yaml
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
license: Apache-2.0
compatibility: Requires python 3.10+ and pdfplumber
metadata:
  author: acme-corp
  version: "1.0.0"
---
```

---

## 3. Progressive Disclosure Architecture

To prevent context bloat and keep token usage efficient, Agent Skills operate on a 3-tier progressive disclosure model:

1. **Discovery (Startup / ~100 tokens)**: The agent loads only the `name` and `description` of every available skill.
2. **Activation (On Match / <5,000 tokens)**: When user prompt or task requires the skill, the agent reads the full `SKILL.md` body.
3. **Execution (On Demand)**: Files in `references/`, `scripts/`, or `assets/` are loaded or run only when specifically called for.

### Line Budget
- Keep `SKILL.md` under **500 lines**.
- Move bulky specifications, long schemas, or large examples into `references/` files and link them with relative Markdown links (e.g., `[schema](references/schema.json)`).

---

## 4. File References & Relative Paths

- Always use relative paths from the skill root: `references/REFERENCE.md` or `scripts/run.py`.
- Keep references 1 level deep from `SKILL.md`.
