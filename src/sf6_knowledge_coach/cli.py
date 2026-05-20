from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .aliases import resolve_query
from .answering import append_answer_log, prepare_answer, verify_answer_packet
from .current_facts import lookup_current_fact, search_moves


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except (LookupError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if result is not None:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sf6")
    subparsers = parser.add_subparsers(required=True)

    context_parser = subparsers.add_parser("context")
    context_subparsers = context_parser.add_subparsers(required=True)
    resolve_parser = context_subparsers.add_parser("resolve")
    resolve_parser.add_argument("query")
    resolve_parser.set_defaults(func=_context_resolve)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.set_defaults(func=_search)

    current_parser = subparsers.add_parser("current")
    current_subparsers = current_parser.add_subparsers(required=True)
    lookup_parser = current_subparsers.add_parser("lookup")
    lookup_parser.add_argument("--character", required=True)
    lookup_parser.add_argument("--move", required=True)
    lookup_parser.add_argument("--field", default="block_adv")
    lookup_parser.set_defaults(func=_current_lookup)

    answer_parser = subparsers.add_parser("answer")
    answer_subparsers = answer_parser.add_subparsers(required=True)
    prepare_parser = answer_subparsers.add_parser("prepare")
    prepare_parser.add_argument("query")
    prepare_parser.add_argument("--log", action="store_true")
    prepare_parser.set_defaults(func=_answer_prepare)
    verify_parser = answer_subparsers.add_parser("verify")
    verify_parser.add_argument("query")
    verify_parser.set_defaults(func=_answer_verify)

    return parser


def _context_resolve(args: argparse.Namespace) -> dict[str, Any]:
    return resolve_query(args.query).to_dict()


def _search(args: argparse.Namespace) -> dict[str, Any]:
    return {"query": args.query, "results": search_moves(args.query, args.limit)}


def _current_lookup(args: argparse.Namespace) -> dict[str, Any]:
    return lookup_current_fact(args.character, args.move, args.field).to_dict()


def _answer_prepare(args: argparse.Namespace) -> dict[str, Any]:
    packet = prepare_answer(args.query)
    if args.log:
        packet["log_path"] = str(append_answer_log(packet))
    return packet


def _answer_verify(args: argparse.Namespace) -> dict[str, Any]:
    packet = prepare_answer(args.query)
    result = verify_answer_packet(packet)
    result["packet_status"] = packet.get("status")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
