#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


_TASK_DIR_PREFIX_RE = re.compile(r"^(?P<num>\d+)-")

_SLUG_ALLOWED_CHARS_RE = re.compile(r"[^A-Za-z0-9-]+")
_SLUG_MULTI_DASH_RE = re.compile(r"-{2,}")

_TITLE_PREFIX_RE = re.compile(r"^[\s#>*\d.()–—-]+")

MAX_SUGGESTED_SLUG_LENGTH = 60

_CYRILLIC_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def _find_repo_root(start_dir: Path) -> Path:
    for candidate in (start_dir, *start_dir.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Не удалось найти корень git-репозитория по .git.")


def _parse_date(raw_date: str | None) -> dt.date:
    if raw_date is None:
        return dt.date.today()
    try:
        return dt.datetime.strptime(raw_date, "%Y-%m-%d").date()
    except ValueError as exc:
        raise RuntimeError("Неверный формат --date, ожидается YYYY-MM-DD.") from exc


def _read_statement(statement_arg: str | None) -> str:
    if statement_arg is not None:
        return statement_arg
    if sys.stdin.isatty():
        raise RuntimeError("Передай постановку задачи через stdin или через --statement.")
    return sys.stdin.read()


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _normalize_title_line(raw_line: str) -> str:
    return _TITLE_PREFIX_RE.sub("", raw_line).strip()


def _transliterate_cyrillic_to_latin(text: str) -> str:
    result_parts: list[str] = []
    for ch in text:
        lower = ch.lower()
        if lower in _CYRILLIC_TO_LATIN:
            latin = _CYRILLIC_TO_LATIN[lower]
            if ch.isupper():
                latin = latin.capitalize()
            result_parts.append(latin)
        else:
            result_parts.append(ch)
    return "".join(result_parts)


def _slugify_from_title(title: str) -> str:
    transliterated = _transliterate_cyrillic_to_latin(title)
    lowered = transliterated.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)
    slug = _SLUG_MULTI_DASH_RE.sub("-", slug).strip("-")
    truncated = _truncate_slug(slug, MAX_SUGGESTED_SLUG_LENGTH)
    return truncated or "task"


def _truncate_slug(slug: str, max_length: int) -> str:
    if max_length <= 0:
        raise RuntimeError("max_length должен быть положительным числом.")
    if len(slug) <= max_length:
        return slug

    parts = [part for part in slug.split("-") if part]
    if not parts:
        return slug[:max_length].strip("-")

    acc: list[str] = []
    for part in parts:
        candidate = "-".join([*acc, part]) if acc else part
        if len(candidate) <= max_length:
            acc.append(part)
            continue
        break

    if acc:
        return "-".join(acc).strip("-")

    return parts[0][:max_length].strip("-")


def _sanitize_user_slug(raw_slug: str) -> str:
    transliterated = _transliterate_cyrillic_to_latin(raw_slug.strip())
    slug = _SLUG_ALLOWED_CHARS_RE.sub("-", transliterated)
    slug = _SLUG_MULTI_DASH_RE.sub("-", slug).strip("-")
    if not slug:
        raise RuntimeError("Пустой slug после нормализации.")
    return slug


def _next_task_number(month_dir: Path) -> int:
    if not month_dir.is_dir():
        return 1

    numbers: list[int] = []
    for entry in month_dir.iterdir():
        if not entry.is_dir():
            continue
        match = _TASK_DIR_PREFIX_RE.match(entry.name)
        if match is None:
            continue
        try:
            numbers.append(int(match.group("num")))
        except ValueError:
            continue

    return (max(numbers) if numbers else 0) + 1


def _touch_empty_file(path: Path) -> None:
    if path.exists():
        raise RuntimeError(f"Файл уже существует: {path}")
    path.touch()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Инициализировать директорию задачи в engineering-log/<yy>/<MM>/<NN>-<slug> "
            "и создать файлы по шаблону."
        ),
    )
    parser.add_argument(
        "--date",
        help="Дата для выбора yy/MM, формат YYYY-MM-DD.",
    )
    parser.add_argument(
        "--slug",
        help="Явно задать slug директории задачи.",
    )
    parser.add_argument(
        "--statement",
        help="Постановка задачи одной строкой, если не хочется использовать stdin.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Не создавать файлы, только показать итоговый путь.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Создать задачу без подтверждения slug, используя предложенный по постановке slug.",
    )
    args = parser.parse_args()

    statement = _read_statement(args.statement)
    if not statement.strip():
        raise RuntimeError("Постановка задачи пустая.")
    if not statement.endswith("\n"):
        statement += "\n"

    start_dir = Path.cwd().resolve()
    repo_root = _find_repo_root(start_dir)
    design_bureau_root = repo_root / "engineering-log"
    if not design_bureau_root.is_dir():
        raise RuntimeError(f"Не найдена директория engineering-log: {design_bureau_root}")

    skill_root = Path(__file__).resolve().parents[1]

    date = _parse_date(args.date)
    yy = date.year % 100
    mm = date.month

    year_dir = design_bureau_root / f"{yy:02d}"
    month_dir = year_dir / f"{mm:02d}"

    task_num = _next_task_number(month_dir)

    suggested_slug: str | None = None
    if args.slug:
        slug = _sanitize_user_slug(args.slug)
    else:
        title_line = _normalize_title_line(_first_nonempty_line(statement))
        suggested_slug = _slugify_from_title(title_line)
        slug = suggested_slug

    task_dir = month_dir / f"{task_num:02d}-{slug}"
    task_dir_rel = task_dir.relative_to(repo_root)

    if args.dry_run:
        print(task_dir_rel)
        return 0

    if args.slug is None and not args.yes:
        raise RuntimeError(
            "Требуется одобрение slug.\n"
            f"Предложенный slug: {suggested_slug}\n"
            f"Предложенный путь: {task_dir_rel}\n"
            f"Запусти повторно с --slug {suggested_slug} или с --yes.",
        )

    month_dir.mkdir(parents=True, exist_ok=True)
    task_dir.mkdir(exist_ok=False)

    chats_dir = task_dir / "chats"
    chats_dir.mkdir(exist_ok=False)

    template_path = skill_root / "assets" / "04-execution-spec.md"
    if not template_path.is_file():
        raise RuntimeError(f"Не найден встроенный шаблон Execution-Spec: {template_path}")

    (task_dir / "01-problem-statement.md").write_text(statement, encoding="utf-8")
    _touch_empty_file(task_dir / "02-solution-options.md")
    _touch_empty_file(task_dir / "03-solution-hld.md")
    (task_dir / "04-execution-spec.md").write_text(
        template_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    _touch_empty_file(chats_dir / "01-exploration-chat-1.md")
    _touch_empty_file(chats_dir / "02-specification-chat-1.md")
    _touch_empty_file(chats_dir / "03-implementation-chat-1.md")

    print(task_dir_rel)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)
