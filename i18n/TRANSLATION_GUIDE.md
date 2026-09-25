# Translation guide — chat-downloader.com

Rules for every localized page under `/<lang>/`. `tools/i18n_build.py` wires the pages together after translation; translators only produce page content.

## What you produce

For each assigned page id (see `i18n/slugs.json`):

1. Read the English source at the path listed in `pages`.
2. Write the translated page to `/<lang>/<slug>/index.html`. Slugs are in `slugs.<lang>`. For `ja`, `ko`, `he`, `ar` the slug is the English path (for example `/ja/how-to-download-claude-chat/index.html`, `/ja/formats/json/index.html`, home is `/ja/index.html`).
3. The group that owns `home` also writes `i18n/labels/<lang>.json`: the same keys as `i18n/labels/en.json`, translated. Keep `{home}` and `{guide}` placeholders and the `<a>` tags in `not_found_lead`.

## HTML rules

- Start from a copy of the English file and replace text. Keep every tag, class, `id`, `datetime`, `src`, `width`/`height`, and script in place.
- **Keep internal links exactly as in English** (`href="/formats/"`, `href="/#faq"`, `https://chat-downloader.com/bulk/` in JSON-LD, canonical and `og:url`). The build script rewrites them to localized slugs. Do not type localized URLs yourself.
- **Do not edit `<header>` or `<footer>`**. They are regenerated from the labels file. Leave them in English.
- **Keep `id` values in English** (`id="faq"`, `id="contact"`, `id="download-with-chrome"` …) and keep the matching `href="#..."` TOC links. Only translate the visible text.
- Translate: `<title>`, `meta description`, `og:title`, `og:description`, `twitter:title`, `twitter:description`, all visible text, `alt`, `aria-label`, `title` attributes, `data-alt`, table captions, and every human-readable string inside JSON-LD (`name`, `text`, `headline`, `description`, breadcrumb `name`). JSON-LD must stay valid JSON: escape `"` as `\"`, do not use raw line breaks.
- Do not translate: content of `<code>`, `<pre>`, `<kbd>`; file paths, commands (`/export`, `~/.claude/projects`), keyboard shortcuts (`Ctrl+P`, `Cmd+P`), file extensions, format names (Markdown, JSON, XML, PNG), URLs, email addresses, `utm_*` values.
- `<html lang="en">` may stay — the build script sets `lang` and `dir`.
- "Updated September 2026" → localized month and year; keep `datetime="2026-09"`.
- Output must be UTF-8. No BOM.

## Length limits

| | Title | Meta description |
|---|---|---|
| Latin-script languages, he, ar | ≤ 60 characters | ≤ 155 characters |
| ja, ko | ≤ 32 characters | ≤ 80 characters |

## Content rules

- Translate meaning, not words. The result must read as if written natively for that market. Short sentences, answer-first, same structure and headings as English (H2s stay questions if they are questions in English).
- **Facts must not change.** The full list is in `seo-workspace/product-facts.md` (extension version 1.16.2). In short: Markdown, plain text, JSON, XML, CSV and PNG exports are unlimited and need no account; PDF and bulk ZIP ("Export All") need Google sign-in and are free up to 3 a day, unlimited on Pro; Pro $3.99/month or $26.99/year (Paddle), 14-day money-back guarantee; seven formats: PDF, Markdown, plain text, JSON, XML, CSV, PNG; everything, PDF included, is built in the browser; desktop Chrome/Chromium only, no mobile app; not affiliated with Anthropic. **Never quote a star rating.**
- **Prices stay in USD.** Use the local number format: de/fr/nl/sv/nb/da/fi `3,99 $` / `26,99 $` (fr/sv/nb/fi use a non-breaking space: `3,99 $`); ja/ko/he/ar `$3.99`.
- **Do not add** new facts, statistics, testimonials, case studies or claims. **Never name competing extensions or exporter apps.** Anthropic products (claude.ai, Claude Desktop, Claude Code, Settings → Privacy → Export data) may be named as the reader's existing tools.
- **English keyword-variant passages.** Some English pages discuss English search spellings (e.g. "download Claude chat vs claude download chat", "Claude export conversation vs export Claude conversation"). Do not translate those literally. Rewrite them around the equivalent local phrasings listed below (e.g. in German: "Claude Chat exportieren" vs "Claude Unterhaltung exportieren"), or around "local phrasing vs the English phrasing people also type". Keep the same answer.
- **Target keyword per page.** Each page gets its own local main keyword (table below, "page focus"). Put it in the title, H1, the first sentence of the lead, and one H2. Use it naturally — max about once per 150 words. Add the English phrasing once where the language table says searchers also type English.
- Brand names stay in English: **Download Claude conversations** (extension name in the Chrome Web Store), **Chat Downloader** (site name), **Claude Chat Downloader**, **Claude**, **Chrome Web Store**, **Pro**.

### Extension and claude.ai interface labels

The extension UI is English-only. Keep its labels in English inside quotes, and add a translation in parentheses on first use per page:

- «Export» / „Export“ button, "Select", "Copy", "Export All", "View and Download All Conversations", "Project files" → "Download ZIP", artifact layouts "Original", "Inline", "Nested", "Flat", sender filter "All / Human / Assistant", Dashboard checkboxes "Chats", "Thinking", "Metadata", "Tools", "Sources".
- The orange button is described, not named: "the orange button next to the message box".

claude.ai itself may be shown in the reader's language. Write the path as `Settings → Privacy → Export data` in English, followed by a short note in parentheses like "(labels may be translated if claude.ai is set to <language>)" the first time on a page. Do not invent localized claude.ai menu names.

