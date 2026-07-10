---
name: skills-sync-workflow
description: "Manage Tim's skills-sync-workflow skill for the split skills-sync workflow: use the public sync engine repo with private or team skills hubs, check sync status, install skills to AI tools, import target edits back to the right hub, and keep the workflow skill itself synchronized."
---

# Skills Sync Workflow Skill

Alias: `skills-sync-workflow`

## Repository Model

The sync engine and skill content are intentionally split.

| Purpose | Local path | GitHub visibility |
|---|---|---|
| Sync tool and workflow skill | `C:\Codex\Tim_Codex\skills-sync-public` | public |
| Tim's personal skills hub | `C:\Codex\Tim_Codex\skills-hub-tim-private` | private |
| Cathay/team skills hub | `C:\Codex\Tim_Codex\skills-hub-cathay` | private |
| Legacy source/migration repo | `C:\Codex\Tim_Codex\skills-sync` | private/archive only |

Use `skills-sync-public` for the CLI. Use `--hub <hub-path>` whenever the
skill content lives in a separate hub.

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private status
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-cathay status
```

Without `--hub`, the CLI treats `skills-sync-public` itself as the hub. That is
mainly for installing or updating this `skills-sync-workflow` skill.

## Common Profiles

Portable profiles:

| Profile | Target folder |
|---|---|
| `claude-user` | `${HOME}/.claude/skills` |
| `agents-user` | `${HOME}/.agents/skills` |
| `opencode-user` | `${HOME}/.config/opencode/skills` |
| `gemini-user` | `${HOME}/.gemini/skills` |
| `antigravity-user` | `${HOME}/.gemini/config/skills` |
| `antigravity-cli` | `${HOME}/.gemini/antigravity-cli/skills` |
| `hermes-user` | `${HOME}/.hermes/skills` |
| `claude-project` | `${PROJECT_ROOT}/.claude/skills` |
| `agents-project` | `${PROJECT_ROOT}/.agents/skills` |
| `opencode-project` | `${PROJECT_ROOT}/.opencode/skills` |
| `gemini-workspace` | `${PROJECT_ROOT}/.gemini/skills` |
| `antigravity-workspace` | `${PROJECT_ROOT}/.agents/skills` |

Tim's backward-compatible profiles:

| Profile | Target folder |
|---|---|
| `claude-code` | `${HOME}/.claude/skills` |
| `codex` | `${HOME}/.codex/skills` |
| `gemini-cli` | `${HOME}/.gemini/skills` |
| `cowork-vault` | `${COWORK_VAULT_DIR}/.claude/skills` |
| `cowork-obsidian` | `${COWORK_OBSIDIAN_DIR}/.claude/skills` |
| `cowork-claude` | `${COWORK_CLAUDE_DIR}/.claude/skills` |
| `cherry-claw` | `${CHERRYSTUDIO_SKILLS_DIR}` |

`cowork` is a logical group in `config/profiles.yaml` that expands to the three
Cowork anchors. `import` must use a concrete anchor, not the group.

## Guardrails

- Treat each hub's `skills/` folder as canonical for that hub.
- Do not put personal skills into `skills-sync-public`.
- Keep `targets.local.yaml` local and untracked.
- Use `--hub C:\Codex\Tim_Codex\skills-hub-tim-private` for Tim's personal skills.
- Use `--hub C:\Codex\Tim_Codex\skills-hub-cathay` for Cathay/team skills.
- Do not use `--force` unless Tim explicitly wants to discard target-side edits.
- Before `import`, run `diff` and inspect what will be pulled into the hub.
- Do not manage Codex built-ins such as `.system` or bundled plugin skills.

## Status Meanings

| Status | Meaning | Usual action |
|---|---|---|
| `synced` | hub, state, and target match | No action |
| `ahead` | hub changed; target still matches last install | Run `install` |
| `drifted` | target changed outside `skills-sync` | Run `diff`, then `import` if the change should be kept |
| `conflict` | hub and target both changed | Inspect both sides; avoid `--force`; import or manually merge |
| `missing` | target does not have the skill yet | Run `install` |

## Check Health

For the public workflow skill:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
git status -sb
python bin\skills-sync check
python bin\skills-sync status
```

For Tim's private hub:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
git -C C:\Codex\Tim_Codex\skills-hub-tim-private status -sb
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private check
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private status
```

For Cathay/team skills:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
git -C C:\Codex\Tim_Codex\skills-hub-cathay status -sb
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-cathay check
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-cathay status
```

## Hermes Agent on Ubuntu

Hermes Agent reads user skills from `${HOME}/.hermes/skills`, so use the
`hermes-user` profile inside the Ubuntu VM where Hermes is installed:

```bash
cd ~/skills-sync-public
python bin/skills-sync --hub ~/skills-hub-public check
python bin/skills-sync --hub ~/skills-hub-public status
python bin/skills-sync --hub ~/skills-hub-public install --profile hermes-user
```

