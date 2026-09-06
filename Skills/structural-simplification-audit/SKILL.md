---
name: structural-simplification-audit
description: "Audit codebases for materially useful structural simplifications in data structures, state representation, control flow, algorithms, and ownership; use for read-only whole-repository or explicitly bounded reviews that remove special cases, invalid states, duplicate work, and unclear responsibility without stylistic churn, speculative abstractions, implementation, tests, or repository edits."
---

# Structural Simplification Audit

Audit the codebase as a system, not as a pile of files. Apply a Torvalds-style structural taste lens: improve the representation until exceptional cases become ordinary cases, then prefer the smallest boring design that preserves real semantics. Do not imitate any person's tone or review style.

## Quick start

1. **Choose the mode.** Default to a full-repository audit unless the user gives an exact boundary. State that the exercise is read-only. Done when scope and exclusions are explicit.
2. **Freeze the baseline.** Record repository identity, revision, tracked files, and the complete working-tree status without changing anything. Keep the audit artifact outside the repository. Done when later comparison is possible.
3. **Establish coverage.** Inventory coherent subsystems and assign every materially relevant tracked file to exactly one subsystem or an explicit exclusion. Done when there are no unexplained files or catch-all rows.
4. **See the forest.** Map ownership, representations, and representative end-to-end flows before judging local code. Done when cross-boundary duplication and state movement are visible.
5. **Review bounded subsystems.** Inspect implementation, interfaces, call sites, and tests; return at most two material candidates per subsystem or `skip`. Done when every subsystem is `recommend` or `skip`.
6. **Verify and score.** Independently re-open every candidate, measure what disappears, reject complexity relocation, deduplicate, and rank. Done when only evidenced recommendations remain.
7. **Audit the audit.** Run fresh coverage, overlap, materiality, schema, and dependency passes; reconcile the final repository status with the baseline. Done when the report is complete and the repository is unchanged.

Use `assets/audit-report-template.md` as the canonical scratchpad and final report structure.

## Workflow chooser

- **Full repository audit — default:** inventory and review the complete first-party codebase, including materially relevant frontend, backend, shared code, platform bridges, generated-contract ownership, tests, and tooling.
- **Bounded audit:** use only when the user names an exact package, service, feature, or path boundary. Inspect its public dependencies and call sites to understand semantics, but do not convert those dependencies into extra audit scope.
- **Audit revalidation:** use when a prior report exists. Rebuild the coverage contract against the current revision, then verify, rescore, merge, supersede, or reject each prior finding. Do not assume old evidence still holds.

## Minimum viable input

Require only:

- a readable repository root;
- an explicit scope, or default full repository;
- a report destination, or default to a temporary artifact outside the repository;
- user constraints, especially generated, vendored, confidential, or inaccessible areas.

Infer languages, build systems, entry points, and subsystem boundaries from the repository. Do not ask for architecture documentation unless access to the repository is insufficient to identify ownership.

## Hard guardrails

- **Audit only.** Do not edit, create, delete, rename, format, generate, migrate, commit, push, or clean anything in the repository.
- **Do not execute project code.** Do not run tests, builds, linters, formatters, code generators, package managers, migrations, dev servers, benchmarks, or project scripts.
- **Use read-only inspection.** Prefer `git ls-files`, `git grep`, `rg`, `find`, `sed`, `awk`, manifest inspection, and direct file reads. Do not execute untrusted repository content.
- **Keep artifacts outside the repository.** Use agent memory or a temporary path unless the user explicitly authorizes another destination.
- **Preserve pre-existing dirt.** Record the full initial status and compare it byte-for-byte at the end. Never reset, stash, checkout, or remove user changes.
- **Review real behavior, not imagined futures.** Use current interfaces, call sites, tests, persisted data, and documented contracts. Do not design for every theoretically possible edge case.
- **Respect compatibility.** A simpler internal model is not material if it silently breaks public, persisted, protocol, concurrency, or generated-contract semantics.

## Structural taste rules

Use these rules as decision tests, not slogans:

