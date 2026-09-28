# briercap.com

Source for [briercap.com](https://briercap.com), the website of Brier Capital LLC, a quantitative
trading firm in prediction markets. Static HTML and CSS with a little JavaScript, served by GitHub Pages.

## Editing

- `index.html`, `style.css`: the home page. `boot.js` and `main.js`: motion only; the page works without them.
- `build.py`: generates `privacy.html`, `terms.html` and `fraud.html` with the header and footer from
  `index.html`. Run `python3 build.py` after editing either.
- Every page sets a Content-Security-Policy allowing only same-origin resources: no inline scripts,
  no `style="..."` attributes, no external fonts or CDNs.
- Preview by opening `index.html` in a browser.

Contact: contact@briercap.com. Security reports: see `.well-known/security.txt`.
