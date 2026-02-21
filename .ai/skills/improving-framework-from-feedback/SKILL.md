---
name: improving-framework-from-feedback
description: "Improve an AI agent framework from git evidence (result commit + fix-up commits); produce targeted patches to <framework>/core|tech and/or <project-local>/ so a rerun with the same prompt/model no longer needs manual fixes."
---

# Improving framework from git feedback

Turn “model output → human fixes” into minimal, generalizable framework changes.

Operate on evidence, not memory.
Prefer small patches that prevent the same class of error.

## Inputs

- `PATCH_MODE` — where to apply patches.
  - `framework-repo`: patch this repository (the framework source repo where you are running) and/or `{PROJECT_DIR}/.ai/project-local/`.
  - `consumer-project`: patch `{PROJECT_DIR}/.ai/ergo/` (framework checkout inside the consumer project) and/or `{PROJECT_DIR}/.ai/project-local/`.
- `PROJECT_DIR` — path to the project repo that contains:
  - a framework checkout (often `.ai/ergo/`), and
  - a project-local overlay `<project-local>/` (often `.ai/project-local/`).
- `MODEL` — model identifier used to produce the result (store verbatim).
- `PROMPT` — exact prompt text used (store verbatim).
- `RESULT_COMMIT` — git commit SHA with the model-produced result (the “before fixes” state).
- `FIX_COMMITS[]` — one or more commit SHAs that correct the result; commit messages include rationale and/or constraints.
- Optional: `FINAL_COMMIT` — the “after fixes” commit to diff against (default: `HEAD`).

## Output

- A set of patches to framework files under:
  - `<framework>/core/` and/or `<framework>/tech/` and/or `<project-local>/`
- Each patch must be explicitly linked to:
  - the mistake pattern observed (from diffs),
  - the fix rationale (from commit messages),
  - the exact framework lever you changed (rule/checklist/template/skill/script).

## Quick start commands

Run these in `PROJECT_DIR`:

- Inspect the model result:
  - `git show --stat RESULT_COMMIT`
  - `git show RESULT_COMMIT`
- Inspect all fixes:
  - `git show --stat <fix1> ...`
  - `git show <fix1> ...`
- See the net effect from result to final:
  - `git diff RESULT_COMMIT..HEAD`
  - If final is a known commit: `git diff RESULT_COMMIT..<FINAL_COMMIT>` (otherwise use `HEAD`).
- Compare fix series structure (useful when multiple fix commits exist):
  - `git range-diff RESULT_COMMIT^..RESULT_COMMIT RESULT_COMMIT..FINAL_COMMIT` (or use `HEAD`).

## Workflow

### 0) Resolve patch roots (mode selection)

Decide `PATCH_MODE`, then resolve patch roots.

- If `PATCH_MODE` is not provided:
  - If `{PROJECT_DIR}/.ai/ergo/` exists: set `PATCH_MODE=consumer-project`.
  - Otherwise: set `PATCH_MODE=framework-repo`.
- Resolve these two directories:
  - `FRAMEWORK_DIR`:
    - If `PATCH_MODE=framework-repo`: `FRAMEWORK_DIR=.` (this repository root).
    - If `PATCH_MODE=consumer-project`: `FRAMEWORK_DIR={PROJECT_DIR}/.ai/ergo/`.
  - `PROJECT_LOCAL_DIR={PROJECT_DIR}/.ai/project-local/`.
- Interpret placeholders:
  - `<framework>/...` means `${FRAMEWORK_DIR}/...`.
  - `<project-local>/...` means `${PROJECT_LOCAL_DIR}/...`.
- Scope guard:
  - Only change files under `${FRAMEWORK_DIR}` and `${PROJECT_LOCAL_DIR}`.
  - Do not change anything else unless the prompt explicitly expands scope.

### 1) Establish the evidence bundle

Create a short internal “evidence bundle” (notes in your working buffer; do not add extra repo docs unless necessary):

- Copy `MODEL` and `PROMPT` verbatim.
- For `RESULT_COMMIT`:
  - Record which files changed and what was produced.
- For each `FIX_COMMIT`:
  - Record (a) what changed, (b) why (commit message), (c) what constraint it implies.

Produce a table in your notes:

- Fix commit → symptom (diff) → stated reason (message) → implied rule/constraint.

### 2) Extract mistake patterns (cluster fixes)

Cluster fixes into mistake patterns. Use the smallest useful set; typical clusters:

- Missing constraints: a requirement existed but wasn’t applied.
- Ambiguous instruction: framework text allowed multiple interpretations.
- Wrong default: the agent chose a plausible but undesired default.
- Tool misuse / workflow gap: correct action required a tool/script but wasn’t enforced.
- Formatting / repo convention violations: names, paths, templates, style rules.
- Scope creep: model changed things outside requested scope.
- Under-specification: prompt lacked critical acceptance criteria; framework did not force asking/deriving them.

