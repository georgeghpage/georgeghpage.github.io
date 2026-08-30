#!/usr/bin/env python3
"""Regenerate index.html from site.json — stdlib only, no dependencies.

Usage: python3 build.py
(The dev terminal — ./dev.sh — calls this automatically on save.)
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE_JSON = ROOT / "site.json"
OUT = ROOT / "index.html"

TEMPLATE = """<!DOCTYPE html>
<!-- Generated from site.json by build.py — do not edit by hand.
     Use ./dev.sh (local dev terminal) or edit site.json + run: python3 build.py -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{name}}</title>
  <meta name="description" content="{{name}} — {{tagline}}">
  <link rel="stylesheet" href="style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23ffd700'/></svg>">
</head>
<body>
  <div class="container">

    <header class="site-header">
      <a class="site-name" href="index.html">{{name}}</a>
      <nav class="site-nav">
        <a href="index.html" class="active">main</a>
        <a href="blog.html">blog</a>
      </nav>
    </header>

    <main>
      <div class="intro">
        <h1>{{name}}</h1>
        <p class="tagline">{{tagline}}</p>
        <div class="contact">
{{contact_links}}
        </div>
      </div>

      <section>
        <h2 class="section-title">About</h2>
        <p>{{about}}</p>
      </section>

      <section>
        <h2 class="section-title">Experience</h2>

{{experience}}
      </section>

      <section>
        <h2 class="section-title">Education</h2>

{{education}}
      </section>

      <section class="skills">
        <h2 class="section-title">Skills</h2>
{{skills}}
      </section>
    </main>

    <footer class="site-footer">
      {{footer}}
    </footer>

  </div>
</body>
</html>
"""


def esc(s):
    return html.escape(str(s or ""), quote=True)


def load_site():
    return json.loads(SITE_JSON.read_text(encoding="utf-8"))


def save_site(data):
    SITE_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _entry(e):
    desc = (e.get("desc") or "").strip()
    if "\n" in desc:
        items = "".join(
            f"\n            <li>{esc(line)}</li>"
            for line in desc.splitlines()
            if line.strip()
        )
        desc_html = f'\n          <ul class="entry-points">{items}\n          </ul>'
    elif desc:
        desc_html = f"\n          <p>{esc(desc)}</p>"
    else:
        desc_html = ""
    return f"""        <div class="entry">
          <div class="entry-head">
            <div>
              <span class="entry-title">{esc(e.get("title"))}</span>
              <span class="entry-org">· {esc(e.get("org"))}</span>
            </div>
            <span class="entry-date">{esc(e.get("date"))}</span>
          </div>{desc_html}
        </div>"""


def render_index(site):
    links = []
    if site.get("email"):
        links.append(f'          <a href="mailto:{esc(site["email"])}">email</a>')
    for key in ("github", "linkedin", "x"):
        url = (site.get("links") or {}).get(key, "")
        if url:
            links.append(f'          <a href="{esc(url)}">{key}</a>')

    replacements = {
        "{{name}}": esc(site.get("name")),
        "{{tagline}}": esc(site.get("tagline")),
        "{{about}}": esc(site.get("about")),
        "{{footer}}": esc(site.get("footer")),
        "{{contact_links}}": "\n".join(links),
        "{{experience}}": "\n\n".join(_entry(e) for e in site.get("experience", [])),
        "{{education}}": "\n\n".join(_entry(e) for e in site.get("education", [])),
        "{{skills}}": "\n".join(
            f'        <p><strong>{esc(s.get("label"))}</strong> — {esc(s.get("items"))}</p>'
            for s in site.get("skills", [])
        ),
    }
    out = TEMPLATE
    for token, value in replacements.items():
        out = out.replace(token, value)
    return out


def main():
    OUT.write_text(render_index(load_site()), encoding="utf-8")
    print(f"rebuilt {OUT.name} from {SITE_JSON.name}")


if __name__ == "__main__":
    main()
