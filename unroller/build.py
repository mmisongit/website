#!/usr/bin/env python3
"""Build the unroller.app landing pages, guides, sitemap and robots.txt, then check the output.

Run from the repository root:  python3 unroller/build.py
Cloudflare Pages serves unroller.app and maps /, /de/ and /guides/ to these files via /_redirects.
"""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import APP_ID, PAGES, PROVIDER_TOKEN, SITE  # noqa: E402
from guides import GUIDES, GUIDES_INDEX  # noqa: E402

ROOT = Path(__file__).resolve().parent          # unroller/
REPO = ROOT.parent
ASSETS = "/unroller/assets/"
RATINGS = ROOT / "ratings.json"
AUTHOR = {"@type": "Person", "name": "Mohamed Makled"}
e = html.escape
GUIDE_BY_SLUG = {g["slug"]: g for g in GUIDES}


# ---------- shared pieces ----------

def store_ratings():
    """Fresh App Store ratings per country; falls back to the last committed values offline."""
    cached = json.loads(RATINGS.read_text()) if RATINGS.exists() else {}
    fresh = {}
    for page in PAGES.values():
        country = page["store_country"]
        try:
            url = f"https://itunes.apple.com/lookup?id={APP_ID}&country={country}"
            with urllib.request.urlopen(url, timeout=10) as r:
                result = json.load(r)["results"][0]
            fresh[country] = {"rating": round(result["averageUserRating"], 1), "count": result["userRatingCount"]}
        except Exception as error:  # offline or lookup change: keep the committed numbers
            print(f"warning: rating lookup for {country} failed ({error}); using cached value")
            fresh[country] = cached[country]
    RATINGS.write_text(json.dumps(fresh, indent=2) + "\n")
    return fresh


def store_url(campaign):
    if len(campaign) > 40:
        raise ValueError(f"campaign token '{campaign}' is longer than App Store Connect's 40 characters")
    if PROVIDER_TOKEN:
        return f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt={PROVIDER_TOKEN}&ct={campaign}&mt=8"
    return f"https://apps.apple.com/app/id{APP_ID}"


def guide_url(slug=None):
    return f"/guides/{slug}/" if slug else "/guides/"


def inline(text):
    """Escape text and turn [label](/path/) into links."""
    return re.sub(r"\[([^\]]+)\]\((/[^)\s]*)\)", r'<a href="\2">\1</a>', e(text))


def plain(text):
    return re.sub(r"\[([^\]]+)\]\((/[^)\s]*)\)", r"\1", text)


def badge(alt, link):
    return (f'<a class="store-badge" href="{e(link)}">'
            f'<img src="/assets/app-store-badge.svg" alt="{e(alt)}" width="150" height="50"></a>')


def shot(file, alt, cls="shot", eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img class="{cls}" src="{ASSETS}{file}" alt="{e(alt)}" width="601" height="1300" {loading}>'


def number(value, lang):
    if lang != "de":
        return f"{value:,}"
    return f"{value}".replace(".", ",") if isinstance(value, float) else f"{value:,}".replace(",", ".")


def head(lang, og_locale, title, description, path, graph, alternates="", preload=""):
    url = SITE + path
    return f"""<!doctype html>
<html lang="{lang}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{e(title)}</title>
    <meta name="description" content="{e(description)}">
    <link rel="canonical" href="{url}">
{alternates}    <meta name="apple-itunes-app" content="app-id={APP_ID}">
    <meta name="theme-color" content="#073781">
    <meta property="og:type" content="{'article' if path.startswith('/guides/') and path != '/guides/' else 'website'}">
    <meta property="og:site_name" content="Unroller">
    <meta property="og:locale" content="{og_locale}">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(description)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}{ASSETS}og.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" href="/Favicon/unroller-app-icon.png">
    <link rel="apple-touch-icon" href="{ASSETS}unroller-icon.jpg">
{preload}    <link rel="stylesheet" href="/unroller/landing.css">
    <script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)}
    </script>
</head>
"""


def topbar(home, links):
    items = "\n".join(f'                <a href="{href}"{extra}>{e(label)}</a>' for label, href, extra in links)
    return f"""        <nav class="topbar wrap" aria-label="Main navigation">
            <a class="brand" href="{home}"><img src="/Favicon/unroller-app-icon.png" alt="" width="32" height="32"><span>Unroller</span></a>
            <div class="topbar-links">
{items}
            </div>
        </nav>"""


def footer(foot, links_extra=""):
    return f"""    <footer class="site-footer">
        <div class="wrap">
            <nav aria-label="Footer navigation">
                <a href="{SITE}/support">{e(foot['support'])}</a>
                <a href="{SITE}/privacy">{e(foot['privacy'])}</a>
                <a href="{SITE}/terms">{e(foot['terms'])}</a>
                <a href="https://mmcapitals.com/">{e(foot['all'])}</a>
{links_extra}            </nav>
            <p>© 2026 Mohamed Makled · <a href="mailto:support@mmcapitals.com">support@mmcapitals.com</a></p>
        </div>
    </footer>
</body>
</html>
"""


def faq_html(items, with_links=False):
    out = []
    for item in items:
        q, a = item[0], item[1]
        more = ""
        if with_links and len(item) > 2:
            more = f' <a href="{guide_url(item[2])}">Read the full guide</a>'
        out.append(f'            <details>\n                <summary>{e(q)}</summary>\n'
                   f'                <p>{e(a)}{more}</p>\n            </details>')
    return "\n".join(out)


def faq_schema(url, items):
    return {"@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [{"@type": "Question", "name": i[0],
                            "acceptedAnswer": {"@type": "Answer", "text": i[1]}} for i in items]}


