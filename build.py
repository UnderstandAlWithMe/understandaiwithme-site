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
VERSION = TODAY.replace("-", "")
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


def page(path, title, description, body, schema=None, og_type="website", extra=""):
    canonical = URL + path
    schemas = schema if isinstance(schema, list) else ([schema] if schema else [])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in schemas)
    t = {x["slug"]: x for x in CFG["tiles"]}
    foot_problems = "".join(
        f'<a href="/fix/{s}/">{e(t[s]["short"])}</a>'
        for s in ["build-ai-automation", "payroll-takes-forever", "cash-flow", "need-an-accountant", "receipts-and-expenses"]
    )
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0f766e">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:site_name" content="{e(CFG['site_name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:image" content="{URL}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{URL}/og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="/style.css?v={VERSION}">
{ld}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="/"><img src="/favicon.svg" width="30" height="30" alt="" style="border-radius:8px"><span>Understand<b>AI</b>withMe</span></a>
<nav aria-label="Main"><a href="/tools/">Free tools</a><a href="/guides/">Guides</a><a href="/about/">About</a><a class="nav-cta" href="/fix/build-ai-automation/">Get it built</a></nav>
</div></header>
<main>{body}</main>
<footer><div class="wrap">
<div class="cols">
<div><b>UnderstandAIwithMe</b><p>{e(CFG['tagline'])} Practical fixes for the admin that eats your week.</p>
<p><a href="{CFG['youtube']}" rel="noopener">YouTube</a> &middot; <a href="{CFG['tiktok']}" rel="noopener">TikTok</a></p></div>
<div><b>Fix a problem</b>{foot_problems}<a href="/">All problems</a></div>
<div><b>Site</b><a href="/tools/admin-time-calculator/">Admin time calculator</a><a href="/tools/ai-readiness-quiz/">AI readiness quiz</a><a href="/guides/">Guides</a><a href="/about/">About</a><a href="/disclosure/">Disclosure</a><a href="/privacy/">Privacy</a></div>
</div>
<p class="small">Some links on this site are affiliate or referral links: we may earn a commission at no cost to you. We are not financial advisers. &copy; {date.today().year} UnderstandAIwithMe</p>
</div></footer>
{extra}
</body>
</html>
"""
    target = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    if path.endswith(".html"):
        target = OUT / path.strip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    return path


def crumbs(*items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": URL + u}
            for i, (n, u) in enumerate([("Home", "/")] + list(items))
        ],
    }


ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": CFG["site_name"],
    "url": URL + "/",
    "logo": URL + "/apple-touch-icon.png",
    "sameAs": [CFG["youtube"], CFG["tiktok"]],
}


def tile_card(t):
    cls = "tile featured" if t.get("featured") else "tile"
    return (
        f'<a class="{cls}" href="/fix/{t["slug"]}/">{icon(t["icon"])}'
        + ('<span class="tag">Done for you</span>' if t.get("featured") else "")
        + f'<span>{e(t["label"])}</span></a>'
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
        related = [g for g in GUIDES if g[2].get("tile") == t["slug"]]
        rel_html = ""
        if related:
            items = "".join(f'<li><a class="g" href="/guides/{s}/"><b>{e(m["title"])}</b><span>{e(m.get("description",""))}</span></a></li>' for _, s, m, _ in related[:3])
            rel_html = f'<h2>Read next</h2><ul class="guides">{items}</ul>'
        others = "".join(tile_card(o) for o in tiles if o["slug"] != t["slug"])
        body = f"""<section class="hero narrow"><div class="wrap">
