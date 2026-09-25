#!/usr/bin/env python3
"""Wire up the localized copies of the site.

Translated pages live at /<lang>/<slug>/index.html. Translators only touch page
content and keep English internal links (/formats/, /#faq, ...). This script:

  * rewrites English internal links and absolute URLs to the localized slugs
  * regenerates the header and footer from i18n/labels/<lang>.json
  * sets <html lang dir>, hreflang alternates, og:locale, extra web fonts
  * adds the language switcher to English pages
  * localizes the root 404.html by path prefix
  * rebuilds sitemap.xml with xhtml:link alternates
  * records which English source each translation was made from (i18n/sources.json)

Usage:
  python3 tools/i18n_build.py            # build everything (idempotent)
  python3 tools/i18n_build.py --check    # validate, exit 1 on errors
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chat-downloader.com"
CWS = "https://chromewebstore.google.com/detail/download-claude-conversat/ljcgfcnobiealkonbknnfckhkdbodhak"
SUPPORT = "smmfedorova@gmail.com"
LEGAL = ["/privacy/", "/terms/", "/refund/"]
GLOBE = ('<svg class="lang-globe" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false" fill="none" '
         'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/>'
         '<path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>')


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


LOCALES = load("i18n/locales.json")
SLUGS = load("i18n/slugs.json")
PAGES = SLUGS["pages"]
PATH_TO_ID = {v: k for k, v in PAGES.items()}
LANGS = [l for l in LOCALES if l != "en"]


def labels(lang):
    p = os.path.join(ROOT, "i18n/labels/%s.json" % lang)
    if not os.path.exists(p):
        return None
    base = load("i18n/labels/en.json")
    base.update(load("i18n/labels/%s.json" % lang))
    return base


def url_for(lang, pid):
    if lang == "en":
        return PAGES[pid]
    if lang in SLUGS["english_slug_langs"]:
        slug = PAGES[pid].strip("/")
    else:
        slug = SLUGS["slugs"][lang][pid]
    return "/%s/%s" % (lang, slug + "/" if slug else "")


def file_for(url):
    return os.path.join(ROOT, url.lstrip("/"), "index.html")


def exists(lang, pid):
    return os.path.exists(file_for(url_for(lang, pid)))


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    if os.path.exists(p) and read(p) == s:
        return False
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    return True


def esc(s):
    return html.escape(s, quote=True)


def strip_block(s, name):
    return re.sub(r"\n?[ \t]*<!-- i18n:%s -->.*?<!-- /i18n:%s -->" % (name, name), "", s, flags=re.S)


def cws(campaign):
    return "%s?utm_source=site&amp;utm_medium=cta&amp;utm_campaign=%s" % (CWS, campaign)


# ---------------------------------------------------------------- fragments

def head_block(lang, pid):
    out = ["<!-- i18n:head -->"]
    if pid is not None:
        for l in LOCALES:
            if l == "en" or exists(l, pid):
                out.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (LOCALES[l]["hreflang"], SITE, url_for(l, pid)))
        out.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, PAGES[pid]))
        out.append('<meta property="og:locale" content="%s">' % LOCALES[lang]["og_locale"])
        for l in LOCALES:
            if l != lang and (l == "en" or exists(l, pid)):
                out.append('<meta property="og:locale:alternate" content="%s">' % LOCALES[l]["og_locale"])
    font = LOCALES[lang]["font"]
    if font:
        out.append('<link href="https://fonts.googleapis.com/css2?family=%s&amp;display=swap" rel="stylesheet">' % font)
    out.append("<!-- /i18n:head -->")
    return "\n  ".join(out)


def switcher(lang, pid, lb):
    items = []
    for l in LOCALES:
        if pid is not None and (l == "en" or exists(l, pid)):
            href = url_for(l, pid)
        else:
            href = url_for(l, "home")
        cur = ' aria-current="true"' if l == lang else ""
        items.append('<li><a href="%s" hreflang="%s" lang="%s"%s>%s</a></li>' % (href, LOCALES[l]["hreflang"], LOCALES[l]["hreflang"], cur, esc(LOCALES[l]["name"])))
    name = esc(LOCALES[lang]["name"])
    return ('<!-- i18n:switch --><details class="lang-switch"><summary aria-label="%s: %s">%s'
            '<span class="lang-name">%s</span><span class="lang-code" aria-hidden="true">%s</span></summary><ul>%s</ul></details><!-- /i18n:switch -->'
            % (esc(lb["language"]), name, GLOBE, name, lang, "".join(items)))


def footer_langs(lang, pid):
    links = []
    for l in LOCALES:
        href = url_for(l, pid) if pid is not None and (l == "en" or exists(l, pid)) else url_for(l, "home")
        links.append('<a href="%s" hreflang="%s" lang="%s">%s</a>' % (href, LOCALES[l]["hreflang"], LOCALES[l]["hreflang"], esc(LOCALES[l]["name"])))
    return '<!-- i18n:langs --><nav class="footer-langs" aria-label="Language">%s</nav><!-- /i18n:langs -->' % " ".join(links)


def header(lang, pid, lb):
    u = lambda p: url_for(lang, p)
    camp = "%s-%s" % (lang, pid)
    nav = [("how-to-download-claude-chat", "nav_how_to_download"), ("how-to-export-claude-chat", "nav_export"),
           ("bulk", "nav_bulk"), ("formats", "nav_formats")]
    links = "".join('<a href="%s"%s>%s</a>' % (u(p), ' aria-current="page"' if p == pid else "", esc(lb[k])) for p, k in nav)
    links += '<a href="%s#faq">%s</a>' % (u("home"), esc(lb["nav_faq"]))
    btn = '<a class="btn-install" href="%s" target="_blank" rel="noopener noreferrer"><img src="/assets/images/chrome.svg" alt="" width="20" height="20"> %s</a>' % (cws(camp), esc(lb["add_to_chrome"]))
    return """<header class="site-header">
  <div class="header-inner">
    <div class="header-left">
      <a class="logo" href="%s">
        <img src="/assets/icon.svg" alt="">
        <span>Download Claude conversations</span>
      </a>
      <nav class="nav" id="site-nav">
        %s
        %s
      </nav>
    </div>
    <div class="header-right">
      %s
      %s
      <button class="nav-toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="%s">☰</button>
    </div>
  </div>