1. **Change the model before adding branches.** Prefer a representation in which the common path and former edge cases share one invariant.
2. **Delete complexity; do not hide it.** Count removed states, branches, passes, representations, ownership hops, and synchronization points. A helper, registry, framework, or type that merely moves them is not a simplification.
3. **Keep one source of truth.** Derive values when derivation is cheap and reliable; do not synchronize mirrored state without a demonstrated need.
4. **Match the structure to the operations.** Choose collections and indexes from actual lookup, update, ordering, and lifecycle needs, not habit.
5. **Give each invariant one owner.** State mutation, lifecycle transitions, validation, and generated contracts need an authoritative module or boundary.
6. **Prefer direct, boring code.** A few explicit cases can be simpler than a generic abstraction. Cleverness must remove more reasoning than it introduces.
7. **Optimize whole flows.** Local elegance is irrelevant when the same data is converted, scanned, validated, or branched on repeatedly across layers.
8. **Keep rare cases proportionate.** Handle reachable failures and contracts, but do not contaminate the organizing model with speculative possibilities.

## Core SOP

### 1. Freeze the repository baseline

Identify the repository root and record, outside the repository:

- repository path and name;
- current revision and branch or detached state;
- complete `git status --porcelain=v1 -uall` output;
- tracked-file inventory from `git ls-files`;
- inaccessible paths, submodules, or worktrees;
- audit mode, user constraints, and timestamp.

For Git repositories, use non-locking reads where supported:

```bash
GIT_OPTIONAL_LOCKS=0 git rev-parse --show-toplevel
GIT_OPTIONAL_LOCKS=0 git rev-parse HEAD
GIT_OPTIONAL_LOCKS=0 git status --porcelain=v1 -uall
GIT_OPTIONAL_LOCKS=0 git ls-files
```

For non-Git repositories, record a read-only file inventory and available revision metadata. Do not claim an unchanged-repository guarantee stronger than the available baseline supports.

**Done when:** the exact initial state can be compared with the final state and the canonical audit artifact exists outside the repository.

### 2. Establish the coverage contract

Discover subsystems from runtime and ownership signals, not top-level folders alone:

- workspace, package, build, deployment, and dependency manifests;
- executable entry points, route or command registration, workers, jobs, and platform bridges;
- public packages, exported APIs, schemas, persisted models, and generated-contract sources;
- major product flows and shared infrastructure;
- test suites, fixtures, and tooling that encode production architecture.

Assign stable IDs such as `S01`, `S02`, and define each row with:

- descriptive name;
- exact ownership boundary, including paths and explicit exclusions;
- key implementation files;
- public interfaces and generated contracts;
- major call sites and dependents;
- relevant tests and fixtures;
- status: `queued`, `in review`, `recommend`, or `skip`.

Reconcile the tracked-file inventory:

- assign every materially relevant first-party source, test, schema, configuration, and tooling file to exactly one authoritative subsystem;
- explicitly exclude vendored dependencies, binaries, static assets, lockfiles, and non-architectural documentation when they are not material;
- assign generated outputs to a `generated output` exclusion and audit the generator, schema, or source contract under its owning subsystem;
- split a row when it contains independent entry points, state owners, or public contracts;
- never use an `other`, `misc`, or broad catch-all row as proof of coverage.
- Use exact directories or globs with enumerated exceptions when that is sufficient; if boundaries overlap, maintain a full file-to-subsystem ledger in the scratchpad until every file has one owner.

**Done when:** every relevant tracked file is assigned once or explicitly excluded, every subsystem boundary is non-overlapping, and every row is `queued`.

### 3. Build the forest maps

Create three compact cross-cutting maps before subsystem reviews.

**Ownership map**

For each important state or invariant, record the authoritative owner, writers, readers, lifecycle authority, and boundary where validation occurs. Flag multiple writers, mirrored stores, split lifecycle control, and rules duplicated across layers.

**Representation map**

For each major domain concept, record its in-memory, transport, persistence, UI, generated, and test representations; conversion points; optional or sentinel fields; discriminators; and source of truth. Flag shape guessing, stringly typed variants, repeated conversion, and stored derived values.

**Flow map**

Trace representative read, write, async/lifecycle, and error paths for each major product flow. Record branch points, scans, sorts, serialization, validation, retries, caches, queues, and ownership handoffs. Flag work repeated across layers or on every item/request.

Use the maps to seed questions, not conclusions. A pattern becomes a recommendation only after subsystem evidence and coordinator verification.

**Done when:** every subsystem is connected to the maps or explicitly justified as isolated, and the coordinator can explain where core data originates, changes form, changes owner, and terminates.

### 4. Run bounded subsystem reviews

