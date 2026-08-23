# Target information architecture

## Recommended end-state

Primary navigation:

- Home
- Track Record
- Century
- Advisory
- AI Diligence
- Insights
- About
- Contact

Secondary links:

- Media & Speaking
- Sources
- LinkedIn
- Century product site
- StackLevel Group

## Staged migration

The current static URLs have value and should not be broken. The first implementation stage may keep the physical filenames while changing navigation labels and page purpose:

| Current file | Stage-one label/purpose | End-state option |
|---|---|---|
| `index.html` | Home | `/` |
| `proof.html` | Track Record | `/track-record/` only if hosting migration is justified |
| `century.html` | Century | `/century/` |
| `enterprise.html` | Enterprise AI | part of `/advisory/` or retained |
| `founders.html` | Founder / CTO Advisory | `/advisory/` section |
| `investors.html` | AI Diligence | `/ai-diligence/` |
| `writing.html` | Insights | `/insights/` |
| `expert.html` | Media & Speaking | `/media-speaking/` |
| `origin.html` | About / Biography | `/about/` |
| `contact.html` | Contact | `/contact/` |
| `sources.html` | Sources / Evidence | retained as noindex or upgraded |

Do not perform a cosmetic URL migration on GitHub Pages without a reliable redirect layer.

## Page purposes

### Home

Fast identity, authority, proof, relevance, and action.

### Track Record

The central evidence page. It must separate verified outcomes, current roles, product recognition, public work, and background.

### Century

The strongest product-building anchor. It needs product scope, architecture, governance, adoption, evidence, and a clear relationship to Vadim.

### Advisory

A clear description of CTO-level work for enterprise teams, founders, and executives. It should describe decisions and deliverables rather than broad consulting language.

### AI Diligence

An investor-specific method and deliverable page. It must never imply investment authority or completed mandates that are not evidenced.

### Insights

A topical-authority hub for durable enterprise AI analysis.

### About

Exact biography, timeline, education, current roles, and approved downloadable bio.

### Media & Speaking

Verified appearances only, with source, date, role, topic, and link.

### Contact

Direct and intent-specific routes. No non-functional form.

## Navigation principles

- Keep primary navigation to roughly 7–8 items on desktop.
- Mobile uses a disclosure menu, not horizontal discovery.
- Use descriptive labels: Track Record, AI Diligence, Insights, About.
- Use `aria-current="page"`.
- Keep Sources available but not prominent.
