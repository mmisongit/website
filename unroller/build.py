#!/usr/bin/env python3
"""Build the unroller.app landing pages, sitemap and robots.txt, then check the output.

Run from the repository root:  python3 unroller/build.py
Cloudflare Pages serves unroller.app and maps / and /de/ to these files via /_redirects.
"""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import APP_ID, PAGES, PROVIDER_TOKEN, SITE  # noqa: E402

ROOT = Path(__file__).resolve().parent          # unroller/
REPO = ROOT.parent
ASSETS = "/unroller/assets/"
RATINGS = ROOT / "ratings.json"
e = html.escape


def store_ratings():
    """Fresh App Store ratings per country; falls back to the last committed values offline."""
    cached = json.loads(RATINGS.read_text()) if RATINGS.exists() else {}
    fresh = {}
    for lang, page in PAGES.items():
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


def store_url(page):
    if PROVIDER_TOKEN:
        return f"https://apps.apple.com/app/apple-store/id{APP_ID}?pt={PROVIDER_TOKEN}&ct={page['campaign']}&mt=8"
    return f"https://apps.apple.com/app/id{APP_ID}"


def badge(page, link):
    return (f'<a class="store-badge" href="{e(link)}">'
            f'<img src="/assets/app-store-badge.svg" alt="{e(page["badge_alt"])}" width="150" height="50"></a>')


def figure(file, alt, cls="shot", eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{ASSETS}{file}" alt="{e(alt)}" width="601" height="1300" {loading}>')


def number(value, lang):
    if lang != "de":
        return f"{value:,}"
    return f"{value}".replace(".", ",") if isinstance(value, float) else f"{value:,}".replace(",", ".")


def jsonld(lang, page, rating):
    url = SITE + page["path"]
    app = {
        "@type": "SoftwareApplication",
        "@id": SITE + "/#app",
        "name": "Unroller",
        "description": page["description"],
        "url": url,
        "operatingSystem": "iOS 17.0 or later",
        "applicationCategory": "UtilitiesApplication",
        "installUrl": f"https://apps.apple.com/app/id{APP_ID}",
        "image": SITE + ASSETS + "unroller-icon.jpg",
        "screenshot": [SITE + ASSETS + f for f, _ in page["hero_images"]],
        "inLanguage": lang,
        "author": {"@type": "Person", "name": "Mohamed Makled"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD" if lang == "en" else "EUR"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": rating["rating"],
                            "ratingCount": rating["count"], "bestRating": 5, "worstRating": 1},
    }
    faq = {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]],
    }
    site = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Unroller", "inLanguage": lang}
    return json.dumps({"@context": "https://schema.org", "@graph": [site, app, faq]}, ensure_ascii=False, indent=1)


