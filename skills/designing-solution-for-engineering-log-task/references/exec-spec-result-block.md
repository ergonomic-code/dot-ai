# RESULT FOR EXECUTION-SPEC block format

Use **exactly** this markdown block format (do not rename fields):

=== RESULT FOR EXECUTION-SPEC ===

Task: (required problem statement in 1–3 sentences)
  - <...>
  - <...>
Chosen approach: (brief, structured description of the chosen solution)
  - <...>
  - <...>
Acceptance test changes: (how acceptance tests must change after this work)
  - Baseline: describe changes as diffs relative to the existing acceptance tests (not as a greenfield rewrite).
  - Added:
    - <...>
  - Changed:
    - <existing case name> — <what changes> — link: <code link/path>
  - Removed:
    - <existing case name> — <why remove> — link: <code link/path>
Key invariants:
  - <...>
  - <...>
  - Illegal states and enforcement: <...> (see `../../../concepts/making-illegal-states-unrepresentable.md`)
Hard constraints:
  - <...>
  - <...>
  - Sources of truth and contract mapping: <...> (see `../../../conventions/contracts.md`)
Responsibility boundaries:
  - <...>
  - <...>
