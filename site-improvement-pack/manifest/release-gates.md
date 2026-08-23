# Release gates

## Brand Release Gate

All conditions must be true before the technical phase begins.

### Identity

- [ ] One primary identity is used consistently.
- [ ] Exact current StackLevel role is verified.
- [ ] Century role is exact and owner-confirmed or safely omitted.
- [ ] No unsupported investor, board-level, global-leader or thought-leader identity remains.
- [ ] MIPT is exact and sourced or absent.

### Evidence

- [ ] Every public signal has a working link, exact date and exact role.
- [ ] No production source TODO remains.
- [ ] Track Record separates personal outcomes from company/product facts.
- [ ] No unverified aggregate metric appears as proof.
- [ ] No company client/logo/metric is attributed personally without evidence.
- [ ] All P0 claim risks are closed or removed.

### Homepage and audience pages

- [ ] Homepage follows Identity → Authority → Proof → Relevance → Depth → Trust → Action.
- [ ] Hero proof is verified.
- [ ] Enterprise page uses regulated/governed language without invented clients.
- [ ] AI Diligence page describes method and limitations without implied mandate history.
- [ ] Founder page describes CTO-level diagnosis without fundraising/growth promises.
- [ ] Century recognition is correctly attributed.
- [ ] Contact actions are defined and functional at least through safe fallbacks.

### Machine parity

- [ ] HTML, metadata, JSON-LD, AI profile files and source page do not contradict each other.
- [ ] No broader claim exists only in an AI-readable file.

## Final Release Gate

### Static quality

- [ ] `node qa/check.mjs` passes.
- [ ] No broken internal link or asset.
- [ ] No empty/placeholder href or form action.
- [ ] No duplicate ID.
- [ ] No production TODO or owner placeholder.
- [ ] All JSON-LD parses.

### Responsive and accessibility

- [ ] No document overflow at 320, 390, 768, 1024 and 1440 px.
- [ ] Mobile menu is discoverable and keyboard operable.
- [ ] Skip link works.
- [ ] Escape closes menu and returns focus.
- [ ] Hidden menu items are not tabbable.
- [ ] Meaningful normal text meets contrast target.
- [ ] No meaningful 9–10 px text remains.
- [ ] Reduced motion works.
- [ ] No serious/critical automated accessibility finding remains.
- [ ] Manual keyboard review is documented.

### SEO and entity

- [ ] Metadata matches page intent.
- [ ] Canonical URLs and sitemap URLs match.
- [ ] Root slash is consistent.
- [ ] Stable Person `@id` is used.
- [ ] `sameAs` links are valid.
- [ ] No hreflang without complete alternates.
- [ ] `/index.html` behavior is described accurately.
- [ ] QA/private files are absent from production output.

### Performance

- [ ] Baseline is measured and dated.
- [ ] LCP element is identified.
- [ ] Image priorities are intentional.
- [ ] OG images resolve and have correct dimensions.
- [ ] No performance score is invented.

### Release evidence

- [ ] External proof links were re-checked.
- [ ] Machine-readable profiles match visible copy.
- [ ] Unresolved owner inputs are listed.
- [ ] Release report is complete.
- [ ] Live smoke test is performed after deployment where possible.
