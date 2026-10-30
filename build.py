"""Builds the static site into ./public from site.json and guides/*.md.

Run:  python3 build.py
No dependencies beyond the Python standard library.
"""
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "public"
CFG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
URL = CFG["site_url"].rstrip("/")
TODAY = date.today().isoformat()
e = html.escape

ICONS = {
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "pay": '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/>',
    "stack": '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 13 9 5 9-5"/>',
    "bank": '<path d="M3 10h18L12 4 3 10Z"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
    "flow": '<path d="M4 16c3-6 5 2 8-4s5 2 8-4"/><path d="M4 20h16"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3Z"/><path d="M9 8h6M9 12h6"/>',
    "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>',
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}


def icon(name):
    return (
        '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        + ICONS.get(name, ICONS["spark"])
        + "</svg>"
    )


def page(path, title, description, body, schema=None):
    canonical = URL + path
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="/style.css">
{ld}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="/">Understand<b>AI</b>withMe</a>
<nav><a href="/guides/">Guides</a><a href="/fix/build-ai-automation/">Get it built</a><a href="{CFG['youtube']}" rel="noopener">YouTube</a></nav>
</div></header>
<main>{body}</main>
<footer><div class="wrap">
<p><b>UnderstandAIwithMe</b> &middot; {e(CFG['tagline'])}</p>
<p class="small">Some links on this site are affiliate or referral links: we may earn a commission at no cost to you. <a href="/disclosure/">Disclosure</a> &middot; <a href="/privacy/">Privacy</a></p>
</div></footer>
</body>
</html>
"""
    target = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    if path.endswith(".html"):
        target = OUT / path.strip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    return path


def tile_card(t):
    cls = "tile featured" if t.get("featured") else "tile"
    return (
        f'<a class="{cls}" href="/fix/{t["slug"]}/">{icon(t["icon"])}'
        f'<span>{e(t["label"])}</span></a>'
    )


def offer_block(t):
    signup = CFG["email_signup_url"]
    kind = t["offer_type"]
    if kind == "live":
        return (
            f'<div class="offer"><p>Our pick: <b>{e(t["offer_name"])}</b>.</p>'
            f'<a class="btn" href="{e(t["offer_url"])}" rel="sponsored noopener">{e(t["cta"])}</a>'
            '<p class="small">Affiliate link: we may earn a commission at no cost to you.</p></div>'
        )
    if kind == "enquiry":
        return enquiry_form()
    if kind == "email":
        return (
            f'<div class="offer"><a class="btn" href="{signup}">{e(t["cta"])}</a>'
            '<p class="small">Free. Unsubscribe any time.</p></div>'
        )
    # pending: partner not yet approved -> capture the visitor instead
    return (
        f'<div class="offer"><p>We are finalising our recommended provider for this. '
        f'Join the free list and we will send you the one we trust, plus a short checklist.</p>'
        f'<a class="btn" href="{signup}">Send me the recommendation</a>'
        '<p class="small">Free. Unsubscribe any time.</p></div>'
    )


def enquiry_form():
    action = CFG.get("enquiry_form_action", "")
    disabled = "" if action else " disabled"
    note = (
        ""
        if action
        else f'<p class="small">Enquiries open shortly. Meanwhile, <a href="{CFG["email_signup_url"]}">join the list</a> and we will be in touch.</p>'
    )
    return f"""<form class="offer form" method="post" action="{e(action)}">
<p>Describe the task. We pass an anonymous summary to a vetted AI automation partner, who replies with whether it fits and a rough estimate. No obligation.</p>
<input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<label>Your name<input name="name" required{disabled}></label>
<label>Work email<input type="email" name="email" required{disabled}></label>
<label>Team size<select name="team_size"{disabled}><option>1-10</option><option>11-50</option><option>51-200</option><option>200+</option></select></label>
<label>The task you want automated<textarea name="task" rows="4" required{disabled}></textarea></label>
<label>Hours it takes per week (rough)<input name="hours"{disabled}></label>
<label>Budget, if known<select name="budget"{disabled}><option>Not sure yet</option><option>Under £5k</option><option>£5k-£15k</option><option>£15k-£50k</option><option>£50k+</option></select></label>
<label>When do you need it?<select name="timing"{disabled}><option>This month</option><option>Next 3 months</option><option>Just exploring</option></select></label>
<button class="btn" type="submit"{disabled}>Send my enquiry</button>
<p class="small">We only use your details to respond to this enquiry. We may earn a referral fee from the partner. See <a href="/privacy/">Privacy</a>.</p>
{note}
</form>"""


def build_tile_pages():
    paths = []
    tiles = CFG["tiles"]
    for t in tiles:
        tips = "".join(f"<li>{e(x)}</li>" for x in t["tips"])
        finance = (
            '<p class="small">We are not financial advisers. Check the provider\'s terms and costs before applying.</p>'
            if t.get("finance")
            else ""
        )
        others = "".join(tile_card(o) for o in tiles if o["slug"] != t["slug"])[:]
        body = f"""<section class="hero narrow"><div class="wrap">
