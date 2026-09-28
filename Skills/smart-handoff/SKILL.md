---
name: smart-handoff
description: Save a durable session handoff to .dev-docs/context (WORKING.md + timestamped history snapshot) so a clean Codex chat can resume fast.
metadata:
  short-description: Save session context to WORKING.md + history snapshot
---

You are preparing a context handoff for the CURRENT Codex session.

Goals:
- Produce an accurate, high-signal handoff that lets a brand-new chat (clean context) resume work immediately.
- Keep a stable "latest" pointer AND keep an immutable history snapshot each run.

Paths (repo-relative):
- Latest pointer: `.dev-docs/context/WORKING.md`
- History snapshots: `.dev-docs/context/history/<TS_FILE>--<TAG_SLUG>.md`
- Optional index: `.dev-docs/context/history/INDEX.md`

Safety / quality rules:
- Prefer verifiable facts from the repo (git status/diff/tests) over memory.
- Never include secrets (tokens, passwords, private keys). If needed, mention WHERE they live (env var name, secret manager, config file path) but not the value.
- If something is unknown, write `Unknown` instead of guessing.
- Keep the snapshot self-contained.

Workflow:
1) Compute timestamps (prefer UTC):
   - TS_ISO: ISO 8601 with timezone, e.g. `2026-01-23T14:22:35Z`
   - TS_FILE: filename-safe version with `:` replaced by `-`, e.g. `2026-01-23T14-22-35Z`

   Preferred shell commands:
   - `TS_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")`
   - `TS_FILE=$(date -u +"%Y-%m-%dT%H-%M-%SZ")`

   If `date` isn’t available, use Python:
   - `python -c "from datetime import datetime,timezone; print(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))"`
   - and then transform `:` -> `-` for TS_FILE.

2) Choose a TAG (short label):
   - If the user provided a tag in their invocation message, use it.
   - Otherwise derive a short tag from the main task.
   - Create TAG_SLUG: lowercase; keep only a–z, 0–9, and hyphens; trim to ~40 chars.

3) Ensure directories exist:
   - `mkdir -p .dev-docs/context/history`

4) Capture repo state (best-effort; if not a git repo, mark Unknown):
   - Branch: `git rev-parse --abbrev-ref HEAD`
   - Commit: `git rev-parse HEAD`
   - Dirty status: `git status --porcelain`
   - Diff summary: `git diff --stat`

5) Write TWO files with the SAME content:
   A) Snapshot (immutable):
      `.dev-docs/context/history/<TS_FILE>--<TAG_SLUG>.md`
   B) Latest pointer (overwrite):
      `.dev-docs/context/WORKING.md`

   Tip: do atomic writes (write temp file then rename) to avoid partial files.

6) Optional (recommended): update an index file
   - Append one line per snapshot to `.dev-docs/context/history/INDEX.md`:
     `- <TS_ISO> — <Main Task/Feature> — <snapshot filename>`

7) After writing the files, print EXACTLY these 3 lines and NOTHING ELSE (no extra punctuation, no code blocks):
✅ Context saved to `.dev-docs/context/WORKING.md`
📦 Snapshot saved to `.dev-docs/context/history/<TS_FILE>--<TAG_SLUG>.md`
🧭 To resume: `/mention .dev-docs/context/WORKING.md`

Write the handoff using this template (fill it in with real content):

# Session Context - <TS_ISO>

## Current Session Overview
- **Main Task/Feature**: <what we are working on right now>
- **Current Status**: <exactly where we are in the process>
- **Session Duration**: <Unknown if not inferable>
- **Last Known Good State**: <what was working last, if known>

## Repo Snapshot
- **Branch**: <branch or Unknown>
- **Commit**: <sha or Unknown>
- **Dirty Working Tree**: <Yes/No/Unknown>
- **git status --porcelain**:
  - <paste or summarize>
- **git diff --stat**:
  - <paste or summarize>

## Recent Activity (most recent work)
- **What We Just Did**:
  - <bullets>
- **Active Problems**:
  - <bullets>
- **Current Files**:
  - <list>
- **Test Status**:
  - <what’s working/broken, last test command if known>

## Key Technical Decisions Made
- **Architecture Choices**:
  - <decision + why>
- **Implementation Approaches**:
  - <patterns + why>
- **Technology Selections**:
  - <libs/frameworks/tools chosen>
- **Performance/Security Considerations**:
  - <constraints and mitigations>

## Code Context
- **Modified Files**:
  - <list>
- **New Patterns / Conventions**:
  - <list>
- **Dependencies**:
  - <added/changed packages>
- **Configuration Changes**:
  - <env/build/config deltas>

## Current Implementation State
- **Completed**:
  - <done + tested>
- **In Progress**:
  - <partial state, very specific>
- **Blocked**:
  - <waiting on what?>
- **Next Steps (priority order)**:
  1. <next action>
  2. <next action>
  3. <next action>

## Running / Testing
- **How to run**:
  - <commands>
- **How to test**:
  - <commands>
- **Known Issues / Gotchas**:
  - <list>

## Conversation Thread
- **Original Goal**:
  - <initial intent>
- **Evolution**:
  - <how scope changed>
- **Lessons Learned**:
  - <key insights>
- **Alternatives Considered**:
  - <what was tried/rejected, and why>

## Resume Checklist
- [ ] `/mention .dev-docs/context/WORKING.md`
- [ ] Review `git status` and `git diff`
- [ ] Run tests
- [ ] Start with “Next Steps #1”
