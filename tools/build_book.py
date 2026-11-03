#!/usr/bin/env python3
"""Compile the Zemax course into a single PDF "book".

Usage (from the repo root):
    python tools/build_book.py                  # whole course -> build/zemax-course.pdf
    python tools/build_book.py --course 04      # only Course 04
    python tools/build_book.py --no-solutions   # drop <details> hint/solution blocks
    python tools/build_book.py --html-only      # just build/zemax-course.html (no PDF)

One-time setup (Windows, macOS or Linux):
    pip install -r tools/requirements-book.txt
    python -m playwright install chromium

The first run downloads KaTeX (math) and Mermaid (diagrams) from the npm
registry into tools/.cache/ (git-ignored); later builds work offline.
Use --assets DIR to point at an existing folder containing katex/ and mermaid/.
"""
from __future__ import annotations

import argparse
import html
import io
import re
import sys
import tarfile
import time
import urllib.request
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

try:  # optional syntax highlighting
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name
    from pygments.util import ClassNotFound
    HAVE_PYGMENTS = True
except ImportError:  # pragma: no cover
    HAVE_PYGMENTS = False

ROOT = Path(__file__).resolve().parent.parent
KATEX_VER = "0.16.11"
MERMAID_VER = "10.9.1"
NPM = "https://registry.npmjs.org/{name}/-/{name}-{ver}.tgz"


# --------------------------------------------------------------------------- model
@dataclass
class Doc:
    path: Path            # absolute path of the .md file
    title: str            # heading shown in the TOC
    kind: str             # front | course | lecture | tasks | back
    anchor: str = ""

    def __post_init__(self):
        rel = self.path.relative_to(ROOT).as_posix()
        self.anchor = "doc-" + re.sub(r"[^a-zA-Z0-9]+", "-", rel.removesuffix(".md")).strip("-").lower()


@dataclass
class Course:
    folder: Path
    title: str
    readme: Doc | None
    lessons: list[tuple[str, list[Doc]]] = field(default_factory=list)  # (lesson title, [lecture, tasks])


def first_heading(md_path: Path, fallback: str) -> str:
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def collect(course_filter: list[str] | None) -> tuple[list[Doc], list[Course], list[Doc]]:
    front = [Doc(ROOT / n, first_heading(ROOT / n, n), "front")
             for n in ("README.md", "CURRICULUM.md") if (ROOT / n).exists()]
    back = [Doc(p, first_heading(p, "References"), "back")
            for p in [ROOT / "references" / "README.md"] if p.exists()]
    courses: list[Course] = []
    for cdir in sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"\d\d-", p.name)):
        if course_filter and cdir.name[:2] not in course_filter:
            continue
        readme = cdir / "README.md"
        rdoc = Doc(readme, first_heading(readme, cdir.name), "course") if readme.exists() else None
        course = Course(cdir, rdoc.title if rdoc else cdir.name, rdoc)
        for ldir in sorted(p for p in cdir.iterdir() if p.is_dir() and re.match(r"L\d\d-", p.name)):
            docs = []
            for fname, kind in (("lecture-notes.md", "lecture"), ("tasks.md", "tasks")):
                f = ldir / fname
                if f.exists():
                    docs.append(Doc(f, first_heading(f, f"{ldir.name} {fname}"), kind))
            if docs:
                course.lessons.append((docs[0].title, docs))
        courses.append(course)
    return front, courses, back


# --------------------------------------------------------------------------- markdown
def make_md() -> MarkdownIt:
    md = (MarkdownIt("commonmark", {"html": True, "linkify": False, "typographer": False})
          .enable(["table", "strikethrough"])
          .use(dollarmath_plugin, allow_space=True, double_inline=True)
          .use(footnote_plugin)
          .use(tasklists_plugin)
          .use(anchors_plugin, max_level=4))

    def fence(self, tokens, idx, options, env):
        tok = tokens[idx]
        lang = (tok.info or "").strip().split()[0] if tok.info else ""
        code = tok.content
        if lang == "mermaid":
            return f'<pre class="mermaid">{html.escape(code)}</pre>\n'
        if HAVE_PYGMENTS and lang:
            try:
                lexer = get_lexer_by_name({"zpl": "basic"}.get(lang, lang))
                return highlight(code, lexer, HtmlFormatter(nowrap=False, cssclass="hl"))
            except ClassNotFound:
                pass
        return f'<pre class="code"><code>{html.escape(code)}</code></pre>\n'

    md.add_render_rule("fence", fence)
    return md


