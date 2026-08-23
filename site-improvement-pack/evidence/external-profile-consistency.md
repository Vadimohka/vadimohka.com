# External profile consistency plan

Codex can generate an action report, but it must not claim to have changed external profiles unless it actually has authenticated access and completes the change.

## Master identity

Preferred long form:

> Enterprise AI CTO and product operator focused on governed private AI for regulated organisations.

Preferred short form:

> Enterprise AI CTO & Product Operator

## Profile-by-profile review

### LinkedIn

Observed multi-role headline:

- CTO;
- Head of R&D;
- AI Platform Architect;
- RAG Expert;
- FinTech / EdTech / E-commerce;
- Security-by-Design.

Risk: too many equal identities and sectors.

Target structure:

1. exact current title;
2. one professional territory;
3. one product/company anchor;
4. no unsupported sector list.

### GitHub

Use a technical version of the same identity. Avoid introducing unrelated founder/company labels that do not appear on the website.

### Legacy `.ru` site

Observed divergent positioning around Corporate AI Architect / R&D Director.

Owner decision required:

- redirect to a Russian-language section;
- rebuild as a true language alternate;
- or deprecate.

Do not add hreflang until complete alternates exist.

### Setka

At audit time, the public profile displayed a job-search status that may conflict with an institutional executive brand.

Re-check and:

- update if obsolete;
- remove the status;
- or document why it is intentional.

### Scholar / Codeforces / Stepik

Keep as supporting sameAs/entity links. Do not force marketing headlines into technical or academic profiles.

## Consistency matrix

Each public profile should agree on:

- spelling/transliteration;
- current StackLevel title;
- Century role, if confirmed;
- primary professional territory;
- location only when intentionally public;
- profile photo family;
- current website URL;
- no obsolete job-search or legacy-title signal.

## Deliverable

Create `reports/external-profile-actions.md` with:

- current observed text;
- risk;
- exact proposed replacement;
- owner action;
- completion status;
- date re-checked.
