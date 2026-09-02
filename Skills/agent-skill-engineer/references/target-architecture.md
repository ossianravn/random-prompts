# Target architecture

Read this file when choosing whether a skill is the right mechanism, when target hosts or deployment are unclear, or when packaging and invocation differ by host.

## Mechanism chooser

| Mechanism | Use when | Avoid when |
| --- | --- | --- |
| Agent Skill | Reusable, on-demand procedural knowledge, specialized judgment, templates, or a bounded workflow should load only when relevant | Guidance must apply automatically to nearly all work, or the task is a one-off |
| `AGENTS.md` or host equivalent | Durable repository or scope guidance should load automatically | The procedure is occasional, bulky, or highly task-specific |
| Script or CLI | The operation is predominantly deterministic and needs little contextual judgment | Interpretation, branching, or human-facing synthesis is central |
| MCP, connector, or tool API | The agent needs authenticated live data or controlled external actions | Static instructions or local deterministic mechanics are sufficient |
| Plugin or host package | Skills and connectors must be installed and distributed to other users | Local authoring or a single repository skill is enough |
| Hook or automation | A lifecycle or event should trigger a command automatically | The user must intentionally select and supervise a workflow |
| Prompt or template | The request is one-off, tiny, or not worth an installable artifact | Reuse, discovery, resources, or evaluation are important |

A skill may combine instructions with scripts and tool dependencies. Keep context-sensitive interpretation in instructions; put repeated deterministic mechanics in scripts or tools.

## Target profile

Resolve and report:

- Work mode: create, revise, audit, migrate, or evaluate.
- Core format: portable Agent Skills or host-specific.
- Target hosts.
- Deployment: repository, user, administrator, hosted API, plugin, source repository, or another scope.
- Invocation: implicit, explicit-only, or both.
- Required tools, runtimes, operating systems, network, credentials, and approvals.
- Delivery: folder, patch, individual files, archive, plugin package, or another artifact.
- Compatibility priority when host extensions conflict.

Defaults:

- Portable core.
- Codex compatibility when Codex or ChatGPT is named or implied.
- Local folder delivery.
- Instruction-only bundle.
- Least privilege.
- Implicit invocation unless collision or intentional manual selection makes explicit-only behavior safer.

## Portable core versus host extensions

Portable core belongs in `SKILL.md` and portable resources. Host-specific behavior belongs in a separate supported file such as `agents/openai.yaml`.

Never treat a host-specific path, schema, validator quirk, registry command, or packaging rule as universal.

When official sources conflict:

1. Prefer the current official documentation for the selected target.
2. Preserve portable core validity where practical.
3. State the compatibility tradeoff.
4. Avoid silently combining incompatible examples from different versions or hosts.

## Invocation policy

Use implicit invocation when users should discover the skill naturally and the activation boundary is distinct.

Use explicit-only invocation when:

- The user requests manual selection.
- The workflow is intentionally named.
- A built-in or neighboring skill has substantially overlapping triggers.
- An accidental invocation would be disruptive or expensive.
- The selected host documents another concrete reason.

Invocation is not authorization. A user mentioning a skill does not grant blanket approval for later destructive, paid, privileged, private-data, publishing, or production actions.

## Packaging decisions

- **Local or repository skill:** deliver the skill directory in the host’s current documented discovery location. Do not archive by default.
- **Hosted API skill:** follow the current upload contract; create a top-level-folder archive only when required.
- **Plugin distribution:** use the current plugin package structure. A standalone skill archive is not a substitute for a plugin.
- **Other host:** follow its current official contract and disclose portability loss.

An archive may be supplied as transport convenience, but label it separately from a target-specific upload package.

## Research and source priority

Research changing facts whenever web or official documentation access is available:

1. Current official target-host documentation and specification.
2. Open Agent Skills specification and creator guidance.
3. Official API, SDK, vendor, standards, legal, or regulatory sources.
4. User-provided project artifacts.
5. Primary-source repositories and release notes.
6. Secondary sources only when primary evidence is unavailable.

Stop once evidence is sufficient for the design decision. Record material access dates or version assumptions when compatibility depends on them.

When offline, distinguish verified stable rules from remembered conventions and assumptions. Do not present an unverified current path, command, schema, policy, or price as fact.

## Current official source map

Use these as starting points and verify their current canonical locations at execution time:

- Portable specification: `https://agentskills.io/specification`
- Creator best practices: `https://agentskills.io/skill-creation/best-practices`
- Description optimization: `https://agentskills.io/skill-creation/optimizing-descriptions`
- Behavioral evaluation: `https://agentskills.io/skill-creation/evaluating-skills`
- OpenAI skill authoring: `https://learn.chatgpt.com/docs/build-skills`
- OpenAI API skills: `https://developers.openai.com/api/docs/guides/tools-skills`

Source map reviewed: 2026-09-02. Treat it as a locator, not permanent proof of current behavior.