</header>""" % (u("home"), links, btn, btn, switcher(lang, pid, lb), esc(lb["menu"]))


def footer(lang, pid, lb):
    u = lambda p: url_for(lang, p)
    a = lambda p, k: '      <a href="%s">%s</a>' % (u(p), esc(lb[k]))
    en = " " + esc(lb["english_only"])
    product = [("features", "page_features"), ("formats", "page_formats"), ("bulk", "page_bulk"), ("how-it-works", "page_how_it_works")]
    guides = [("how-to-download-claude-chat", "page_how_to_download"), ("how-to-export-claude-chat", "page_how_to_export"),
              ("export-claude-chat", "page_export_claude_chat"), ("claude-conversation-extractor", "page_extractor"),
              ("claude-code-export", "page_claude_code"), ("download-claude-chat-as-pdf", "page_pdf"),
              ("export-claude-desktop-chat", "page_desktop"), ("claude-export-conversation", "page_claude_export_conversation"),
              ("how-to-save-claude-conversation", "page_how_to_save"), ("download-claude-conversation", "page_download_conversation")]
    return """<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <a class="logo" href="%(home)s"><img src="/assets/icon.svg" alt=""><span>Download Claude conversations</span></a>
      <p class="legal-note">%(tagline)s</p>
    </div>
    <div>
      <h2>%(install)s</h2>
      <a class="install-link" href="%(cws)s" target="_blank" rel="noopener noreferrer"><img src="/assets/images/chrome.svg" alt="" width="20" height="20"> %(ext)s</a>
    </div>
    <div>
      <h2>%(product_h)s</h2>
%(product)s
    </div>
    <div>
      <h2>%(guides_h)s</h2>
%(guides)s
    </div>
    <div>
      <h2>%(legal_h)s</h2>
