# Product facts — Download Claude conversations 1.16.2

Source of truth for every page on chat-downloader.com, English and localized. Checked against the published extension package (version 1.16.2, Chrome Web Store, updated 25 September 2026). When the extension changes, update this file first, then the pages.

## Plans and limits

**Free — $0, no account.**
- Single-chat export in **Markdown, Plain Text, JSON, XML, CSV and PNG** is **unlimited** and anonymous. No Google sign-in, no counter.
- **Copy** to the clipboard (Markdown, Text, JSON, XML, CSV) is unlimited. Copy is not available for PDF or PNG.
- **Artifact ZIPs**, **project files ZIP** (on a Project page: "Project files" → "Download ZIP") and **session ZIPs** are unlimited.
- Message selection ("Select") and the sender filter (All / Human / Assistant) are free.
- **PDF export** and **bulk ZIP export** ("Export All" on the Dashboard) ask for **Google sign-in** from the first use and are capped at **3 per day** on the free plan, combined. The day resets at midnight UTC.
- In a bulk export every conversation in the ZIP uses one of the 3. If the selection is larger than what is left today, the whole batch is blocked (not cut short): pick fewer chats or upgrade.

**Pro — $3.99 a month or $26.99 a year** (≈ $2.25 a month billed yearly), paid through Paddle.
- Unlimited PDF exports and unlimited bulk export of the whole history.
- Requires a Google-linked account (sign in with the same Google account to restore Pro on a new install).
- Cancel any time: extension Options page → "Cancel subscription", or through Paddle.
- 14-day money-back guarantee on the first payment.

Short forms to use in copy:
- "Unlimited Markdown, text, JSON, XML, CSV and PNG exports — free, no account."
- "PDF and bulk ZIP: 3 a day free with Google sign-in, unlimited on Pro."

## Formats — seven

PDF, Markdown, Plain Text, JSON, XML, CSV, PNG.

- **PDF** is built in the browser (no print dialog). The PDF dialog sets file name, page size, margins, light or dark mode, font and font size, page numbers, a table of contents, timestamps, and a page break before every prompt.
- **CSV** — one row per message; opens in Excel, Google Sheets, Numbers.
- **PNG** — one image of the conversation.
- Code blocks keep language and formatting; tables and lists survive; artifacts can be nested in the file or pulled out into their own folder inside a ZIP (artifact layouts "Original", "Inline", "Nested", "Flat" on the Dashboard). Extended thinking, web search sources and tool / MCP steps are each opt-in.

## Where things are

- **Export panel**: the round orange download button to the right of the message box on claude.ai. Panel options: Messages (All / Human / Assistant), Format, a **Thinking** checkbox, **Select** (tick individual messages), **Copy**, **Export**. Tool / MCP steps and web search sources for panel exports are switched on in Settings.
- **Dashboard**: the extension popup → "View and Download All Conversations". Search, filters (All conversations / New / Updated / Previously exported), Chat and Cowork tabs, project search, a "Chat format" picker with all seven formats (PDF included), checkboxes Chats / Thinking / Metadata / Tools / Sources, artifact format (Original / Inline / Nested / Flat), **Export All** (one ZIP, one file per chat, in the chosen format), backup and restore. Exporting a single chat from the Dashboard follows the same rules as the panel (free and unlimited unless the format is PDF).
- **Settings** (Options page): filename template, "Copy instead of download", embed images in Markdown, include tool / MCP steps, include web search sources, date and time format, backup and restore, subscription.
- Works with regular chats, **Projects**, **Cowork** sessions and **Claude Code on the web** sessions (claude.ai/code) — anything that opens on claude.ai in Chrome.

## Privacy

- Every format, PDF included, is generated locally in the browser. Conversation text is never uploaded, stored or analysed.
- The only data that leaves the browser is a subscription / quota check that sends the Google account email — and only after the user signs in for PDF, bulk or Pro. Single-chat exports in the other formats send nothing.

## Unchanged

- Desktop Chrome and Chromium-based browsers that install from the Chrome Web Store. No mobile app. Does not run inside the Claude Desktop app.
- Does not read local Claude Code terminal sessions (`~/.claude/projects`, `/export`). Claude Code on the web (claude.ai/code) is covered.
- Anthropic's own account export: Settings → Privacy → Export data (emails a ZIP of JSON).
- Extension UI is English only (the Chrome Web Store listing is localized).
- Not affiliated with Anthropic, PBC.

## Do not claim

- No star rating or "rated 5.0". The Chrome Web Store rating changes; do not quote it. No `aggregateRating` in JSON-LD.
- No user counts, testimonials, or case studies.
- Never name competing extensions or exporter apps.
- Old facts that are now wrong: "3 free exports per account", "sign in with Google before the first export", "five formats", "no PDF export / print to PDF instead", "version 1.13.0".
