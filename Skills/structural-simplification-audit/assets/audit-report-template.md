# Structural Simplification Audit — {repository name}

## Repository snapshot

- Audit mode: {full repository | bounded | revalidation}
- Repository root: `{absolute path}`
- Revision: `{commit or revision identifier}`
- Branch/state: `{branch or detached state}`
- Audit started: `{timestamp}`
- Audit completed: `{timestamp}`
- User constraints: {constraints}
- Inaccessible areas: {none or exact paths/reasons}
- Baseline status: {clean or exact pre-existing status, stored below}
- Final status matches baseline: {yes | no}
- Runtime validation performed: no; audit-only

### Baseline repository status

```text
{complete baseline status output}
```

### Final repository status

```text
{complete final status output}
```

## Executive summary

- Coverage: {reviewed subsystem count}/{total subsystem count}; {assigned relevant files}/{total relevant files}; {explicit exclusions}; {unassigned count}
- Confirmed recommendations: {count}
- Explicit skips: {count}
- Priority mix: {A count} A, {B count} B, {C count} C
- Highest-value structural pattern: {one sentence}
- Best first implementation slice: {finding ID and one sentence}
- Important limitation: {none or one sentence}

## Coverage contract

### File reconciliation

| Category | Tracked count | Assigned to subsystem | Explicitly excluded | Unassigned | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| First-party implementation |  |  |  |  |  |
| Tests and fixtures |  |  |  |  |  |
| Schemas and generated-contract sources |  |  |  |  |  |
| Build, deployment, and tooling |  |  |  |  |  |
| Generated outputs |  |  |  |  |  |
| Vendored, binary, assets, lockfiles, non-material docs |  |  |  |  |  |
| **Total** |  |  |  |  |  |

### Subsystem inventory

| ID | Subsystem | Exact ownership boundary | Key implementation | Public interfaces and generated contracts | Major call sites/dependents | Tests/fixtures | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 |  | Included:  Excluded: |  |  |  |  | queued |

### Explicit file/path exclusions

| Path or pattern | Category | Reason | Authoritative source/owner when generated | Verified by |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Forest maps

### Ownership map

| State, invariant, or lifecycle | Authoritative owner | Writers | Readers | Validation boundary | Ownership concern/evidence |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### Representation map

| Domain concept | Representations | Source of truth | Conversion points | Optional/sentinel/discriminator fields | Concern/evidence |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### Flow map

| Flow ID and name | Entry point | Subsystems traversed | Branches/transforms/work | Ownership handoffs | Exit/result | Concern/evidence |
| --- | --- | --- | --- | --- | --- | --- |
| P01 |  |  |  |  |  |  |

## Confirmed recommendations

### F001 — {concise title}

- Authoritative subsystem: `{Sxx — name}`
- Verdict: recommend
- Priority: `{A | B | C}`
- Confidence: `{high | medium | low}`

#### Evidence

- Implementation: `{path:line-line — what it proves}`
- Public interface/contract: `{path:line-line — what it proves}`
- Major call sites: `{path:line-line — what they prove}`
- Tests/fixtures: `{path:line-line — what they constrain}`
- Cross-flow evidence: `{flow/map row or additional path:line-line}`

#### Current model and material complexity

{Describe the present data structure, state representation, control flow, algorithm, or ownership model. State the concrete special cases, invalid combinations, repeated work, or divided authority.}

#### Proposed model

{Describe the smallest representation or ownership change. Explain why it is simpler across the complete flow, not just one file.}

#### Complexity delta

| Measure | Before | After | Evidence/assumption |
| --- | ---: | ---: | --- |
| State combinations or lifecycle flags |  |  |  |
| Branch/special-case sites |  |  |  |
| Representations/conversions |  |  |  |
| Scans/passes/sorts/serialization cycles |  |  |  |
| State owners/mutation paths |  |  |  |
| Interfaces/pass-through layers |  |  |  |

Remove rows that do not apply. Do not invent counts.

#### Smallest credible implementation slice

- Affected files: {exact files}
- Affected interfaces/contracts: {exact interfaces}
- Slice boundary: {what changes}
- Explicit non-goals: {what does not change}
- Independently useful outcome: {why the slice earns its keep}