<p class="eyebrow"><a href="/">&larr; All problems</a></p>
<h1>{e(t["headline"])}</h1>
<p class="lead">{e(t["intro"])}</p>
</div></section>
<section class="wrap narrow">
<h2>Three things to do first</h2>
<ol class="tips">{tips}</ol>
<h2>The fastest fix</h2>
{offer_block(t)}
{finance}
<p class="small">Not sure this is your biggest time sink? <a href="/tools/admin-time-calculator/">Work out where your admin hours go</a> in two minutes.</p>
{rel_html}
</section>
<section class="wrap"><h2 class="muted">Something else eating your time?</h2><div class="grid small-grid">{others}</div></section>"""
        paths.append(page(f"/fix/{t['slug']}/", f"{t['short']}: the fastest fix | UnderstandAIwithMe", t["intro"][:155], body, crumbs((t["short"], f"/fix/{t['slug']}/"))))
    return paths


def build_home():
    grid = "".join(tile_card(t) for t in CFG["tiles"])
    latest = "".join(
        f'<li><a class="g" href="/guides/{s}/"><b>{e(m["title"])}</b><span>{e(m.get("description",""))}</span></a></li>'
        for _, s, m, _ in GUIDES[:3]
    )
    body = f"""<section class="hero home"><div class="wrap">
<a class="pill" href="/tools/admin-time-calculator/"><span class="dot"></span>New: free admin time calculator &rarr;</a>
<h1>What&rsquo;s eating your <em>time</em> this week?</h1>
<p class="lead">Pick your biggest admin headache. You&rsquo;ll get a short, practical fix: an AI workflow, the right tool, or the right person. Built for UK small businesses.</p>
<div class="actions"><a class="btn" href="/tools/admin-time-calculator/">Calculate my admin hours</a><a class="btn ghost" href="/tools/ai-readiness-quiz/">Take the 2-minute AI quiz</a></div>
<div class="grid">{grid}</div>
</div></section>
<section class="band"><div class="wrap">
<p class="eyebrow">How it works</p>
<h2>From &ldquo;where does my week go?&rdquo; to fixed, in three steps</h2>
<div class="steps">
<div class="step"><h3>Spot the time sink</h3><p>Pick a problem above, or use the calculator to see which admin task costs you most per year.</p></div>
<div class="step"><h3>Get the practical fix</h3><p>Three plain-English steps you can do today, plus the one tool or partner we&rsquo;d actually use.</p></div>
<div class="step"><h3>Automate what&rsquo;s left</h3><p>For bigger jobs, describe the task and a vetted AI automation partner replies with a rough estimate.</p></div>
</div></div></section>
<section class="wrap">
<p class="eyebrow">Free tools</p>
<h2>Two minutes, real numbers</h2>
<div class="tools">
<a class="tool-card" href="/tools/admin-time-calculator/"><span class="kicker">Calculator</span><h3>Admin time calculator</h3><p>Enter rough hours for invoicing, payroll, receipts and emails. See what admin costs you each year and what to fix first.</p><span class="go">Work it out &rarr;</span></a>
<a class="tool-card" href="/tools/ai-readiness-quiz/"><span class="kicker">Quiz</span><h3>Is your business ready for AI?</h3><p>Eight quick questions. Get a readiness score and the single next step that makes sense for you.</p><span class="go">Take the quiz &rarr;</span></a>
</div>
</section>
<section class="wrap">
<p class="eyebrow">Latest guides</p>
<h2>Plain-English, step by step</h2>
<ul class="guides">{latest}</ul>
<p><a href="/guides/">All guides &rarr;</a></p>
</section>
<section class="wrap split" style="margin-top:32px">
<div><img class="photo" src="/constantin-160.webp" width="88" height="88" alt="Constantin" loading="lazy"><p class="eyebrow">Who&rsquo;s behind this</p><h2 style="margin-top:0">Practical AI for real work</h2>
<p>I&rsquo;m Constantin. I build AI workflows and explain them in plain English on <a href="{CFG['youtube']}" rel="noopener">YouTube</a> and <a href="{CFG['tiktok']}" rel="noopener">TikTok</a>. This site turns those videos into step-by-step guides, and points you to tools I&rsquo;d actually use.</p>
<p><a class="btn ghost" href="/about/">More about this site</a></p></div>
<div class="card signup"><h3>Not sure where to start?</h3><p>Join the free list for a short series on finding the admin tasks that cost you most, and what to fix first.</p><a class="btn" href="{CFG['email_signup_url']}">Get the free series</a><p class="small">Free. Unsubscribe any time.</p></div>
</section>"""
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": CFG["site_name"], "url": URL + "/"},
        ORG,
    ]
    return page("/", "UnderstandAIwithMe | Practical AI and tools to cut admin", "Pick your biggest admin problem and get a practical fix: an AI workflow, the right software, or the right person. Free admin time calculator and AI readiness quiz for UK small businesses.", body, schema)


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
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return s


GUIDES = []  # (date, slug, meta, body_md), newest first


def load_guides():
    """Guides are guides/<slug>.md with a front-matter block:
    ---
    title: ...
    description: ...
    date: YYYY-MM-DD
    tile: <tile slug the guide points to>
    ---
    """
    gdir = ROOT / "guides"
    for f in sorted(gdir.glob("*.md")) if gdir.exists() else []:
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            continue
        meta = dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)
        GUIDES.append((meta.get("date", ""), f.stem, meta, m.group(2)))
    GUIDES.sort(key=lambda g: (g[0], g[1]), reverse=True)


def build_guides():
    paths = []
    tiles = {t["slug"]: t for t in CFG["tiles"]}
    for d, slug, meta, md in GUIDES:
        t = tiles.get(meta.get("tile", "not-sure"), tiles["not-sure"])
        words = len(md.split())
        mins = max(2, round(words / 220))
        cta = f'<div class="card cta"><p class="eyebrow" style="color:#7dd3c8">Your next step</p><h3>{e(t["label"])}?</h3><p>{e(t["intro"])}</p><a class="btn" href="/fix/{t["slug"]}/">See the fastest fix</a></div>'
        more = "".join(
            f'<li><a class="g" href="/guides/{s}/"><b>{e(m["title"])}</b><span>{e(m.get("description",""))}</span></a></li>'
            for _, s, m, _ in [g for g in GUIDES if g[1] != slug][:3]
        )
        body = f"""<article class="wrap narrow guide" style="padding-top:44px">
