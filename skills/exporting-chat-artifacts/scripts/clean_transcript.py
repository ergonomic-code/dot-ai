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


BAD_MARKERS = [
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

BAD_RE = re.compile("|".join(f"(?:{p})" for p in BAD_MARKERS), flags=re.MULTILINE)

AGENTS_BLOCK_RE = re.compile(r"(?s)^# AGENTS\.md instructions.*?</INSTRUCTIONS>\s*", re.MULTILINE)
ENV_BLOCK_RE = re.compile(r"(?s)^<environment_context>.*?</environment_context>\s*", re.MULTILINE)


def clean_user_body(body: str) -> str:
    text = body.strip("\n")
    if not text.strip():
        return ""

    text = AGENTS_BLOCK_RE.sub("", text)
    text = ENV_BLOCK_RE.sub("", text)

    # If the message contains IDE context blocks, keep only the actual request parts.
    if "# Context from my IDE setup:" in text and "## My request for Codex:" in text:
        chunks = re.split(r"(?m)^# Context from my IDE setup:\s*$", text)
        extracted: list[str] = []
        for chunk in chunks:
            if "## My request for Codex:" not in chunk:
                continue
            after = chunk.split("## My request for Codex:", 1)[1]
            candidate = after.strip()
            if not candidate:
                continue
            extracted.append(candidate)
        return "\n\n".join(extracted).strip()

    # Otherwise, drop any remaining harness-ish headings that may have slipped through.
    lines = [line for line in text.splitlines() if not BAD_RE.match(line)]
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


def clean_fenced_dialogue(text: str) -> str | None:
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
            cleaned = clean_user_body(body)
            if not cleaned:
                last_end = m.end()
                continue
            out.append(f"**User:**\n```md\n{cleaned}\n```\n\n")
        else:
            out.append(text[m.start() : m.end()])

        last_end = m.end()

    out.append(text[last_end:])
    return "".join(out)


def is_bad_section(section: Section) -> bool:
    candidate = section.body.lstrip()
    if not candidate:
        return False
    # A section is "bad" only if it appears to be purely harness/system content.
    return BAD_RE.search(candidate) is not None and section.header == "## User"


def render(prefix: str, sections: list[Section]) -> str:
    out: list[str] = [prefix.rstrip(), ""]

    for section in sections:
        body = section.body.strip("\n")
        if section.header == "## User":
            body = clean_user_body(body)
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
        description="Clean exported chat transcript by removing system/IDE/context blocks."
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
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")

    fenced_cleaned = clean_fenced_dialogue(text)
    if fenced_cleaned is not None:
        cleaned = fenced_cleaned.rstrip() + "\n"
    else:
        prefix, sections = split_sections(text)
        cleaned = render(prefix, sections)

    if args.inplace:
        args.input.write_text(cleaned, encoding="utf-8")
        return

    if args.output is not None:
        args.output.write_text(cleaned, encoding="utf-8")
        return

    print(cleaned, end="")


if __name__ == "__main__":
    main()
