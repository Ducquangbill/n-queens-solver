# Issue Tracker: GitHub Issues

Issues live in this repository's GitHub Issues. Uses `gh` CLI for all operations.

## Workflow

1. **Create issue**: `gh issue create --title "Title" --body "Description" --label "needs-triage"`
2. **List issues**: `gh issue list --label "ready-for-agent"`
3. **Update status**: `gh issue edit <num> --add-label "ready-for-agent" --remove-label "needs-triage"`
4. **Close issue**: `gh issue close <num> --comment "Done"`

## Labels (match triage vocabulary)

| Label | Purpose |
|-------|---------|
| `needs-triage` | New issue, not yet assessed |
| `needs-info` | Blocked awaiting clarification |
| `ready-for-agent` | Clear spec, ready for AI implementation |
| `ready-for-human` | Requires human decision/approval |
| `wontfix` | Explicitly deferred/rejected |

## GitHub CLI Setup

```bash
# Authenticate (one-time)
gh auth login

# Set default repo (optional)
gh repo set-default owner/repo
```

## Migration from Local Markdown

Existing issues in `.scratch/n-queens-solver/` can be imported:

```bash
# Example: create issue from markdown file
gh issue create --title "Project setup" --body-file .scratch/n-queens-solver/001-project-setup.md --label "ready-for-agent"
```

## Notes

- Requires `gh` CLI installed and authenticated
- Issues persist on GitHub, not in local repo
- Labels must exist in repo (create once via `gh label create`)
- PRs can reference issues: `Fixes #123`