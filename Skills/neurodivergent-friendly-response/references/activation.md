# Activation and Portability

The skill is designed as an always-on presentation layer, but host behavior matters. An implicit skill matcher can permit universal use without guaranteeing that the skill is loaded on every turn.

## Codex installation

Install the folder at user scope so it is available in every repository:

```bash
mkdir -p ~/.agents/skills
cp -R neurodivergent-friendly-response ~/.agents/skills/
```

`agents/openai.yaml` explicitly permits implicit invocation. Codex still selects implicit skills from the `description`, so the description begins with “Always-on” and names broad message categories.

## Strict always-on Codex behavior

For the strongest guarantee, pair the skill with a small global instruction. Add this to `~/.codex/AGENTS.md`:

```md
## Response shaping

For every user-facing response, apply the installed `neurodivergent-friendly-response` skill as a presentation layer after solving the underlying task. Explicit user format and accessibility preferences override the skill's defaults.
```

This keeps the rich procedure in the skill while using global guidance only as an activation pointer.

## Other compatible agents

- Install the skill in the host's user-level skill directory when one exists.
- Keep implicit invocation enabled.
- If the host only loads skills by semantic matching, mirror the one-line activation pointer in its global instructions.
- If the host supports explicit invocation only, use a router or global instruction rather than expecting every user to name the skill.
- Do not duplicate the full SOP in multiple configuration files; keep `SKILL.md` as the source of truth.

## Exact-format tasks

The skill remains conceptually active for every user message, but must not add headings, estimates, or prose that violate an exact output contract. Examples include strict JSON, a single classification token, byte-exact transcription, or code-only output.

## Activation test

After installation, try prompts from unrelated categories:

1. “Why is my Python loop skipping items?”
2. “Plan my afternoon.”
3. “Explain DNS.”
4. “Hey.”

The skill should shape all four responses, with proportional structure. The greeting should stay natural rather than showing a state ledger.

## Host limitation

A skill bundle cannot control a host that never loads it. When universal response behavior is a hard requirement, host-level global instructions are the enforcement point; the skill remains the reusable procedure and source of truth.