<p class="eyebrow"><a href="/guides/">Guides</a></p>
<h1>{e(meta['title'])}</h1>
<p class="meta">By <a href="/about/">Constantin</a> &middot; {e(d)} &middot; {mins} min read</p>
{md_to_html(md)}
{cta}
<p class="small">Want numbers for your own business? Try the <a href="/tools/admin-time-calculator/">admin time calculator</a> or the <a href="/tools/ai-readiness-quiz/">AI readiness quiz</a>.</p>
<h2>More guides</h2>
<ul class="guides">{more}</ul>
</article>"""
        schema = [
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": meta["title"],
                "description": meta.get("description", ""),
                "datePublished": d or TODAY,
                "dateModified": meta.get("updated", d or TODAY),
                "image": URL + "/og.png",
                "mainEntityOfPage": URL + f"/guides/{slug}/",
                "author": {"@type": "Person", "name": "Constantin", "url": URL + "/about/"},
                "publisher": {"@type": "Organization", "name": CFG["site_name"], "logo": {"@type": "ImageObject", "url": URL + "/apple-touch-icon.png"}},
            },
            crumbs(("Guides", "/guides/"), (meta["title"], f"/guides/{slug}/")),
        ]
        paths.append(page(f"/guides/{slug}/", meta["title"] + " | UnderstandAIwithMe", meta.get("description", ""), body, schema, og_type="article"))
    items = "".join(
        f'<li><a class="g" href="/guides/{s}/"><b>{e(mt["title"])}</b><span>{e(mt.get("description",""))} &middot; {e(d)}</span></a></li>'
        for d, s, mt, _ in GUIDES
    ) or "<li>First guides are on the way.</li>"
    paths.append(page("/guides/", "Guides: practical AI and admin fixes | UnderstandAIwithMe", "Practical, plain-English guides to using AI and better tools to cut admin in a UK small business.", f'<section class="hero narrow"><div class="wrap"><p class="eyebrow">Guides</p><h1>Plain-English guides to cutting admin</h1><p class="lead">Step-by-step, no jargon. Each guide ends with the one fix we&rsquo;d try first.</p></div></section><section class="wrap narrow"><ul class="guides">{items}</ul></section>', crumbs(("Guides", "/guides/"))))
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


CALC_TASKS = [
    ("cash-flow", "Invoicing and chasing payments", "Raising invoices, sending reminders, matching payments"),
    ("payroll-takes-forever", "Payroll, rotas and HR paperwork", "Pay runs, holiday requests, contracts, new starters"),
    ("receipts-and-expenses", "Receipts and expenses", "Collecting receipts, expense claims, reconciling cards"),
    ("need-an-accountant", "Bookkeeping and tax prep", "Categorising transactions, VAT, getting ready for year-end"),
    ("build-ai-automation", "Repetitive emails, quotes and reports", "Same-shape emails, quotes, weekly reports, data entry"),
    ("too-many-tools", "Re-keying data between tools", "Copying the same info between apps and spreadsheets"),
]

QUIZ = [
    ("Where does most of your business information live?", [("On paper or in people's heads", 0), ("In spreadsheets", 1), ("In a few cloud apps", 2), ("In cloud apps that talk to each other", 3)]),
    ("Do you have tasks that follow the same steps every time?", [("Not really", 0), ("One or two", 1), ("Several a week", 2), ("Lots, every day", 3)]),
    ("Could you write down, step by step, how one of those tasks is done?", [("No, it changes every time", 0), ("Roughly", 1), ("Yes, easily", 2), ("It's already documented", 3)]),
    ("How do you use AI tools like ChatGPT or Claude today?", [("Never tried them", 0), ("Tried once or twice", 1), ("Most weeks", 2), ("Every day, for real work", 3)]),
    ("How do you write customer emails and quotes?", [("From scratch every time", 0), ("Copy and edit an old one", 1), ("Mostly from templates", 2), ("Templates plus some automation", 3)]),
    ("What do you use for your accounts?", [("Nothing formal yet", 0), ("A spreadsheet", 1), ("Accounting software, entered by hand", 2), ("Accounting software linked to the bank", 3)]),
    ("Roughly how many hours a week go on admin across the team?", [("Under 2", 0), ("2 to 5", 1), ("5 to 10", 2), ("More than 10", 3)]),
]


def build_tools():
    tiles = {t["slug"]: t for t in CFG["tiles"]}
    rows = "".join(
        f'<div class="row"><label for="t-{slug}">{e(lbl)}<span>{e(hint)}</span></label>'
        f'<input id="t-{slug}" type="number" inputmode="decimal" min="0" step="0.5" placeholder="0" data-task="{slug}" data-label="{e(lbl)}" data-short="{e(tiles[slug]["short"])}"></div>'
        for slug, lbl, hint in CALC_TASKS
    )
    calc_body = f"""<section class="hero narrow"><div class="wrap">
