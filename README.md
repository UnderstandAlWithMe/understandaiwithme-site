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

## Tracked partner links (/go/)

Every partner link on the site points to `/go/<slug>` instead of the raw affiliate URL. `functions/go/[offer].js` counts the click and redirects to the real link from `site.json` → `go_links` (copied into `lib/go-links.js` by `build.py`).

- To add an offer: add `"slug": "https://the-tracking-link"` to `go_links`, then give the tile or recommended item `"go": "slug"`. Run `python3 build.py` and push.
- Counting needs a KV namespace bound to the Pages project as `CLICKS` (one-time setup in Cloudflare). Without it, links still redirect but aren't counted.
- Counts are stored as `date|slug|page` → number. No IP addresses or personal data.
- impact.com links (`*.sjv.io`) also get `subId1=<source page tag>`, so impact.com commission reports show which page earned.
- `/go/` is blocked in robots.txt and the links carry `rel="sponsored nofollow"`.
- In a guide or money page, write partner links as `[text](/go/slug)`. `build.py` adds `rel="sponsored nofollow noopener"` and stops with an error if the slug isn't in `go_links`. `/go/` links are redirects, not built pages, so a link check should treat any slug listed in `go_links` as valid.

## Rules for content

- One useful guide beats five thin ones. Every guide must contain real steps from a video, live or genuine experience.
- Every guide points to exactly one tile.
- Every affiliate link keeps `rel="sponsored"` and the disclosure line.
- Never promote finance offers on TikTok; on the site, keep the "not financial advisers" note.
