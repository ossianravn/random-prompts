# Source transformation

Read this file when the input is a system prompt, runbook, demonstration, trace, project corpus, or existing skill. Preserve the source’s terminology, decision logic, and constraints where they are part of the requested basis; distinguish any new recommendation, current research, or inference.

## Transformation principle

Convert source material into reusable execution knowledge rather than copying its surface form.

Preserve:

- Recurring user goals and outcomes.
- Natural trigger language.
- Ordered procedures and branch conditions.
- Domain-specific decisions, corrections, and gotchas.
- Required inputs, artifacts, approvals, and validation.
- Failure handling and observable completion.
- Organization-specific context when it creates the skill’s value.

Remove or translate:

- Persona theater that does not change execution.
- Always-on behavior unrelated to the skill’s task.
- Platform rules the skill cannot supersede.
- Repeated declarations without an operational consequence.
- One-off instance details that should become parameters or examples.
- Hidden activation logic that belongs in frontmatter `description`.
- Instructions to reveal private reasoning or violate host policy.

## System prompt to skill

Use this mapping:

| Source prompt element | Skill destination |
| --- | --- |
| Identity or role | Short outcome statement or title; retain only expertise that changes decisions |
| Mission or goal | `SKILL.md` outcome and definition of done |
| Activation conditions | Frontmatter `description` and trigger evals |
| Global interaction style | Keep only task-specific interaction rules |
| Inputs and assumptions | Minimum viable input and defaults |
| Ordered phases | Core SOP and workflow chooser |
| Long policy or domain detail | Focused `references/` files with precise load conditions |
| Deterministic mechanics | `scripts/` when code materially improves reliability |
| Reusable templates | `assets/` or a short inline template |
| Output format | Delivery contract or output template |
| Validation rules | Validation workflow and `evals/` |
| Safety boundaries | Approval gates, stop conditions, and least-privilege rules |

A system prompt is always active; a skill is conditionally loaded. Therefore:

1. Put the full activation boundary in `description`.
2. Keep only instructions relevant after activation.
3. Move bulky conditional branches behind explicit file pointers.
4. Translate universal “always” instructions into task-scoped rules.
5. Preserve exact response formats only when they improve downstream reliability; otherwise use a stable artifact contract with adaptive prose.
6. State that system, developer, host, and user policies remain higher priority than the skill.

## Runbook to skill

Extract:

1. Preconditions and required access.
2. Trigger and intended outcome.
3. Default sequence.
4. Branch conditions and decision rules.
5. Commands or operations whose exact form matters.
6. Verification after consequential steps.
7. Recovery, rollback, and escalation paths.
8. Final artifacts and audit evidence.

Replace role-specific assumptions with explicit inputs. Keep organization-specific identifiers only when the skill is intentionally organization-specific.

## Demonstration or trace to skill

Study successful and failed execution, not just the final answer.

Capture:

- Decisions that remained invariant across the run.
- Corrections supplied by the user.
- Steps that prevented or caused rework.
- Tool choices that were necessary rather than incidental.
- Inputs the agent inferred correctly or incorrectly.
- Observable signs that the task was complete.

Discard incidental filenames, temporary paths, exact wording, and detours unless they reveal a reusable gotcha.

## Project corpus to skill

1. Inventory the corpus and identify authoritative files.
2. Separate stable project facts from frequently changing data.
3. Put stable, execution-relevant facts in focused references.
4. Instruct runtime retrieval for current APIs, prices, regulations, schemas, or operational state.
5. Preserve provenance for facts whose authority or freshness matters.
6. Do not copy entire manuals or repositories into references.

## Existing skill revision

Before editing:

1. Read the complete current bundle and relevant neighboring skills.
2. Record the current name, description, invocation policy, inputs, outputs, scripts, references, dependencies, and packaging.
3. Identify observed failures rather than assuming more detail is better.
4. Snapshot or otherwise preserve the previous version when behavioral comparison is possible.

During revision:

- Preserve working interfaces and filenames unless change is necessary.
- Remove duplication before adding new material.
- Tighten routing before creating a router.
- Treat host migration as a compatibility layer, not a rewrite of the portable core.
- Identify breaking changes and migration steps explicitly.

## Archetype versus one-purpose skill

Default to a reusable archetype when the source names a particular company, product, application, or workflow only as an example.

Keep a one-purpose design when:

- Organization-specific data, policy, or integration is the source of value.
- The user explicitly requests a private or product-specific skill.
- Generalizing would erase necessary constraints.
- Authorization, compliance, or operational context cannot be parameterized safely.

## Source fidelity check

Before authoring, be able to label each material instruction as one of:

- **Source-derived:** directly supported by the provided material.
- **Verified current fact:** supported by current external research.
- **Inference:** a reasoned design choice based on the evidence.
- **Assumption:** a default chosen because evidence is absent.
- **Recommendation:** a proposed improvement rather than a source requirement.

Do not silently correct, reconcile, or replace source content when the user asked the source to be the basis. Surface conflicts and choose only when the task requires a decision.
