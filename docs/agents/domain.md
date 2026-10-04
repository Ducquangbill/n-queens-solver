# Domain Docs: Single-Context Layout

This repo uses **single-context** domain documentation.

## Structure

```
CONTEXT.md          # Root domain model — ubiquitous language, core entities, key rules
docs/adr/           # Architecture Decision Records
  001-decision-title.md
  002-another-decision.md
```

## CONTEXT.md

Single source of truth for domain vocabulary. Contains:

- **Ubiquitous language** — terms, definitions, aliases
- **Core entities** — attributes, relationships, invariants
- **Key business rules** — constraints, edge cases
- **Bounded context** — what's in/out of scope

Update when domain understanding changes. Keep concise — link to ADRs for rationale.

## ADRs (docs/adr/)

One file per architectural decision:

```markdown
# ADR 001: Title

## Status
Accepted | Superseded | Deprecated

## Context
Problem, constraints, assumptions.

## Decision
What we chose and why.

## Consequences
### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

## References
- Link to related ADR, issue, or doc
```

Number sequentially (`001-`, `002-`, ...). Never delete — supersede with new ADR.

## Consumer Rules

- **Agents** read `CONTEXT.md` first for domain vocabulary
- **ADRs** consulted for "why" behind technical choices
- **Both** are read-only during implementation — edit only when domain/architecture changes