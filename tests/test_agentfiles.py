import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "agentfiles"


def run_agentfiles(*args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def write_skill(path: Path, name: str = "test-skill") -> None:
    path.mkdir(parents=True)
    (path / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        "description: Test skill.\n"
        "---\n\n"
        "Do the thing.\n"
    )


class AgentfilesTests(unittest.TestCase):
    def test_render_includes_global_and_repo_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            (source / "repos" / "repo-a" / "instructions").mkdir(parents=True)
            (source / "repos" / "repo-a" / "instructions" / "00-repo.md").write_text("Repo rule.\n")

            result = run_agentfiles(
                "--source",
                str(source),
                "render",
                "--target",
                "codex",
                "--repo-overlay",
                "repo-a=/tmp/repo-a",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("# Codex Instructions", result.stdout)
            self.assertIn("Global rule.", result.stdout)
            self.assertIn("When working under `/tmp/repo-a`", result.stdout)
            self.assertIn("Repo rule.", result.stdout)

    def test_install_links_skills_and_writes_managed_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            home = Path(tmp) / "home"
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            write_skill(source / "global" / "skills" / "test-skill")

            result = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "codex",
                "--home",
                str(home),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            instructions = home / ".codex" / "AGENTS.md"
            self.assertTrue(instructions.exists())
            self.assertIn("managed by agentfiles", instructions.read_text())
            skill_link = home / ".agents" / "skills" / "test-skill"
            self.assertTrue(skill_link.is_symlink())
            self.assertEqual(skill_link.resolve(), (source / "global" / "skills" / "test-skill").resolve())
            codex_skill_link = home / ".codex" / "skills" / "test-skill"
            self.assertTrue(codex_skill_link.is_symlink())
            self.assertEqual(codex_skill_link.resolve(), (source / "global" / "skills" / "test-skill").resolve())

    def test_install_preflights_all_skill_destinations(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            home = Path(tmp) / "home"
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            write_skill(source / "global" / "skills" / "test-skill")
            unmanaged = home / ".codex" / "skills" / "test-skill"
            unmanaged.mkdir(parents=True)

            result = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "codex",
                "--home",
                str(home),
            )

            self.assertEqual(result.returncode, 2)
            self.assertFalse((home / ".codex" / "AGENTS.md").exists())
            self.assertFalse((home / ".agents" / "skills" / "test-skill").exists())

    def test_install_preflights_skill_root_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            home = Path(tmp) / "home"
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            write_skill(source / "global" / "skills" / "test-skill")
            skill_root = home / ".codex" / "skills"
            skill_root.parent.mkdir(parents=True)
            skill_root.write_text("not a directory\n")

            result = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "codex",
                "--home",
                str(home),
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("exists and is not a directory", result.stderr)
            self.assertFalse((home / ".codex" / "AGENTS.md").exists())
            self.assertFalse((home / ".agents" / "skills" / "test-skill").exists())

    def test_install_preflights_instruction_path_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            home = Path(tmp) / "home"
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            write_skill(source / "global" / "skills" / "test-skill")
            instruction_path = home / ".codex" / "AGENTS.md"
            instruction_path.mkdir(parents=True)

            result = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "codex",
                "--home",
                str(home),
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("exists and is not a regular file", result.stderr)
            self.assertTrue(instruction_path.is_dir())
            self.assertFalse((home / ".agents" / "skills" / "test-skill").exists())

    def test_install_preflights_all_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            home = Path(tmp) / "home"
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            write_skill(source / "global" / "skills" / "test-skill")
            unmanaged = home / ".claude" / "skills" / "test-skill"
            unmanaged.mkdir(parents=True)

            result = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "all",
                "--home",
                str(home),
            )

            self.assertEqual(result.returncode, 2)
            self.assertFalse((home / ".codex" / "AGENTS.md").exists())
            self.assertFalse((home / ".agents" / "skills" / "test-skill").exists())
            self.assertFalse((home / ".codex" / "skills" / "test-skill").exists())
            self.assertFalse((home / ".claude" / "CLAUDE.md").exists())

    def test_install_is_idempotent_across_codex_skill_destinations(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            home = Path(tmp) / "home"
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            write_skill(source / "global" / "skills" / "test-skill")

            first = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "codex",
                "--home",
                str(home),
            )
            second = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "codex",
                "--home",
                str(home),
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(second.stdout.count("unchanged"), 3)

    def test_install_refuses_unmanaged_instruction_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            home = Path(tmp) / "home"
            (source / "global" / "instructions").mkdir(parents=True)
            (source / "global" / "instructions" / "00-global.md").write_text("Global rule.\n")
            unmanaged = home / ".codex" / "AGENTS.md"
            unmanaged.parent.mkdir(parents=True)
            unmanaged.write_text("human file\n")

            result = run_agentfiles(
                "--source",
                str(source),
                "install",
                "--target",
                "codex",
                "--home",
                str(home),
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("not managed by agentfiles", result.stderr)
            self.assertEqual(unmanaged.read_text(), "human file\n")

    def test_add_skill_creates_skeleton(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)

            result = run_agentfiles(
                "--source",
                str(source),
                "add-skill",
                "new-skill",
                "--description",
                "Use for tests.",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            skill = source / "global" / "skills" / "new-skill" / "SKILL.md"
            self.assertTrue(skill.exists())
            self.assertIn("name: new-skill", skill.read_text())
            self.assertTrue((source / "global" / "skills" / "new-skill" / "references").is_dir())
            self.assertTrue((source / "global" / "skills" / "new-skill" / "scripts").is_dir())

    def test_doctor_rejects_duplicate_skill_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            write_skill(source / "global" / "skills" / "one", name="same")
            write_skill(source / "repos" / "repo-a" / "skills" / "two", name="same")

            result = run_agentfiles(
                "--source",
                str(source),
                "doctor",
                "--repo-overlay",
                "repo-a",
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate skill metadata names", result.stderr)


if __name__ == "__main__":
    unittest.main()

