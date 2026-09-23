# Agent Skills Best Practices & Guidelines (agentskills.io)

Core principles distilled from the official [agentskills.io](https://agentskills.io/skill-creation/best-practices) documentation:

---

## 1. Grounding in Real Expertise
- **Extract from actual workflow traces**: Capture real sequences, shell commands, and edge cases rather than generic best-practice summaries.
- **Add what the agent lacks, omit what it knows**: The model already knows standard programming concepts. Focus strictly on domain-specific conventions, APIs, schemas, and gotchas.

---

## 2. Calibrating Control
- **Match Specificity to Fragility**:
  - Flexible tasks (e.g. brainstorming, code reviews): give the agent autonomy and explain *why*.
  - Fragile tasks (e.g. database migrations, deployment commands): be strictly prescriptive with exact commands and parameters.
- **Defaults over Menus**: Pick a strong default tool/approach and mention alternatives as fallbacks, rather than giving a paralyzing list of equal choices.
- **Procedures over Declarations**: Teach *how to approach* the class of problems, not just what to output for one isolated instance.

---

## 3. High-Value Instruction Patterns
- **Gotchas Section**: Call out non-obvious traps upfront in `SKILL.md` (e.g., subtle API limits, soft deletes, naming quirks).
- **Templates**: Provide concrete output schemas and markdown templates.
- **Checklists**: Use step-by-step progress tracking for multi-stage workflows.
- **Self-Validation Loops**: Instruct the agent to run a validator script or verification step before finalizing output.
- **Plan-Validate-Execute**: For complex or destructive tasks, require an intermediate plan file that is validated prior to execution.

---

## 4. Optimizing Skill Descriptions
- Descriptions must tell the agent **both what the skill does AND when to use it**.
- Include specific action keywords, trigger phrases, file extensions, or tool names.
- Keep description under 1,024 characters.
