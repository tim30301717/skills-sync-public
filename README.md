# skills-sync

## Overview / 概覽

`skills-sync` is a small CLI for keeping AI tool skills synchronized across
local tools, user profiles, and project folders.

`skills-sync` 是一個小型 CLI，用來把 AI 工具的 skills 同步到不同本機工具、
使用者 profile，以及專案資料夾。

The sync tool is intentionally separate from skill content.

同步工具刻意和 skill 內容分離。

- `skills-sync-public`: sync engine, profile templates, docs, and the
  `skills-sync-workflow` helper skill.
- `skills-sync-public`：同步引擎、profile 範本、文件，以及
  `skills-sync-workflow` 輔助 skill。
- `skills-hub-*`: skill content hubs. A hub owns its `skills/`,
  `targets.yaml`, and `.skills-sync-state/`.
- `skills-hub-*`：skill 內容倉庫。每個 hub 擁有自己的 `skills/`、
  `targets.yaml` 和 `.skills-sync-state/`。

## Quick Start / 快速開始

```powershell
# Clone this repo and move into it.
# 複製這個 repo，並進入資料夾。
git clone https://github.com/tim30301717/skills-sync-public.git
cd skills-sync-public

# Optional: create local machine-specific settings.
# 選用：建立只屬於本機的設定檔。
Copy-Item targets.local.yaml.example targets.local.yaml

# Validate the public workflow skill in this repo.
# 驗證這個 repo 內建的 public workflow skill。
python bin\skills-sync check

# Validate or install a separate skills hub.
# 驗證或安裝另一個 skills hub。
$hub = "<path-to-your-skills-hub>"
python bin\skills-sync --hub $hub check
python bin\skills-sync --hub $hub status
python bin\skills-sync --hub $hub install --profile claude-user
```

You can also set `SKILLS_SYNC_HUB` instead of passing `--hub`.

你也可以設定 `SKILLS_SYNC_HUB` 環境變數，取代每次傳入 `--hub`。

## Hub Layout / Hub 結構

```text
skills-hub-example/
  skills/
    <skill-id>/
      SKILL.md
      skill.yaml
      references/
      scripts/
  targets.yaml
  targets.local.yaml        # optional, ignored / 選用，會被忽略
  .skills-sync-state/       # ignored / 會被忽略
```

`targets.yaml` chooses which profiles this hub syncs to. Machine-specific
paths belong in `targets.local.yaml`, never in shared public repos.

`targets.yaml` 決定這個 hub 要同步到哪些 profiles。和個人電腦有關的路徑
應該放在 `targets.local.yaml`，不要放進共享的 public repo。

## Hermes Agent / Ubuntu VM

Hermes Agent uses the Agent Skills format and reads user skills from
`${HOME}/.hermes/skills`. To sync a hub into Hermes inside an Ubuntu VM,
clone both repos inside the VM and install with the `hermes-user` profile:

```bash
cd ~/skills-sync-public
python bin/skills-sync --hub ~/skills-hub-public check
python bin/skills-sync --hub ~/skills-hub-public status
python bin/skills-sync --hub ~/skills-hub-public install --profile hermes-user
```

To make Hermes part of a hub's default sync targets, enable it in that hub's
`targets.yaml`:

```yaml
profiles:
  - hermes-user
```

If you prefer Hermes to scan a shared read-only skill directory instead, sync
to `agents-user` and add the external directory in `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
```
## Useful Commands / 常用指令

```powershell
python bin\skills-sync --hub <hub-path> check
python bin\skills-sync --hub <hub-path> status
python bin\skills-sync --hub <hub-path> install
python bin\skills-sync --hub <hub-path> diff --profile <profile> <skill-id>
python bin\skills-sync --hub <hub-path> import <profile>/<skill-id>
```

Without `--hub`, the CLI uses the tool repo itself as the hub. That is useful
for syncing the bundled `skills-sync-workflow` skill.

如果沒有傳入 `--hub`，CLI 會把同步工具 repo 本身視為 hub。這主要用來同步
內建的 `skills-sync-workflow` skill。