## Per-language terms and keywords

Keywords come from Google autocomplete in each market (`seo-workspace/i18n/suggestions-flat.txt`). No volume data — use them as phrasing, not as targets to stuff.

### de — German (Sie)
- export → exportieren / Export; download → herunterladen; save → speichern; chat → Chat; conversation → Unterhaltung; history → Verlauf; extension → Chrome-Erweiterung; bulk → alle Chats auf einmal / Massenexport; print → drucken.
- Autocomplete: claude chat exportieren, claude chats exportieren, claude chat herunterladen, claude chat speichern, claude chat als pdf (exportieren), claude unterhaltung exportieren, claude verlauf, claude code chat exportieren, kann man claude chats exportieren, claude ganzen/kompletten chat exportieren. English also typed: claude export chat, claude exporter.

### fr — French (vous)
- export → exporter / exportation; download → télécharger; save → sauvegarder / enregistrer; chat/conversation → conversation (also discussion); history → historique; extension → extension Chrome.
- Autocomplete: exporter conversation claude, comment exporter conversation claude, exporter discussion claude, sauvegarder conversation claude, enregistrer conversation claude, historique claude / historique conversation, télécharger conversation claude. English also typed: claude export chat, claude exporter.

### nl — Dutch (je)
- exporteren, downloaden, opslaan, gesprek, chat, geschiedenis, Chrome-extensie.
- Autocomplete: claude chat downloaden, claude geschiedenis. Most searches are English: claude export chat, claude export conversation, claude export to pdf, claude exporter. Pair Dutch + English phrasing in titles where natural.

### sv — Swedish (du)
- exportera, ladda ner, spara, konversation, chatt, historik, Chrome-tillägg.
- Autocomplete: claude ladda ner, claude historia. Mostly English searches: claude export chat, claude export all chats, claude chat exporter.

### nb — Norwegian Bokmål (du)
- eksportere, laste ned, lagre, samtale, chat, historikk, Chrome-utvidelse.
- Autocomplete: claude laste ned. Mostly English: claude export chats, claude chat download, claude export chat history.

### da — Danish (du)
- eksportere, downloade, gemme, samtale, chat, historik, Chrome-udvidelse.
- Mostly English searches: claude chat export, claude export all chats, claude export chat to pdf.

### fi — Finnish (sinä, neutral)
- viedä / vienti (export), ladata / lataus, tallentaa, keskustelu, chat, historia, Chrome-laajennus.
- Autocomplete: claude lataa, lataa claude ai. Mostly English: claude export chats, claude chat export, claude export history.

### ja — Japanese (です・ます)
- エクスポート, ダウンロード, 保存, 会話, チャット, 履歴 / 会話履歴 / チャット履歴, Chrome拡張機能, 一括エクスポート.
- Autocomplete: claude 会話 エクスポート, claude チャット エクスポート, claude 会話履歴 エクスポート, claude チャット履歴 保存, claude 会話 保存, claude 保存方法, claude 会話 ダウンロード, claude エクスポート json, claude markdown 出力, claude pdf 出力, claude code 会話 エクスポート. Note "claude ダウンロード" alone usually means downloading the app — say 会話 / チャット explicitly.

### ko — Korean (합니다체)
- 내보내기, 다운로드, 저장, 대화, 채팅, 대화 기록 / 채팅 기록, Chrome 확장 프로그램, 일괄 내보내기.
- Both "Claude" and "클로드" are searched. Autocomplete: claude 대화 내보내기, 클로드 대화 내보내기, claude 대화 저장, 클로드 대화 내용 저장, claude 채팅 내보내기, 클로드 대화기록 내보내기, 클로드 pdf 저장, claude code 대화 내보내기. Use "Claude(클로드)" once near the top of each page.

### he — Hebrew (neutral, plural "אתם" or impersonal)
- ייצוא, הורדה, שמירה, שיחה, צ'אט, היסטוריה, תוסף Chrome.
- Searches are almost all English: claude export chat, claude export chat history, claude exporter extension. Keep "Claude" in Latin script. Mix LTR terms carefully — Latin terms, formats and paths are fine inline.

### ar — Arabic (Modern Standard Arabic, formal)
- تصدير، تنزيل، حفظ، محادثة، سجل المحادثات، إضافة Chrome.
- Searches are almost all English: claude export chat, claude export chat to pdf, claude save chat as pdf. Keep "Claude" in Latin script. Use Western digits (3, 7, 1.16.2).

## Page focus (main local keyword per page)

Use the language's terms above. English page intent → what to target:

| page id | intent |
|---|---|
| home | Claude chat downloader / export Claude chats (brand + main term) |
| how-to-download-claude-chat | how to download a Claude chat (how-to) |
| download-claude-conversation | download a Claude conversation (use the "conversation" noun) |
| how-to-save-claude-conversation | how to save a Claude conversation (save verb) |
| export-claude-chat | export Claude chat (export verb + chat) |
| claude-export-conversation | Claude export conversation (export + conversation noun; alternative phrasing) |
| claude-conversation-extractor | Claude conversation extractor / extract conversations |
| how-to-export-claude-chat | how to export a Claude chat (question form, step-by-step) |
| claude-code-export | export Claude Code conversation / session |
| download-claude-chat-as-pdf | Claude chat as PDF / save Claude chat as PDF |
| export-claude-desktop-chat | export Claude Desktop chat |
| bulk | export all Claude chats / entire history |
| features, formats, formats-*, how-it-works, about, contact | as named |

Where the language has one natural phrase for two English variants, differentiate by angle (how-to vs product, chat vs history vs single conversation) instead of repeating the same title.