<p class="eyebrow"><a href="/">&larr; Back to all problems</a></p>
<h1>{e(t["headline"])}</h1>
<p class="lead">{e(t["intro"])}</p>
</div></section>
<section class="wrap narrow">
<h2>Three things to do first</h2>
<ol class="tips">{tips}</ol>
<h2>The fastest fix</h2>
{offer_block(t)}
{finance}
</section>
<section class="wrap"><h2 class="muted">Something else eating your time?</h2><div class="grid small-grid">{others}</div></section>"""
        paths.append(page(f"/fix/{t['slug']}/", f"{t['short']}: the fastest fix | UnderstandAIwithMe", t["intro"][:155], body))
    return paths


def build_home():
    grid = "".join(tile_card(t) for t in CFG["tiles"])
    body = f"""<section class="hero"><div class="wrap">
<p class="eyebrow">For UK small businesses and busy professionals</p>
<h1>What&rsquo;s eating your time this week?</h1>
<p class="lead">Pick one. You&rsquo;ll get a short, practical fix: an AI workflow, the right tool, or the right person.</p>
<div class="grid">{grid}</div>
</div></section>
<section class="wrap split">
<div><h2>Practical AI for real work</h2>
<p>I&rsquo;m Constantin. I build AI workflows for real teams and explain them in plain English on <a href="{CFG['youtube']}" rel="noopener">YouTube</a> and <a href="{CFG['tiktok']}" rel="noopener">TikTok</a>. This site turns those videos into step-by-step guides, and points you to tools I&rsquo;d actually use.</p>
<p><a class="btn ghost" href="/guides/">Read the guides</a></p></div>
<div class="card"><h3>Not sure where to start?</h3><p>Join the free list for a short series on finding the admin tasks that cost you most.</p><a class="btn" href="{CFG['email_signup_url']}">Get the free series</a></div>
</section>"""
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": CFG["site_name"],
        "url": URL + "/",
    }
    return page("/", "UnderstandAIwithMe | Practical AI and tools to cut admin", "Pick your biggest admin problem and get a practical fix: an AI workflow, the right software, or the right person. For UK small businesses.", body, schema)


def md_to_html(md):
    out, in_list = [], None
    for line in md.splitlines():
        s = line.rstrip()
        m_ul = re.match(r"^[-*] (.+)", s)
        m_ol = re.match(r"^\d+\. (.+)", s)
        kind = "ul" if m_ul else "ol" if m_ol else None
        if in_list and kind != in_list:
            out.append(f"</{in_list}>")
            in_list = None
        if kind:
            if not in_list:
                out.append(f"<{kind}>")
                in_list = kind
            out.append(f"<li>{inline((m_ul or m_ol).group(1))}</li>")
        elif s.startswith("### "):
            out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("## "):
            out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s:
            out.append(f"<p>{inline(s)}</p>")
    if in_list:
        out.append(f"</{in_list}>")
    return "\n".join(out)


def inline(s):
    s = e(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return s


def build_guides():
    """Guides are guides/<slug>.md with a front-matter block:
    ---
    title: ...
    description: ...
    date: YYYY-MM-DD
    tile: <tile slug the guide points to>
    ---
    """
    gdir = ROOT / "guides"
    guides, paths = [], []
    tiles = {t["slug"]: t for t in CFG["tiles"]}
    for f in sorted(gdir.glob("*.md")) if gdir.exists() else []:
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            continue
        meta = dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)
        slug = f.stem
        t = tiles.get(meta.get("tile", "not-sure"), tiles["not-sure"])
        cta = f'<div class="card cta"><h3>{e(t["label"])}?</h3><p>{e(t["intro"])}</p><a class="btn" href="/fix/{t["slug"]}/">See the fastest fix</a></div>'
        body = f"""<article class="wrap narrow guide">
