# Validation playbook

Read this file before validating a new or revised skill. Structural validity is necessary but does not prove correct activation or better task performance.

## Validation record

For every layer, record:

- Checks actually run.
- Inputs or environment used.
- Result.
- Fixes made.
- Checks rerun.
- Checks not run and exact reason.
- Strongest manual substitute.
- Remaining risk.

Never infer a pass from absence of visible errors.

## A. Structural validation

Use the current official validator for the selected target.

For portable Agent Skills, prefer:

```bash
skills-ref validate ./<skill-name>
```

When unavailable, use this skill’s fallback:

```bash
python3 scripts/validate_skill.py /path/to/<skill-name>
```

The fallback checks portable frontmatter, naming, body presence, common relative links, JSON resources, OpenAI YAML parseability, and unsafe bundle residue. It does not replace current host schema validation or behavioral testing.

Manually verify:

- Folder and frontmatter `name` match.
- `SKILL.md` exists and YAML parses.
- Required fields and target constraints pass.
- Optional fields are justified and target-supported.
- Referenced paths exist and remain inside the bundle.
- No placeholder, cache, generated workspace, credential, private fixture, or unrelated output is present.
- Packaging matches the selected target.

Do not invent commands such as `skills validate` or `skills run` unless current official host documentation defines them.

## B. Resource validation

For every script:

1. Run syntax, lint, or type checks when available.
2. Run `--help` or equivalent.
3. Run the happy-path smoke test in an isolated workspace.
4. Exercise at least one expected error path.
5. Confirm exit codes, stdout, stderr, and structured output.
6. Inspect dependency declarations, path handling, secret handling, network access, and side effects.

For references and assets:

- Check relative links and load conditions.
- Parse every JSON, YAML, or schema file.
- Confirm templates contain no unresolved placeholders in delivered outputs.
- Confirm fixtures contain no secrets or unnecessary personal information.

## C. Activation evaluation

Create realistic labeled prompts that cover:

- Explicit invocation.
- Direct implicit invocation.
- Alternate natural phrasing.
- Contextual or noisy requests.
- Incomplete but in-scope requests.
- Adjacent near-misses.
- Out-of-scope requests with overlapping vocabulary.
- Collision cases with neighboring skills.

For a nontrivial finished skill, aim for roughly 8–10 positive and 8–10 negative cases. Start smaller for an early draft and expand after the first run.

Positive cases should vary phrasing, detail, explicitness, and complexity. Negative cases should be plausible near-misses rather than obviously unrelated prompts.

When the environment permits:

1. Run each implicit-routing prompt multiple times.
2. Keep a holdout subset that was not used to tune the description.
3. Record actual activation, not only expected activation.
4. Tighten the description or scope when false positives and false negatives reveal a pattern.

## D. Behavioral evaluation

Define success before grading. A behavioral case includes:

- A realistic prompt.
- Human-readable expected output.
- Optional input files.
- Assertions only after output behavior is understood well enough to avoid brittle checks.

Store authored cases in `evals/evals.json`. Store generated run output in a sibling workspace, not inside the skill.

Run each case in a clean context:

- With the skill.
- Without the skill, or with a snapshot of the previous version.

Evaluate applicable dimensions:

- **Outcome:** The task and artifact are correct.
- **Process:** Required decisions, tools, validations, and approvals occurred.
- **Contract:** Output follows required structure without brittle wording dependence.
- **Efficiency:** The skill reduces detours, repeated work, or unnecessary context.
- **Cleanliness:** No unexpected files, mutations, or residue remain.

Inspect traces, tool calls, and artifacts as well as final prose. For Codex, use a currently documented trace mechanism such as `codex exec --json` when available and appropriate; verify the current command before use.

Use deterministic assertions for objective properties and rubric or human review for subjective quality. Compare quality and cost against the baseline rather than grading the skill in isolation.

## E. Safety evaluation

Exercise relevant cases:

- Prompt injection in a retrieved document or repository file.
- Missing or malformed inputs.
- Unauthorized destructive or privileged action.
- Path traversal or unsafe filenames.
- Secret exposure in input, logs, output, fixtures, or archive.
- Network or tool failure.
- Partial completion and rollback.
- Validator failure.
- Repeated retry loops.
- Unexpectedly broad batch scope.
- Paid, publishing, production, or private-data actions without timely approval.

Verify that the skill stops, narrows scope, asks for approval near the consequential action, or reports the failure truthfully as appropriate.

## F. Packaging validation

When an archive or plugin package is required:

- Validate the uncompressed source first.
- Confirm required top-level structure.
- Confirm all and only intended files are included.
- Exclude caches, hidden credentials, generated eval workspaces, build output, and the archive itself.
- List archive contents.
- Re-extract into a clean temporary directory and validate the extracted bundle.
- Record archive size and checksum when useful.

Use this skill’s packager for a standard one-top-level-folder zip:

```bash
python3 scripts/package_skill.py /path/to/<skill-name> --output /path/to/<skill-name>.zip
```

## Repair loop

For each fixable failure:

1. Identify the underlying cause: routing, scope, hierarchy, instruction ambiguity, missing default, resource defect, safety gap, or packaging error.
2. Change the smallest source-of-truth location.
3. Remove superseded wording rather than layering another exception.
4. Rerun the affected layer and any downstream layer the change can influence.
5. Record the new result.

Report unresolved blockers plainly. A skipped check is not a failed check, but it remains an evidence gap.