def resolve_link(href: str, src: Path, anchors: dict[Path, str]) -> str | None:
    """Map a relative link to an in-book anchor; None if the target is not in the book."""
    target, _, frag = href.partition("#")
    if not target:
        return None  # pure fragment, handled separately
    p = (src.parent / target).resolve()
    candidates = [p] if p.suffix == ".md" else [p / "lecture-notes.md", p / "README.md"]
    for c in candidates:
        if c in anchors:
            return "#" + anchors[c] + (f"--{frag}" if frag else "")
    return None


def render_doc(md: MarkdownIt, doc: Doc, anchors: dict[Path, str], no_solutions: bool) -> str:
    text = doc.path.read_text(encoding="utf-8")
    if no_solutions:
        text = re.sub(r"<details>.*?</details>", "", text, flags=re.S | re.I)
    body = md.render(text)
    # Namespace heading ids per document so "learning-objectives" etc. stay unique.
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{doc.anchor}--{m.group(1)}"', body)

    def fix_href(m: re.Match) -> str:
        href = html.unescape(m.group(1))
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I):  # http:, mailto:, computer:, ...
            return m.group(0)
        if href.startswith("#"):
            return f'href="#{doc.anchor}--{href[1:]}"'
        new = resolve_link(href, doc.path, anchors)
        if new:
            return f'href="{new}"'
        return 'class="dead-link" title="not part of the book (e.g. your work/ folder)"'

    body = re.sub(r'href="([^"]*)"', fix_href, body)
    # Dead links become plain text (an <a> without href)
    return f'<section class="doc {doc.kind}" id="{doc.anchor}">\n{body}\n</section>\n'


# --------------------------------------------------------------------------- assets
def ensure_assets(cache: Path) -> Path:
    for name, ver, probe in (("katex", KATEX_VER, "dist/katex.min.js"),
                             ("mermaid", MERMAID_VER, "dist/mermaid.min.js")):
        dest = cache / name
        if (dest / probe).exists():
            continue
        url = NPM.format(name=name, ver=ver)
        print(f"Downloading {name} {ver} from {url} ...")
        data = urllib.request.urlopen(url, timeout=120).read()
        dest.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
            for m in tf.getmembers():
                if not m.name.startswith("package/dist/") or m.issym() or m.islnk():
                    continue
                rel = Path(m.name).relative_to("package")
                if ".." in rel.parts:
                    continue
                out = dest / rel
                if m.isdir():
                    out.mkdir(parents=True, exist_ok=True)
                elif m.isfile():
                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_bytes(tf.extractfile(m).read())
    return cache