%(about)s
      <a href="%(about_url)s#contact">%(contact)s</a>
      <a href="/privacy/" hreflang="en">%(privacy)s%(en)s</a>
      <a href="/terms/" hreflang="en">%(terms)s%(en)s</a>
      <a href="/refund/" hreflang="en">%(refunds)s%(en)s</a>
    </div>
  </div>
  <div class="footer-bottom">
    <div>%(copy)s</div>
    <div>
      <a href="/privacy/" hreflang="en">%(pp)s%(en)s</a>
      <a href="/terms/" hreflang="en">%(tos)s%(en)s</a>
      <a href="/refund/" hreflang="en">%(refunds)s%(en)s</a>
    </div>
  </div>
  %(langs)s
  <p class="disclaimer">%(disc)s <a href="mailto:%(mail)s">%(mail)s</a>.</p>
</footer>""" % dict(
        home=u("home"), tagline=esc(lb["footer_tagline"]), install=esc(lb["footer_install"]),
        cws=cws("%s-footer" % lang), ext=esc(lb["footer_chrome_extension"]), product_h=esc(lb["footer_product"]),
        product="\n".join(a(p, k) for p, k in product), guides_h=esc(lb["footer_guides"]),
        guides="\n".join(a(p, k) for p, k in guides), legal_h=esc(lb["footer_legal"]), about=a("about", "page_about"),
        about_url=u("about"), contact=esc(lb["page_contact"]), privacy=esc(lb["privacy"]), terms=esc(lb["terms"]),
        refunds=esc(lb["refunds"]), en=en, copy=esc(lb["copyright"]), pp=esc(lb["privacy_policy"]),
        tos=esc(lb["terms_of_service"]), langs=footer_langs(lang, pid), disc=esc(lb["disclaimer"]), mail=SUPPORT)


# ---------------------------------------------------------------- page passes

def localize_links(s, lang):
    def href(m):
        path, rest = m.group(2), m.group(3) or ""
        if path in PATH_TO_ID:
            return '%s="%s%s"' % (m.group(1), url_for(lang, PATH_TO_ID[path]), rest)
        return m.group(0)
    s = re.sub(r'\b(href)="(/[^"#?]*)(#[^"]*)?"', href, s)

    def absolute(m):
        path = m.group(1)
        if path in PATH_TO_ID:
            return SITE + url_for(lang, PATH_TO_ID[path])
        return m.group(0)
    return re.sub(re.escape(SITE) + r'(/[a-z0-9/-]*)(?=["#?\s<])', absolute, s)


def tag_campaigns(s, lang):
    def fix(m):
        c = m.group(1)
        return m.group(0) if c.startswith(lang + "-") else "utm_campaign=%s-%s" % (lang, c)
    return re.sub(r"utm_campaign=([a-z0-9_-]+)", fix, s)


def set_html_attrs(s, lang):
    loc = LOCALES[lang]
    tag = '<html lang="%s"%s>' % (loc["hreflang"], ' dir="rtl"' if loc["dir"] == "rtl" else "")
    return re.sub(r"<html[^>]*>", tag, s, count=1)


def put_head(s, lang, pid):
    s = strip_block(s, "head")
    block = head_block(lang, pid)
    if '<link rel="canonical"' in s:
        return re.sub(r'(<link rel="canonical"[^>]*>)', lambda m: m.group(1) + "\n  " + block, s, count=1)
    return s.replace("</head>", "  " + block + "\n</head>", 1)


def build_localized(lang, pid):
    lb = labels(lang)
    p = file_for(url_for(lang, pid))
    s = read(p)
    s = set_html_attrs(s, lang)
    s = localize_links(s, lang)
    s = tag_campaigns(s, lang)
    s = s.replace('"inLanguage":"en-US"', '"inLanguage":"%s"' % LOCALES[lang]["hreflang"])
    s = put_head(s, lang, pid)
    s = re.sub(r'<a class="skip" href="#main">.*?</a>', '<a class="skip" href="#main">%s</a>' % esc(lb["skip"]), s, count=1)
    s = re.sub(r'<header class="site-header">.*?</header>', lambda m: header(lang, pid, lb), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: footer(lang, pid, lb), s, count=1, flags=re.S)
    return write(p, s)


def build_english(path, pid):
    lb = labels("en")
    p = file_for(path) if path != "/404.html" else os.path.join(ROOT, "404.html")
    s = read(p)
    if pid is not None:
        s = put_head(s, "en", pid)
    s = strip_block(s, "switch")
    s = s.replace('<button class="nav-toggle"', switcher("en", pid, lb) + '\n      <button class="nav-toggle"', 1)
    s = strip_block(s, "langs")
    s = s.replace('\n  <p class="disclaimer">', "\n  " + footer_langs("en", pid) + '\n  <p class="disclaimer">', 1)
    return write(p, s)


def build_404():
    p = os.path.join(ROOT, "404.html")
    s = strip_block(read(p), "404")
    data = {}
    for lang in LANGS:
        lb = labels(lang)
        if not lb or not exists(lang, "home"):
            continue
        data[lang] = {
            "dir": LOCALES[lang]["dir"],
            "title": lb["not_found_title"],
            "lead": lb["not_found_lead"].replace("{home}", url_for(lang, "home")).replace("{guide}", url_for(lang, "how-to-download-claude-chat")),
        }
    script = """<!-- i18n:404 --><script>