<p class="eyebrow"><a href="/tools/">Free tools</a></p>
<h1>Admin time calculator</h1>
<p class="lead">How many hours, and how much money, does admin really cost your business each year? Enter rough numbers. Nothing you type leaves your browser.</p>
</div></section>
<section class="wrap narrow">
<form id="calc" class="tool" novalidate>
<div class="row"><label for="people">People doing admin<span>Including you</span></label><input id="people" name="people" type="number" inputmode="numeric" min="1" step="1" value="1"></div>
<div class="row"><label for="rate">Cost of an hour (&pound;)<span>Your hourly rate, or wage plus overheads</span></label><input id="rate" name="rate" type="number" inputmode="decimal" min="0" step="1" value="25"></div>
<h3 style="margin:22px 0 4px">Hours per person, per week</h3>
{rows}
<button class="btn" type="submit" style="margin-top:18px">Show my results</button>
<div id="calc-out" class="result hidden" aria-live="polite">
<p>Every year, admin takes about</p>
<div class="big" data-o="hours">0 hours</div>
<p>costing roughly <b data-o="cost"></b></p>
<div class="stats">
<div class="stat"><b data-o="weekly"></b><span>per week across the team</span></div>
<div class="stat"><b data-o="days"></b><span>working days a year</span></div>
<div class="stat"><b data-o="saved"></b><span>back each year if you cut it by 40%</span></div>
</div>
<p>Biggest time sink: <b data-o="top"></b></p>
<div class="bar"><i data-o="topshare" style="width:0"></i></div>
<p class="small" style="color:rgba(255,255,255,.7)" data-o="toppct"></p>
<a class="btn" data-o="fix" href="/">See the fastest fix</a>
<p class="small" style="color:rgba(255,255,255,.7);margin-top:14px">Want a plan for the rest? <a href="{CFG['email_signup_url']}">Get the free admin-time series</a>.</p>
</div>
</form>
<h2>How the numbers work</h2>
<p>Yearly hours = hours per person per week &times; people &times; 46 working weeks (52 minus holidays and bank holidays). Cost = yearly hours &times; your hourly cost. The &ldquo;cut by 40%&rdquo; figure is an illustration, not a promise: how much you save depends on the task and the fix.</p>
<p>If you are not sure of the hourly cost, use what you would pay someone else to do the work, or your own charge-out rate. For staff, wage plus around 20 to 30% for employer costs is a reasonable starting point.</p>
<h2>What to do with the result</h2>
<ol class="tips"><li>Start with the biggest time sink only. Fixing one thing properly beats tinkering with five.</li><li>Check whether the task needs a tool (software), a process (a template or checklist) or a person.</li><li>Re-run the calculator in a month to see what changed.</li></ol>
</section>"""
    app = lambda name, desc, path: {
        "@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": desc,
        "url": URL + path, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"},
    }
    paths = [page("/tools/admin-time-calculator/", "Admin Time Calculator: what does admin cost your business? | UnderstandAIwithMe",
                  "Free calculator for UK small businesses: see how many hours and pounds admin costs you each year, and which task to fix first.",
                  calc_body, [app("Admin time calculator", "See how many hours and how much money admin costs your business each year.", "/tools/admin-time-calculator/"), crumbs(("Free tools", "/tools/"), ("Admin time calculator", "/tools/admin-time-calculator/"))],
                  extra='<script src="/tools.js?v=' + VERSION + '" defer></script>')]

    qhtml = ""
    for i, (q, opts) in enumerate(QUIZ):
        o = "".join(f'<label><input type="radio" name="q{i}" value="{v}"> {e(t)}</label>' for t, v in opts)
        qhtml += f'<fieldset class="q" style="border:0;margin:0;padding:18px 0"><h3>{i+1}. {e(q)}</h3><div class="opts">{o}</div></fieldset>'
    pain = "".join(
        f'<label><input type="radio" name="pain" value="{t["slug"]}" data-short="{e(t["short"])}"> {e(t["label"])}</label>'
        for t in CFG["tiles"]
    )
    qhtml += f'<fieldset class="q" style="border:0;margin:0;padding:18px 0"><h3>{len(QUIZ)+1}. Which of these would you fix first?</h3><div class="opts">{pain}</div></fieldset>'
    total = len(QUIZ) + 1
    quiz_body = f"""<section class="hero narrow"><div class="wrap">
