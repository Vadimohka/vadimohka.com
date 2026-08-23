# Performance baseline — 2026-08-22

Measured locally against `http://127.0.0.1:4173/index.html` with Lighthouse
13.4.1, Chromium headless, and the static Python server. These are lab results,
not field or marketing claims.

| Profile | Performance | Accessibility | Best practices | SEO | LCP | Transfer |
|---|---:|---:|---:|---:|---:|---:|
| Mobile emulation | 100 | 100 | 100 | 100 | 1.1 s | 90 KiB |
| Desktop emulation | 96 | 100 | 100 | 100 | 1.2 s | 90 KiB |

The LCP request is the preloaded hero portrait (`assets/portraits/vadim-boardroom-960.webp`
at the mobile viewport); the page keeps explicit image dimensions and aspect
ratios to protect CLS. The main render-blocking request is the 22KiB shared CSS;
the site has no custom font or runtime analytics dependency. Raw Lighthouse JSON
is generated locally by the command below and ignored from commits.

```text
python3 -m http.server 4173
npx --yes lighthouse http://127.0.0.1:4173/index.html --output=json \
  --output-path=qa/performance/baseline-mobile.json \
  --chrome-flags="--headless=new --no-sandbox" --form-factor=mobile \
  --screenEmulation.mobile=true --quiet
npx --yes lighthouse http://127.0.0.1:4173/index.html --output=json \
  --output-path=qa/performance/baseline-desktop.json \
  --chrome-flags="--headless=new --no-sandbox" --form-factor=desktop \
  --screenEmulation.mobile=false --quiet
```
