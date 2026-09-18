import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "bin" / "skills-sync"


class CheckValidationTests(unittest.TestCase):
    def run_check(
        self,
        directory: str,
        frontmatter: str,
        targets: list[str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            hub = Path(temp_dir)
            skill_dir = hub / "skills" / directory
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f"---\n{frontmatter}---\n\nInstructions.\n",
                encoding="utf-8",
            )
            if targets is not None:
                target_lines = "\n".join(f"- {target}" for target in targets)
                (skill_dir / "skill.yaml").write_text(
                    f"targets:\n{target_lines}\n",
                    encoding="utf-8",
                )
            return subprocess.run(
                [sys.executable, str(CLI), "--hub", str(hub), "check"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

    def test_accepts_copilot_compatible_frontmatter(self):
        result = self.run_check(
            "valid-skill",
            "name: valid-skill\ndescription: A valid portable skill.\n",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_name_that_does_not_match_directory(self):
        result = self.run_check(
            "valid-directory",
            "name: different-name\ndescription: A mismatched skill.\n",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must match the skill directory", result.stdout)

    def test_rejects_invalid_name_and_long_description(self):
        result = self.run_check(
            "invalid_name",
            f"name: invalid_name\ndescription: {'x' * 1025}\n",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must use lowercase letters", result.stdout)
        self.assertIn("description' exceeds 1024 characters", result.stdout)

    def test_warns_for_legacy_non_agent_target(self):
        result = self.run_check(
            "legacy-directory",
            "name: legacy-name\ndescription: A legacy tool-specific skill.\n",
            targets=["claude-code"],
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN legacy-directory/SKILL.md", result.stdout)

    def test_installs_copilot_user_profile(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            hub = root / "hub"
            skill_dir = hub / "skills" / "copilot-ready"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: copilot-ready\n"
                "description: A Copilot-compatible skill.\n---\n\nInstructions.\n",
                encoding="utf-8",
            )
            (skill_dir / "skill.yaml").write_text(
                "targets:\n- copilot-user\n",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["HOME"] = str(root / "home")

            result = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "--hub",
                    str(hub),
                    "install",
                    "--profile",
                    "copilot-user",
                ],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

            installed = root / "home" / ".copilot" / "skills" / "copilot-ready" / "SKILL.md"
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(installed.is_file())


if __name__ == "__main__":
    unittest.main()