For each cluster, write:
- “If the framework had X, the mistake would likely not happen.”

### 3) Decide where the fix belongs: core vs tech vs project-local

Place guidance where it will be reused, with minimal blast radius.

Use these rules:

- Patch `<framework>/core/` when:
  - the rule is technology-agnostic (process, structure, acceptance criteria discipline),
  - the failure mode can happen in any stack.
- Patch `<framework>/tech/` when:
  - the rule depends on a specific stack/tooling (Kotlin, Spring, Gradle, Detekt, etc.),
  - the fix is a known ecosystem convention or command sequence.
- Patch `<project-local>/` when:
  - the constraint is project-specific (repo layout, domain naming, non-general rules),
  - the fix is not confidently reusable across projects.

Prefer core/tech over project-local only if you can state a general rule without leaking project specifics.

### 4) Map each mistake pattern to a framework lever

Pick the cheapest lever that would have prevented the mistake:

- Agent rule (global) when: the failure mode is broad and severe.
- Skill description (triggering) when: the wrong skill did trigger or the right one didn’t.
- Skill body checklist when: the skill triggered but missed steps.
- Template / scaffold asset when: the model repeatedly miscreates boilerplate.
- Script when: the task is deterministic, fragile, or repeatedly reimplemented.
- Reference doc when: the agent needs long, specific “lookup” material (schemas, conventions).

Do not introduce new docs unless they are directly load-bearing (a skill, a reference, a script, or an asset).

### 5) Implement minimal framework patches

For each patch:

- State the observed mistake pattern in one line (internal note).
- Add the smallest instruction that forces the correct behavior next time:
  - Convert “nice-to-have” into a checklist gate if it was the cause of failure.
  - Add explicit “do not” constraints when scope creep happened.
  - Add decision rules when defaults were wrong (“if A, choose B; else C”).
  - Add required validation commands when the error was catchable locally.

Write instructions so an agent can mechanically follow them:
- Prefer imperative steps.
- Prefer short checklists with “stop conditions”.
- Prefer exact filenames/paths/patterns.
- Add a tiny example only when it disambiguates (keep examples short).

### 6) Add a regression hook (lightweight)

Ensure the same failure becomes detectable in the future:

- Store the prompt and expected constraints as a standalone “regression case” file in a dedicated directory:
  - If project-specific: `<project-local>/regressions/` (create if missing).
  - If general: `<framework>/regressions/` (create if missing).
- Keep regression cases out of framework articles (for example, `<framework>/ergo/tech/...`), unless the prompt explicitly requests adding them there.
- Do not add links from articles to regression cases unless the prompt explicitly asks for it.
- Prefer naming regression case files in `kebab-case.md` with a short domain prefix (e.g. `spring-data-jdbc-...`).

A regression hook must include:
- The prompt fragment that triggered the mistake,
- The rule that must fire,
- The expected observable behavior (“must” statement).
- A concrete pointer to the enforcing mechanism (file path + section name, or script name) in the “Framework hook” section.

Recommended structure for a regression case file:

- Title: one short sentence that names the behavior.
- Sections:
  - “Prompt fragment” (verbatim).
  - “Expected behavior” (a “must” checklist).
  - “Framework hook” (what rule/checklist/skill/script should enforce it).

### 7) Validate and finish

- Run framework validation (where applicable), e.g.:
  - `scripts/quick_validate.py <path/to/skill-folder>` (if present in the framework repo).
- Ensure patches do not bloat context:
  - Keep SKILL.md bodies lean; move detail to `references/` only if it’s truly lookup material.
- Create one minimal commit per distinct mistake cluster (preferably).
- In the commit message, include:
  - the mistake pattern,
  - the framework lever changed.

## Patch patterns (ready-to-copy)

Use these patterns in SKILL.md bodies or agent rules.

### Checklist gate

- “Before producing output, verify: …”
- “If verification fails, stop and fix before continuing.”

### Decision rule for defaults

- “If <condition>, choose <option A>; otherwise choose <option B>.”
- “Do not choose <option C> unless the prompt explicitly requests it.”

### Scope guard

- “Only change files under <path(s)> unless the prompt explicitly expands scope.”
- “Do not reformat unrelated code.”

### Evidence-first requirement

- “Derive constraints from: prompt text + repository conventions + existing files.”
- “If unclear and high-risk, ask one targeted question; otherwise apply repo-local precedent.”

## What “done” looks like

You have produced framework patches such that, if the same prompt is run again with the same model:

- each fix commit’s rationale is covered by an explicit rule/checklist/asset/script,
- the rules are placed in core vs tech vs project-local appropriately,
- the framework change is minimal and generalizable,
- the skill triggering likelihood improves (when relevant),
- there is at least one regression hook that documents the prevented failure mode.
