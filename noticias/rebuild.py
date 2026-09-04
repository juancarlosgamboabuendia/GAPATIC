#!/usr/bin/env python3
"""Rebuild Insights listings from noticias/posts.json.

Rewrites only:
  - the inner HTML of div.blog-grid in blog.html
  - the inner HTML of ul.notes in index.html #insights

Does not touch nav, footer, or article pages.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

MESES = (
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POSTS_PATH = HERE / "posts.json"


def format_es_date(iso: str) -> str:
    y, m, d = (int(p) for p in iso.split("-"))
    return f"{d} de {MESES[m - 1]}, {y}"


def replace_inner(doc: str, open_re: str, tag: str, new_inner: str) -> str:
    m = re.search(open_re, doc, flags=re.IGNORECASE)
    if not m:
        raise SystemExit(f"No se encontró <{tag}> con el patrón esperado.")
    open_end = m.end()
    i = open_end
    depth = 1
    open_token = f"<{tag}"
    close_token = f"</{tag}>"
    while i < len(doc) and depth:
        nxt_open = doc.find(open_token, i)
        nxt_close = doc.find(close_token, i)
        if nxt_close < 0:
            raise SystemExit(f"No se encontró el cierre </{tag}>.")
        is_real_open = False
        if nxt_open != -1 and nxt_open < nxt_close:
            after = doc[nxt_open + len(open_token) : nxt_open + len(open_token) + 1]
            is_real_open = after in " >\n\t/"
        if is_real_open:
            depth += 1
            i = nxt_open + len(open_token)
            continue
        depth -= 1
        if depth == 0:
            return doc[:open_end] + new_inner + doc[nxt_close:]
        i = nxt_close + len(close_token)
    raise SystemExit(f"HTML mal formado alrededor de <{tag}>.")


def blog_cards(posts: list[dict]) -> str:
    chunks = ["\n"]
    for post in posts:
        slug = html.escape(post["slug"], quote=True)
        img = html.escape(post["image"], quote=True)
        title = html.escape(post["title"])
        excerpt = html.escape(post["excerpt"])
        cat = html.escape(post["category"])
        when = html.escape(format_es_date(post["date"]))
        alt = html.escape(post.get("image_alt") or post["title"])
        chunks.append(
            f"""          <a class="blog-card reveal" href="{slug}">
            <img src="{img}" alt="{alt}">
            <div class="blog-card-body">
              <p class="blog-card-meta"><span class="cat">{cat}</span><span>{when}</span></p>
              <h3>{title}</h3>
              <p>{excerpt}</p>
              <span class="more-link">Leer</span>
            </div>
          </a>
"""
        )
    chunks.append("        ")
    return "".join(chunks)


def insight_notes(posts: list[dict]) -> str:
    latest = posts[:3]
    chunks = ["\n"]
    for i, post in enumerate(latest, start=1):
        slug = html.escape(post["slug"], quote=True)
        title = html.escape(post.get("note_title") or post["title"])
        excerpt = html.escape(post.get("note_excerpt") or post["excerpt"])
        kind = html.escape(post.get("note_kind") or "Laboratorio · lectura")
        chunks.append(
            f"""          <li>
            <a class="note reveal" href="{slug}">
              <p class="note-id">Nota {i:02d}</p>
              <h3>{title}</h3>
              <p>{excerpt}</p>
              <p class="note-kind">{kind}</p>
              <span class="more-link">Leer</span>
            </a>
          </li>
"""
        )
    chunks.append("        ")
    return "".join(chunks)



def prune_to_current_month(posts: list[dict]) -> list[dict]:
    """Keep only posts from the current America/Lima month; delete older HTML pages."""
    try:
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("America/Lima"))
    except Exception:
        now = datetime.utcnow()
    ym = f"{now.year:04d}-{now.month:02d}"
    keep, drop = [], []
    for post in posts:
        if str(post.get("date", "")).startswith(ym):
            keep.append(post)
        else:
            drop.append(post)
    for post in drop:
        page = ROOT / post["slug"]
        if page.is_file():
            page.unlink()
    if len(keep) != len(posts):
        POSTS_PATH.write_text(
            json.dumps(keep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return keep

def load_posts() -> list[dict]:
    posts = json.loads(POSTS_PATH.read_text(encoding="utf-8"))
    if not isinstance(posts, list) or not posts:
        raise SystemExit("posts.json debe ser un arreglo no vacío.")
    required = ("slug", "title", "date", "category", "excerpt", "image", "author")
    for i, post in enumerate(posts):
        missing = [k for k in required if k not in post]
        if missing:
            raise SystemExit(f"Post {i} sin campos: {', '.join(missing)}")
        date.fromisoformat(post["date"])
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    return posts


def assert_files(posts: list[dict]) -> None:
    missing = []
    for post in posts:
        page = ROOT / post["slug"]
        image = ROOT / post["image"]
        if not page.is_file():
            missing.append(str(page))
        if not image.is_file():
            missing.append(str(image))
    if missing:
        raise SystemExit("Faltan archivos referenciados:\n  " + "\n  ".join(missing))


def main() -> int:
    posts = load_posts()
    posts = prune_to_current_month(posts)
    if not posts:
        raise SystemExit("No quedan posts del mes actual.")
    assert_files(posts)

    blog_path = ROOT / "blog.html"
    index_path = ROOT / "index.html"
    blog = blog_path.read_text(encoding="utf-8")
    index = index_path.read_text(encoding="utf-8")

    blog = replace_inner(blog, r'<div class="blog-grid">', "div", blog_cards(posts))
    index = replace_inner(
        index, r'<ul class="notes" role="list">', "ul", insight_notes(posts)
    )

    blog_path.write_text(blog, encoding="utf-8")
    index_path.write_text(index, encoding="utf-8")
    print(f"OK: {len(posts)} posts → blog.html y 3 notas en index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
