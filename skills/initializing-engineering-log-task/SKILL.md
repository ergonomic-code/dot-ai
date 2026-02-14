---
name: initializing-engineering-log-task
description: Initialization of a solution design directory in the engineering-log based on a template, including file creation, copying 04-execution-spec.md, and writing the original problem statement to 01-problem-statement.md.
---

# engineering-log task init

## Purpose

* Create a task directory at `engineering-log/<yy>/<MM>/<NN>-<slug>`.
* Create files and directories according to the defined structure.
* Write the input problem statement to `01-problem-statement.md`.
* Copy the embedded template `./assets/04-execution-spec.md` to `04-execution-spec.md`.

## Input

* Informal problem statement in free form.
* Optional: `--slug`, if directory naming needs to be controlled.

## Output

* Created task directory in `engineering-log/<yy>/<MM>/`.
* The script prints the relative path of the created directory.
* Created files:

  * `chats/02-problem-formalization-chat-1.md`
  * `chats/02-solution-exploration-chat-1.md`
  * `chats/03-solution-specification-chat-1.md`
  * `chats/04-solution-implementation-chat-1.md`
  * `01-problem-statement.md`
  * `01-problem-statement-formal.md`
  * `02-solution-options.md`
  * `03-solution-hld.md`
  * `04-execution-spec.md`

## Algorithm

1. Run from the repository root.
2. Pass the problem statement to the script via stdin.
3. Attempt to generate a `slug` based on the problem statement.
   The proposed `slug` must be in English (not transliterated) and no longer than 60 characters.
4. Present the proposed `slug` to the user.
5. Obtain approval or a corrected `slug`.
6. Determine the next number `NN` within the month by scanning directories in `engineering-log/<yy>/<MM>/`.
7. Create the directory and files without overwriting existing ones.

## Commands

### Propose slug (without creating files)

```bash
cat <<'EOF' | python3 ./scripts/init_task_dir.py --dry-run
<paste problem statement here>
EOF
```

### Create after slug approval

```bash
cat <<'EOF' | python3 ./scripts/init_task_dir.py --slug <approved-slug>
<paste problem statement here>
EOF
```

### Create task for a specific date (for yy/MM) after slug approval

```bash
cat <<'EOF' | python3 ./scripts/init_task_dir.py --date 2026-02-07 --slug <approved-slug>
<paste problem statement here>
EOF
```

### Create without slug approval (not recommended)

```bash
cat <<'EOF' | python3 ./scripts/init_task_dir.py --yes
<paste problem statement here>
EOF
```
