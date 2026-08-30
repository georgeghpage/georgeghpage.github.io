# Personal site — CV + blog

Plain HTML/CSS on GitHub Pages, plus a local-only **dev terminal** for editing.
Live at https://georgeghpage.github.io

## Everyday use: the dev terminal

```bash
./dev.sh
```

Then open http://127.0.0.1:4173/dev — edit CV details (name, experience,
education, skills…), create / edit / delete blog posts, and **publish**
(git commit + push) from one page. Site preview runs at
http://127.0.0.1:4173/ next to it.

**Only you can use it:**
- the server binds to `127.0.0.1` — unreachable from the network
- every action requires a random per-start token that is injected into the
  page when the local server serves it
- `dev/` and `dev.sh` are gitignored — none of it exists on the public site

## How it fits together

| File | What it is |
|---|---|
| `site.json` | All CV content — the source of truth |
| `build.py` | Regenerates `index.html` from `site.json` (stdlib only) |
| `index.html` | **Generated** — don't hand-edit; use the dev terminal |
| `blog.html` | Blog index; new rows go under the `<!-- dev:new-posts -->` marker |
| `posts/` | One HTML file per post |
| `posts/_template.html` | Skeleton for new posts |
| `style.css` | The whole design, one file |
| `dev/`, `dev.sh` | Local dev terminal (gitignored, never published) |
| `new-post.sh` | CLI alternative for creating a post |

## Without the dev terminal

Edit `site.json`, then:

```bash
python3 build.py
git add -A && git commit -m "update cv" && git push
```

New post from the CLI:

```bash
./new-post.sh my-post-slug "My post title"
# then paste the printed row at the top of the list in blog.html
```

## First-time deploy (already done)

Repo must be named exactly `georgeghpage.github.io`; user sites publish
automatically from `main`, no Pages setting to toggle.

```bash
git init -b main && git add -A && git commit -m "initial"
gh repo create georgeghpage.github.io --public --source . --push
```

## PDF of the CV

Open the site and Print → Save as PDF. Print styles are handled
(nav hidden, tight margins, fits one page).
