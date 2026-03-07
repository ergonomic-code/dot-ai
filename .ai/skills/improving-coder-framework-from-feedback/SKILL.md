---
name: improving-coder-framework-from-feedback
description: "Improve an AI agent framework from implementation evidence: analyze the model-produced result commit, human fix-up commits, and optional implementation chat evidence; then patch the correct framework artifacts and/or <project-local>/ so a rerun with the same prompt/model no longer needs the same manual fixes."
---

# Improving framework from implementation feedback

Turn “model output → human fixes” into minimal, generalizable framework changes.

Operate on evidence, not memory.
Prefer small patches that prevent the same class of implementation error.

## When to use

Use when the main evidence is in git history.
Use when the model produced code, tests, migrations, configs, or repo changes that later required manual fix-up commits.
Use when you want framework changes that reduce the need for similar future fixes with the same or similar prompts.

## Do not use

Do not use when the main problem happened during requirements or design work and the evidence is mostly chat plus design artifacts.
For that case, use the designer feedback improvement skill.

## Inputs

- `PATCH_MODE` — execution target override.
  - `framework-repo`:
    - patch the framework checkout currently being edited and/or `<project-local>/` resolved inside `PROJECT_DIR`;
  - `consumer-project`:
    - patch the framework checkout resolved inside `PROJECT_DIR` and/or `<project-local>/` resolved inside `PROJECT_DIR`.
- `PROJECT_DIR` — path to the evidence repository whose git history contains:
  - `RESULT_COMMIT`,
  - `FIX_COMMITS[]`,
  - and, when relevant, a framework checkout plus a project-local overlay.
- `MODEL` — model identifier used to produce the result.
  Store verbatim.
- `PROMPT` — exact prompt text used.
  Store verbatim.
- `RESULT_COMMIT` — git commit SHA with the model-produced result.
  This is the “before fixes” state.
- `FIX_COMMITS[]` — one or more commit SHAs that correct the result.
  Commit messages should contain rationale and/or constraints when available.
- Optional: `FINAL_COMMIT` — the “after fixes” commit to diff against.
  Default: `HEAD`.
- Optional: `EXPORT_DIR` — path to exported implementation chat evidence containing:
  - `transcript.md`,
  - `brief.md`.
  Use it when the rationale is not fully visible in git history.
  If `transcript.md` contains `### Guidance files considered`, use that section as evidence about guidance selection and omission.

## Output

- A set of patches to framework artifacts under `<framework>/...` and/or `<project-local>/...`.
- Place general knowledge in `<framework>/ergo/core/` or `<framework>/ergo/tech/` only when those are the real enforcing layers.
- Patch the actual enforcing artifact when the lever is a role, skill, process, template, convention, concept, regression, script, or asset under `<framework>/...`.
- Each patch must be explicitly linked to:
  - the mistake pattern observed from diffs,
  - the fix rationale from commit messages and optional chat evidence,
  - the exact framework lever you changed.

## Quick start commands

Run these in `PROJECT_DIR`:

- inspect the model result:
  - `git show --stat RESULT_COMMIT`
  - `git show RESULT_COMMIT`
- inspect all fixes:
  - `git show --stat <fix1> <fix2> ...`
  - `git show <fix1> <fix2> ...`
- see the net effect from result to final:
  - `git diff RESULT_COMMIT..HEAD`
  - if final is known:
    - `git diff RESULT_COMMIT..<FINAL_COMMIT>`
- compare the fix series structure:
  - `git range-diff RESULT_COMMIT^..RESULT_COMMIT RESULT_COMMIT..FINAL_COMMIT`
  - or use `HEAD` when `FINAL_COMMIT` is omitted

## Workflow

### 0) Resolve patch target and writable roots

Treat `PROJECT_DIR` as the evidence repository.