Use fresh read-only agents when available. Keep only as many concurrent lanes as the coordinator can actively compare; default to at most four. Give each worker one exact, non-overlapping subsystem boundary and only the relevant forest-map context. If workers are unavailable, run the same reviews sequentially with a fresh subsystem brief.

Use this worker brief verbatim, filling in the boundary fields:

```text
Review subsystem {ID}: {name}.

Ownership boundary:
{exact included paths, interfaces, and explicit exclusions}

This is read-only. Do not edit files, run tests, execute project code, install dependencies, or expand scope.

Inspect the implementation, public interfaces, major call sites, relevant tests, and the supplied ownership/representation/flow context. Find at most two materially useful structural simplifications in data structures, state representation, control flow, algorithms, or ownership. Prefer a changed model that removes special cases, invalid states, repeated work, or divided authority.

Do not recommend stylistic consistency, speculative extensibility, generic layers, minor line-count reduction, helper extraction, switch-to-registry conversion, caching, or state machines unless they demonstrably remove current complexity. Prefer boring local code when it is already clear.

For each candidate return:
1. Verdict: recommend or skip.
2. Exact evidence: file and line references, public interface, major call sites, and tests.
3. Current model and the concrete complexity or invalid states it creates.
4. Proposed representation or ownership model.
5. Complexity delta: what states, branches, representations, passes, lookups, or owners disappear.
6. Smallest credible implementation slice, affected files, and interfaces.
7. Regression, compatibility, concurrency, and migration risks.
8. Existing validation and additional validation required.
9. Preliminary scores and confidence.
10. Cross-subsystem notes, without expanding scope.

Return at most two candidates. Return `skip` when no candidate clearly passes the materiality gate.
```

The coordinator harvests results in batches, closes completed workers where the host supports it, and updates the canonical report. Do not interrupt a productive worker solely because another lane finished.

**Done when:** every inventory row has been reviewed and has either at least one candidate awaiting verification or an evidenced `skip`.

### 5. Apply the review lenses

Inspect each subsystem through these lenses.

**Data and state representation**

- Boolean, nullable, sentinel, or optional-field combinations permit contradictory or unreachable states.
- A single concept has parallel types or object shapes with repeated assumptions and conversions.
- Derived state is stored and synchronized instead of computed from an owner.
- Strings, integers, or option bags encode variants that should be explicit.
- A state machine or discriminated union would remove invalid combinations and centralize real transitions; do not introduce one for a trivial two-state value.

**Control flow**

- The same discriminator is switched on across multiple call sites.
- First, last, empty, legacy, retry, or mode cases exist because the representation makes them exceptional.
- Flags steer long procedures through unrelated modes.
- Async or lifecycle behavior is spread across callbacks, booleans, timers, and nullable handles that can become stale or contradictory.
- A table or registry is simpler only when behavior is genuinely data-like, stable, and inspectable; it is worse when it hides control flow.

**Algorithms and collections**

- Repeated linear scans, nested joins, sorts, parsing, serialization, filtering, or normalization occur on a meaningful path.
- A list is used as an index, a map as an ordered sequence, or multiple collections mirror the same membership.
- Work is recomputed across layers or per item when one boundary computation would suffice.
- A cache is acceptable only when measured or structurally obvious repeated work is material and invalidation has a single clear owner. Otherwise caching adds state and is a rejection.

**Ownership and boundaries**

- Multiple modules can mutate the same invariant or lifecycle.
- UI, service, persistence, and transport layers each re-decide the same business rule.
- Pass-through wrappers, facades, or adapters add hops without owning validation, translation, policy, or lifecycle.
- Generated output is edited or reasoned about instead of its schema or generator owner.
- Shared mutable singletons, ambient context, or event buses obscure who initiates and completes work.

**Whole-flow simplification**

- Data crosses several nearly identical representations and returns to its original shape.
- Validation is duplicated at internal layers instead of performed once at a trusted boundary.
- A local abstraction makes one file smaller while increasing concepts, calls, or state across the flow.
- Separate implementations that must change together have one stable shared rule; merge only that rule, not superficially similar code.

**AI-shaped accretion signals**

Treat these as search cues, never as proof by themselves:

- A feature added a new helper, model, service, cache, or fallback even though an existing owner already performs the same job.
- Near-duplicate types or utilities differ only because each task was solved in local context.
- Defensive null checks, option bags, and fallback branches compensate for an invariant that no boundary owns.
- Old and new paths both remain active because additions were layered around existing behavior instead of replacing it.
- Several locally reasonable transformations or scans compose into needless system-wide work.
- Comments explain coordination that a simpler ownership or state model could make obvious.