# --------------------------------------------------------------------------- html
CSS = r"""
@page { size: A4; margin: 20mm 17mm 20mm 17mm; }
html { font-size: 10.5pt; }
body { font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 1.9em; border-bottom: 2px solid #2b5797; padding-bottom: .2em; color: #2b5797; }
h2 { font-size: 1.4em; color: #2b5797; margin-top: 1.4em; }
h3 { font-size: 1.15em; } h4 { font-size: 1.02em; }
h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
a { color: #2b5797; text-decoration: none; }
a.dead-link { color: inherit; }
p, li { orphans: 3; widows: 3; }
blockquote { border-left: 4px solid #c8d3e6; margin: .8em 0; padding: .2em .9em; color: #333; background: #f5f7fb; }
table { border-collapse: collapse; margin: .8em 0; font-size: .92em; width: auto; max-width: 100%; }
th, td { border: 1px solid #c9c9c9; padding: 3px 6px; vertical-align: top; }
th { background: #eef2f8; }
tr, img, pre, .math.block, svg { break-inside: avoid; }
code { font-family: Consolas, "Cascadia Mono", "DejaVu Sans Mono", monospace; font-size: .9em; background: #f3f3f3; padding: 0 2px; }
pre, .hl pre { background: #f6f8fa; border: 1px solid #e1e4e8; padding: 7px 9px; font-size: .82em;
               white-space: pre-wrap; word-break: break-word; overflow: hidden; }
pre code { background: none; padding: 0; }
pre.mermaid { background: none; border: none; text-align: center; }
details { border: 1px dashed #9aa9c4; padding: .3em .8em; margin: .8em 0; background: #fbfcfe; }
summary { font-weight: 600; color: #2b5797; }
.math.block { overflow-x: hidden; margin: .6em 0; }
.doc { break-before: page; page-break-before: always; }
.doc.tasks > h1 { border-bottom-color: #b5651d; color: #b5651d; }
.course-divider { break-before: page; page-break-before: always; height: 230mm; display: flex;
                  flex-direction: column; justify-content: center; text-align: center; }
.course-divider .num { font-size: 4em; color: #c8d3e6; font-weight: 700; }
.course-divider .name { font-size: 2.2em; color: #2b5797; font-weight: 600; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; text-align: center; }
.cover .t { font-size: 3em; font-weight: 700; color: #2b5797; }
.cover .s { font-size: 1.3em; margin-top: .6em; color: #444; }
.cover .d { margin-top: 3em; color: #777; }
nav.toc { break-before: page; page-break-before: always; }
nav.toc ul { list-style: none; padding-left: 1.2em; }
nav.toc > ul { padding-left: 0; }
nav.toc li.course { margin-top: .7em; font-weight: 600; }
nav.toc li.lesson { font-weight: 400; }
nav.toc .tk { color: #b5651d; font-size: .9em; margin-left: .6em; }
"""

JS = r"""
window.__bookReady = (async () => {
  document.querySelectorAll('details').forEach(d => d.open = true);
  for (const el of document.querySelectorAll('.math')) {
    const display = el.classList.contains('block');
    try { katex.render(el.textContent, el, {displayMode: display, throwOnError: false, strict: 'ignore'}); }
    catch (e) { console.warn('KaTeX', e); }
  }
  if (window.mermaid) {
    mermaid.initialize({startOnLoad: false, theme: 'neutral', securityLevel: 'loose'});
    try { await mermaid.run({querySelector: 'pre.mermaid', suppressErrors: true}); }
    catch (e) { console.warn('Mermaid', e); }
  }
  return true;
})();
"""


