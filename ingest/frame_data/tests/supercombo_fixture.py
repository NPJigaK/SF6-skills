from __future__ import annotations

from typing import Iterable


LABEL_BLOCKS: tuple[tuple[str, ...], ...] = (
    ("Damage", "Chip Dmg", "Dmg Scaling", "Guard", "Cancel", "Hitconfirm Window"),
    ("Startup", "Active", "Recovery", "Hitstun", "Blockstun", "Hitstop"),
    ("Total", "DriveDmg Blk", "DriveDmg Hit [PC]", "Drive Gain", "Super Gain Hit", "Super Gain Blk"),
    ("Invuln", "Armor", "Airborne", "Juggle Start", "Juggle Increase", "Juggle Limit"),
    ("After DR Hit", "After DR Blk", "Projectile Speed", "Attack Range", "DR Cancel Hit", "DR Cancel Blk"),
    ("Punish Advantage", "Perfect Parry Advantage"),
    ("Hit Advantage", "Block Advantage"),
    ("Notes",),
)


DEFAULT_VALUES = {
    "Damage": "300",
    "Chip Dmg": "0",
    "Dmg Scaling": "-",
    "Guard": "All",
    "Cancel": "Special",
    "Hitconfirm Window": "13",
    "Startup": "5",
    "Active": "3",
    "Recovery": "11",
    "Hitstun": "11",
    "Blockstun": "9",
    "Hitstop": "9",
    "Total": "18",
    "DriveDmg Blk": "-500",
    "DriveDmg Hit [PC]": "-2000",
    "Drive Gain": "250",
    "Super Gain Hit": "300",
    "Super Gain Blk": "150",
    "Invuln": "-",
    "Armor": "-",
    "Airborne": "-",
    "Juggle Start": "-",
    "Juggle Increase": "-",
    "Juggle Limit": "-",
    "After DR Hit": "+8",
    "After DR Blk": "+4",
    "Projectile Speed": "0.13",
    "Attack Range": "2.4",
    "DR Cancel Hit": "+4",
    "DR Cancel Blk": "+1",
    "Punish Advantage": "+2",
    "Perfect Parry Advantage": "-6",
    "Hit Advantage": "+4",
    "Block Advantage": "-2",
    "Notes": "Fixture note",
}


def build_supercombo_contract_html(include_tokens: set[str] | None = None) -> str:
    return build_supercombo_contract_html_with_tables(
        [
        (
            "Character Data",
            "Character Vitals",
            "Vitals",
            None,
            '<table><tr><th>Vitals</th><th>JP</th></tr><tr><td>HP</td><td>10000</td></tr></table>',
        ),
        (
            "Normals",
            "Normals and Target Combos",
            "5LP",
            "jp_5lp",
            build_supercombo_move_table(
                raw_source_token="jp_5lp",
                notation="5LP",
                move_name="Standing Light Punch",
                overrides={"Notes": "Chains into 5LP"},
            ),
        ),
        (
            "Normals",
            "Normals and Target Combos",
            "J.LP",
            "jp_jlp",
            build_supercombo_move_table(
                raw_source_token="jp_jlp",
                notation="j.LP",
                move_name="Jumping Light Punch",
                overrides={"Notes": "Alias drift row"},
            ),
        ),
        (
            "Supers",
            "Supers",
            "236236K (CA)",
            "jp_236236k(ca)",
            build_supercombo_move_table(
                raw_source_token="jp_236236k(ca)",
                notation="236236K",
                move_name="CA Zappriet",
                overrides={"Punish Advantage": "KD +44", "Notes": "CA token must stay verbatim"},
            ),
        ),
        (
            "Drive and Throw",
            "Drive and Throw",
            "6HPHK Recovery",
            "jp_6hphk_recovery",
            build_supercombo_move_table(
                raw_source_token="jp_6hphk_recovery",
                notation="6HPHK",
                move_name="Exilio (Recovery)",
                overrides={"Invuln": "1-20 Full", "Notes": "Wakes up into drive reversal"},
            ),
        ),
        (
            "Drive and Throw",
            "Drive and Throw",
            "MPMK 66 DRC",
            "jp_mpmk_66_drc",
            build_supercombo_move_table(
                raw_source_token="jp_mpmk_66_drc",
                notation="66",
                move_name="Cancel Drive Rush",
                overrides={"After DR Hit": "+12", "After DR Blk": "+8", "Notes": "Confirmed F binding"},
            ),
        ),
        (
            "Specials",
            "Special Moves",
            "22PP",
            "jp_22pp",
            build_supercombo_move_table(
                raw_source_token="jp_22pp",
                notation="22PP",
                move_name="OD Triglav",
                overrides={"Notes": "One-to-many withheld"},
            ),
        ),
        (
            "Specials",
            "Special Moves",
            "214P~214HP",
            "jp_214p_214hp",
            build_supercombo_move_table(
                raw_source_token="jp_214p_214hp",
                notation="214P~214HP",
                move_name="Vihaat Cheni",
                overrides={"Punish Advantage": "KD +58(+60)", "Notes": "Collision withheld"},
            ),
        ),
        (
            "Specials",
            "Special Moves",
            "22K Bomb",
            "jp_22k_bomb",
            build_supercombo_move_table(
                raw_source_token="jp_22k_bomb",
                notation="22K",
                move_name="Amnesia Bomb",
                overrides={"Notes": "Excluded G row"},
            ),
        ),
        ],
        include_tokens=include_tokens,
    )


def build_supercombo_contract_html_with_tables(
    tables: list[tuple[str, str, str, str | None, str]],
    *,
    include_tokens: set[str] | None = None,
    character_label: str = "JP",
    page_title: str = "Street Fighter 6/JP/Data - SuperCombo Wiki",
) -> str:
    parts = ["<!doctype html>", "<html lang=\"en\">", "  <head>", "    <meta charset=\"utf-8\">", f"    <title>{page_title}</title>", "  </head>", "  <body>", "    <main>"]
    for h2, h4, h5, raw_source_token, table_html in tables:
        if include_tokens is not None and raw_source_token is not None and raw_source_token not in include_tokens:
            continue
        parts.append(f"      <h2>{h2}</h2>")
        parts.append(f"      <h4>{h4}</h4>")
        parts.append(f"      <h5>{h5}</h5>")
        parts.append(f"      {table_html}")
    parts.append("      <p>This page was last edited on 11 February 2026, at 00:00.</p>")
    parts.append("    </main>")
    parts.append("  </body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def build_supercombo_move_table(
    *,
    raw_source_token: str,
    notation: str,
    move_name: str,
    overrides: dict[str, str],
    character_label: str = "JP",
) -> str:
    values = {**DEFAULT_VALUES, **overrides}
    rows = [
        f"        <tr><th colspan=\"6\">{character_label} {raw_source_token}</th></tr>",
        f"        <tr><th colspan=\"6\">{notation} {move_name}</th></tr>",
        "        <tr><td colspan=\"6\"><img src=\"about:blank\" alt=\"\"></td></tr>",
    ]
    for labels in LABEL_BLOCKS:
        rows.append(_header_row(labels))
        rows.append(_value_row(values[label] for label in labels))
    return "<table>\n" + "\n".join(rows) + "\n      </table>"


def _header_row(labels: Iterable[str]) -> str:
    return "        <tr>" + "".join(f"<th>{label}</th>" for label in labels) + "</tr>"


def _value_row(values: Iterable[str]) -> str:
    return "        <tr>" + "".join(f"<td>{value}</td>" for value in values) + "</tr>"