Resolve `PATCH_MODE`, `FRAMEWORK_DIR`, `PROJECT_LOCAL_DIR`, placeholder interpretation, writable-scope policy, and ambiguity handling using the canonical rules in `../../conventions/framework-patch-target-resolution.md`.

In this skill:

- `<framework>/...` means paths under the resolved `FRAMEWORK_DIR`;
- `<project-local>/...` means paths under the resolved `PROJECT_LOCAL_DIR`;
- only files under those resolved writable roots may be changed unless the prompt explicitly expands scope.

### 1) Establish the evidence bundle

Create a short internal evidence bundle.

Copy `MODEL` and `PROMPT` verbatim.
For `RESULT_COMMIT`, record:

- which files changed;
- what was produced;
- what acceptance criteria or constraints were apparently missed.

For each `FIX_COMMIT`, record:

- what changed;
- why it changed:
  - from the commit message,
  - from the diff,
  - from optional implementation transcript evidence;
- what rule or constraint it implies.

If `EXPORT_DIR` is provided, also read:

- `brief.md`;
- `transcript.md`.

Use them only to clarify rationale that is not visible in git evidence.
Do not let chat evidence override the actual diff.
If `transcript.md` contains `### Guidance files considered`, extract:

- which guidance artifacts were actually read;
- which were discovered but not read;
- the stated `reason` and `source_of_awareness` for each entry;
- whether the failure was caused by wrong guidance selection, wrong prioritization, or a missing enforcement step after the right guidance was read.
Use this section only as evidence about the files explicitly listed there.
Do not treat it as proof of hidden instructions or of files that never became visibly discoverable in the transcript or repository context.

Also analyze the most recent framework history to detect recurring failure modes:

- review the last 10 commits in `FRAMEWORK_DIR`;
- infer which agent mistakes those commits were correcting from diffs and commit messages;
- compare those mistake patterns against the current case;
- if you find a match, stop and reconsider prevention:
  - think through why the prior prevention did not hold in this run;
  - try a different prevention mechanism, not just “be more careful”.

Produce a compact notes table:

- fix commit → symptom in diff → stated reason → implied rule or constraint.

### 2) Extract mistake patterns

Cluster fixes into the smallest useful set of implementation mistake patterns.

Typical clusters:

- missing constraints:
  - a requirement existed but was not applied;
- ambiguous instruction:
  - framework text allowed multiple interpretations;
- wrong default:
  - the agent chose a plausible but undesired default;
- tool misuse or workflow gap:
  - the correct action required a tool or script but was not enforced;
- formatting or repo-convention violations:
  - names, paths, templates, style rules, artifact placement;
- scope creep:
  - the model changed things outside requested scope;
- under-specification:
  - the prompt lacked critical acceptance criteria and the framework did not force deriving or asking for them;
- incomplete validation:
  - the error was catchable locally by tests, linters, build, or diff inspection, but those checks were not required;
- unsafe refactor:
  - behavior changed beyond the requested scope;
- weak backward-compatibility handling:
  - public contracts were changed without approval;
- missing tests:
  - required acceptance tests or regression tests were not added or updated.
- wrong guidance selection:
  - the assistant read the wrong governing artifact or skipped the right one;
- guidance-priority ambiguity:
  - multiple visible guidance files existed, but their read order or precedence was not enforced clearly enough;
- guidance read without execution:
  - the right guidance was read, but the workflow had no hard gate that forced using it.

For each cluster, write:

- “If the framework had X, the mistake would likely not happen.”

### 3) Decide where the fix belongs

Place guidance where it will be reused, with minimal blast radius.

Use these rules:

- patch `<framework>/ergo/core/` when:
  - the rule is technology-agnostic,
  - the failure mode can happen in any stack;
- patch `<framework>/ergo/tech/` when:
  - the rule depends on a specific stack or toolchain;
- patch another framework artifact under `<framework>/...` when:
  - the enforcing mechanism is itself a role, skill, process, template, convention, concept, regression, script, or asset;