#### Risks and migration

- Regression risks: {specific risks}
- Compatibility/persistence/protocol risks: {specific risks or none}
- Concurrency/lifecycle risks: {specific risks or none}
- Migration concerns: {ordering, dual-read/write, rollout, or none}

#### Validation

- Existing validation: {tests, type checks, contracts, callers; not run}
- Additional validation required: {specific tests/checks for a later implementation}
- Runtime evidence still needed: {measurement or none}

#### Scores

| S | C | R | F | Value/12 | E | B | Cost/6 | Net | Confidence |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
|  |  |  |  |  |  |  |  |  |  |

#### Dependencies and alternatives

- Prerequisites: {finding IDs or none}
- Enables: {finding IDs or follow-on work}
- Rejected alternatives: {alternative and why it only moves/adds complexity}
- Cross-subsystem notes: {notes without unowned scope}

## Explicit skips

### Sxx — {subsystem name}

- Status: skip
- Boundary inspected: {exact boundary}
- Representative implementation: {paths and lines}
- Interfaces and major call sites: {paths and lines}
- Tests/fixtures: {paths and lines}
- Why no candidate passed the materiality gate: {specific reason}
- Intentional complexity worth preserving: {specific semantics or none}
- Rejected candidates: {brief candidate/reason or none}
- Confidence: {high | medium | low}

## Cross-cutting patterns

Record evidence-backed patterns that help explain the system. Do not count them as recommendations until they have one owner and a bounded material slice.

| Pattern ID | Observation | Evidence | Affected subsystems | Disposition |
| --- | --- | --- | --- | --- |
| X01 |  |  |  | {informational | owned by Fxxx | rejected} |

## Duplicates, rejected, and superseded findings

| Candidate ID | Origin subsystem | Disposition | Authoritative finding or reason | Evidence checked by |
| --- | --- | --- | --- | --- |
|  |  | {duplicate | rejected | narrowed | superseded} |  |  |

## Priority and dependencies

| Rank | Finding | Priority | Value | Cost | Net | Confidence | Prerequisites | Blast radius | Why this order |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |  |  |

### Best first implementation slices

1. **{Finding ID — title}:** {small slice, concrete benefit, validation boundary, and why it comes first}.
2. **{Finding ID — title}:** {next slice or omit}.
3. **{Finding ID — title}:** {next slice or omit}.

This section describes future implementation order only. No implementation occurred during the audit.

## Audit-the-audit validation

### Coverage pass

- Reviewer/context: {fresh agent or fresh pass}
- Tracked-file reconciliation checked: {yes/no}
- Missing subsystem or boundary found: {none or details}
- Corrective action: {none or new subsystem/review}
- Result: {pass/fail}

### Ownership-overlap pass

- Reviewer/context: {fresh agent or fresh pass}
- Duplicate file/interface/state ownership found: {none or details}
- Corrective action: {none or details}
- Result: {pass/fail}

### Materiality and over-abstraction pass

- Reviewer/context: {fresh agent or fresh pass}
- Findings rejected/narrowed/demoted: {none or IDs/reasons}
- Remaining recommendations remove rather than move complexity: {yes/no}
- Result: {pass/fail}

### Schema-completeness pass

- Reviewer/context: {fresh agent or fresh pass}
- Missing fields: {none or details}
- Corrective action: {none or details}
- Result: {pass/fail}

### Priority-and-dependency pass

- Reviewer/context: {fresh agent or fresh pass}
- Score inconsistencies or ordering issues: {none or details}
- Corrective action: {none or details}
- Result: {pass/fail}

### Repository immutability check

- Baseline and final status compared exactly: {yes/no}
- Difference: {none or exact difference}
- Repository unchanged by audit: {yes/no/not provable}

## Audit log

| Time/order | Action | Scope | Evidence/artifact | Decision/result |
| --- | --- | --- | --- | --- |
| 1 | Baseline captured | Repository | revision, status, tracked files |  |
| 2 | Coverage contract established | Repository | subsystem and file reconciliation |  |
