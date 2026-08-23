# Content and evidence model

## Claim object

Every substantive claim should be representable as:

```json
{
  "id": "C001",
  "claim": "Vadim Vladymtsev is CTO at StackLevel Group.",
  "subject": "Vadim Vladymtsev",
  "claim_type": "current_role",
  "status": "verified",
  "scope": "personal",
  "sources": ["S001"],
  "valid_from": null,
  "valid_to": null,
  "last_checked": "2026-08-22",
  "allowed_surfaces": ["html", "metadata", "jsonld", "llms", "sources"],
  "notes": "Re-check if role changes."
}
```

## Evidence status

- `verified`: direct authoritative or primary source supports the exact claim.
- `partially_verified`: source supports only part of the wording.
- `owner_confirmed`: owner can truthfully confirm, but no independent source is available.
- `company_level_only`: source proves a company fact, not a personal contribution.
- `unverified`: not safe to publish as fact.
- `remove_or_clarify`: wording is reputationally risky.
- `low_authority`: true but not useful in top-level executive proof.

## Public proof record

A Track Record item should contain:

1. Title.
2. Date or range.
3. Context.
4. Personal mandate.
5. Scale, when verified.
6. Decision or action.
7. Outcome, when verified.
8. Source link.
9. Confidentiality note only when necessary.

## Case study model

```yaml
title:
date_range:
organisation_display:
sector:
confidentiality:
context:
decision:
personal_mandate:
team_scope:
technical_scope:
constraints:
actions:
outcomes:
metrics:
verification:
source_urls:
approved_quote:
cta:
```

No field should be inferred merely to complete the template.

## Publication/speaking record

```yaml
type: article | quote | panel | talk | interview | podcast
title:
outlet_or_event:
date:
role:
topic:
url:
recording_url:
language:
verified:
```

## Synchronisation rule

When a claim changes, search for all variants of:

- name;
- role;
- company;
- product;
- metric;
- audience;
- award;
- credential.

Then update every public and machine-readable representation in the same task.