<p class="eyebrow"><a href="/tools/">Free tools</a></p>
<h1>Is your business ready for AI?</h1>
<p class="lead">{total} quick questions, about two minutes. You get a readiness score and the one next step that makes sense for you. Nothing is stored or sent anywhere.</p>
</div></section>
<section class="wrap narrow">
<form id="quiz" class="tool" novalidate>
<div class="progress"><span id="quiz-count">0 of {total} answered</span><div class="bar"><i id="quiz-bar" style="width:0"></i></div></div>
{qhtml}
<button class="btn" type="submit" style="margin-top:12px">See my result</button>
<div id="quiz-out" class="result hidden" aria-live="polite">
<p>Your AI readiness score</p>
<div class="big" data-o="score">0/100</div>
<div class="bar"><i data-o="bar" style="width:0"></i></div>
<div data-band="basics"><h3 style="margin-top:16px">Start with the basics</h3><p>AI works best on tidy, repeatable work. Your quickest wins are simpler: get information out of paper and heads into one place, and pick one tool for money in and out. Then AI has something to work with.</p></div>
<div data-band="quick"><h3 style="margin-top:16px">Ready for quick wins</h3><p>You have repeatable tasks and some systems in place. Pick one task you could write down step by step, and use AI or a better tool on that alone for a month. Expect hours back, not a revolution.</p></div>
<div data-band="ready"><h3 style="margin-top:16px">Ready to automate</h3><p>Your processes are clear and your tools are connected. A small custom AI workflow, built around one high-volume task, is likely to pay back quickly. Start with a scoped pilot rather than a big project.</p></div>
<a class="btn" data-o="fix" href="/">Your next step</a>
<p class="small" style="color:rgba(255,255,255,.7);margin-top:14px">Want the numbers? Try the <a href="/tools/admin-time-calculator/">admin time calculator</a>.</p>
</div>
</form>
<h2>What &ldquo;ready for AI&rdquo; actually means</h2>
<p>Being ready has less to do with technology than with how repeatable your work is. A task that follows the same steps every time, with information already in a digital tool, is a good candidate. A task that changes every time, or lives in someone&rsquo;s head, needs a process before it needs AI.</p>
<p>A low score is useful too: it tells you that a simple tool or a checklist will save more time right now than any AI project.</p>
</section>"""
    paths.append(page("/tools/ai-readiness-quiz/", "Is Your Business Ready for AI? Free 2-Minute Quiz | UnderstandAIwithMe",
                      "Free quiz for small businesses: get an AI readiness score and the one practical next step that fits your business.",
                      quiz_body, [app("AI readiness quiz", "Score how ready your business is to use AI and get one practical next step.", "/tools/ai-readiness-quiz/"), crumbs(("Free tools", "/tools/"), ("AI readiness quiz", "/tools/ai-readiness-quiz/"))],
                      extra='<script src="/tools.js?v=' + VERSION + '" defer></script>'))

    index = """<section class="hero narrow"><div class="wrap"><p class="eyebrow">Free tools</p><h1>Free tools to find your time back</h1><p class="lead">Quick, private, no sign-up. Everything runs in your browser.</p></div></section>