# ---------- landing pages ----------

def render_landing(lang, page, rating):
    url = SITE + page["path"]
    link = store_url(page["campaign"])
    nav, sw = page["nav"], page["switch"]
    rating_text = page["rating"].format(rating=number(rating["rating"], lang), count=number(rating["count"], lang))
    alternates = "".join(
        f'    <link rel="alternate" hreflang="{p["html_lang"]}" href="{SITE}{p["path"]}">\n' for p in PAGES.values())
    alternates += f'    <link rel="alternate" hreflang="x-default" href="{SITE}/">\n'
    hero_a, hero_b = page["hero_images"]
    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Unroller", "inLanguage": lang},
        {
            "@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "Unroller",
            "description": page["description"], "url": url, "operatingSystem": "iOS 17.0 or later",
            "applicationCategory": "UtilitiesApplication", "installUrl": f"https://apps.apple.com/app/id{APP_ID}",
            "image": SITE + ASSETS + "unroller-icon.jpg",
            "screenshot": [SITE + ASSETS + f for f, _ in page["hero_images"]],
            "inLanguage": lang, "author": AUTHOR,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD" if lang == "en" else "EUR"},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": rating["rating"],
                                "ratingCount": rating["count"], "bestRating": 5, "worstRating": 1},
        },
        faq_schema(url, page["faq"]),
    ]
    links = [(nav["how"], "#how", ""), (nav["features"], "#features", "")]
    if lang == "en":
        links.append(("Guides", guide_url(), ""))
    links += [(nav["faq"], "#faq", ""), (sw["label"], sw["path"], f' hreflang="{sw["lang"]}" lang="{sw["lang"]}"')]
    steps = "\n".join(f"                <li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in page["how"]["steps"])
    features = "\n".join(f"                <li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in page["features"]["items"])
    feature_shots = "\n".join(f"                {shot(f, a)}" for f, a in page["features"]["images"])
    extra_foot = f'                <a href="{guide_url()}">Guides</a>\n' if lang == "en" else ""
    extra_foot += f'                <a href="{sw["path"]}" hreflang="{sw["lang"]}" lang="{sw["lang"]}">{e(sw["label"])}</a>\n'

    return head(page["html_lang"], page["og_locale"], page["title"], page["description"], page["path"], graph,
                alternates, f'    <link rel="preload" as="image" href="{ASSETS}{hero_a[0]}">\n') + f"""<body>
    <a class="skip-link" href="#main-content">{e(page['skip'])}</a>
    <header class="hero">
{topbar(page['path'], links)}
        <div class="hero-body wrap">
            <div class="hero-copy">
                <h1>{e(page['h1'])}</h1>
                <p class="lead">{e(page['lead'])}</p>
                {badge(page['badge_alt'], link)}
                <p class="note">{e(page['note'])}</p>
                <p class="rating"><span aria-hidden="true">★★★★★</span> {e(rating_text)}</p>
            </div>
            <div class="hero-shots">
                {shot(*hero_a, cls="shot shot-front", eager=True)}
                {shot(*hero_b, cls="shot shot-back", eager=True)}
            </div>
        </div>
    </header>
    <main id="main-content">
        <section class="section wrap split" id="how" aria-labelledby="how-title">
            <div>
                <h2 id="how-title">{e(page['how']['h2'])}</h2>
                <ol class="steps">
{steps}
                </ol>
            </div>
            {shot(*page['how']['image'])}
        </section>
        <section class="section band" id="features" aria-labelledby="features-title">
            <div class="wrap">
                <h2 id="features-title">{e(page['features']['h2'])}</h2>
                <ul class="features">
{features}
                </ul>
                <div class="shot-row">
{feature_shots}
                </div>
            </div>
        </section>
        <section class="section wrap two-col" aria-label="{e(page['privacy']['h2'])}">
            <div>
                <h2>{e(page['privacy']['h2'])}</h2>
                <p>{e(page['privacy']['text'])} <a href="{SITE}/privacy">{e(page['privacy']['link'])}</a></p>
            </div>
            <div>
                <h2>{e(page['pricing']['h2'])}</h2>
                <p>{e(page['pricing']['text'])}</p>
            </div>
        </section>
        <section class="section wrap faq" id="faq" aria-labelledby="faq-title">
            <h2 id="faq-title">{e(page['faq_h2'])}</h2>
{faq_html(page['faq'], with_links=True)}
        </section>
        <section class="cta" aria-labelledby="cta-title">
            <div class="wrap">
                <h2 id="cta-title">{e(page['cta']['h2'])}</h2>
                <p>{e(page['cta']['text'])}</p>
                {badge(page['badge_alt'], link)}
            </div>
        </section>
    </main>
""" + footer(page["footer"], extra_foot)


# ---------- guides ----------

EN = PAGES["en"]
GUIDE_NAV = [("Guides", guide_url(), ""), ("FAQ", "/#faq", ""), ("Download", store_url("web-guides"), "")]


def callout(campaign):
    return f"""                <aside class="callout" aria-label="Unroller">
                    <img class="callout-icon" src="{ASSETS}unroller-icon.jpg" alt="" width="64" height="64" loading="lazy">
                    <div>
                        <p><strong>Unroller</strong> shows your photos one at a time. Swipe left to delete, right to keep, and work through your library month by month. Swiping is free; deleting needs Unroller Pro.</p>
                        {badge(EN['badge_alt'], store_url(campaign))}
                    </div>
                </aside>"""


def render_guide(guide):
    path = guide_url(guide["slug"])
    url = SITE + path
    campaign = ("guide-" + guide["slug"])[:40]
    body = []
    for section in guide["sections"]:
        parts = [f'            <section>\n                <h2>{e(section["h2"])}</h2>']
        parts += [f"                <p>{inline(p)}</p>" for p in section.get("paras", [])]
        if section.get("steps"):
            items = "\n".join(f"                    <li>{inline(s)}</li>" for s in section["steps"])
            parts.append(f'                <ol class="howto">\n{items}\n                </ol>')
        if section.get("figure"):
            file, alt, caption = section["figure"]
            parts.append(f'                <figure>\n                    {shot(file, alt)}\n'
                         f'                    <figcaption>{e(caption)}</figcaption>\n                </figure>')
        parts += [f"                <p>{inline(p)}</p>" for p in section.get("after", [])]
        if section.get("cta"):
            parts.append(callout(campaign))
        parts.append("            </section>")
        body.append("\n".join(parts))
    related = "\n".join(
        f'                <li><a href="{guide_url(s)}">{e(GUIDE_BY_SLUG[s]["h1"])}</a></li>' for s in guide["related"])
    graph = [
        {"@type": "Article", "@id": url + "#article", "headline": guide["h1"], "description": guide["description"],
         "image": SITE + ASSETS + "og.jpg", "datePublished": guide["published"],
         "dateModified": guide.get("modified", guide["published"]), "author": AUTHOR, "publisher": AUTHOR,
         "mainEntityOfPage": url, "inLanguage": "en", "about": {"@id": SITE + "/#app"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Unroller", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + guide_url()},
            {"@type": "ListItem", "position": 3, "name": guide["h1"], "item": url}]},
        faq_schema(url, guide["faq"]),
    ]
    date = guide.get("modified", guide["published"])
    pretty = f"{int(date[8:10])} {['January','February','March','April','May','June','July','August','September','October','November','December'][int(date[5:7]) - 1]} {date[:4]}"
    intro = "\n".join(f'            <p class="article-lead">{inline(p)}</p>' for p in guide["intro"])
    return head("en", "en_US", guide["title"], guide["description"], path, graph) + f"""<body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="guide-header">
{topbar('/', GUIDE_NAV)}
    </header>
    <main id="main-content" class="wrap article">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Unroller</a> › <a href="{guide_url()}">Guides</a></nav>
        <article>
            <h1>{e(guide['h1'])}</h1>
            <p class="byline">By Mohamed Makled, developer of Unroller · Updated <time datetime="{date}">{pretty}</time></p>
{intro}
{chr(10).join(body)}
            <section class="faq" id="faq">
                <h2>Questions</h2>
{faq_html(guide['faq'])}
            </section>
        </article>
        <aside class="related" aria-labelledby="related-title">
            <h2 id="related-title">Related guides</h2>
            <ul>
{related}
            </ul>
        </aside>
    </main>
""" + footer(EN["footer"], f'                <a href="{guide_url()}">Guides</a>\n')


def render_guides_index():
    path = guide_url()
    url = SITE + path
    cards = "\n".join(
        f'                <li><a href="{guide_url(g["slug"])}"><h2>{e(g["h1"])}</h2><p>{e(g["card"])}</p></a></li>'
        for g in GUIDES)
    graph = [{"@type": "CollectionPage", "@id": url, "url": url, "name": GUIDES_INDEX["h1"],
              "description": GUIDES_INDEX["description"], "inLanguage": "en",
              "hasPart": [{"@type": "Article", "headline": g["h1"], "url": SITE + guide_url(g["slug"])} for g in GUIDES]},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Unroller", "item": SITE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Guides", "item": url}]}]
    return head("en", "en_US", GUIDES_INDEX["title"], GUIDES_INDEX["description"], path, graph) + f"""<body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="guide-header">
{topbar('/', GUIDE_NAV)}
    </header>
    <main id="main-content" class="wrap article">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Unroller</a> › Guides</nav>
        <h1>{e(GUIDES_INDEX['h1'])}</h1>
        <p class="article-lead">{e(GUIDES_INDEX['intro'])}</p>
        <ul class="guide-cards">
{cards}
        </ul>
{callout('web-guides-index')}
    </main>
""" + footer(EN["footer"])