### 6. Enforce the materiality gate and score candidates

Accept a recommendation only when all are true:

1. Current complexity is evidenced in the present repository, not hypothetical.
2. The proposed model removes complexity rather than relocating or renaming it.
3. The affected semantics, interfaces, call sites, and tests have been inspected.
4. The smallest credible slice is bounded and independently useful.
5. Risks and validation are specific enough for a later implementer.
6. The structural score is at least `2` and total value is at least `6`.

Every accepted finding must state at least one before-to-after delta, for example:

- valid and invalid state combinations;
- branch or special-case sites;
- representations and conversion points;
- full scans, passes, sorts, or serialization cycles;
- state owners or mutation paths;
- lifecycle flags and transition sites;
- interfaces or pass-through layers.

Score without false precision:

| Dimension | Range | Meaning |
| --- | ---: | --- |
| Structural reduction `S` | 0-4 | 0 cosmetic; 1 local cleanup; 2 removes one recurring structural burden; 3 removes several; 4 changes the model so a class of special cases disappears. |
| Correctness leverage `C` | 0-3 | 0 none; 1 clearer invariant; 2 prevents plausible stale or contradictory state; 3 removes a serious reachable correctness class. |
| Runtime/work reduction `R` | 0-3 | 0 none; 1 modest repeated work; 2 material common-path work; 3 asymptotic or high-volume reduction. |
| Reach/frequency `F` | 0-2 | 0 rare/local; 1 recurring within a subsystem; 2 common or cross-subsystem. |
| Implementation effort `E` | 0-3 | 0 local; 1 small multi-file slice; 2 moderate coordinated change; 3 broad migration or redesign. |
| Blast/migration risk `B` | 0-3 | 0 private; 1 limited internal interface; 2 many callers or public/persisted contract; 3 compatibility, data, or concurrency migration. |

Calculate:

- `Value = S + C + R + F` out of 12.
- `Cost = E + B` out of 6.
- `Net = Value - Cost`, used only as a ranking aid.
- `Confidence = high`, `medium`, or `low`, based on evidence completeness and semantic certainty.

Priority bands:

- **A:** value 9-12, cost 0-3, high or medium confidence, and no hard prerequisite.
- **B:** value 7-12, net at least 3, and high or medium confidence.
- **C:** value at least 6 but blocked, costly, broad, or lower-confidence; keep only when still clearly material.

A numeric score never rescues weak evidence. Reject candidates that miss the gate even when a formula looks favorable.

### 7. Verify, deduplicate, and synthesize

The coordinator independently re-opens every candidate's evidence and checks:

- the cited code and lines exist at the audited revision;
- public interfaces and major callers actually rely on the claimed behavior;
- tests confirm or constrain the semantics;
- the proposed model handles current reachable cases without inventing future ones;
- complexity is removed across the flow, not shifted behind a helper, type, registry, service, cache, or event;
- the smallest slice can land without requiring the entire redesign;
- scores match the evidence.

Reject, narrow, merge, or demote findings that are vague, duplicated, intentionally complex, compatibility-blind, or over-abstracted. Assign each accepted finding to one authoritative subsystem. Record overlapping candidates in `Duplicates and superseded findings` rather than counting them twice.

Set a subsystem to:

- `recommend` when at least one verified finding belongs to it;
- `skip` when review is complete and no candidate passes the gate.

Record cross-cutting patterns separately. Do not turn a pattern into a recommendation unless it has one owner, a bounded slice, and complete evidence.

**Done when:** all rows are `recommend` or `skip`, every accepted finding is independently verified, and no duplicate recommendation remains.

### 8. Audit the audit

Run fresh independent passes, using new agents where available:

1. **Coverage:** compare the tracked-file inventory, manifests, entry points, and report. Find unassigned files, hidden runtime units, missing generated-contract owners, and overly broad boundaries.
2. **Ownership overlap:** find files, interfaces, state, and findings claimed by multiple subsystems; choose one authoritative owner or split the boundary.
3. **Materiality:** challenge every recommendation for style-only value, speculative design, hidden complexity, cleverness, unnecessary state machines, registries, caches, service layers, and generic abstractions.
4. **Schema completeness:** verify every finding and skip has all required evidence, scope, delta, risk, validation, score, confidence, and ownership fields.
5. **Priority and dependencies:** check score consistency, prerequisites, migration order, blast radius, and whether the proposed first slices are independently useful.

