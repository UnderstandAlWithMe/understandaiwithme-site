# understandaiwithme-site

Static site for UnderstandAIwithMe: the problem grid, matched fix pages, guides, disclosure and privacy pages.

## How it works

- `site.json` holds the site settings and the 10 grid tiles (label, matched page copy, offer).
- `guides/*.md` are the written guides. Each has front matter with `title`, `description`, `date` and `tile` (the grid tile it points to).
- `assets/style.css` is the stylesheet.
- `python3 build.py` regenerates everything into `public/`, including `sitemap.xml` and `robots.txt`.
- Cloudflare Pages serves `public/` directly (no build command needed). Every push to `main` goes live.

## Switching an offer on

When a partner approves, change that tile in `site.json`:

```json
"offer_type": "live",
"offer_url": "https://the-tracking-link"
```

Then run `python3 build.py` and push. Tiles marked `pending` send visitors to the email list until then.

## Rules for content

- One useful guide beats five thin ones. Every guide must contain real steps from a video, live or genuine experience.
- Every guide points to exactly one tile.
- Every affiliate link keeps `rel="sponsored"` and the disclosure line.
- Never promote finance offers on TikTok; on the site, keep the "not financial advisers" note.
