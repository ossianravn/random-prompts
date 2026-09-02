# Authoring guide

Read the relevant sections while naming a skill, writing frontmatter, designing progressive disclosure, or deciding whether to add scripts, references, assets, evals, or OpenAI metadata.

## Coherent scope

Give each skill one recognizable user goal or one tightly connected end-to-end workflow.

Split when branches have materially different users, activation contexts, permissions, tools, outputs, or definitions of success. Keep variations together when they share the same outcome and workflow foundation.

Avoid:

- Tiny skills that must always load together.
- “Everything about this domain” bundles.
- Unrelated utilities grouped by department or technology.
- Product documentation presented as a procedure.
- A one-off answer embedded as reusable guidance.

## Naming

Use a short action-oriented name recognizable to users and agents.

Portable constraints:

- 1–64 characters.
- Lowercase ASCII letters, digits, and hyphens.
- No leading or trailing hyphen.
- No consecutive hyphens.
- Exact match with the parent folder name.

Check visible skills for collisions. A distinct name plus a precise description is better than a router in most cases.

## Description as routing contract

Write the description for activation, not as marketing copy.

It should state:

- The user outcome or job.
- When the skill applies.
- Diagnostic source types, artifacts, workflow phases, or contexts.
- The closest meaningful boundary.
- The outcome when that helps distinguish it.

Use user intent and natural phrasing rather than internal implementation details. Front-load diagnostic terms because hosts may truncate metadata. Include useful synonyms without keyword stuffing.

A good pattern is:

```yaml
description: >-
  Use this skill to [outcome] from [diagnostic inputs or situations]. Apply it when [contexts and trigger language]. Do not use it for [closest near-miss boundary].
```

The portable `description` must be non-empty and at most 1024 characters. Valid YAML scalar forms are allowed; quote only when syntax, clarity, or the target requires it.

## Frontmatter

Required portable fields:

- `name`
- `description`

Optional portable fields:

- `license`
- `compatibility`
- `metadata`
- `allowed-tools`

Use optional fields only when they add information consumed by the selected target.

- `compatibility` must be 1–500 characters when present and should describe real environment requirements.
- `metadata` is a string-to-string map; namespace keys when collision is plausible.
- `allowed-tools` is experimental and host-dependent. Never treat it as the sole security boundary.
- Do not add versions, authors, licenses, or compatibility claims without a real purpose and known value.
- Keep host-only fields outside the portable frontmatter unless the current host specification explicitly supports them there.

## `SKILL.md` body

There is no mandatory universal outline. Include only sections that help execution, such as:

- Outcome.
- Minimum viable input or preflight.
- Workflow chooser.
- Core procedure.
- Gotchas.
- Output contract or template.
- Validation and repair loop.
- Safety and approval gates.
- Definition of done.
- Troubleshooting.
- Resource map.

Write imperatively. Identify inputs and outputs where ambiguity is likely. Use checklists for dependent or easily skipped steps. Put checkable gates at consequential transitions and define observable overall completion.

Keep the core under 500 lines and roughly 5,000 tokens where practical. These are design recommendations unless the target enforces them.

## Stable defaults and calibrated control

Choose one sensible default path and give narrow escape conditions. Avoid unranked menus of equivalent tools or formats.

Use flexible reasoning guidance when several approaches are valid and variation is harmless. Explain the reason for non-obvious constraints when it improves generalization.

Use exact sequences, schemas, commands, validators, and stop conditions when:

- Order matters.
- The action is destructive or difficult to reverse.
- A machine-readable contract must be satisfied.
- Small deviations frequently fail.
- Auditability or regulatory evidence matters.
- The agent repeatedly reinvents fragile logic.

## Progressive disclosure

Keep in `SKILL.md`:

- The primary workflow.
- Common decisions.
- Early non-obvious gotchas.
- Universal output and completion conditions.

Move to focused references:

- Branch-specific procedures.
- Long schemas or policies.
- API and vendor notes.
- Extended examples.
- Troubleshooting matrices.
- Stable project context.

State exactly when to read each reference. “Read `references/api-errors.md` after a non-success API response” is stronger than “see references.”

Use relative paths from the skill root. Keep supporting files one level deep where practical and avoid reference-to-reference chains.

Maintain one source of truth. Do not duplicate a rule in `SKILL.md`, a reference, and a template.

## Scripts

Add a script when it materially improves determinism, reliability, repeatability, validation, or tool orchestration. First check whether a stable existing command with a small explicit invocation already solves the problem.

Scripts should:

- Have a narrow non-interactive interface.
- Provide useful `--help` or equivalent usage.
- Validate arguments and paths before mutation.
- Produce predictable stdout and stderr.
- Use structured output when another agent consumes it.
- Exit nonzero on failure.
- Print actionable errors without secrets.
- Handle expected edge cases.
- Be idempotent where practical.
- Document dependencies.
- Pin versions only when reproducibility requires it.
- Minimize network and filesystem access.
- Avoid downloading or executing untrusted code.
- Support dry-run or plan output for risky batch operations when useful.
- Provide a smoke-test path and at least one tested failure path.

## References

Use references for focused conditional or bulky execution knowledge. Capture only stable, relevant material rather than copying whole manuals.

For current APIs, law, regulation, pricing, vendor behavior, or operational state, specify whether to retrieve current information at runtime, use a pinned version, or follow an offline fallback. Preserve provenance when authority or freshness matters.

## Assets

Use assets for static templates, fixtures, starter files, boilerplate, lookup data, or schemas. Assets are resources, not hidden behavioral instructions.

Remove every placeholder from copied assets before final validation.

## Evals

Add evals when activation precision or outcome quality matters, when replacing an existing version, when distributing the skill, or when the user requests a durable test harness.

Keep generated eval workspaces outside the skill directory. Keep fixtures free of secrets, customer data, and unnecessary personal information.

Use:

- `evals/trigger-evals.json` for labeled activation queries.
- `evals/evals.json` for behavioral prompts, expected outputs, optional files, and later assertions.

## `agents/openai.yaml`

Add this file only for ChatGPT or Codex targets when it provides supported interface metadata, invocation policy, or declared MCP dependencies.

Follow the current official schema. Common supported sections may include `interface`, `policy`, and `dependencies`, but verify them at execution time.

Do not add placeholder icons, colors, prompts, or dependencies. Keep host-specific configuration separate from portable instructions.

Use `policy.allow_implicit_invocation: false` deliberately for explicit-only behavior; its documented default is normally true.

## File hygiene

Before validation, remove:

- TODOs and scaffolding placeholders.
- Empty generated directories.
- Duplicate or superseded references.
- Build output and caches.
- Eval run workspaces.
- `.env` files, credentials, private keys, tokens, and customer data.
- Unrequested README, changelog, contribution, installation, or license files.

Add supplementary files only when the user, legal context, distribution target, or execution workflow needs them.
