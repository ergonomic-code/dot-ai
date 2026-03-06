---
name: improving-framework-from-feedback
description: "Improve an AI agent framework from git evidence (result commit + fix-up commits); produce targeted patches to the correct framework artifacts and/or <project-local>/ so a rerun with the same prompt/model no longer needs manual fixes."
---

# Improving framework from git feedback

Turn “model output → human fixes” into minimal, generalizable framework changes.

Operate on evidence, not memory.
Prefer small patches that prevent the same class of error.

## Inputs

- `PATCH_MODE` — where to apply patches.
  - `framework-repo`: patch the framework checkout you are currently editing and/or `<project-local>/` resolved inside `PROJECT_DIR`.
  - `consumer-project`: patch the framework checkout resolved inside `PROJECT_DIR` and/or `<project-local>/` resolved inside `PROJECT_DIR`.
- `PROJECT_DIR` — path to the evidence repository whose git history contains:
  - `RESULT_COMMIT`,
  - `FIX_COMMITS[]`,
  - and, when relevant, a framework checkout plus a project-local overlay.
- `MODEL` — model identifier used to produce the result (store verbatim).
- `PROMPT` — exact prompt text used (store verbatim).
- `RESULT_COMMIT` — git commit SHA with the model-produced result (the “before fixes” state).
- `FIX_COMMITS[]` — one or more commit SHAs that correct the result; commit messages include rationale and/or constraints.
- Optional: `FINAL_COMMIT` — the “after fixes” commit to diff against (default: `HEAD`).

## Output

- A set of patches to framework artifacts under `<framework>/...` and/or `<project-local>/...`.
- Place general knowledge in `<framework>/ergo/core/` or `<framework>/ergo/tech/` when those are the real enforcing layers.
- Patch the actual enforcing artifact when the lever is a role, skill, process, template, convention, concept, regression, script, or asset under `<framework>/...`.
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

### 0) Resolve the evidence repo, framework root, and project-local root

Treat `PROJECT_DIR` as the evidence repository for git inspection.

- Decide `PATCH_MODE`.
  - If `PATCH_MODE` is provided, use it.
  - Otherwise resolve `PROJECT_FRAMEWORK_DIR` from `PROJECT_DIR` using the canonical framework-root discovery rules.
  - Also resolve `CURRENT_FRAMEWORK_DIR` as the framework checkout you are currently editing, if one exists.
  - If `PROJECT_FRAMEWORK_DIR` is not found, use `framework-repo`.
  - If both roots are found and resolve to the same filesystem path, use `framework-repo`.
  - If both roots are found and resolve to different filesystem paths, stop and ask which checkout to patch instead of guessing.
  - Otherwise use `consumer-project`.
- Resolve `FRAMEWORK_DIR` using the canonical framework-root discovery rules from `AGENTS.md` and `bootstrap/AGENTS.md`.
  - If `PATCH_MODE=framework-repo`, resolve the framework checkout you are currently editing.
  - If `PATCH_MODE=consumer-project`, use the already-resolved framework checkout inside `PROJECT_DIR`.
- Resolve `PROJECT_LOCAL_DIR` by interpreting `<project-local>/...` via the canonical rules from `AGENTS.md` and `bootstrap/AGENTS.md`.
- Interpret placeholders:
  - `<framework>/...` means paths under the resolved `FRAMEWORK_DIR`.
  - `<project-local>/...` means paths under the resolved `PROJECT_LOCAL_DIR`.
- In framework materials, keep project-local references written as `<project-local>/...`.
- Use resolved filesystem paths only for execution notes and terminal commands.
- Scope guard:
  - Only change files under the resolved `${FRAMEWORK_DIR}` and `${PROJECT_LOCAL_DIR}` roots.
  - Do not change anything else unless the prompt explicitly expands scope.

### 1) Establish the evidence bundle

Create a short internal “evidence bundle” (notes in your working buffer; do not add extra repo docs unless necessary):

- Copy `MODEL` and `PROMPT` verbatim.
- For `RESULT_COMMIT`:
  - Record which files changed and what was produced.
- For each `FIX_COMMIT`:
  - Record (a) what changed, (b) why (commit message), (c) what constraint it implies.

Also analyze the most recent framework history to detect recurring failure modes:

- Review the last 10 commits in `FRAMEWORK_DIR` (for example, `git -C "${FRAMEWORK_DIR}" log --oneline -n 10`).
- Infer which agent mistakes those commits were correcting (from diffs + commit messages).
- Compare those mistake patterns against your current chat behavior.
- If you find a match (you are repeating a previously-fixed mistake), stop and reconsider prevention:
  - Think through why the prior prevention did not hold in this chat.
  - Try a different prevention mechanism (a different framework lever), not just “be more careful”.

Produce a table in your notes:

- Fix commit → symptom (diff) → stated reason (message) → implied rule/constraint.

### 2) Extract mistake patterns (cluster fixes)

Cluster fixes into mistake patterns.
Use the smallest useful set; typical clusters:

- Missing constraints: a requirement existed but wasn’t applied.
- Ambiguous instruction: framework text allowed multiple interpretations.
- Wrong default: the agent chose a plausible but undesired default.
- Tool misuse / workflow gap: correct action required a tool/script but wasn’t enforced.
- Formatting / repo convention violations: names, paths, templates, style rules.
- Scope creep: model changed things outside requested scope.
- Under-specification: prompt lacked critical acceptance criteria; framework did not force asking/deriving them.

For each cluster, write:
- “If the framework had X, the mistake would likely not happen.”

### 3) Decide where the fix belongs: framework layer vs project-local

Place guidance where it will be reused, with minimal blast radius.

Use these rules:

- Patch `<framework>/ergo/core/` when:
  - the rule is technology-agnostic (process, structure, acceptance criteria discipline),
  - the failure mode can happen in any stack.
- Patch `<framework>/ergo/tech/` when:
  - the rule depends on a specific stack/tooling (Kotlin, Spring, Gradle, Detekt, etc.),
  - the fix is a known ecosystem convention or command sequence.
- Patch another framework artifact under `<framework>/...` when:
  - the enforcing mechanism is itself a role, skill, process, template, convention, concept, regression, script, or asset,
  - placing the rule in `ergo/core|tech` would hide the real lever or duplicate knowledge.
- Patch `<project-local>/` when:
  - the constraint is project-specific (repo layout, domain naming, non-general rules),
  - the fix is not confidently reusable across projects.

Prefer framework artifacts over `<project-local>/` only if you can state a general rule without leaking project specifics.
Do not force every framework change into `ergo/core|tech`.
Patch the real enforcing lever instead.

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
- In persisted framework docs, keep framework links relative and keep project-local links written as `<project-local>/...`.
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
- the rules are placed in the correct framework artifact or in `<project-local>/` as appropriate,
- the framework change is minimal and generalizable,
- the skill triggering likelihood improves (when relevant),
- there is at least one regression hook that documents the prevented failure mode.