<section class="wrap narrow"><div class="tools">
<a class="tool-card" href="/tools/admin-time-calculator/"><span class="kicker">Calculator</span><h3>Admin time calculator</h3><p>See how many hours and pounds admin costs you each year, and which task to fix first.</p><span class="go">Work it out &rarr;</span></a>
<a class="tool-card" href="/tools/ai-readiness-quiz/"><span class="kicker">Quiz</span><h3>Is your business ready for AI?</h3><p>A readiness score and the one next step that makes sense for you.</p><span class="go">Take the quiz &rarr;</span></a>
</div></section>"""
    paths.append(page("/tools/", "Free tools for small business admin | UnderstandAIwithMe", "Free, private tools for UK small businesses: an admin time calculator and an AI readiness quiz.", index, crumbs(("Free tools", "/tools/"))))
    return paths


def build_about():
    body = f"""<section class="hero narrow"><div class="wrap">
<p class="eyebrow">About</p>
<h1>Practical AI for real work. No coding, no hype.</h1>
<p class="lead">UnderstandAIwithMe helps small businesses and busy professionals get hours back from admin, using AI where it genuinely helps and better tools or people where it doesn&rsquo;t.</p>
</div></section>
<section class="wrap narrow">
<div class="card" style="margin-top:8px"><img class="photo" src="/constantin-400.webp" width="120" height="120" alt="Constantin, founder of UnderstandAIwithMe">
<h2 style="margin-top:0">Hi, I&rsquo;m Constantin</h2>
<p>I build AI workflows and explain them in plain English on <a href="{CFG['youtube']}" rel="noopener">YouTube</a> and <a href="{CFG['tiktok']}" rel="noopener">TikTok</a>. Most of the people I talk to don&rsquo;t need an &ldquo;AI strategy&rdquo;. They need the invoice reminders to go out on time, payroll to stop eating a day, and fewer copy-and-paste jobs.</p>
<p>This site is where the videos turn into step-by-step guides, plus a short list of tools and partners I&rsquo;d actually use.</p></div>
<h2>How this site works</h2>
<ol class="tips"><li>Pick the problem that costs you most time. Each one has a page with three things to do first.</li><li>Where a tool or partner is the fastest fix, we name one. Some of those links are affiliate links.</li><li>For bigger jobs, you can describe a task and a vetted AI automation partner replies with a rough estimate.</li></ol>
<h2>Our rules</h2>
<ul><li><b>Useful first.</b> Every guide must contain steps you can do today, even if you never click a link.</li><li><b>One recommendation per problem.</b> Not a list of twenty. If we wouldn&rsquo;t use it, it isn&rsquo;t here.</li><li><b>Clear about money.</b> We may earn a commission when you sign up through a link. It never changes your price. See the <a href="/disclosure/">disclosure</a>.</li><li><b>Not financial advice.</b> For finance products, always check the provider&rsquo;s own terms and costs.</li></ul>
<div class="card cta"><h3>Start with your biggest time sink</h3><p>Two minutes with the calculator shows which admin task to fix first.</p><a class="btn" href="/tools/admin-time-calculator/">Open the calculator</a></div>
</section>"""
    person = {"@context": "https://schema.org", "@type": "AboutPage", "url": URL + "/about/", "mainEntity": {"@type": "Person", "name": "Constantin", "url": URL + "/about/", "image": URL + "/constantin-400.jpg", "sameAs": [CFG["youtube"], CFG["tiktok"]]}}
    return [page("/about/", "About UnderstandAIwithMe | Practical AI for small businesses", "Who is behind UnderstandAIwithMe, how the site works and how it makes money.", body, [person, crumbs(("About", "/about/"))])]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for f in (ROOT / "assets").iterdir():
        if f.is_file():
            shutil.copy(f, OUT / f.name)
    load_guides()
    paths = [build_home()] + build_tools() + build_tile_pages() + build_guides() + build_about() + build_legal()
    page("/fix/build-ai-automation/thanks/", "Enquiry received | UnderstandAIwithMe", "Your enquiry has been received.", '<section class="wrap narrow hero"><h1>Thanks, your enquiry is in</h1><p class="lead">We will review it and send an anonymous summary to our AI automation partner. Expect a reply by email within two working days with whether it fits and a rough estimate.</p><p><a class="btn ghost" href="/guides/">Read the guides meanwhile</a></p></section>')
    page("/fix/build-ai-automation/error/", "Something went wrong | UnderstandAIwithMe", "The enquiry could not be sent.", '<section class="wrap narrow hero"><h1>Sorry, that did not go through</h1><p class="lead">Please go back and try again in a minute. If it keeps failing, <a href="'+CFG["email_signup_url"]+'">join the list</a> and reply to the first email with your task.</p></section>')
    page("/404.html", "Page not found | UnderstandAIwithMe", "Page not found.", '<section class="wrap narrow hero"><h1>Page not found</h1><p class="lead">That page has moved or never existed.</p><p><a class="btn" href="/">Back to the start</a></p></section>')
    for extra in ("/fix/build-ai-automation/thanks/", "/fix/build-ai-automation/error/"):
        f = OUT / extra.strip("/") / "index.html"
        f.write_text(f.read_text(encoding="utf-8").replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1), encoding="utf-8")
    lastmod = {f"/guides/{s}/": m.get("updated", d) for d, s, m, _ in GUIDES}
    urls = "".join(f"<url><loc>{URL}{p}</loc><lastmod>{lastmod.get(p) or TODAY}</lastmod></url>" for p in paths)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {URL}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(paths)} pages into {OUT}")


if __name__ == "__main__":
    main()
