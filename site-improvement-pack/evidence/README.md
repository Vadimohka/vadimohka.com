# Evidence directory

This directory prevents a polished site from publishing claims that the available evidence cannot support.

## Files

- `source-register.csv` — public sources and what each source actually proves.
- `claim-register.csv` — current claims, evidence status, safe wording and owner action.
- `claim-policy.md` — rules for using evidence.
- `source-notes.md` — practical interpretation of the public source set.
- `owner-input.example.yaml` — structured unknowns that only the owner can safely provide.
- `owner-questionnaire.md` — interview questions for creating real case studies.
- `external-profile-consistency.md` — off-site reputation cleanup.

## Important distinction

A source can be real and still be insufficient.

Examples:

- An official company page can verify a current title but not every client engagement.
- A product award can verify recognition of the product but not a personal award.
- A university article can verify a specific coaching event but not an aggregate “200+ teams” figure.
- A first-party profile can reveal current positioning but does not independently prove it.

## Update practice

For every source used in production:

1. check that it still resolves;
2. record the exact publication/event date;
3. record the exact wording supported;
4. avoid broader paraphrases;
5. update `last checked` in the internal claim ledger;
6. remove the public claim if the source disappears and no alternative exists.