<p class="eyebrow"><a href="/guides/">Guides</a> &middot; {e(meta.get('date',''))}</p>
<h1>{e(meta['title'])}</h1>
{md_to_html(m.group(2))}
{cta}
</article>"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": meta["title"],
            "datePublished": meta.get("date", TODAY),
            "author": {"@type": "Person", "name": "Constantin"},
        }
        paths.append(page(f"/guides/{slug}/", meta["title"] + " | UnderstandAIwithMe", meta.get("description", ""), body, schema))
        guides.append((meta.get("date", ""), slug, meta))
    guides.sort(reverse=True)
    items = "".join(
        f'<li><a href="/guides/{s}/"><b>{e(mt["title"])}</b></a><br><span class="small">{e(mt.get("description",""))}</span></li>'
        for _, s, mt in guides
    ) or "<li>First guides are on the way.</li>"
    paths.append(page("/guides/", "Guides | UnderstandAIwithMe", "Practical, plain-English guides to using AI and better tools at work.", f'<section class="wrap narrow"><h1>Guides</h1><ul class="guides">{items}</ul></section>'))
    return paths


def build_legal():
    disclosure = """<section class="wrap narrow"><h1>Affiliate disclosure</h1>
<p>Some links on this site are affiliate or referral links. If you sign up, book a demo or buy through them, we may earn a commission or referral fee. It costs you nothing extra.</p>
<p>We only recommend tools and partners we believe fit the problem described. Commission never changes the price you pay.</p>
<p>We are not financial advisers. Finance products are subject to the provider's own eligibility checks and terms.</p></section>"""
    privacy = """<section class="wrap narrow"><h1>Privacy</h1>
<p><b>What we collect:</b> if you join our email list or send an enquiry, we store the details you give us (such as your name, email and the task you describe).</p>
<p><b>Why:</b> to send you the emails you asked for, or to respond to your enquiry. For build enquiries we share an anonymous summary with a vetted partner first; we only share your company details with your agreement.</p>
<p><b>Your rights:</b> you can unsubscribe at any time from any email, and ask us to see or delete your data by replying to any of our emails.</p>
<p>This site does not use advertising cookies. Affiliate partners may set their own cookies when you click through to their sites.</p></section>"""
    return [
        page("/disclosure/", "Affiliate disclosure | UnderstandAIwithMe", "How UnderstandAIwithMe earns money from affiliate and referral links.", disclosure),
        page("/privacy/", "Privacy | UnderstandAIwithMe", "How UnderstandAIwithMe handles your data.", privacy),
    ]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "assets" / "style.css", OUT / "style.css")
    paths = [build_home()] + build_tile_pages() + build_guides() + build_legal()
    page("/fix/build-ai-automation/thanks/", "Enquiry received | UnderstandAIwithMe", "Your enquiry has been received.", '<section class="wrap narrow hero"><h1>Thanks, your enquiry is in</h1><p class="lead">We will review it and send an anonymous summary to our AI automation partner. Expect a reply by email within two working days with whether it fits and a rough estimate.</p><p><a class="btn ghost" href="/guides/">Read the guides meanwhile</a></p></section>')
    page("/fix/build-ai-automation/error/", "Something went wrong | UnderstandAIwithMe", "The enquiry could not be sent.", '<section class="wrap narrow hero"><h1>Sorry, that did not go through</h1><p class="lead">Please go back and try again in a minute. If it keeps failing, <a href="'+CFG["email_signup_url"]+'">join the list</a> and reply to the first email with your task.</p></section>')
    page("/404.html", "Page not found | UnderstandAIwithMe", "Page not found.", '<section class="wrap narrow"><h1>Page not found</h1><p><a href="/">Back to the start</a></p></section>')
    urls = "".join(f"<url><loc>{URL}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in paths)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(paths)} pages into {OUT}")


if __name__ == "__main__":
    main()
