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
from sf6_knowledge_coach.paths import repo_root


class CleanSlateCliTests(unittest.TestCase):
    def test_resolves_current_fact_query_without_legacy_alias_fixture(self) -> None:
        context = resolve_query("JPの5LPってガードで何F？")
        self.assertEqual(context.character_slug, "jp")
        self.assertEqual(context.move_input, "5LP")
        self.assertEqual(context.field, "block_adv")

    def test_prepare_numeric_answer_holds_after_legacy_raw_retirement(self) -> None:
        packet = prepare_answer("JPの5LPはガードで何F？")
        self.assertEqual(packet["status"], "hold")
        self.assertIsNone(packet["answer"])
        self.assertEqual(packet["evidence"], [])
        self.assertIn("Legacy raw-backed current-fact lookup has been retired", packet["uncertainty"][0])
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
            self.assertEqual(record["packet"]["status"], "hold")

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

    def test_cli_current_lookup_is_unavailable_after_legacy_raw_retirement(self) -> None:
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
        self.assertEqual(payload["status"], "unavailable")
        self.assertIsNone(payload["value"])
        self.assertIn("Legacy raw-backed current-fact CLI lookup/search has been retired", payload["uncertainty"][0])

    def test_cli_search_is_unavailable_after_legacy_raw_retirement(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "sf6_knowledge_coach.cli",
                "search",
                "5LP",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "unavailable")
        self.assertEqual(payload["results"], [])


if __name__ == "__main__":
    unittest.main()
