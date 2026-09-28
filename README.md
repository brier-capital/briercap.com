# briercap.com

Static site for Brier Capital LLC. Hand-written HTML, CSS and a little JavaScript for motion; no framework.
This repository is public (GitHub Pages): keep anything operational or sensitive out of it.

- `index.html`, `style.css`: the page. Light and dark themes follow the visitor's OS setting.
- `main.js`: motion only. A first-visit intro (once per browser session: the lockup assembles on navy,
  then the monogram and wordmark fly to their places) and a rise-in as sections scroll into view.
  Skipped entirely for reduced-motion visitors; any click, key or scroll skips the intro. Without JS
  the page is static. To replay the intro, add `?intro` to the URL (or open a new tab).
- `assets/monogram.svg`, `assets/wordmark.svg`: the logo, traced from `assets/logo-source.jpeg` (navy and gold
  layers separated, then vectorized with potrace). Inlined in `index.html` so CSS can recolor them for dark mode.
- `favicon.svg`, `assets/apple-touch-icon.png`, `assets/og.png`: derived from the monogram.
- `CNAME`: custom domain for GitHub Pages.

- `boot.js`: tiny script in `<head>` that sets the motion/intro classes before first paint. It is a
  file rather than inline so the Content-Security-Policy can forbid inline scripts.
- `build.py`: generates `privacy.html`, `terms.html` and `fraud.html` (their text lives in it) with
  the header, footer and CSP copied from `index.html`. Re-run `python3 build.py` after editing either.
- `fraud.html`: fraud and impersonation warning. Its promises (we only email from @briercap.com, never
  solicit over social media or messaging apps, never ask for money, keys or codes) must stay true in
  practice; if the firm's behaviour changes, change the page.
- `.well-known/security.txt` (RFC 9116): where to report vulnerabilities. Renew `Expires` before it lapses.
  `.nojekyll` makes GitHub Pages publish the `.well-known` directory.
- `privacy.html`, `terms.html`: plain-language legal pages linked from the footer. Written to be true of
  the site as built (no cookies, analytics, forms or third-party requests); revisit both if that changes,
  and have a lawyer review them before publishing.
- `assets/fonts/`: Albert Sans, self-hosted under the SIL Open Font License (`OFL.txt` must ship with it).

Preview: open `index.html` in a browser. Links between pages are relative (`index.html`, `privacy.html`)
so they work both from disk and on the live site; only `404.html` uses root paths, because GitHub Pages
serves it at arbitrary URLs.

## Deploy (GitHub Pages, DNS stays at Northwest)

1. Verify briercap.com for the `brier-capital` org (org Settings → Pages → Add a domain). GitHub gives a
   `_github-pages-challenge-brier-capital` TXT record to add at Northwest. This stops any other GitHub
   account from serving a site on the domain.
2. Push to `brier-capital/briercap.com` and enable Pages from the `main` branch root.
3. At Northwest (businessidentity.llc), replace only the web records:
   - `@` A → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` CNAME → `brier-capital.github.io`
4. Leave MX, DMARC and DKIM alone. In the SPF (TXT) record remove only the `a` mechanism, which would
   otherwise authorize the new web host's IPs to send mail for the domain.
5. Once the certificate issues, tick "Enforce HTTPS" in the Pages settings. If no certificate appears
   within ~15 minutes of the DNS change (Pages API `https_certificate` stays null), remove and restore
   the custom domain: commit a deletion of `CNAME`, push, wait for the build, then restore it. On
   2026-09-28 that issued the certificate within 30 seconds after 45 minutes of waiting.

## Content rules

- Firm only: no individual names.
- Name the venue (Kalshi) and market categories (crypto, commodities, sports, combos, elections,
  politics). Never how or why we trade them: no models, signals, parameters or data sources.
- Stay vague and conventional, in the register of other trading firms' sites. No claims about whose
  capital is traded; keep the not-an-offer disclaimer in the footer.
- No performance figures until they come from live account history, rounded down and dated.
- No solicitation: no "invest with us" and no investor form.

## Security

Every page carries a Content-Security-Policy meta tag: `default-src 'none'`, with scripts, styles, fonts
and images allowed only from the site itself, and no forms, base-URI changes or third-party requests.
Consequences for editing: no inline `<script>`, no `style="..."` attributes, and no external CDNs or
fonts. Check the browser console for CSP violations after any change. GitHub Pages cannot send HTTP
headers, so `frame-ancestors`/clickjacking protection is unavailable; the site has nothing to click-jack.
