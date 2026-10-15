#!/usr/bin/env python3
"""Rebuild 'Oportunidades de IA para empresas peruanas' from casos/casos.json.

Rewrites only:
  - inner HTML of div.opp-filters and div.opp-grid in proyectos.html
  - inner HTML of div.case-stack in index.html #casos (3 most recent)

NEVER prunes: the catalog accumulates. Idempotent: same JSON -> same HTML.
"""
from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = HERE / "casos.json"
POSTS = ROOT / "noticias" / "posts.json"
REQUIRED = ("slug", "date", "title", "categoria", "sector", "servicio", "excerpt", "image", "url", "tipo")
TIPOS = ("Oportunidad", "Caso real")
FORBIDDEN = ("durero", "san borja")


def es_date(iso: str) -> str:
    y, m, d = (int(p) for p in iso.split("-"))
    return f"{d} de {MESES[m - 1]}, {y}"


def key(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def replace_inner(doc: str, open_re: str, tag: str, new_inner: str) -> str:
    m = re.search(open_re, doc, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        raise SystemExit(f"No se encontró <{tag}> con el patrón {open_re!r}.")
    open_end = i = m.end()
    depth = 1
    ot, ct = f"<{tag}", f"</{tag}>"
    while i < len(doc):
        no, nc = doc.find(ot, i), doc.find(ct, i)
        if nc < 0:
            raise SystemExit(f"No se encontró el cierre </{tag}>.")
        if no != -1 and no < nc and doc[no + len(ot): no + len(ot) + 1] in " >\n\t/":
            depth += 1
            i = no + len(ot)
            continue
        depth -= 1
        if depth == 0:
            return doc[:open_end] + new_inner + doc[nc:]
        i = nc + len(ct)
    raise SystemExit(f"HTML mal formado alrededor de <{tag}>.")


def categorias() -> list[str]:
    """Categorías de Insights (noticias/posts.json), en orden de primera aparición."""
    posts = json.loads(POSTS.read_text(encoding="utf-8"))
    if isinstance(posts, dict):
        posts = posts.get("posts", [])
    out: list[str] = []
    for p in posts:
        c = p.get("category")
        if c and c not in out:
            out.append(c)
    if not out:
        raise SystemExit("noticias/posts.json no tiene categorías.")
    return sorted(out, key=key)


def load() -> list[dict]:
    cats = categorias()
    items = json.loads(DATA.read_text(encoding="utf-8"))
    if not isinstance(items, list) or not items:
        raise SystemExit("casos.json debe ser un arreglo no vacío.")
    seen = set()
    for i, it in enumerate(items):
        miss = [k for k in REQUIRED if not it.get(k)]
        if miss:
            raise SystemExit(f"Item {i} sin campos: {', '.join(miss)}")
        date.fromisoformat(it["date"])
        if it["categoria"] not in cats:
            raise SystemExit(f"Item {i}: categoria {it['categoria']!r} no es una categoría de Insights {cats}")
        if it["tipo"] not in TIPOS:
            raise SystemExit(f"Item {i}: tipo debe ser uno de {TIPOS}")
        if it["url"] in seen:
            raise SystemExit(f"URL duplicada: {it['url']}")
        seen.add(it["url"])
    return sorted(items, key=lambda x: (x["date"], x["url"]), reverse=True)


def check(items: list[dict]) -> None:
    errs = []
    for it in items:
        page, img = ROOT / it["url"], ROOT / it["image"]
        if not page.is_file():
            errs.append(f"falta página {page}")
        else:
            txt = page.read_text(encoding="utf-8")
            low = txt.lower()
            if any(f in low for f in FORBIDDEN):
                errs.append(f"{page.name}: contiene una dirección física prohibida")
            if f'<span class="cat">{e(it["categoria"])}</span>' not in txt:
                errs.append(f"{page.name}: article-meta debe mostrar la categoría {it['categoria']!r}")
            if it["tipo"] == "Oportunidad" and "escenario ilustrativo" not in txt:
                errs.append(f"{page.name}: falta el aviso 'Caso aplicable: escenario ilustrativo…'")
            for ref in re.findall(r'(?:href|src)="([^"#:]+?)(?:#[^"]*)?"', txt):
                if ref and not (ROOT / ref).exists():
                    errs.append(f"{page.name}: enlace roto {ref}")
        if not img.is_file():
            errs.append(f"falta imagen {img}")
    if errs:
        raise SystemExit("Errores:\n  " + "\n  ".join(errs))


def e(s: str) -> str:
    return html.escape(s, quote=True)


def filters(items: list[dict]) -> str:
    present = {it["categoria"] for it in items}
    sectors = [c for c in categorias() if c in present]
    out = ['\n          <button class="opp-chip is-active" type="button" data-filter="todos" aria-pressed="true">Todos</button>\n']
    for s in sectors:
        out.append(f'          <button class="opp-chip" type="button" data-filter="{key(s)}" aria-pressed="false">{e(s)}</button>\n')
    out.append("        ")
    return "".join(out)


def cards(items: list[dict]) -> str:
    out = ["\n"]
    for it in items:
        out.append(f"""          <a class="blog-card reveal" href="{e(it['url'])}" data-categoria="{key(it['categoria'])}">
            <img src="{e(it['image'])}" alt="{e(it.get('image_alt') or it['title'])}">
            <div class="blog-card-body">
              <p class="blog-card-meta"><span class="cat">{e(it['categoria'])}</span><span>{e(it['sector'])}</span><span>{e(it['tipo'])}</span><span>{e(es_date(it['date']))}</span></p>
              <h3>{e(it['title'])}</h3>
              <p>{e(it['excerpt'])}</p>
              <span class="more-link">Ver oportunidad</span>
            </div>
          </a>
""")
    out.append("        ")
    return "".join(out)


def home(items: list[dict]) -> str:
    out = ["\n"]
    for i, it in enumerate(items[:3], start=1):
        out.append(f"""          <a class="case-file reveal" href="{e(it['url'])}">
            <header class="case-meta">
              <p class="case-id">{e(it['tipo'])} {i:02d}</p>
              <p class="case-sector case-cat">{e(it['categoria'])}</p>
            </header>
            <div class="case-body">
              <h3>{e(it.get('home_title') or it['title'])}</h3>
              <p>{e(it['excerpt'])}</p>
              <span class="more-link">Ver oportunidad</span>
            </div>
            <p class="case-service">Sector: {e(it['sector'])} · Servicio: {e(it['servicio'])}</p>
          </a>
""")
    out.append("        ")
    return "".join(out)


def main() -> int:
    items = load()
    check(items)
    lp, ip = ROOT / "proyectos.html", ROOT / "index.html"
    lst, idx = lp.read_text(encoding="utf-8"), ip.read_text(encoding="utf-8")
    lst = replace_inner(lst, r'<div class="opp-filters"[^>]*>', "div", filters(items))
    lst = replace_inner(lst, r'<div class="blog-grid opp-grid">', "div", cards(items))
    idx = replace_inner(idx, r'<section class="casos" id="casos">.*?<div class="case-stack">', "div", home(items))
    for p, t in ((lp, lst), (ip, idx)):
        if p.read_text(encoding="utf-8") != t:
            p.write_text(t, encoding="utf-8")
    print(f"OK: {len(items)} oportunidades → proyectos.html; {min(3, len(items))} en index.html #casos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
