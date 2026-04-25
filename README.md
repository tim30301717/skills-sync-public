# skills-sync

`skills-sync` is a small CLI for keeping AI tool skills synchronized across
local tools, user profiles, and project folders.

The tool repo is intentionally separate from skill content:

- `skills-sync-public`: sync engine, profile templates, docs, and the
  `skills-sync-workflow` helper skill.
- `skills-hub-*`: skill content hubs. A hub owns its `skills/`,
  `targets.yaml`, and `.skills-sync-state/`.

## Quick Start

```powershell
cd C:\Project\ClaudeCode\skills-sync-public
copy targets.local.yaml.example targets.local.yaml

# Validate the public workflow skill in this repo.
python bin\skills-sync check

# Validate or install a separate hub.
python bin\skills-sync --hub C:\Project\ClaudeCode\skills-hub-cathay check
python bin\skills-sync --hub C:\Project\ClaudeCode\skills-hub-cathay status
python bin\skills-sync --hub C:\Project\ClaudeCode\skills-hub-cathay install --profile claude-user
```

You can also set `SKILLS_SYNC_HUB` instead of passing `--hub`.

## Hub Layout

```text
skills-hub-example/
  skills/
    <skill-id>/
      SKILL.md
      skill.yaml
      references/
      scripts/
  targets.yaml
  targets.local.yaml        # optional, ignored
  .skills-sync-state/       # ignored
```

`targets.yaml` chooses which profiles this hub syncs to. Machine-specific
paths belong in `targets.local.yaml`, never in shared public repos.

## Useful Commands

```powershell
python bin\skills-sync --hub <hub-path> check
python bin\skills-sync --hub <hub-path> status
python bin\skills-sync --hub <hub-path> install
python bin\skills-sync --hub <hub-path> diff --profile <profile> <skill-id>
python bin\skills-sync --hub <hub-path> import <profile>/<skill-id>
```

Without `--hub`, the CLI uses the tool repo itself as the hub. That is useful
for syncing the bundled `skills-sync-workflow` skill.
