#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Section:
    header: str
    body: str


BAD_MARKERS_MINIMAL = [
    r"^# AGENTS\.md instructions",
    r"^<INSTRUCTIONS>",
    r"^<permissions instructions>",
    r"^<environment_context>",
    r"^# Context from my IDE setup:",
    r"^## My request for Codex:",
    r"^## Open tabs:",
    r"^## Active file:",
    r"^## Active selection of the file:",
    r"^developer message",
    r"^system prompt",
]

BAD_MARKERS_VERBOSE = [
    r"^<permissions instructions>",
    r"^developer message",
    r"^system prompt",
]

BAD_RE_MINIMAL = re.compile("|".join(f"(?:{p})" for p in BAD_MARKERS_MINIMAL), flags=re.MULTILINE)
BAD_RE_VERBOSE = re.compile("|".join(f"(?:{p})" for p in BAD_MARKERS_VERBOSE), flags=re.MULTILINE)

AGENTS_BLOCK_RE = re.compile(r"(?s)^# AGENTS\.md instructions.*?</INSTRUCTIONS>\s*", re.MULTILINE)
PERMISSIONS_BLOCK_RE = re.compile(r"(?s)<permissions instructions>.*?</permissions instructions>\s*", re.MULTILINE)
ENV_BLOCK_RE = re.compile(r"(?s)<environment_context>.*?</environment_context>\s*", re.MULTILINE)

IDE_CONTEXT_SPLIT_RE = re.compile(r"(?m)^# Context from my IDE setup:\s*$")
ACTIVE_SELECTION_BLOCK_RE = re.compile(
    r"(?ms)^## Active selection of the file:\s*\n.*?(?=^## |\Z)"
)
OPEN_TABS_BLOCK_RE = re.compile(r"(?m)^## Open tabs:\s*$\n(?:^[ \t]*- [^\n]*\n)*")


def render_environment_context(block: str) -> str:
    cwd = None
    shell = None

    m = re.search(r"(?s)<cwd>\s*(.*?)\s*</cwd>", block)
    if m:
        cwd = m.group(1).strip()

    m = re.search(r"(?s)<shell>\s*(.*?)\s*</shell>", block)
    if m:
        shell = m.group(1).strip()

    if not cwd and not shell:
        return ""

    out: list[str] = ["Context (environment):"]
    if cwd:
        out.append(f"- cwd: `{cwd}`")
    if shell:
        out.append(f"- shell: `{shell}`")
    return "\n".join(out)


def replace_environment_context(text: str, *, mode: str) -> str:
    if mode == "minimal":
        return ENV_BLOCK_RE.sub("", text)

    def repl(m: re.Match[str]) -> str:
        rendered = render_environment_context(m.group(0))
        if not rendered:
            return ""
        return f"{rendered}\n"

    return ENV_BLOCK_RE.sub(repl, text)


def render_ide_context(*, chunk: str) -> str:
    active_file = None
    open_tabs: list[str] = []

    m = re.search(r"(?m)^## Active file:\s*(.*?)\s*$", chunk)
    if m:
        active_file = m.group(1).strip()

    m = re.search(r"(?m)^## Open tabs:\s*$", chunk)
    if m:
        after = chunk[m.end() :].splitlines()
        for line in after:
            if line.startswith("## "):
                break
            if line.startswith("- "):
                open_tabs.append(line[2:].strip())

    ctx_lines: list[str] = []
    if active_file:
        ctx_lines.append(f"- Active file: `{active_file}`")
    if open_tabs:
        ctx_lines.append("- Open tabs:")
        ctx_lines.extend(f"  - {tab}" for tab in open_tabs)

    if not ctx_lines:
        return ""

    out = ["Context (IDE):", *ctx_lines]
    return "\n".join(out).strip()


def extract_environment_context(text: str) -> tuple[str, str]:
    rendered_blocks: list[str] = []

    def repl(m: re.Match[str]) -> str:
        rendered = render_environment_context(m.group(0)).strip()
        if rendered:
            rendered_blocks.append(rendered)
        return ""

    cleaned = ENV_BLOCK_RE.sub(repl, text)
    return cleaned, "\n\n".join(rendered_blocks).strip()


def strip_ide_noise(text: str, *, mode: str) -> str:
    text = ACTIVE_SELECTION_BLOCK_RE.sub("", text)
    if mode != "minimal":
        return text

    text = OPEN_TABS_BLOCK_RE.sub("", text)
    text = re.sub(r"(?m)^# Context from my IDE setup:\s*$\n?", "", text)
    text = re.sub(r"(?m)^## Active file:.*\n?", "", text)
    text = re.sub(r"(?m)^## My request for Codex:\s*$\n?", "", text)
    return text