def render(lang, page, rating):
    url = SITE + page["path"]
    link = store_url(page)
    nav, foot, sw = page["nav"], page["footer"], page["switch"]
    rating_text = page["rating"].format(rating=number(rating["rating"], lang), count=number(rating["count"], lang))
    alternates = "\n".join(
        f'    <link rel="alternate" hreflang="{p["html_lang"]}" href="{SITE}{p["path"]}">' for p in PAGES.values())

    steps = "\n".join(
        f'                <li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in page["how"]["steps"])
    features = "\n".join(
        f'                <li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in page["features"]["items"])
    feature_shots = "\n".join(f"                {figure(f, a)}" for f, a in page["features"]["images"])
    faq = "\n".join(
        f'            <details>\n                <summary>{e(q)}</summary>\n                <p>{e(a)}</p>\n            </details>'
        for q, a in page["faq"])
    hero_a, hero_b = page["hero_images"]

    return f"""<!doctype html>
<html lang="{page['html_lang']}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{e(page['title'])}</title>
    <meta name="description" content="{e(page['description'])}">
    <link rel="canonical" href="{url}">
{alternates}
    <link rel="alternate" hreflang="x-default" href="{SITE}/">
    <meta name="apple-itunes-app" content="app-id={APP_ID}">
    <meta name="theme-color" content="#073781">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Unroller">
    <meta property="og:locale" content="{page['og_locale']}">
    <meta property="og:title" content="{e(page['title'])}">
    <meta property="og:description" content="{e(page['description'])}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}{ASSETS}og.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" href="/Favicon/unroller-app-icon.png">
    <link rel="apple-touch-icon" href="{ASSETS}unroller-icon.jpg">
    <link rel="preload" as="image" href="{ASSETS}{hero_a[0]}">
    <link rel="stylesheet" href="/unroller/landing.css">
    <script type="application/ld+json">
{jsonld(lang, page, rating)}
    </script>
</head>
<body>
    <a class="skip-link" href="#main-content">{e(page['skip'])}</a>
    <header class="hero">
        <nav class="topbar wrap" aria-label="Main navigation">
            <a class="brand" href="{page['path']}"><img src="/Favicon/unroller-app-icon.png" alt="" width="32" height="32"><span>Unroller</span></a>
            <div class="topbar-links">
                <a href="#how">{e(nav['how'])}</a>
                <a href="#features">{e(nav['features'])}</a>
                <a href="#faq">{e(nav['faq'])}</a>
                <a href="{sw['path']}" hreflang="{sw['lang']}" lang="{sw['lang']}">{e(sw['label'])}</a>
            </div>
        </nav>
        <div class="hero-body wrap">
            <div class="hero-copy">
                <h1>{e(page['h1'])}</h1>
                <p class="lead">{e(page['lead'])}</p>
                {badge(page, link)}
                <p class="note">{e(page['note'])}</p>
                <p class="rating"><span aria-hidden="true">★★★★★</span> {e(rating_text)}</p>
            </div>
            <div class="hero-shots">
                {figure(*hero_a, cls="shot shot-front", eager=True)}
                {figure(*hero_b, cls="shot shot-back", eager=True)}
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
            {figure(*page['how']['image'])}
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
{faq}
        </section>
        <section class="cta" aria-labelledby="cta-title">
            <div class="wrap">
                <h2 id="cta-title">{e(page['cta']['h2'])}</h2>
                <p>{e(page['cta']['text'])}</p>
                {badge(page, link)}
            </div>
        </section>
    </main>
    <footer class="site-footer">
        <div class="wrap">
            <nav aria-label="Footer navigation">
                <a href="{SITE}/support">{e(foot['support'])}</a>
                <a href="{SITE}/privacy">{e(foot['privacy'])}</a>
                <a href="{SITE}/terms">{e(foot['terms'])}</a>
                <a href="https://mmcapitals.com/">{e(foot['all'])}</a>
                <a href="{sw['path']}" hreflang="{sw['lang']}" lang="{sw['lang']}">{e(sw['label'])}</a>
            </nav>
            <p>© 2026 Mohamed Makled · <a href="mailto:support@mmcapitals.com">support@mmcapitals.com</a></p>
        </div>
    </footer>
</body>
</html>
"""


def out_file(page):
    return ROOT / page["path"].lstrip("/") / "index.html"


def write_meta_files():
    urls = "\n".join(f"  <url><loc>{SITE}{p['path']}</loc></url>" for p in PAGES.values())
    extra = "\n".join(f"  <url><loc>{SITE}/{p}</loc></url>" for p in ("support", "privacy", "terms"))
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n{extra}\n</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def check():
    """Fail the build on the mistakes that cost rankings: H1s, schema, FAQ drift, dead local links, lengths."""
    problems = []
    for lang, page in PAGES.items():
        doc = out_file(page).read_text()
        name = out_file(page).relative_to(REPO)
        if len(re.findall(r"<h1[ >]", doc)) != 1:
            problems.append(f"{name}: needs exactly one h1")
        if len(page["title"]) > 60:
            problems.append(f"{name}: title is {len(page['title'])} chars (max 60)")
        if len(page["description"]) > 155:
            problems.append(f"{name}: description is {len(page['description'])} chars (max 155)")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S)
        try:
            graph = [json.loads(b) for b in blocks][0]["@graph"]
            faq_names = [q["name"] for n in graph if n["@type"] == "FAQPage" for q in n["mainEntity"]]
            visible = [html.unescape(s) for s in re.findall(r"<summary>(.*?)</summary>", doc)]
            if faq_names != visible:
                problems.append(f"{name}: FAQ schema and visible FAQ differ")
        except (ValueError, IndexError, KeyError) as error:
            problems.append(f"{name}: JSON-LD invalid ({error})")
        for ref in re.findall(r'(?:src|href)="(/[^"#]*)"', doc):
            if ref in ("/", "/de/"):
                continue
            if not (REPO / ref.lstrip("/")).exists():
                problems.append(f"{name}: missing local file {ref}")
        for word in ("—", "seamless", "effortless", "delve", "leverage", "robust", "game-chang"):
            if word in doc.lower():
                problems.append(f"{name}: contains '{word}'")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("checks passed")


def main():
    ratings = store_ratings()
    for lang, page in PAGES.items():
        target = out_file(page)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(lang, page, ratings[page["store_country"]]))
        print(f"wrote {target.relative_to(REPO)}")
    write_meta_files()
    check()


if __name__ == "__main__":
    main()
