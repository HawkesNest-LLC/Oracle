# Mobile relay contract | proposal, not installed
Goal: eliminate Noah's repetitive copy/paste while preserving explicit authority and receipts.

**Current functional channel:** GitHub draft PR link, readable on phone and by any agent with web/GitHub access. Reading is not automatic.

**Near-term manual-light workflow:** Open the dispatch PR from the iPhone, use the native Share sheet to send a short link to another AI app if it accepts URLs; instruct that agent to retrieve source and publish a delta to GitHub. This still requires user taps and possibly app login.

**Possible iOS Shortcuts build:** A Shortcut that presents a menu (Gemini, Claude, ChatGPT, browser), copies the one-line link to clipboard, and opens the selected app via its supported URL scheme or public web URL. Do not claim prompt auto-injection. App URL schemes and iOS permissions require verification on the device; no Shortcut was installed by this session.

**Future actual integration:** A trusted broker service with OAuth/API credentials per provider, an approved task queue, audit receipts and per-agent read acknowledgments. Avoid storing secrets in a public repo. The broker must not act as Noah.Physical or promote canon.

**Security:** Never distribute raw private corpus to public GitHub. Human authorization for consequential external actions. Use synthetic or approved redacted sources for model tests.
