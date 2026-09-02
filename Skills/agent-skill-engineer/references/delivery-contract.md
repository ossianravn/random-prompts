# Delivery contract

Read this file immediately before responding to the user.

## Phase 1: clarification only when material

When unresolved information materially changes scope, authorization, safety, target compatibility, bundle structure, or the deliverable, return exactly these top-level labels and no other section:

```text
Questions:
- ...

Proposed defaults:
- ...
```

Ask the minimum number of questions, normally one to four. Do not repeat a question already answered or ask for information available in files, tools, or current official documentation.

Otherwise skip Phase 1 and build with labeled assumptions.

## Phase 2: completed work

Return exactly these four top-level sections in this order:

### 1) SKILL SUMMARY

Include:

- Work mode.
- Skill name.
- One-sentence purpose.
- Target hosts.
- Deployment and packaging target.
- Invocation policy.
- Key activation boundary.
- Included resources.
- Resource rationale.
- Specification and host-document basis.
- Material assumptions.
- Breaking changes, when revising.
- Artifact status.

### 2) FILE TREE

Show a simple tree rooted at the skill folder. The root name must equal frontmatter `name`.

### 3) DELIVERY

When files were created:

- List created or changed files.
- Link the actual skill artifact and any separately useful files.
- Summarize material design or migration decisions.
- Do not repeat complete contents unless requested.

When files could not be created:

- Provide every complete file under a heading `### <relative/path/from/skill-root>`.
- Use an appropriate fenced language tag.
- Provide exactly one packaging command only when the selected target requires packaging.

For audit-only work:

- Do not mutate files.
- Provide findings and the requested patch or corrected files.

### 4) VALIDATION

Include:

- Checks run.
- Checks not run and why.
- Structural result.
- Activation result.
- Behavioral result.
- Resource and script result.
- Safety result.
- Packaging result.
- Representative activation cases.
- Remaining risks or assumptions.
- Recommended next validation.

For representative activation cases, show prompt, expected activation, expected outcome, and actual result when run. When a complete eval file is delivered, summarize at least three positive and three near-miss negative cases. When no eval file is delivered, provide six to ten positive and three to six negative prompts.

Do not claim an activation or behavioral result was executed when it was only reviewed manually.

## Artifact rules

- Provide a working link for every created user-facing artifact.
- Prefer one bundle archive for transport when the interface cannot link a directory, while labeling whether it is merely transport packaging or a target-specific upload archive.
- Keep a single top-level skill folder in zip archives when that structure is required or intentionally selected.
- Do not expose font files, secrets, credentials, private fixtures, or unrelated project material.
- Do not duplicate the archive’s entire contents in prose.

## Completion check

Before sending, verify:

- The mechanism choice is justified or a mismatch is disclosed.
- The target profile is explicit.
- The source basis, assumptions, research, and recommendations are distinguishable.
- The description contains the activation boundary.
- The skill captures reusable procedure rather than the source’s one-off surface details.
- Every optional resource has a reason and a precise use condition.
- Portable and host-specific behavior are separated.
- Defaults, non-goals, completion gates, and approval boundaries are clear.
- Structural validity is not presented as proof of behavior.
- Positive and realistic near-miss activation cases were considered.
- Applicable scripts, resources, safety cases, and package structure were tested.
- Fixable failures were repaired and retested.
- The final response contains no extra top-level section.

Complete the strongest safe version in the current response. Do not promise later or background work.
