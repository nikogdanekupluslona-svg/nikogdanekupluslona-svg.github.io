#!/usr/bin/env python3
"""Rebuild a page's FAQPage JSON-LD from its visible FAQ.

  python3 tools/faq_jsonld.py path/index.html [...]   rewrite the FAQPage block
  python3 tools/faq_jsonld.py --check path [...]       report pages whose JSON-LD differs

Visible FAQ is either <details><summary>Q</summary>A…</details> inside the
id="faq" section (home page) or <h3>Q</h3> followed by answer blocks after
<h2 id="faq"> (guides). Answer text is the visible text with tags removed.
"""
import html
import json
import re
import sys

LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def text(fragment):
    fragment = re.sub(r"</?(p|li|ul|ol|div|br|table|thead|tbody|tr|td|th|blockquote|figure|figcaption)\b[^>]*>", " ", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def visible_faq(s):
    m = re.search(r'<section[^>]*id="faq"[^>]*>(.*?)</section>', s, re.S)
    if m and "<details" in m.group(1):
        return [(text(q), text(a)) for q, a in
                re.findall(r"<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>", m.group(1), re.S)]
    m = re.search(r'<h2[^>]*id="faq"[^>]*>.*?</h2>(.*?)(?=<h2\b|</article>|</main>|<section\b|<aside\b)', s, re.S)
    if not m:
        return []
    parts = re.split(r"<h3[^>]*>(.*?)</h3>", m.group(1), flags=re.S)
    return [(text(parts[i]), text(parts[i + 1])) for i in range(1, len(parts) - 1, 2)]


def entities(pairs):
    return [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]


def process(path, check):
    s = open(path, encoding="utf-8").read()
    pairs = visible_faq(s)
    if not pairs:
        return "no visible FAQ"
    for m in LD.finditer(s):
        data = json.loads(m.group(2))
        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            want = entities(pairs)
            if data.get("mainEntity") == want:
                return "ok (%d)" % len(pairs)
            if check:
                have = [e["name"] for e in data.get("mainEntity", [])]
                return "DIFFERS (%d visible, %d in JSON-LD; names equal: %s)" % (len(pairs), len(have), have == [q for q, _ in pairs])
            data["mainEntity"] = want
            new = m.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + m.group(3)
            open(path, "w", encoding="utf-8").write(s[:m.start()] + new + s[m.end():])
            return "rewritten (%d)" % len(pairs)
    return "no FAQPage JSON-LD"


if __name__ == "__main__":
    args = sys.argv[1:]
    check = "--check" in args
    for p in [a for a in args if a != "--check"]:
        print("%-60s %s" % (p, process(p, check)))
