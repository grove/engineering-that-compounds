#!/usr/bin/env python3
"""Static site generator for the essays collection (Python stdlib only)."""

from __future__ import annotations

import hashlib
import html
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from narration import validate_audio

ROOT = Path(__file__).resolve().parent.parent
ESSAYS_DIR = ROOT / "essays"
RESEARCH_DIR = ROOT / "research"
README_PATH = ROOT / "README.md"
STYLE_PATH = Path(__file__).resolve().parent / "style.css"
OUT_DIR = ROOT / "_site"
REPO_URL = "https://github.com/grove/engineering-that-compounds"
SITE_URL = "https://grove.github.io/engineering-that-compounds/"
ORIGINAL_URL = "https://grove.github.io/software-that-improves-with-age/"
PARTS = {
    "what-would-ten-times-look-like": ("ambition", "The ambition"),
    "engineering-capital": ("0", "What we accumulate"),
    "designing-for-decisions-we-havent-made-yet": ("1", "How capabilities develop"),
    "organizations-that-improve-with-age": ("2", "Engineering as an institution"),
    "the-ability-to-delegate": ("3", "Engineering the work"),
}
LEGACY_ANCHORS = {
    "measuring-the-capacity-for-change": {
        "a-twelve-week-field-check": "a-twelve-week-field-check-and-how-to-test-compounding",
        "what-would-make-us-change-our-minds": "what-would-prove-this-framework-wrong",
    },
}

FOREST_SVG = ('<svg class="forest-mark" width="36" height="36" viewBox="0 0 40 40" '
              'fill="none" aria-hidden="true"><path d="M10 33C9 15 21 7 33 7c0 15-7 27-23 26Z" '
              'fill="currentColor" opacity=".22"/><path d="M7 36 28 13M13 30l-1-11m7 5 10-1m-5-4V9" '
              'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
FAVICON_DATA = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E"
                "%3Crect width='40' height='40' rx='9' fill='%23243f30'/%3E"
                "%3Cpath d='M10 32C9 16 21 7 32 8c0 14-7 25-22 24Z' fill='%23b5c68a'/%3E"
                "%3Cpath d='m9 34 19-20' stroke='%23243f30' stroke-width='2'/%3E%3C/svg%3E")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def strip_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_]+", "", text)
    return " ".join(text.split())


def reading_minutes(text: str) -> int:
    words = len(re.findall(r"\b\w+(?:['’]\w+)*\b", strip_markdown(text)))
    return max(1, math.ceil(words / 230))


# Stdlib Markdown subset (headings, lists, blockquotes, fences, inline
# code/bold/italic/links with balanced parens); swap in python-markdown or pandoc
# if future essays need tables, footnotes, or nested lists.
def render_inline(text: str, resolve_link) -> str:
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "`":
            end = text.find("`", i + 1)
            if end != -1:
                out.append(f"<code>{html.escape(text[i + 1 : end])}</code>")
                i = end + 1
                continue
        elif ch == "[":
            close_bracket = text.find("]", i + 1)
            if close_bracket != -1 and close_bracket + 1 < n and text[close_bracket + 1] == "(":
                depth = 1
                j = close_bracket + 2
                while j < n and depth > 0:
                    if text[j] == "(":
                        depth += 1
                    elif text[j] == ")":
                        depth -= 1
                    j += 1
                if depth == 0:
                    label = render_inline(text[i + 1 : close_bracket], resolve_link)
                    href = resolve_link(text[close_bracket + 2 : j - 1].strip())
                    out.append(f'<a href="{html.escape(href, quote=True)}">{label}</a>')
                    i = j
                    continue
        elif text.startswith("**", i):
            end = text.find("**", i + 2)
            if end != -1 and end > i + 2:
                out.append(f"<strong>{render_inline(text[i + 2 : end], resolve_link)}</strong>")
                i = end + 2
                continue
        elif ch == "*":
            end = text.find("*", i + 1)
            if end != -1 and end > i + 1 and not text[i + 1].isspace():
                out.append(f"<em>{render_inline(text[i + 1 : end], resolve_link)}</em>")
                i = end + 1
                continue
        out.append(html.escape(ch))
        i += 1
    return "".join(out)


