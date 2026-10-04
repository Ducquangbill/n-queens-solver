# Triage Label Vocabulary

Default five canonical labels — used by the `triage` skill.

| Label | Purpose |
|-------|---------|
| `needs-triage` | New issue, not yet assessed |
| `needs-info` | Blocked awaiting clarification from user/stakeholder |
| `ready-for-agent` | Clear spec, ready for AI implementation |
| `ready-for-human` | Requires human decision, design, or approval |
| `wontfix` | Explicitly deferred or rejected |

## Usage

- Apply exactly one triage label per issue at any time
- Labels are mutually exclusive — move issue through them sequentially
- `triage` skill reads/writes these labels automatically