def build_html(course_filter, no_solutions: bool, assets: Path) -> str:
    front, courses, back = collect(course_filter)
    all_docs = front + [d for c in courses for d in ([c.readme] if c.readme else [])
                        + [x for _, ds in c.lessons for x in ds]] + back
    anchors = {d.path.resolve(): d.anchor for d in all_docs}
    md = make_md()

    toc = ['<nav class="toc"><h1>Contents</h1><ul>']
    for d in front:
        toc.append(f'<li><a href="#{d.anchor}">{html.escape(d.title)}</a></li>')
    for c in courses:
        head = c.readme.anchor if c.readme else ""
        toc.append(f'<li class="course"><a href="#{head}">{html.escape(c.title)}</a><ul>')
        for title, ds in c.lessons:
            lec = next((d for d in ds if d.kind == "lecture"), ds[0])
            tsk = next((d for d in ds if d.kind == "tasks"), None)
            t = f' <a class="tk" href="#{tsk.anchor}">tasks</a>' if tsk else ""
            toc.append(f'<li class="lesson"><a href="#{lec.anchor}">{html.escape(title)}</a>{t}</li>')
        toc.append("</ul></li>")
    for d in back:
        toc.append(f'<li class="course"><a href="#{d.anchor}">{html.escape(d.title)}</a></li>')
    toc.append("</ul></nav>")

    parts = []
    for d in front:
        parts.append(render_doc(md, d, anchors, no_solutions))
    for c in courses:
        m = re.match(r"(\d\d)", c.folder.name)
        parts.append(f'<div class="course-divider"><div class="num">Course {m.group(1)}</div>'
                     f'<div class="name">{html.escape(re.sub(r"^Course \d+\s*[—-]\s*", "", c.title))}</div></div>')
        if c.readme:
            parts.append(render_doc(md, c.readme, anchors, no_solutions))
        for _, ds in c.lessons:
            for d in ds:
                parts.append(render_doc(md, d, anchors, no_solutions))
    for d in back:
        parts.append(render_doc(md, d, anchors, no_solutions))

    katex_dir = (assets / "katex" / "dist").resolve().as_uri()
    mermaid_js = (assets / "mermaid" / "dist" / "mermaid.min.js").resolve().as_uri()
    pyg_css = HtmlFormatter(style="default").get_style_defs(".hl") if HAVE_PYGMENTS else ""
    subtitle = "From 101 to professional — lecture notes and tasks"
    if course_filter:
        subtitle += " · Course " + ", ".join(course_filter)
    if no_solutions:
        subtitle += " · without solutions"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Zemax OpticStudio course</title>
<link rel="stylesheet" href="{katex_dir}/katex.min.css">
<script src="{katex_dir}/katex.min.js"></script>
<script src="{mermaid_js}"></script>
<style>{CSS}\n{pyg_css}</style>
</head><body>
<div class="cover"><div class="t">Zemax OpticStudio</div>
<div class="s">{html.escape(subtitle)}</div>
<div class="d">Built {date.today().isoformat()}</div></div>
{''.join(toc)}
{''.join(parts)}
<script>{JS}</script>
</body></html>"""


# --------------------------------------------------------------------------- pdf
def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    from playwright.sync_api import sync_playwright
    footer = ('<div style="font-size:8px;width:100%;text-align:center;color:#888;">'
              '<span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda m: m.type in ("error", "warning")
                and "No character metrics" not in m.text and print("  [browser]", m.text))
        page.goto(html_path.resolve().as_uri(), wait_until="load", timeout=0)
        page.evaluate("window.__bookReady")
        page.emulate_media(media="print")
        kw = dict(path=str(pdf_path), format="A4", print_background=True,
                  display_header_footer=True, header_template="<div></div>", footer_template=footer,
                  margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
        try:
            page.pdf(**kw, outline=True, tagged=True)  # bookmarks (Playwright >= 1.42)
        except TypeError:
            page.pdf(**kw)
        browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--course", action="append", metavar="NN",
                    help="include only this course number (repeatable), e.g. --course 01 --course 02")
    ap.add_argument("--no-solutions", action="store_true", help="remove <details> hint/solution blocks")
    ap.add_argument("--html-only", action="store_true", help="write the HTML and skip the PDF step")
    ap.add_argument("--out", type=Path, default=ROOT / "build" / "zemax-course.pdf", help="output PDF path")
    ap.add_argument("--assets", type=Path, default=ROOT / "tools" / ".cache",
                    help="folder with katex/ and mermaid/ (downloaded on first run if missing)")
    args = ap.parse_args()

    t0 = time.time()
    course_filter = [c.zfill(2) for c in args.course] if args.course else None
    assets = ensure_assets(args.assets)
    out_pdf = args.out.resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out_html = out_pdf.with_suffix(".html")
    out_html.write_text(build_html(course_filter, args.no_solutions, assets), encoding="utf-8")
    print(f"HTML: {out_html}")
    if not args.html_only:
        print("Rendering PDF (the full course takes a few minutes) ...")
        html_to_pdf(out_html, out_pdf)
        print(f"PDF:  {out_pdf}  ({out_pdf.stat().st_size / 1e6:.1f} MB)")
    print(f"Done in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
