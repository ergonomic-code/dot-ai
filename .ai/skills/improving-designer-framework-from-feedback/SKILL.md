---
name: improving-designer-framework-from-feedback
description: "Improve the AI framework from design-stage evidence: analyze exported chat artifacts plus design documents such as the formal task statement, HLD, and execution spec; then patch the correct framework artifacts and/or <project-local>/ so similar future design chats require fewer clarifications, less rewriting, and produce more executable specs."
---

# Improving framework from design feedback

Turn “design chat → accepted design artifacts → friction and rewrites” into minimal, generalizable framework changes.

Operate on evidence, not memory.
Prefer small patches that prevent the same class of design failure.

## When to use

Use when the problematic loop happened in design work rather than coding.
Use when the main evidence is in chats and design artifacts, not in fix-up commits.
Use when the model eventually produced acceptable design artifacts, but only after avoidable clarification, backtracking, or manual rewriting.

Typical cases:

- weak or late clarification;
- requirements were restated but not made testable;
- solution options were skipped when they were needed;
- HLD mixed architecture with implementation detail;
- the wrong source of truth was assumed;
- DTO or domain invariants were left implicit;
- execution spec remained ambiguous or non-executable;
- artifact boundaries between formal statement, HLD, and execution spec were violated.

## Do not use

Do not use when the main evidence is a model-produced code commit plus human fix-up commits.
For that case, use the coder feedback improvement skill.

## Inputs

- `PATCH_MODE` — execution target override.
  - `framework-repo`:
    - patch the framework checkout currently being edited and/or `<project-local>/` resolved inside `PROJECT_DIR`;
  - `consumer-project`:
    - patch the framework checkout resolved inside `PROJECT_DIR` and/or `<project-local>/` resolved inside `PROJECT_DIR`.
- `PROJECT_DIR` — path to the evidence repository that contains:
  - the exported evidence package,
  - the relevant design artifacts,
  - and, when relevant, a framework checkout plus a project-local overlay.
- `EXPORT_DIR` — path to the exported evidence package containing:
  - `transcript.md`,
  - `brief.md`.
  If `transcript.md` contains `### Guidance files considered`, use that section as evidence about guidance selection and omission.
- `ARTIFACT_PATHS[]` — one or more load-bearing design artifacts.
  Typical examples:
  - task statement,
  - formal task statement,
  - solution options,
  - HLD,
  - execution spec,
  - accepted rewritten version,
  - adjacent prompts/templates/checklists.
- Optional: `FINAL_ACCEPTED_ARTIFACTS[]` — explicit paths to the final accepted versions when they differ from the artifacts discussed in the chat.
- Optional: `MODEL` — model identifier used in the design chat.
- Optional: `PROMPT` — exact prompt text used for the design stage when it is available verbatim.

## Output

- A set of patches to framework artifacts under `<framework>/...` and/or `<project-local>/...`.
- Place general knowledge in `<framework>/ergo/core/` or `<framework>/ergo/tech/` only when those are the real enforcing layers.
- Patch the actual enforcing artifact when the lever is a role, skill, process, template, convention, concept, regression, script, or asset under `<framework>/...`.
- Each patch must be explicitly linked to:
  - the design failure pattern observed,
  - the evidence that demonstrates it,
  - the exact framework lever you changed.

## Design evidence to inspect

Treat the evidence as a chain, not as isolated files.

Inspect, when available:

- `transcript.md`;
- `brief.md`;
- original task statement;
- formalized requirements;
- solution options;
- HLD;
- execution spec;
- accepted rewritten artifacts;
- related prompts, templates, checklists, conventions, and concepts that were supposed to guide the stage.

When several artifact versions exist, compare draft vs accepted version.
Focus on the delta that required human clarification or rewriting.

## Quick start inspection checklist

Read in this order:

1. `brief.md`
2. `transcript.md`
3. the earliest input artifact
4. the final accepted artifact for the same stage
5. adjacent upstream/downstream artifacts that expose where the stage leaked or under-specified

Build a compact evidence bundle in your working notes.
Do not create extra repo documents unless needed for the final patch or regression hook.

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

Capture:

- the task goal from `brief.md`;
- the main friction points from `brief.md`;
- the key clarification turns from `transcript.md`;
- guidance-file evidence from `transcript.md` when `### Guidance files considered` is present;
- the artifact chain:
  - input artifact,
  - intermediate artifact,
  - accepted artifact;
- if available, `MODEL` and `PROMPT` verbatim.

For each load-bearing artifact, record:

- what stage it belongs to;
- what it was supposed to do;
- what was missing, ambiguous, or wrong;
- what the accepted version added, removed, or clarified.

For each guidance-file evidence entry, record:

- whether the file was `read` or `discovered_not_read`;
- whether it should have influenced role selection, source-of-truth choice, scope boundaries, or stage behavior;
- whether the stated `reason` reveals a missing rule, a bad priority rule, or a missing stop condition.
Use this section only as evidence about the files explicitly listed there.
Do not treat it as proof of hidden instructions or of files that never became visibly discoverable in the transcript or repository context.

Also analyze the most recent framework history to detect recurring failure modes:

- review the last 10 commits in `FRAMEWORK_DIR`;
- infer which design-agent mistakes those commits were correcting;
- compare those mistake patterns against the current case;
- if you find a match, stop and reconsider prevention:
  - think through why the prior prevention did not hold;
  - try a different prevention mechanism, not just “be more careful”.

Produce a compact notes table:

