from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT_JSON = ROOT / "data/validator-audits/20260523-validator-test-fact-source-audit.json"
AUDIT_MD = ROOT / "docs/validator-audits/20260523-validator-test-fact-source-audit.md"
EVIDENCE_CLASSES = {
    "source_derived",
    "policy_derived",
    "synthetic_contract",
    "privacy_boundary",
    "artifact_consistency",
    "governance_boundary",
}


def main() -> int:
    errors: list[str] = []
    if not AUDIT_JSON.exists():
        errors.append(f"Missing {AUDIT_JSON.relative_to(ROOT)}")
    if not AUDIT_MD.exists():
        errors.append(f"Missing {AUDIT_MD.relative_to(ROOT)}")
    if errors:
        return _finish(errors)

    payload = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
    if payload.get("artifact_schema_version") != "validator_test_fact_source_audit/v1":
        errors.append("unexpected audit schema version")
    files = payload.get("files", [])
    audited_files = {record.get("file") for record in files}
    current_files = {
        path.relative_to(ROOT).as_posix()
        for pattern in ("tests/test_*.py", "tests/validation/validate_*.py")
        for path in ROOT.glob(pattern)
    }
    if audited_files != current_files:
        errors.append(f"audit file coverage mismatch: missing={sorted(current_files - audited_files)} extra={sorted(audited_files - current_files)}")
    for index, record in enumerate(files):
        if record.get("evidence_class") not in EVIDENCE_CLASSES:
            errors.append(f"files[{index}] has invalid evidence_class")
        if record.get("status") != "accepted_with_limits":
            errors.append(f"files[{index}] must be accepted_with_limits")
        if not record.get("primary_evidence"):
            errors.append(f"files[{index}] requires primary_evidence")
        if not record.get("limitations"):
            errors.append(f"files[{index}] requires limitations")
    return _finish(errors)


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Validator/test audit validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
