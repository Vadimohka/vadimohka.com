# Site health checks

This directory is development-only and is excluded from the published artifact.

- `check.py`: validate local links/anchors, canonicals, preview metadata, image candidates, schema references, market context and synchronized discovery output.
- `generate-discovery.py`: generate public metadata/documents from `search-config.json` and visible page text. Run `--write` intentionally and `--check` in CI. The modification date is editorial, not the clock.
- `approved-changes.json`: exact historical/replacement hashes for the owner-requested maintenance. Historical baselines are not rewritten.
- `browser.mjs`: additional source-anchor, label, locale and nested-404 regressions used by the existing complete browser suite.
- `build.mjs`: assemble the public artifact using an explicit allowlist.
- `removed-assets.json`: provenance and size ledger for unused removed media.

The Site health Actions workflow runs pinned Lighthouse 13.4.1. Its before/after builds use identical local HTTP serving and throttling; the published Pages site uses different HTTP compression/cache headers. Home mobile has three trials; other measurements are spot checks. These are lab results, not field Core Web Vitals or US/UAE geographic latency tests. The report includes the exact raw measurements, and a failure to obtain field data is explicitly recorded.

An intermediate measurement identified that the Work hero selected a 1000px source on a 412px/DPR1.75 viewport because 640px was too small. The final source includes 768px candidates and matching responsive preload hints. Publication `sizes` now reflects the actual full-width mobile / two-column desktop layout rather than borrowing the homepage's narrow-thumbnail hint. All original images remain unchanged.

The English page is deliberately the same for en-US and en-AE contexts; regional relevance is expressed through actual service descriptions, without geographic redirects or invented offices. Search/AI inclusion is not guaranteed by this implementation.
