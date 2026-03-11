from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_import_does_not_import_scrapling() -> None:
    src_dir = Path(__file__).resolve().parents[1] / "src"
    script = f"""
import sys
sys.path.insert(0, r"{src_dir}")
import sf6_ingest.cli
loaded = any(name.startswith("scrapling") for name in sys.modules)
print(loaded)
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, check=True)
    assert result.stdout.strip() == "False"


def test_cli_accepts_configured_luke_character_without_importing_fetchers() -> None:
    src_dir = Path(__file__).resolve().parents[1] / "src"
    script = f"""
import sys
sys.path.insert(0, r"{src_dir}")
from sf6_ingest.cli import build_parser
args = build_parser().parse_args(["fetch", "--character", "luke", "--source", "official"])
loaded = any(name.startswith("scrapling") for name in sys.modules)
print(args.character)
print(loaded)
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, check=True)
    assert result.stdout.splitlines() == ["luke", "False"]