def render_markdown(md: str, resolve_link) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[str] = []
    seen_ids: dict[str, int] = {}
    i, n = 0, len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            code_lines: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            blocks.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            raw = heading.group(2).strip()
            base_id = slugify(strip_markdown(raw))
            count = seen_ids.get(base_id, 0)
            seen_ids[base_id] = count + 1
            hid = base_id if count == 0 else f"{base_id}-{count + 1}"
            blocks.append(f'<h{level} id="{hid}">{render_inline(raw, resolve_link)}</h{level}>')
            i += 1
            continue

        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            blocks.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                q = lines[i].lstrip()[1:]
                quote_lines.append(q[1:] if q.startswith(" ") else q)
                i += 1
            inner = render_markdown("\n".join(quote_lines), resolve_link)
            blocks.append(f"<blockquote>\n{inner}\n</blockquote>")
            continue

        if re.match(r"^[-*]\s+", stripped):
            items: list[str] = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip(), count=1))
                i += 1
            rendered = "\n".join(f"<li>{render_inline(it, resolve_link)}</li>" for it in items)
            blocks.append(f"<ul>\n{rendered}\n</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip(), count=1))
                i += 1
            rendered = "\n".join(f"<li>{render_inline(it, resolve_link)}</li>" for it in items)
            blocks.append(f"<ol>\n{rendered}\n</ol>")
            continue

        para_lines: list[str] = []
        while i < n:
            cur = lines[i].strip()
            if (
                not cur
                or cur.startswith("```")
                or cur.startswith(">")
                or re.match(r"^(#{1,6})\s+", cur)
                or re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", cur)
                or re.match(r"^([-*]|\d+\.)\s+", cur)
            ):
                break
            para_lines.append(cur)
            i += 1
        blocks.append(f"<p>{render_inline(' '.join(para_lines), resolve_link)}</p>")

    return "\n".join(blocks)


def split_header(md: str) -> tuple[str, str | None, str]:
    """Extract leading '# Title', optional '*Subtitle*', and remaining body."""
    lines = md.replace("\r\n", "\n").split("\n")
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    title = ""
    if idx < len(lines) and lines[idx].startswith("# "):
        title = lines[idx][2:].strip()
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    subtitle = None
    if idx < len(lines):
        cand = lines[idx].strip()
        if cand.startswith("*") and cand.endswith("*") and not cand.startswith("**") and cand.count("*") == 2:
            subtitle = cand[1:-1].strip()
            idx += 1
    body = "\n".join(lines[idx:]).strip()
    return title, subtitle, body


def first_paragraph_text(md: str) -> str:
    for block in re.split(r"\n\s*\n", md.strip()):
        s = block.strip()
        if s and not s.startswith(("#", ">", "-", "*", "```")):
            return strip_markdown(s)[:180]
    return ""


def parse_readme(md: str) -> tuple[str, str | None, str, str, list[dict[str, str]]]:
    title, subtitle, body = split_header(md)
    parts = re.split(r"^##\s+Reading order\s*$", body, maxsplit=1, flags=re.MULTILINE)
    intro_md = parts[0].strip()
    rest = parts[1] if len(parts) > 1 else ""
    rest = re.split(r"^##\s+", rest, maxsplit=1, flags=re.MULTILINE)[0].strip()

    note_lines: list[str] = []
    entries: list[dict[str, str]] = []
    item_re = re.compile(
        r"^\d+\.\s+\*\*\[([^\]]+)\]\(\./essays/([^)]+)\.md\)\*\*\s*(?:[—–-]\s*(.+))?$"
    )
    for line in rest.splitlines():
        s = line.strip()
        if not s:
            continue
        m = item_re.match(s)
        if m:
            entries.append(
                {
                    "slug": m.group(2),
                    "title": m.group(1).strip(),
                    "summary": (m.group(3) or "").strip(),
                }
            )
        elif not entries:
            note_lines.append(s)

    return title, subtitle, intro_md, " ".join(note_lines), entries


def html_shell(*, title: str, description: str, css_href: str, body: str, path: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta name="theme-color" content="#243f30">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="{SITE_URL}{path}">
  <meta property="og:type" content="{'article' if path else 'website'}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:url" content="{SITE_URL}{path}">
  <link rel="icon" href="{FAVICON_DATA}">
  <link rel="stylesheet" href="{css_href}?v={hashlib.sha256((ROOT / 'site/style.css').read_bytes()).hexdigest()[:16]}">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="collection-bar">
    <nav class="collection-nav" aria-label="Collections">
      <a class="collection-home" href="https://grove.github.io/compounding-engineering/">
        <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true"><circle cx="16" cy="16" r="13" stroke="currentColor"/><circle cx="16" cy="16" r="8.5" stroke="currentColor"/><circle cx="16" cy="16" r="4" stroke="currentColor"/></svg>
        <span>Compounding Engineering</span>
      </a>
      <ul>
        <li><a href="https://grove.github.io/software-that-improves-with-age/" aria-label="Software that improves with age">Software</a></li>
        <li><a href="https://grove.github.io/engineering-that-compounds/" aria-label="Engineering that compounds" aria-current="true">Engineering</a></li>
        <li><a href="https://grove.github.io/patterns-of-compounding-engineering/" aria-label="Patterns of compounding engineering">Patterns</a></li>
      </ul>
    </nav>
  </div>
  <div class="page">
{body}
    <footer class="site-footer">
      <span class="footer-mark">{FOREST_SVG}<span>Engineering that compounds</span></span>
      <div class="footer-links">
        <a href="{REPO_URL}/blob/main/LICENSE">Apache License 2.0</a>
        <a href="{REPO_URL}">GitHub</a>
      </div>
    </footer>
  </div>
</body>
</html>
"""


def build(out_dir: Path = OUT_DIR) -> list[Path]:
    readme_md = README_PATH.read_text(encoding="utf-8")
    site_title, site_subtitle, intro_md, reading_note, listed = parse_readme(readme_md)
    # Ensure every essay in essays/ is included even if not yet added to README.md.
    by_slug = {e["slug"]: e for e in listed}
    ordered = list(listed)
    for path in sorted(ESSAYS_DIR.glob("*.md")):
        if path.stem not in by_slug:
            t, sub, b = split_header(path.read_text(encoding="utf-8"))
            ordered.append({"slug": path.stem, "title": t or path.stem, "summary": sub or first_paragraph_text(b)})

    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "essays").mkdir(parents=True, exist_ok=True)
    shutil.copy2(STYLE_PATH, out_dir / "style.css")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    internal_links: list[tuple[Path, str]] = []
    written: list[Path] = []

    def make_resolver(page_path: Path):
        def resolve(href: str) -> str:
            if href == "./LICENSE":
                return f"{REPO_URL}/blob/main/LICENSE"
            if href.startswith(("http://", "https://", "mailto:", "#")):
                return href
            parsed = urlsplit(href)
            if parsed.path.endswith(".md"):
                source_dir = ROOT / page_path.relative_to(out_dir).parent
                source = (source_dir / unquote(parsed.path)).resolve()
                if source.parent in (ESSAYS_DIR, RESEARCH_DIR):
                    if not source.is_file():
                        raise RuntimeError(f"Missing Markdown source: {href}")
                    destination = out_dir / source.relative_to(ROOT).with_suffix(".html")
                    target = Path(os.path.relpath(destination, page_path.parent)).as_posix()
                    internal_links.append((page_path, target))
                    if parsed.query:
                        target += "?" + parsed.query
                    if parsed.fragment:
                        target += "#" + parsed.fragment
                    return target
            return href

        return resolve

    total = len(ordered)
    for idx, entry in enumerate(ordered):
        md_path = ESSAYS_DIR / f"{entry['slug']}.md"
        raw_md = md_path.read_text(encoding="utf-8")
        title, subtitle, body_md = split_header(raw_md)
        entry["title"] = title or entry["title"]
        entry["minutes"] = str(reading_minutes(raw_md))

        out_path = out_dir / "essays" / f"{entry['slug']}.html"
        resolve = make_resolver(out_path)
        body_html = render_markdown(body_md, resolve)
        for current, previous in LEGACY_ANCHORS.get(entry["slug"], {}).items():
            heading = f'<h2 id="{current}">'
            if heading not in body_html:
                raise RuntimeError(f"Missing heading for legacy anchor: {current}")
            body_html = body_html.replace(heading, f'<span id="{previous}"></span>\n{heading}', 1)

        prev_link = ""
        if idx > 0:
            p = ordered[idx - 1]
            prev_link = (
                f'<a class="pager-link prev" href="{p["slug"]}.html">'
                f'<span class="pager-label">Previous essay</span>'
                f'<span class="pager-title">{html.escape(p["title"])}</span></a>'
            )
        next_link = ""
        if idx + 1 < total:
            nx = ordered[idx + 1]
            next_link = (
                f'<a class="pager-link next" href="{nx["slug"]}.html">'
                f'<span class="pager-label">Next essay</span>'
                f'<span class="pager-title">{html.escape(nx["title"])}</span></a>'
            )

        subtitle_html = f'\n      <p class="subtitle">{html.escape(subtitle)}</p>' if subtitle else ""
        page_body = f"""    <nav class="top-nav" aria-label="Breadcrumb">
      <a class="back-link" href="../">All essays</a>
      <span class="top-meta">{idx + 1:02d} / {total:02d} &middot; {entry["minutes"]} min read</span>
    </nav>
    <main id="main">
      <article>
        <header>
          <h1>{html.escape(entry["title"])}</h1>{subtitle_html}
        </header>
        {body_html}
      </article>
      <nav class="pager" aria-label="Essay navigation">
        {prev_link}
        {next_link}
      </nav>
    </main>"""

        desc = subtitle or entry["summary"] or first_paragraph_text(body_md)
        out_path.write_text(
            html_shell(
                title=f"{entry['title']} — {site_title}",
                description=desc,
                css_href="../style.css",
                body=page_body,
                path=f"essays/{entry['slug']}.html",
            ),
            encoding="utf-8",
        )
        written.append(out_path)

    # Research protocols are supporting material, outside the essay reading order.
    for md_path in sorted(RESEARCH_DIR.glob("*.md")):
        title, subtitle, body_md = split_header(md_path.read_text(encoding="utf-8"))
        out_path = out_dir / "research" / f"{md_path.stem}.html"
        out_path.parent.mkdir(exist_ok=True)
        subtitle_html = f'<p class="subtitle">{html.escape(subtitle)}</p>' if subtitle else ""
        body_html = render_markdown(body_md, make_resolver(out_path))
        page_body = f"""    <nav class="top-nav" aria-label="Breadcrumb">
      <a class="back-link" href="../essays/measuring-the-capacity-for-change.html">Measuring the capacity for change</a>
      <span class="top-meta">Research protocol</span>
    </nav>
    <main id="main">
      <article>
        <header><h1>{html.escape(title)}</h1>{subtitle_html}</header>
        {body_html}
      </article>
    </main>"""
        out_path.write_text(html_shell(
            title=f"{title} — {site_title}",
            description=subtitle or first_paragraph_text(body_md),
            css_href="../style.css", body=page_body,
            path=f"research/{md_path.stem}.html",
        ), encoding="utf-8")
        written.append(out_path)

    # Index page
    index_path = out_dir / "index.html"
    intro_html = render_markdown(intro_md, make_resolver(index_path))
    list_items: list[str] = []
    for idx, entry in enumerate(ordered, start=1):
        if entry["slug"] in PARTS:
            part, part_title = PARTS[entry["slug"]]
            if idx > 1:
                list_items.append("</ol></section>")
            list_items.append(f'<section class="reading-part" aria-labelledby="part-{part}">'
                              f'<h3 class="part-heading" id="part-{part}">{html.escape(part_title)}</h3>'
                              f'<ol class="essay-list" role="list" start="{idx}">')
        summary_html = (
            f'<p class="essay-summary">{render_inline(entry["summary"], make_resolver(index_path))}</p>'
            if entry["summary"]
            else ""
        )
        list_items.append(
            f"""        <li class="essay-item">
          <div class="essay-card">
            <span class="essay-num" aria-hidden="true">{idx:02d}</span>
            <div class="essay-head">
              <a class="essay-title-link" href="essays/{entry['slug']}.html">{html.escape(entry['title'])}</a>
              <span class="essay-meta">{entry['minutes']} min</span>
            </div>
            {summary_html}
          </div>
        </li>"""
        )
    list_items.append("</ol></section>")

    subtitle_html = f'\n      <p class="subtitle">{html.escape(site_subtitle)}</p>' if site_subtitle else ""
    note_html = f'\n      <p class="reading-note">{html.escape(reading_note)}</p>' if reading_note else ""
    index_body = f"""    <header class="site-header">
      <div class="collection-mark">{FOREST_SVG}</div>
      <h1>{html.escape(site_title)}</h1>{subtitle_html}
    </header>
    <main id="main">
      <section class="intro">
        {intro_html}
      </section>
      <section aria-labelledby="reading-order">
        <h2 id="reading-order" class="section-heading">Reading order</h2>{note_html}
        <div class="reading-parts">
{chr(10).join(list_items)}
        </div>
      </section>
      <aside class="companion-note" aria-labelledby="companion-collection">
        <h2 id="companion-collection" class="section-heading">Companion collection</h2>
        <p class="companion-title"><a href="{ORIGINAL_URL}">Software that improves with age</a></p>
        <p class="companion-description"><em>Software that improves with age</em> is the earlier collection this series builds on. It looks at what happens inside a codebase when AI makes writing code cheaper: how discovery, module boundaries, independent verification, production operations and deliberate removal affect whether a system becomes easier or harder to change over time.</p>
        <p class="companion-description">That codebase-level foundation explains why the questions here arise. Several essays in this collection pick up directly where the first series leaves off, moving from how delegating implementation weakens a team's mental model to how engineers develop judgment in the first place, what rationale and tools a team should keep, and how to tell whether earlier work actually helps the next change.</p>
      </aside>
    </main>"""

    index_path.write_text(
        html_shell(
            title=site_title,
            description=site_subtitle or first_paragraph_text(intro_md),
            css_href="style.css",
            body=index_body,
        ),
        encoding="utf-8",
    )
    written.append(index_path)

    # Verify every rewritten internal link resolves to a generated file.
    for source, target in internal_links:
        resolved = (source.parent / target).resolve()
        if not resolved.exists():
            raise RuntimeError(f"Broken internal link in {source.name}: {target}")

    return written


class LinkInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.h1_count = 0
        self.audio_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            if values["id"] in self.ids:
                raise RuntimeError(f"Duplicate HTML id: {values['id']}")
            self.ids.add(values["id"])
        self.h1_count += tag == "h1"
        self.audio_count += tag == "audio"
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.links.append(values[attribute])


def check_generated_pages(pages: list[Path]) -> None:
    inventories = {}
    for page in pages:
        inventory = LinkInventory()
        inventory.feed(page.read_text(encoding="utf-8"))
        if inventory.h1_count != 1:
            raise RuntimeError(f"Expected one page title: {page}")
        if page.parent.name == "essays" and inventory.audio_count:
            raise RuntimeError(f"Unexpected narration player: {page}")
        inventories[page.resolve()] = inventory
    for page, inventory in inventories.items():
        for href in inventory.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                raise RuntimeError(f"Broken local link in {page.name}: {href}")
            if url.fragment and target in inventories and unquote(url.fragment) not in inventories[target].ids:
                raise RuntimeError(f"Missing link target in {page.name}: {href}")


def self_check(*, include_audio: bool = True) -> None:
    id_res = lambda u: u
    # Balanced parentheses in URLs (e.g., DOI link in implementation-and-understanding.md)
    doi = render_inline("[Paper](https://doi.org/10.1016/0165-6074(85)90032-8)", id_res)
    assert 'href="https://doi.org/10.1016/0165-6074(85)90032-8"' in doi, doi
    # Inline code escapes HTML and preserves asterisks
    code = render_inline("call `fsync(*a < b)` now", id_res)
    assert "<code>fsync(*a &lt; b)</code>" in code, code
    # Multi-paragraph blockquote
    bq = render_markdown("> First\n>\n> Second", id_res)
    assert bq == "<blockquote>\n<p>First</p>\n<p>Second</p>\n</blockquote>", bq
    essays = sorted(ESSAYS_DIR.glob("*.md"))
    listed = parse_readme(README_PATH.read_text())[4]
    slugs = [entry["slug"] for entry in listed]
    if len(slugs) != len(set(slugs)) or set(slugs) != {p.stem for p in essays}:
        raise RuntimeError("README reading order must list every essay exactly once.")
    for entry in listed:
        path = ESSAYS_DIR / f"{entry['slug']}.md"
        title = split_header(path.read_text())[0]
        if title != entry["title"]:
            raise RuntimeError(f"README title differs from essay title: {path.name}")
    if include_audio:
        validate_audio(essays)
    # Build and verify all essays rendered
    pages = build()
    expected = len(list(ESSAYS_DIR.glob("*.md"))) + len(list(RESEARCH_DIR.glob("*.md"))) + 1
    assert len(pages) == expected, f"Expected {expected} pages, built {len(pages)}"
    check_generated_pages(pages)


if __name__ == "__main__":
    if "--check" in sys.argv or "--check-text" in sys.argv:
        self_check(include_audio="--check" in sys.argv)
        print("OK: self-check and build passed.")
    else:
        built = build()
        print(f"Built {len(built)} pages into {OUT_DIR.relative_to(ROOT)}/")
