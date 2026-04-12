from __future__ import annotations

import argparse
import sys

from .config import available_character_slugs, load_character, load_fetch_profile, repo_root, selected_sources
from .core.io import load_snapshot, save_snapshot
from .core.pipeline import parse_from_raw, publish_run
from .core.prune import prune_latest_published_state
from .logging_utils import configure_logging
from .registry import load_registry
from .supercombo_binding_generation import (
    build_supercombo_binding_policy_document,
    write_supercombo_binding_policy_document,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SF6 frame data ingestion v3")
    subparsers = parser.add_subparsers(dest="command", required=True)
    character_choices = list(available_character_slugs())

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("--character", choices=character_choices, required=True)
    fetch_parser.add_argument("--source", choices=["official", "supercombo", "all"], default="all")

    parse_parser = subparsers.add_parser("parse-from-raw")
    parse_parser.add_argument("--character", choices=character_choices, required=True)
    parse_parser.add_argument("--source", choices=["official", "supercombo", "all"], default="all")
    parse_parser.add_argument("--official-snapshot-id")
    parse_parser.add_argument("--supercombo-snapshot-id")

    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("--character", choices=character_choices, required=True)
    publish_parser.add_argument("--run-id", required=True)

    binding_parser = subparsers.add_parser("generate-supercombo-binding")
    binding_parser.add_argument("--character", choices=character_choices, required=True)
    binding_parser.add_argument("--supercombo-snapshot-id", required=True)
    binding_parser.add_argument("--write", action="store_true")

    prune_parser = subparsers.add_parser("prune")
    prune_parser.add_argument("--character", choices=character_choices, required=True)
    mode_group = prune_parser.add_mutually_exclusive_group()
    mode_group.add_argument("--dry-run", action="store_true")
    mode_group.add_argument("--apply", action="store_true")
    prune_parser.add_argument("--verbose", action="store_true")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--character", choices=character_choices, required=True)
    run_parser.add_argument("--source", choices=["official", "supercombo", "all"], default="all")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = configure_logging()
    base_repo_root = repo_root()

    if args.command == "fetch":
        snapshot_ids = _fetch_command(args.character, args.source, base_repo_root)
        for source, snapshot_id in snapshot_ids.items():
            logger.info("fetched source=%s snapshot_id=%s", source, snapshot_id)
        return 0

    if args.command == "parse-from-raw":
        snapshot_ids = _snapshot_ids_from_args(args)
        run_id = parse_from_raw(args.character, snapshot_ids, base_repo_root)
        logger.info("normalized run created run_id=%s", run_id)
        return 0

    if args.command == "publish":
        summary = publish_run(args.character, args.run_id, base_repo_root)
        logger.info("publish complete run_id=%s states=%s", summary.run_id, summary.dataset_states)
        return 0

    if args.command == "generate-supercombo-binding":
        snapshot = load_snapshot(base_repo_root, "supercombo", args.character, args.supercombo_snapshot_id)
        registry = load_registry(args.character)
        document = build_supercombo_binding_policy_document(args.character, snapshot, registry)
        if args.write:
            path = write_supercombo_binding_policy_document(args.character, document)
            logger.info("binding policy written character=%s path=%s entries=%s", args.character, path, len(document.entries))
        else:
            logger.info("binding policy generated character=%s entries=%s (use --write to persist)", args.character, len(document.entries))
        return 0

    if args.command == "prune":
        summary = prune_latest_published_state(
            args.character,
            apply=args.apply,
            verbose=args.verbose,
            base_repo_root=base_repo_root,
        )
        for line in summary.render_lines(verbose=args.verbose):
            logger.info("%s", line)
        return 0

    if args.command == "run":
        snapshot_ids = _fetch_command(args.character, args.source, base_repo_root)
        run_id = parse_from_raw(args.character, snapshot_ids, base_repo_root)
        summary = publish_run(args.character, run_id, base_repo_root)
        logger.info("run complete run_id=%s states=%s", summary.run_id, summary.dataset_states)
        return 0

    parser.print_help(sys.stderr)
    return 2


def _fetch_command(character_slug: str, source: str, base_repo_root) -> dict[str, str]:
    character = load_character(character_slug)
    snapshot_ids: dict[str, str] = {}
    for source_name in selected_sources(character_slug, source):
        profile = load_fetch_profile(source_name)
        if source_name == "official":
            from .fetch.official import fetch_official_snapshot

            raw_bytes, metadata = fetch_official_snapshot(character, profile)
        else:
            from .fetch.supercombo import fetch_supercombo_snapshot

            raw_bytes, metadata = fetch_supercombo_snapshot(character, profile)
        saved = save_snapshot(base_repo_root, raw_bytes, metadata)
        snapshot_ids[source_name] = saved.metadata.snapshot_id
    return snapshot_ids


def _snapshot_ids_from_args(args: argparse.Namespace) -> dict[str, str]:
    snapshot_ids: dict[str, str] = {}
    chosen_sources = set(selected_sources(args.character, args.source))
    if "official" in chosen_sources:
        if not args.official_snapshot_id:
            raise SystemExit("--official-snapshot-id is required for parse-from-raw when source includes official")
        snapshot_ids["official"] = args.official_snapshot_id
    if "supercombo" in chosen_sources:
        if not args.supercombo_snapshot_id:
            raise SystemExit("--supercombo-snapshot-id is required for parse-from-raw when source includes supercombo")
        snapshot_ids["supercombo"] = args.supercombo_snapshot_id
    return snapshot_ids


if __name__ == "__main__":
    raise SystemExit(main())