Prefer cloning the sync tool and hub inside the VM instead of syncing directly
from a Windows `C:\Project\...` path. If you want Hermes to read shared skills
without owning them, install to `agents-user` and configure Hermes
`skills.external_dirs` with `~/.agents/skills`.

## OpenCode

OpenCode discovers Agent Skills natively from:

- User scope: `${HOME}/.config/opencode/skills/<skill-id>/SKILL.md`
- Project scope: `${PROJECT_ROOT}/.opencode/skills/<skill-id>/SKILL.md`

It also reads Claude-compatible `${HOME}/.claude/skills` and
agent-compatible `${HOME}/.agents/skills`, so the existing `claude-code` or
`agents-user` profiles may already be visible to OpenCode. Prefer
`opencode-user` when you want an explicit OpenCode target with independent
status, diff, and import tracking.

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private check
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private status --profile opencode-user
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private install --profile opencode-user
```

For project-local OpenCode skills, set `PROJECT_ROOT` in `targets.local.yaml`
and install with `--profile opencode-project`.

If a skill has a `targets:` allow-list in `skill.yaml`, add `opencode-user` or
`opencode-project` to that list before installing to the OpenCode profile.

## Google Antigravity

Official Google docs describe Antigravity CLI as the terminal-first surface for
Antigravity agents and the individual-user replacement path for Gemini CLI.
Antigravity 2.0, Antigravity IDE, and Antigravity CLI share a common agent
harness. Agent Skills are still plain folders with `SKILL.md`, so this repo can
support Antigravity with profiles instead of a separate sync engine.

Use `antigravity-user` as the default global target:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private check
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private install --profile antigravity-user
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private status --profile antigravity-user
```

Use `antigravity-cli` only when you specifically want CLI-scoped global skills
under Antigravity CLI's own config tree:

```powershell
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private install --profile antigravity-cli
```

For project-local Antigravity skills, set `PROJECT_ROOT` in
`targets.local.yaml` on that machine and install with
`--profile antigravity-workspace`. This writes to `${PROJECT_ROOT}/.agents/skills`,
which is the shared workspace Agent Skills path.

Recommended cross-machine shape:

- Clone `skills-sync-public` and the owning `skills-hub-*` repos separately on
  Windows and macOS.
- Keep each machine's absolute paths in its own untracked `targets.local.yaml`.
- Use Git commits/pushes in the hub as the cross-machine source of truth.
- Before importing target-side edits, run `status` and `diff` on the concrete
  profile where the edit happened, such as `antigravity-user/<skill-id>`.
- Avoid iCloud/OneDrive live-sync folders for active skill targets; agent tools
  can create conflicts while editing.

## Install Skills

Install the public workflow skill to all enabled profiles in
`skills-sync-public/targets.yaml`:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync check
python bin\skills-sync install --skill skills-sync-workflow
python bin\skills-sync status
```

Install Tim's private hub:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private check
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private install
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private status
```

Install the Cathay/team hub:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-cathay check
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-cathay install
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-cathay status
```

For one skill:

```powershell
python bin\skills-sync --hub <hub-path> install --profile <profile> --skill <skill-id>
```

## Import Target Edits

Pick the hub that owns the skill, then import from the profile where the edit
happened.

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync --hub <hub-path> status --profile <profile>
python bin\skills-sync --hub <hub-path> diff --profile <profile> <skill-id>
python bin\skills-sync --hub <hub-path> import <profile>/<skill-id>
python bin\skills-sync --hub <hub-path> check
git -C <hub-path> diff -- skills/<skill-id>
```

Examples:

```powershell
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private import codex/obsidian-search
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private import claude-code/obsidian-search
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-tim-private import cowork-vault/obsidian-search
python bin\skills-sync --hub C:\Codex\Tim_Codex\skills-hub-cathay import claude-user/<skill-id>
```

After reviewing, commit in the hub repo:

```powershell
git -C <hub-path> status -sb
git -C <hub-path> add skills/<skill-id>
git -C <hub-path> commit -m "Update <skill-id> skill"
git -C <hub-path> push
```

## Add A New Skill

Create the skill in the owning hub:

```text
<hub-path>/
  skills/
    <skill-id>/
      SKILL.md
      skill.yaml
```

Minimal `skill.yaml`:

```yaml
id: <skill-id>
version: 0.1.0
variants:
  default: SKILL.md
targets:
  - claude-user
```

Then validate and install:

```powershell
cd C:\Codex\Tim_Codex\skills-sync-public
python bin\skills-sync --hub <hub-path> check
python bin\skills-sync --hub <hub-path> install --profile <profile> --skill <skill-id>
python bin\skills-sync --hub <hub-path> status --profile <profile>
```

For Tim-only skills, prefer `skills-hub-tim-private`. For company/team skills,
prefer `skills-hub-cathay`.
