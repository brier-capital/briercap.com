#!/usr/bin/env python3
"""Generate the legal pages (privacy.html, terms.html, fraud.html) from their text below.

The header wordmark, footer and security headers are copied from index.html, so every page stays
identical to the homepage. Run after editing the page text or the homepage footer:

    python3 build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = (ROOT / "index.html").read_text()


def extract(pattern, what):
    m = re.search(pattern, INDEX, re.S)
    if not m:
        raise SystemExit(f"build.py: could not find the {what} in index.html")
    return m.group(0)


CSP = extract(r'  <meta http-equiv="Content-Security-Policy"[^>]*>\n', "Content-Security-Policy meta")
BRAND = extract(r'    <a class="brand".*?</a>\n', "header wordmark")
FOOTER = extract(r'  <footer.*?</footer>\n', "footer")
MAIL = '<a href="mailto:contact@briercap.com">contact@briercap.com</a>'


def link(href, text):
    return f'<a href="{href}" rel="noopener noreferrer">{text}</a>'


PAGES = {
    "privacy.html": dict(
        title="Privacy",
        desc="How Brier Capital handles information on briercap.com.",
        h1="Privacy policy",
        date="Effective 28 September 2026",
        sections=[
            ("Overview", ["This policy explains what information Brier Capital LLC (&ldquo;Brier Capital&rdquo;, "
                          "&ldquo;we&rdquo;) collects through briercap.com (the &ldquo;site&rdquo;)."]),
            ("What we collect", ["The site does not use cookies, analytics, advertising or other tracking "
                                 "technologies, and it has no forms. It does not load fonts, scripts or other "
                                 "resources from third parties."]),
            ("Server logs", ["The site is served by a hosting provider that may automatically record technical "
                             "information about each request, such as IP address, browser type and time of access, "
                             "to operate and secure its service. We do not use this information to identify visitors."]),
            ("Browser storage", ["To avoid replaying the opening animation, the site saves a single flag in your "
                                 "browser&rsquo;s session storage. It contains no personal information, is never sent "
                                 "to us, and is deleted when you close the tab."]),
            ("Email", ["If you email us, we receive your email address and the contents of your message. We use "
                       "them only to respond and to keep a record of our correspondence. We do not sell or share "
                       "them, except where required by law."]),
            ("Changes", ["We may update this policy from time to time. The effective date above changes when we do."]),
            ("Contact", [f"Questions about this policy can be sent to {MAIL}."]),
        ],
    ),
    "terms.html": dict(
        title="Terms of use",
        desc="Terms of use for briercap.com.",
        h1="Terms of use",
        date="Effective 28 September 2026",
        sections=[
            ("Acceptance", ["By using briercap.com (the &ldquo;site&rdquo;), you agree to these terms. If you do "
                            "not agree, please do not use the site."]),
            ("Information only", ["The site provides general information about Brier Capital LLC (&ldquo;Brier "
                                  "Capital&rdquo;, &ldquo;we&rdquo;). Nothing on it constitutes an offer to sell, or a "
                                  "solicitation of an offer to buy, any security, fund interest or other financial "
                                  "product, or investment, legal, tax or other advice, and it should not be relied "
                                  "on in making any financial decision."]),
            ("No warranty", ["The site is provided &ldquo;as is&rdquo;. We make no representations or warranties of "
                             "any kind, express or implied, about its accuracy, completeness or availability, and "
                             "we may change or remove content at any time without notice."]),
            ("Limitation of liability", ["To the fullest extent permitted by law, Brier Capital is not liable for "
                                         "any loss or damage arising from your use of, or reliance on, the site."]),
            ("Intellectual property", ["The content of the site, including the Brier Capital name and logo, belongs "
                                       "to Brier Capital. You may view and print it for your own reference, but you "
                                       "may not reproduce or modify it, or use our name or logo, without our written "
                                       "permission."]),
            ("Other websites", ["Links to other websites are provided for convenience. We do not control those "
                                "websites and are not responsible for their content."]),
            ("Governing law", ["These terms are governed by the laws of the State of Connecticut, without regard "
                               "to its conflict-of-law rules."]),
            ("Changes", ["We may revise these terms at any time by updating this page. The effective date above "
                         "changes when we do."]),
            ("Contact", [f"Questions about these terms can be sent to {MAIL}."]),
        ],
    ),
    "fraud.html": dict(
        title="Fraud and impersonation warning",
        desc="How to recognise communications that genuinely come from Brier Capital.",
        h1="Fraud and impersonation warning",
        date="Last updated 28 September 2026",
        sections=[
            ("Overview", ["Criminals impersonate legitimate financial firms, using their names, logos, look-alike "
                          "websites and email addresses to ask for money or personal information. This page sets "
                          "out how Brier Capital LLC communicates, so that you can recognise messages that do not "
                          "come from us."]),
            ("How we communicate", [
                "Our only website is <strong>briercap.com</strong>. Our email addresses end in exactly "
                "<strong>@briercap.com</strong>. Messages from any other address, including look-alike spellings "
                "and other domains that contain our name, are not from us. We are not affiliated with other "
                "organisations that use similar names.",
                "We do not use social media, messaging apps or unsolicited phone calls to offer investments or to "
                "request payments.",
            ]),
            ("What we will never do", [
                "We do not offer investments, accounts, funds, returns or trading signals to the public. We have "
                "not issued any cryptocurrency, token or app.",
                "We will never ask you to send money or cryptocurrency, or for passwords, private keys, recovery "
                "phrases, one-time codes or remote access to your device.",
                "We never charge job candidates fees, and we do not ask for payment or bank details as part of "
                "hiring.",
            ]),
            ("If you are contacted", [
                "Do not send money, open links or attachments, or share personal information. To check whether a "
                f"message is genuine, write to us at {MAIL}, typing the address yourself rather than replying to "
                "the message.",
                "If you have already sent money or cryptocurrency, contact your bank or exchange immediately. In "
                f"the United States you can report fraud to the FBI at {link('https://www.ic3.gov/', 'ic3.gov')}, "
                f"the Federal Trade Commission at {link('https://reportfraud.ftc.gov/', 'reportfraud.ftc.gov')} "
                f"and the Commodity Futures Trading Commission at "
                f"{link('https://www.cftc.gov/complaint', 'cftc.gov/complaint')}. Elsewhere, contact your local "
                "police or financial regulator.",
            ]),
        ],
    ),
}


def render(fname, title, desc, h1, date, sections):
    body = ""
    for heading, paras in sections:
        body += f"\n        <h2>{heading}</h2>\n"
        body += "".join(f"        <p>{p}</p>\n" for p in paras)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{CSP}  <title>{title} · Brier Capital</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#f5f5f2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0c1624" media="(prefers-color-scheme: dark)">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="preload" href="assets/fonts/albert-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- Generated by build.py from index.html; edit there, not here. -->
  <header class="wrap masthead">
{BRAND}  </header>

  <main>
    <article class="wrap row doc" aria-labelledby="doc-h">
      <p class="label">Legal</p>
      <div class="body">
        <h1 id="doc-h">{h1}</h1>
        <p class="updated">{date}</p>
{body}      </div>
    </article>
  </main>

{FOOTER}</body>
</html>
"""


for fname, page in PAGES.items():
    (ROOT / fname).write_text(render(fname, **page))
    print("wrote", fname)