def clean_user_body(body: str, *, mode: str) -> str:
    text = body.strip("\n")
    if not text.strip():
        return ""

    text = PERMISSIONS_BLOCK_RE.sub("", text)
    text = AGENTS_BLOCK_RE.sub("", text)
    text = ACTIVE_SELECTION_BLOCK_RE.sub("", text)

    # If the message contains IDE context blocks, keep only the actual request parts.
    if "# Context from my IDE setup:" in text and "## My request for Codex:" in text:
        chunks = IDE_CONTEXT_SPLIT_RE.split(text)
        extracted: list[str] = []
        for chunk in chunks:
            if "## My request for Codex:" not in chunk:
                continue
            chunk_without_env, env_ctx = extract_environment_context(chunk)
            prefix, after = chunk_without_env.split("## My request for Codex:", 1)
            request = after.strip()
            if not request.strip():
                continue
            if mode == "minimal":
                extracted.append(request)
            else:
                parts: list[str] = []
                ide_ctx = render_ide_context(chunk=prefix)
                if ide_ctx:
                    parts.append(ide_ctx)
                if env_ctx:
                    parts.append(env_ctx)
                parts.append(f"Request:\n{request.strip()}")
                extracted.append("\n\n".join(parts).strip())
        return "\n\n".join(extracted).strip()

    text = strip_ide_noise(text, mode=mode)
    text = replace_environment_context(text, mode=mode)

    # Otherwise, drop any remaining harness-ish headings that may have slipped through.
    bad_re = BAD_RE_MINIMAL if mode == "minimal" else BAD_RE_VERBOSE
    lines = [line for line in text.splitlines() if not bad_re.match(line)]
    return "\n".join(lines).strip()


def split_sections(text: str) -> tuple[str, list[Section]]:
    m = re.search(r"(?m)^(## (?:User|Assistant))\s*$", text)
    if not m:
        return text.rstrip() + "\n", []

    prefix = text[: m.start()].rstrip() + "\n"
    rest = text[m.start() :]

    parts = re.split(r"(?m)^(## (?:User|Assistant))\s*$", rest)
    # parts: ["", header1, body1, header2, body2, ...]
    sections: list[Section] = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append(Section(header=header, body=body))

    return prefix, sections


FENCED_TURN_RE = re.compile(
    r"(?ms)^\*\*(User|Assistant):\*\*\s*\n```[^\n]*\n(.*?)\n```\s*(?:\n|$)"
)


def clean_fenced_dialogue(text: str, *, mode: str) -> str | None:
    matches = list(FENCED_TURN_RE.finditer(text))
    if not matches:
        return None

    out: list[str] = []
    last_end = 0

    for m in matches:
        out.append(text[last_end : m.start()])
        role = m.group(1)
        body = m.group(2)

        if role == "User":
            cleaned = clean_user_body(body, mode=mode)
            if not cleaned:
                last_end = m.end()
                continue
            out.append(f"**User:**\n```md\n{cleaned}\n```\n\n")
        else:
            out.append(text[m.start() : m.end()])

        last_end = m.end()

    out.append(text[last_end:])
    return "".join(out)


def render(prefix: str, sections: list[Section], *, mode: str) -> str:
    out: list[str] = [prefix.rstrip(), ""]

    for section in sections:
        body = section.body.strip("\n")
        if section.header == "## User":
            body = clean_user_body(body, mode=mode)
        else:
            body = body.strip()

        if not body:
            continue

        out.append(section.header)
        out.append(body.rstrip())
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean exported chat transcript by removing system blocks and normalizing runtime context."
    )
    parser.add_argument("input", type=Path, help="Path to transcript markdown file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write cleaned transcript to this path (default: stdout unless --inplace)",
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Rewrite input file in place (overrides --output)",
    )
    parser.add_argument(
        "--mode",
        choices=["minimal", "verbose"],
        default="minimal",
        help="Cleaning mode (minimal drops runtime context, verbose preserves it in normalized form).",
    )
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")

    fenced_cleaned = clean_fenced_dialogue(text, mode=args.mode)
    if fenced_cleaned is not None:
        cleaned = fenced_cleaned.rstrip() + "\n"
    else:
        prefix, sections = split_sections(text)
        cleaned = render(prefix, sections, mode=args.mode)

    if args.inplace:
        args.input.write_text(cleaned, encoding="utf-8")
        return

    if args.output is not None:
        args.output.write_text(cleaned, encoding="utf-8")
        return

    print(cleaned, end="")


if __name__ == "__main__":
    main()