If coverage reveals a real omission, add a new explicit subsystem row and run its bounded review. Never conceal an omission by broadening an already completed row. Repeat the affected validation pass after every correction.

Finally, capture the repository status using the same method as the baseline and compare the complete output. Report pre-existing changes exactly; do not repair them.

**Done when:** all five passes are clean or their findings are resolved, unassigned relevant files equal zero, and final repository state matches the baseline.

## Output contract

Maintain one canonical artifact throughout the audit. It must contain:

- repository snapshot, scope, constraints, and unchanged-state evidence;
- complete subsystem coverage contract and file reconciliation;
- ownership, representation, and flow maps;
- confirmed recommendations;
- explicit subsystem skips;
- cross-cutting patterns;
- rejected, duplicate, and superseded candidates;
- dependency-aware ranking and first implementation slices;
- independent audit-validation results;
- chronological audit log.

For every confirmed recommendation include:

1. ID, title, authoritative subsystem, verdict, and priority.
2. Exact file-and-line evidence, public interfaces, major call sites, and tests.
3. Current representation, control flow, algorithm, or ownership model.
4. Concrete current complexity or invalid states.
5. Proposed model and why it is simpler.
6. Before-to-after complexity delta.
7. Smallest credible implementation slice and affected interfaces.
8. Regression, compatibility, concurrency, and migration risks.
9. Existing validation and additional validation required.
10. `S`, `C`, `R`, `F`, value, `E`, `B`, cost, net, and confidence.
11. Dependencies, prerequisites, and rejected alternatives.

For every skip include the inspected boundary, representative implementation, interfaces, call sites, tests, reason no candidate passed the gate, intentional complexity worth preserving, and confidence.

Do not include patches or claim runtime validation. Tiny pseudocode or type sketches are allowed only when necessary to explain a representation change.

## Definition of done

The audit is complete only when:

- the repository scope and immutable baseline are recorded;
- every materially relevant tracked file is assigned once or explicitly excluded;
- every identifiable subsystem has an exact non-overlapping boundary;
- every subsystem is `recommend` or `skip`;
- implementation, interfaces, major call sites, and tests were inspected for every reviewed subsystem;
- every accepted finding passes the materiality gate and has complete evidence, delta, scope, risk, validation, scores, confidence, and ownership;
- duplicates, weak abstractions, style-only findings, and speculative edge-case designs are removed;
- cross-cutting findings have one authoritative owner;
- priorities and dependencies are internally consistent;
- first implementation slices are bounded and independently useful;
- all five audit-the-audit passes are complete;
- final repository status exactly matches the baseline;
- the report states limitations instead of implying unsupported coverage.

## Troubleshooting

- **Repository is too large for one context:** keep the file inventory and canonical report as external state, split by coherent ownership, use bounded fresh reviews, and continue until every row closes. Do not sample and call it complete.
- **Subsystem boundary is ambiguous:** follow the invariant and public interface. The subsystem that authoritatively mutates the state or defines the contract owns the finding; callers are evidence, not co-owners.
- **Generated code dominates:** exclude generated outputs explicitly, locate their schema or generator, and audit that source under one owner. If the source is external or inaccessible, state the limitation.
- **Tests are missing:** inspect all available call sites and contracts, record the gap as implementation risk, and specify validation a later change would need. Do not run or invent tests during the audit.
- **Working tree is already dirty:** preserve and report the exact baseline. Completion requires equality with that baseline, not a clean tree.
- **Candidate only shortens code:** reject it unless it removes a state, branch, pass, representation, owner, or material unit of work.
- **State machine seems attractive:** first enumerate actual valid and invalid combinations and transition sites. Reject it when a simple enum, nullable value, or direct branch is clearer.
- **Registry or abstraction seems attractive:** list all current cases and future evidence. Reject it when cases are few, behavior differs, or indirection hides control flow.
- **Performance benefit is uncertain:** report it as unscored speculation or request later measurement; do not use it to pass the materiality gate.

## Resource map

- `assets/audit-report-template.md` — canonical coverage ledger, finding schema, scoring tables, validation passes, and audit log. Copy it only to a location outside the audited repository.
