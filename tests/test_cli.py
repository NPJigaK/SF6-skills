from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from sf6_knowledge_coach.aliases import resolve_query
from sf6_knowledge_coach.answering import append_answer_log, prepare_answer, verify_answer_packet
from sf6_knowledge_coach.current_facts import lookup_current_fact
from sf6_knowledge_coach.paths import repo_root


class CleanSlateCliTests(unittest.TestCase):
    def test_resolves_seed_alias_fixture(self) -> None:
        context = resolve_query("リュウの屈中Pってガードで何F？")
        self.assertEqual(context.character_slug, "ryu")
        self.assertEqual(context.move_input, "2MP")
        self.assertEqual(context.field, "block_adv")

    def test_current_fact_lookup_uses_official_raw(self) -> None:
        fact = lookup_current_fact("jp", "5LP", "block_adv")
        self.assertEqual(fact.value, "-2")
        self.assertEqual(fact.authority, "data/exports official_raw")
        self.assertTrue(fact.source_path.endswith("data/exports/jp/official_raw.json"))

    def test_prepare_numeric_answer_requires_deterministic_evidence(self) -> None:
        packet = prepare_answer("JPの5LPはガードで何F？")
        self.assertEqual(packet["status"], "answered")
        self.assertEqual(packet["evidence"][0]["kind"], "deterministic_current_fact_lookup")
        verification = verify_answer_packet(packet)
        self.assertTrue(verification["ok"], verification)

    def test_numeric_answer_holds_without_lookup_context(self) -> None:
        packet = prepare_answer("これはガードで何F？")
        self.assertEqual(packet["status"], "hold")
        self.assertIn("character_slug", packet["uncertainty"][0])

    def test_answer_log_is_outside_repo(self) -> None:
        packet = prepare_answer("JPの5LPはガードで何F？")
        with tempfile.TemporaryDirectory() as tmp:
            path = append_answer_log(packet, Path(tmp))
            self.assertTrue(path.exists())
            self.assertNotIn(repo_root(), path.resolve().parents)
            record = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(record["packet"]["status"], "answered")

    def test_answer_log_rejects_repo_internal_base_dir_without_writing(self) -> None:
        packet = prepare_answer("JPの5LPはガードで何F？")
        target_dir = repo_root() / "__forbidden_answer_log_dir__"
        target_file = target_dir / "answer-log.jsonl"
        self.assertFalse(target_dir.exists())

        with self.assertRaises(ValueError):
            append_answer_log(packet, target_dir)

        self.assertFalse(target_dir.exists())
        self.assertFalse(target_file.exists())

    def test_answer_log_rejects_repo_internal_env_dir_without_writing(self) -> None:
        packet = prepare_answer("JPの5LPはガードで何F？")
        target_dir = repo_root() / "__forbidden_env_answer_log_dir__"
        target_file = target_dir / "answer-log.jsonl"
        self.assertFalse(target_dir.exists())

        with mock.patch.dict(os.environ, {"SF6_COACH_LOG_DIR": str(target_dir)}):
            with self.assertRaises(ValueError):
                append_answer_log(packet)

        self.assertFalse(target_dir.exists())
        self.assertFalse(target_file.exists())

    def test_cli_current_lookup(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "sf6_knowledge_coach.cli",
                "current",
                "lookup",
                "--character",
                "jp",
                "--move",
                "5LP",
                "--field",
                "block_adv",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["value"], "-2")


if __name__ == "__main__":
    unittest.main()