- evidence item → observed friction → accepted correction → implied rule.

### 2) Extract design failure patterns

Cluster the evidence into the smallest useful set of design failure patterns.

Typical clusters:

- missing clarification:
  - the stage proceeded before scope, actors, permissions, or edge cases were fixed;
- wrong stage behavior:
  - a stage produced output that belonged to another stage;
- ambiguous source of truth:
  - the design did not explicitly decide where truth lives;
- non-testable requirements:
  - acceptance criteria were not black-box verifiable;
- skipped alternative analysis:
  - the model converged too early when multiple options mattered;
- weak option comparison:
  - options existed but tradeoffs or criteria were missing;
- HLD not execution-oriented:
  - the HLD did not prepare a stable handoff for the execution spec;
- execution spec not literal enough:
  - the executor would still need to guess;
- hidden illegal states:
  - DTO or domain invariants stayed implicit instead of being made explicit in the design;
- missing compatibility or contract thinking:
  - external API, DB, or event compatibility constraints were omitted;
- framework rule not enforced:
  - the right convention, concept, or checklist existed but the stage did not force it.
- wrong guidance selection:
  - the assistant read the wrong guiding artifact or skipped the right one during the design stage;
- guidance-priority ambiguity:
  - multiple visible guidance files existed, but precedence between them was not explicit enough;
- guidance read without stage enforcement:
  - the right guidance was read, but no hard gate forced the stage to apply it.

For each cluster, write:

- “If the framework had X, this design failure would likely not happen.”

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
  - the repository layout is project-specific,
  - the vocabulary or artifacts are not confidently reusable across projects.

Prefer patching the actual enforcing lever over adding a generic article.

### 4) Map each failure pattern to a framework lever

Pick the cheapest lever that would have prevented the failure.

Typical designer-side levers:

- agent role rule:
  - when the failure mode is broad and severe;
- skill description:
  - when the wrong skill triggered or the right one did not;
- skill body checklist:
  - when the stage triggered but skipped required reasoning or stop conditions;
- prompt/reference file:
  - when the stage prompt needs stronger sequencing or harder stop points;
- template:
  - when the output shape itself fails to force completeness;
- convention/concept:
  - when the stage needs a stable reusable rule such as source-of-truth selection, contract discipline, or illegal-state handling;
- script:
  - when validation is deterministic and repeatedly forgotten;
- regression case:
  - when the failure is recurring or caused by a risky default.

When `### Guidance files considered` exists, treat it as first-class evidence for choosing the lever.
If the failure came from wrong file selection, wrong precedence, or unjustified omission, prefer patching the role, skill, or convention that governs source-of-truth and stage sequencing.
Do not infer invisible governing artifacts from this section alone.

Do not introduce new docs unless they are directly load-bearing.

### 5) Implement minimal framework patches

For each patch:

- state the observed design failure pattern in one line in your working notes;
- add the smallest instruction that forces the correct behavior next time;
- prefer imperative steps;
- prefer explicit stop conditions;
- prefer exact file names and artifact paths;
- prefer “must / must not” wording for gates;
- add a tiny example only when it truly disambiguates.

Common patch shapes:

- require a stage to ask clarifying questions before proceeding;
- make a decision explicit:
  - source of truth,
  - scope boundary,
  - actor/permission matrix,
  - compatibility policy,
  - acceptance-test source;
- force separation between artifacts:
  - requirements,
  - HLD,
  - execution spec,
  - implementation;
- strengthen a handoff block or result block;
- require explicit mention of invariants or illegal states;
- require explicit testability or black-box acceptance criteria;
- require explicit comparison of alternatives when multiple options are plausible.

### 6) Add a regression hook

Ensure the same design failure becomes detectable in the future.

Store the regression case as a standalone file:

- if project-specific:
  - `<project-local>/regressions/...`;
- if general:
  - `<framework>/regressions/...`.

Do not bury regression cases inside framework articles unless the prompt explicitly asks for it.

Prefer `kebab-case.md` with a short domain prefix.

A regression hook must include:

- title:
  - one short sentence naming the expected behavior;
- `Prompt fragment`:
  - the load-bearing part of the user request or design task;
- `Evidence of failure`:
  - the concrete observed misbehavior;
- `Expected behavior`:
  - a “must” checklist;
- `Framework hook`:
  - exact enforcing mechanism:
    - file path plus section,
    - or script name.

### 7) Validate and finish

- run framework validation when applicable;
- ensure the patch does not bloat context;
- prefer one minimal commit per distinct failure cluster;
- in the commit message, include:
  - the design failure pattern,
  - the framework lever changed.

## Quality criteria

- every patch is tied to concrete evidence from chat or artifacts;
- guidance-file evidence from exported chat artifacts is used when available to separate “wrong guidance chosen” from “right guidance present but not enforced”;
- the patch changes the real enforcing lever;
- the patch is reusable beyond the single incident unless clearly project-local;
- the patch reduces future clarification or rewriting;
- artifact-boundary rules become clearer, not heavier;
- no new framework text is added without an enforcement reason;
- the resulting rule is executable and verifiable.

## Interop

Use `exporting-chat-artifacts` first when evidence is still only in the chat.
Use this skill after evidence exists.

Typical upstream inputs:

- requirements formalization;
- solution design;
- execution spec generation.
- `### Guidance files considered` in `transcript.md`, when present.

Typical downstream effects:

- better role rules;
- sharper stage prompts;
- stronger templates;
- new regression cases;
- more explicit conventions and concepts.