# ---------- output and checks ----------

def outputs():
    """(file, page config for checks) for every generated HTML page."""
    files = [(ROOT / p["path"].lstrip("/") / "index.html", {"title": p["title"], "description": p["description"]})
             for p in PAGES.values()]
    files.append((ROOT / "guides" / "index.html", GUIDES_INDEX))
    files += [(ROOT / "guides" / g["slug"] / "index.html", g) for g in GUIDES]
    return files


def write_meta_files():
    paths = [p["path"] for p in PAGES.values()] + [guide_url()] + [guide_url(g["slug"]) for g in GUIDES]
    paths += ["/support", "/privacy", "/terms"]
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc></url>" for p in paths)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def local_file(ref):
    """Map a site-absolute URL to the file Cloudflare serves for it."""
    ref = ref.split("?")[0]
    if ref in ("/", "/de/"):
        return ROOT / ref.lstrip("/") / "index.html"
    if ref.startswith("/guides/"):
        return ROOT / ref.lstrip("/") / "index.html"
    return REPO / ref.lstrip("/")


def check():
    """Fail the build on the mistakes that cost rankings: H1s, schema, FAQ drift, dead local links, lengths."""
    problems = []
    for file, meta in outputs():
        doc = file.read_text()
        name = file.relative_to(REPO)
        if len(re.findall(r"<h1[ >]", doc)) != 1:
            problems.append(f"{name}: needs exactly one h1")
        if len(meta["title"]) > 60:
            problems.append(f"{name}: title is {len(meta['title'])} chars (max 60)")
        if len(meta["description"]) > 155:
            problems.append(f"{name}: description is {len(meta['description'])} chars (max 155)")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S)
        try:
            graph = json.loads(blocks[0])["@graph"]
            faq_names = [q["name"] for n in graph if n["@type"] == "FAQPage" for q in n["mainEntity"]]
            visible = [html.unescape(s) for s in re.findall(r"<summary>(.*?)</summary>", doc)]
            if faq_names != visible:
                problems.append(f"{name}: FAQ schema and visible FAQ differ")
        except (ValueError, IndexError, KeyError) as error:
            problems.append(f"{name}: JSON-LD invalid ({error})")
        for ref in re.findall(r'(?:src|href)="(/[^"#]*)"', doc):
            if not local_file(ref).exists():
                problems.append(f"{name}: broken local link {ref}")
        for word in ("—", "seamless", "effortless", "delve", "leverage", "robust", "game-chang", "crucial",
                     "elevate", "streamline", "it's not just"):
            if word in doc.lower():
                problems.append(f"{name}: contains '{word}'")
    for g in GUIDES:
        words = sum(len(plain(t).split()) for s in g["sections"]
                    for t in s.get("paras", []) + s.get("steps", []) + s.get("after", []))
        words += sum(len(p.split()) for p in g["intro"])
        if not 450 <= words <= 1200:
            problems.append(f"guide {g['slug']}: {words} words (aim for 450-1200)")
        for slug in g["related"]:
            if slug not in GUIDE_BY_SLUG:
                problems.append(f"guide {g['slug']}: unknown related guide {slug}")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("checks passed")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"wrote {path.relative_to(REPO)}")


def main():
    ratings = store_ratings()
    for lang, page in PAGES.items():
        write(ROOT / page["path"].lstrip("/") / "index.html", render_landing(lang, page, ratings[page["store_country"]]))
    write(ROOT / "guides" / "index.html", render_guides_index())
    for guide in GUIDES:
        write(ROOT / "guides" / guide["slug"] / "index.html", render_guide(guide))
    write_meta_files()
    check()


if __name__ == "__main__":
    main()