- patch `<project-local>/` when:
  - the constraint is project-specific,
  - the repository layout or naming is local,
  - the rule is not confidently reusable across projects.

Prefer framework artifacts over `<project-local>/` only if you can state a general rule without leaking project specifics.
Patch the real enforcing lever instead of writing a broad article.

### 4) Map each mistake pattern to a framework lever

Pick the cheapest lever that would have prevented the mistake.

Typical coder-side levers:

- agent rule:
  - when the failure mode is broad and severe;
- skill description:
  - when the wrong skill triggered or the right one did not;
- skill body checklist:
  - when the skill triggered but skipped critical steps;
- template or scaffold asset:
  - when boilerplate is repeatedly created incorrectly;
- script:
  - when the task is deterministic, fragile, or repeatedly reimplemented by hand;
- tech convention:
  - when the error is ecosystem-specific and stable;
- regression case:
  - when the failure is recurring or caused by a risky default.

When `### Guidance files considered` exists, treat it as first-class evidence for choosing the lever.
If the observed problem is wrong file selection or wrong precedence, prefer patching the artifact that defines read order, scope boundaries, or skill-trigger rules over adding another general reminder elsewhere.
Do not infer invisible governing artifacts from this section alone.

Do not introduce new docs unless they are directly load-bearing.

### 5) Implement minimal framework patches

For each patch:

- state the observed mistake pattern in one line in your working notes;
- add the smallest instruction that forces the correct behavior next time;
- convert “nice-to-have” into a checklist gate if it was the cause of failure;
- add explicit “do not” constraints when scope creep happened;
- add decision rules when defaults were wrong:
  - “if A, choose B; else C”;
- add required validation commands when the error was catchable locally;
- prefer imperative steps;
- prefer short checklists with stop conditions;
- prefer exact filenames, paths, and command patterns;
- add a tiny example only when it truly disambiguates.

### 6) Add a regression hook

Ensure the same implementation failure becomes detectable in the future.

Store the regression case as a standalone file:

- if project-specific:
  - `<project-local>/regressions/...`;
- if general:
  - `<framework>/regressions/...`.

Keep regression cases out of framework articles unless the prompt explicitly requests otherwise.

Prefer `kebab-case.md` with a short domain prefix.

A regression hook must include:

- title:
  - one short sentence that names the behavior;
- `Prompt fragment`:
  - the load-bearing part of the original implementation prompt;
- `Expected behavior`:
  - a “must” checklist;
- `Framework hook`:
  - exact enforcing mechanism:
    - file path plus section,
    - or script name.

Optional but recommended:

- `Observed failure`:
  - short summary tied to the fix commit series.

### 7) Validate and finish

- run framework validation when applicable;
- ensure patches do not bloat context;
- keep `SKILL.md` bodies lean;
- move long lookup detail to `references/` only when it is truly lookup material;
- prefer one minimal commit per distinct mistake cluster;
- in the commit message, include:
  - the mistake pattern,
  - the framework lever changed.

## Quality criteria

- every patch is grounded in git evidence;
- chat evidence is used only as supporting rationale, not as a substitute for diff analysis;
- guidance-file evidence from exported chat artifacts is used when available to distinguish “wrong rule” from “right rule, not enforced”;
- the patch changes the real enforcing lever;
- the same class of future fix becomes less likely;
- the patch is reusable beyond the single incident unless clearly project-local;
- the patch does not widen scope or add theory without enforcement value;
- the resulting rule is executable and verifiable.

## Interop

Use `exporting-chat-artifacts` first when implementation chat context explains why the fix commits happened.
Otherwise git evidence is sufficient.

Typical upstream evidence:

- result commit;
- fix commits;
- final diff;
- implementation transcript and brief.
- `### Guidance files considered` in `transcript.md`, when present.

Typical downstream changes:

- stronger coding-skill checklists;
- sharper tech conventions;
- required validation commands;
- better prompts and templates;
- new regression cases.
