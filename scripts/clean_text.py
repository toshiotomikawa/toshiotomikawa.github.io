"""Deterministic Unicode watermark and invisible character cleaner.
Based on standards from https://github.com/guillaumemeyer/watermarks-remover.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Format and invisible controls commonly used for steganography, tracking, or broken pastes.
STRIP_CODEPOINTS: frozenset[int] = frozenset(
    {
        0x00AD,  # soft hyphen
        0x034F,  # combining grapheme joiner
        0x061C,  # Arabic letter mark
        0x115F,  # Hangul choseong filler
        0x1160,  # Hangul jungseong filler
        0x17B4,  # Khmer vowel inherent AQ
        0x17B5,  # Khmer vowel inherent AA
        0x180B,  # Mongolian free variation selector-1
        0x180C,  # Mongolian free variation selector-2
        0x180D,  # Mongolian free variation selector-3
        0x180E,  # Mongolian vowel separator
        0x180F,  # Mongolian free variation selector-4
        0x200B,  # zero-width space
        0x200C,  # zero-width non-joiner
        0x200D,  # zero-width joiner
        0x200E,  # left-to-right mark
        0x200F,  # right-to-left mark
        0x202A,  # left-to-right embedding
        0x202B,  # right-to-left embedding
        0x202C,  # pop directional formatting
        0x202D,  # left-to-right override
        0x202E,  # right-to-left override
        0x2060,  # word joiner
        0x2061,  # function application
        0x2062,  # invisible times
        0x2063,  # invisible separator
        0x2064,  # invisible plus
        0x2065,  # unassigned default-ignorable
        0x2066,  # left-to-right isolate
        0x2067,  # right-to-left isolate
        0x2068,  # first strong isolate
        0x2069,  # pop directional isolate
        0x206A,  # inhibit symmetric swapping
        0x206B,  # activate symmetric swapping
        0x206C,  # inhibit Arabic form shaping
        0x206D,  # activate Arabic form shaping
        0x206E,  # national digit shapes
        0x206F,  # nominal digit shapes
        0x3164,  # Hangul filler
        0xFFA0,  # halfwidth Hangul filler
        0xFFF9,  # interlinear annotation anchor
        0xFFFA,  # interlinear annotation separator
        0xFFFB,  # interlinear annotation terminator
        0xFEFF,  # byte order mark / zero-width no-break space
    }
    | set(range(0xFE00, 0xFE10))    # Variation selectors VS1..VS16
    | set(range(0xE0100, 0xE01F0))  # Variation selectors supplement VS17..VS256
    | set(range(0xFFF0, 0xFFF9))    # Reserved ignorable range
    | set(range(0xE0080, 0xE0100))  # Reserved ignorable range
)

# Spaces that substitute for standard ASCII space U+0020.
SPACE_HOMOGLYPHS: dict[int, str] = {
    0x00A0: " ",  # no-break space
    0x1680: " ",  # Ogham space mark
    0x2000: " ",  # en quad
    0x2001: " ",  # em quad
    0x2002: " ",  # en space
    0x2003: " ",  # em space
    0x2004: " ",  # three-per-em space
    0x2005: " ",  # four-per-em space
    0x2006: " ",  # six-per-em space
    0x2007: " ",  # figure space
    0x2008: " ",  # punctuation space
    0x2009: " ",  # thin space
    0x200A: " ",  # hair space
    0x202F: " ",  # narrow no-break space
    0x205F: " ",  # medium mathematical space
    0x3000: " ",  # ideographic space
}


def clean_text(text: str) -> str:
    """Normalize space homoglyphs and strip invisible characters."""
    buf = []
    for ch in text:
        cp = ord(ch)
        if cp in STRIP_CODEPOINTS:
            continue
        if cp in SPACE_HOMOGLYPHS:
            buf.append(SPACE_HOMOGLYPHS[cp])
            continue
        buf.append(ch)
    return "".join(buf)


def audit_text(text: str) -> list[tuple[int, int, str]]:
    """Return a list of (index, codepoint, description) for detected watermarks."""
    findings = []
    for idx, ch in enumerate(text):
        cp = ord(ch)
        if cp in STRIP_CODEPOINTS:
            findings.append((idx, cp, f"Invisible/Strippable U+{cp:04X}"))
        elif cp in SPACE_HOMOGLYPHS:
            findings.append((idx, cp, f"Space homoglyph U+{cp:04X}"))
    return findings


def process_file(path: Path, fix: bool = False) -> list[tuple[int, int, str]]:
    text = path.read_text(encoding="utf-8")
    findings = audit_text(text)
    if findings and fix:
        cleaned = clean_text(text)
        path.write_text(cleaned, encoding="utf-8")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and clean invisible Unicode watermarks.")
    parser.add_argument("--fix", action="store_true", help="Clean detected watermarks in-place.")
    parser.add_argument("paths", nargs="*", help="File paths to inspect or clean.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    if not args.paths:
        paths = list((root / "content").glob("*.json")) + [
            root / "assets/site.css",
            root / "assets/preferences.js",
            root / "scripts/build.py",
        ]
    else:
        paths = [Path(p) for p in args.paths]

    total_findings = 0
    for p in paths:
        if not p.exists():
            continue
        findings = process_file(p, fix=args.fix)
        if findings:
            total_findings += len(findings)
            print(f"[{'FIXED' if args.fix else 'FOUND'}] {p}: {len(findings)} watermark codepoint(s)")
            for idx, cp, desc in findings:
                print(f"  at index {idx}: {desc}")

    if total_findings == 0:
        print("Clean: 0 watermark codepoints found across inspected files.")
        return 0
    return 0 if args.fix else 1


if __name__ == "__main__":
    sys.exit(main())