(function () {
  var t = %s;
  var l = location.pathname.split("/")[1];
  var d = t[l];
  if (!d) return;
  document.documentElement.lang = l;
  document.documentElement.dir = d.dir;
  document.title = d.title + " — Download Claude conversations";
  var h = document.querySelector("main h1"), p = document.querySelector("main .lead");
  if (h) h.textContent = d.title;
  if (p) p.innerHTML = d.lead;
})();
</script><!-- /i18n:404 -->""" % json.dumps(data, ensure_ascii=False)
    s = s.replace("</body>", script + "\n</body>", 1)
    build = write(p, s)
    return build_english("/404.html", None) or build


def build_sitemap():
    old = read(os.path.join(ROOT, "sitemap.xml"))
    lastmod = dict(re.findall(r"<loc>%s(/[^<]*)</loc><lastmod>([^<]+)</lastmod>" % re.escape(SITE), old))
    rows = []

    def entry(loc, mod, alts):
        x = "  <url><loc>%s%s</loc><lastmod>%s</lastmod>" % (SITE, loc, mod)
        for hl, href in alts:
            x += '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (hl, SITE, href)
        return x + ("\n  </url>" if alts else "</url>")

    for pid, path in PAGES.items():
        if pid == "contact" and path not in lastmod:
            langs = []
        else:
            langs = [l for l in LOCALES if l == "en" or exists(l, pid)]
        alts = [(LOCALES[l]["hreflang"], url_for(l, pid)) for l in langs]
        if len(alts) > 1:
            alts.append(("x-default", path))
        else:
            alts = []
        for l in langs:
            if l == "en":
                mod = lastmod.get(path, datetime.date.today().isoformat())
            else:
                mtime = os.path.getmtime(file_for(url_for(l, pid)))
                mod = datetime.date.fromtimestamp(mtime).isoformat()
            rows.append(entry(url_for(l, pid), mod, alts))
    for path in LEGAL:
        rows.append(entry(path, lastmod.get(path, datetime.date.today().isoformat()), []))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    return write(os.path.join(ROOT, "sitemap.xml"), xml)


# ---------------------------------------------------------------- source tracking

def source_hash(pid):
    s = read(file_for(PAGES[pid]))
    for name in ("head", "switch", "langs", "404"):
        s = strip_block(s, name)
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def stamp_sources():
    p = os.path.join(ROOT, "i18n/sources.json")
    data = load("i18n/sources.json") if os.path.exists(p) else {}
    for lang in LANGS:
        for pid in PAGES:
            if exists(lang, pid):
                data.setdefault(lang, {}).setdefault(pid, source_hash(pid))
    write(p, json.dumps(data, indent=1, sort_keys=True) + "\n")


# ---------------------------------------------------------------- checks

EN_WORDS = re.compile(r"\b(the|and|you|your|with|this|that|from|when|which|does|not|file|button|download|without)\b", re.I)


def visible_text(s):
    s = re.sub(r"<(script|style|header|footer|code|pre)\b.*?</\1>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def check():
    errors, warns = [], []
    sources = load("i18n/sources.json") if os.path.exists(os.path.join(ROOT, "i18n/sources.json")) else {}
    for lang in LANGS:
        have = [pid for pid in PAGES if exists(lang, pid)]
        if not have:
            continue
        missing = [pid for pid in PAGES if pid not in have]
        if missing:
            errors.append("%s: missing pages %s" % (lang, ", ".join(missing)))
        if not labels(lang) or not os.path.exists(os.path.join(ROOT, "i18n/labels/%s.json" % lang)):
            errors.append("%s: missing i18n/labels/%s.json" % (lang, lang))
        for pid in have:
            url = url_for(lang, pid)
            s = read(file_for(url))
            tag = "%s%s" % (lang, url[len(lang) + 1:])
            if '<html lang="%s"' % LOCALES[lang]["hreflang"] not in s:
                errors.append("%s: wrong <html lang>" % tag)
            if '<link rel="canonical" href="%s%s">' % (SITE, url) not in s:
                errors.append("%s: canonical is not self" % tag)
            if s.count('rel="alternate" hreflang=') < 3:
                errors.append("%s: hreflang block missing" % tag)
            body = strip_block(strip_block(s, "switch"), "langs")
            for m in re.finditer(r'<!-- i18n:(?:switch|langs) -->.*?<!-- /i18n:(?:switch|langs) -->', s, re.S):
                for h in re.findall(r'href="(/[^"#?]*)', m.group(0)):
                    if not os.path.exists(file_for(h)):
                        warns.append("%s: language switcher points to missing %s" % (tag, h))
            for m in re.finditer(r'href="(/[^"#?]*)', body):
                h = m.group(1)
                if h.startswith("/assets/") or h in LEGAL:
                    continue
                if h in PATH_TO_ID and h != "/" and not h.startswith("/%s/" % lang):
                    errors.append("%s: English link left: %s" % (tag, h))
                elif not os.path.exists(file_for(h)):
                    errors.append("%s: broken link %s" % (tag, h))
            for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
                try:
                    json.loads(m.group(1))
                except ValueError as e:
                    errors.append("%s: invalid JSON-LD (%s)" % (tag, e))
            t = re.search(r"<title>(.*?)</title>", s, re.S)
            d = re.search(r'<meta name="description" content="([^"]*)"', s)
            if not t or not t.group(1).strip():
                errors.append("%s: empty title" % tag)
            elif len(html.unescape(t.group(1))) > (38 if lang in ("ja", "ko") else 70):
                warns.append("%s: long title (%d)" % (tag, len(html.unescape(t.group(1)))))
            if not d:
                errors.append("%s: no meta description" % tag)
            elif len(html.unescape(d.group(1))) > (90 if lang in ("ja", "ko") else 160):
                warns.append("%s: long description (%d)" % (tag, len(html.unescape(d.group(1)))))
            if pid == "home" and 'id="faq"' not in s:
                errors.append("%s: id=\"faq\" missing (nav links to it)" % tag)
            if pid == "about" and 'id="contact"' not in s:
                errors.append("%s: id=\"contact\" missing (footer links to it)" % tag)
            main = re.search(r"<main\b.*?</main>", s, re.S)
            words = visible_text(main.group(0) if main else s).split()
            en = len(EN_WORDS.findall(" ".join(words)))
            if words and en / len(words) > 0.04:
                warns.append("%s: looks partly English (%d/%d marker words)" % (tag, en, len(words)))
            if lang in sources and pid in sources[lang] and sources[lang][pid] != source_hash(pid):
                warns.append("%s: English source changed since translation" % tag)
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print("%d errors, %d warnings" % (len(errors), len(warns)))
    return not errors


def main():
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    changed = 0
    for lang in LANGS:
        if not labels(lang) or not os.path.exists(os.path.join(ROOT, "i18n/labels/%s.json" % lang)):
            continue
        for pid in PAGES:
            if exists(lang, pid):
                changed += build_localized(lang, pid)
    for pid, path in PAGES.items():
        changed += build_english(path, pid)
    for path in LEGAL:
        changed += build_english(path, None)
    changed += build_404()
    changed += build_sitemap()
    stamp_sources()
    print("%d files changed" % changed)


if __name__ == "__main__":
    main()
