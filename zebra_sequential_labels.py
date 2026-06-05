"""
Zebra Library Shelf Label Generator
=====================================
Designed for high-density library storage facilities.
Generates ZPL labels for a single Range Side per job,
or all range sides at once using --batch mode.

Label size: 1" H x 2" W @ 203 dpi = 203 (H) x 402 (W) dots

Label layout:
  ┌──────────────────────────────────────┐
  │  RANGE      │  LADDER     │  SHELF   │
  │  (small)    │  (small)    │  (small) │
  │    5L       │    04       │    07    │
  │  (large)    │  (large)    │  (large) │
  └──────────────────────────────────────┘
  Large bold numbers dominate for easy wayfinding.
  Small text labels sit centered above each number.
  The entire block (descriptor + gap + number) is
  vertically centered on the label as a unit.

Usage:
  Single run:   python zebra_sequential_labels.py
  Preview mode: python zebra_sequential_labels.py --preview
  Labelary PNG: python zebra_sequential_labels.py --png
  Batch mode:   python zebra_sequential_labels.py --batch
"""

import socket
import os
import sys
import urllib.request
import urllib.error
import time

# ─────────────────────────────────────────────
# CONFIGURATION — Edit this section per job
# ─────────────────────────────────────────────

RANGE_SIDE   = "5L"     # e.g., "1L", "1R", "2L" ... "9R"
NUM_LADDERS  = 58       # Number of ladders on this range side
NUM_SHELVES  = 16       # Default number of shelves per ladder

LADDER_START = 1        # Starting ladder number (usually 1)
SHELF_START  = 1        # Starting shelf number (usually 1)

# Optional: specify different shelf counts for specific ladders.
# Use this for ladders that contain flat file drawers with more shelves
# than the standard count. Any ladder NOT listed here will use NUM_SHELVES.
#
# Example for 5R (ladders with flat files have 26 shelves):
#   SPECIAL_SHELVES = {2:26, 4:26, 6:26, 8:26, 10:26, 12:26, 14:26,
#                      16:26, 18:26, 20:26, 21:26, 22:26, 24:26, 26:26}
#
# Leave as {} for uniform shelf counts across all ladders.
SPECIAL_SHELVES = {}

# Optional: add a suffix to the output filename.
# Use this when running a range side in multiple parts (e.g., 8L).
#   Run 1 → FILE_SUFFIX = "_part1"  →  labels_8L_part1.zpl
#   Run 2 → FILE_SUFFIX = "_part2"  →  labels_8L_part2.zpl
# Leave as "" for standard naming (e.g., labels_5L.zpl).
FILE_SUFFIX = ""

# Label dimensions @ 203 dpi
LABEL_WIDTH_DOTS  = 402     # 2 inches
LABEL_HEIGHT_DOTS = 203     # 1 inch

# Output filename (auto-named by range side and optional suffix)
OUTPUT_FILE = f"labels_{RANGE_SIDE}{FILE_SUFFIX}.zpl"

# Optional: send directly to a networked Zebra printer
PRINT_DIRECTLY = False
PRINTER_IP     = "192.168.1.100"
PRINTER_PORT   = 9100


# ─────────────────────────────────────────────
# BATCH CONFIGURATION
# All range sides pre-loaded for --batch mode.
# Each entry: (RANGE_SIDE, NUM_LADDERS, NUM_SHELVES, LADDER_START, SPECIAL_SHELVES, FILE_SUFFIX)
# ─────────────────────────────────────────────

BATCH_JOBS = [
    # Range Side  Ladders  Shelves  Start  Special Shelves                                                                                              Suffix
    ("2R",  7,  17, 1, {}, ""),
    ("3L",  58, 18, 1, {}, ""),
    ("3R",  58, 16, 1, {}, ""),
    ("4L",  58, 16, 1, {}, ""),
    ("4R",  58, 16, 1, {}, ""),
    ("5L",  58, 16, 1, {}, ""),
    ("5R",  54, 14, 1, {2:26, 4:26, 6:26, 8:26, 10:26, 12:26, 14:26, 16:26, 18:26, 20:26, 21:26, 22:26, 24:26, 26:26}, ""),
    ("6L",  54, 14, 1, {1:25, 3:25, 5:25, 7:25, 9:25, 11:25, 13:25, 15:25, 17:25, 19:25, 21:25, 23:25, 25:25, 27:25}, ""),
    ("6R",  54, 14, 1, {2:25, 6:25, 8:25, 10:25, 12:25, 14:25, 16:25, 18:25, 20:25, 22:25, 25:25, 27:25}, ""),
    ("7L",  54, 14, 1, {5:25, 7:25, 9:25, 11:25, 13:25, 15:25, 17:25, 19:25}, ""),
    ("7R",  54, 16, 1, {1:25, 3:25, 5:25, 7:25, 9:25, 11:25, 13:25}, ""),
    ("8L",  6,  16, 1,  {}, "_part1"),
    ("8L",  5,  16, 50, {}, "_part2"),
]


# ─────────────────────────────────────────────
# LABEL LAYOUT CONSTANTS (dots)
# ─────────────────────────────────────────────
#
# Three columns across the 2" label:
#   Col 1 — Range  (left)
#   Col 2 — Ladder (center)
#   Col 3 — Shelf  (right)
#
# Vertical centering math (entire block centered as a unit):
#   FONT_SMALL  = 24 dots tall
#   GAP         = 13 dots (space between descriptor and number)
#   FONT_LARGE  = 112 dots tall
#   Total block = 24 + 13 + 112 = 149 dots
#   ROW_LABEL_Y = 42  (top of descriptor)
#   ROW_VALUE_Y = 79  (top of large number)
#   Bottom of number = 79 + 112 = 191 dots → bottom margin = 12 dots

# X positions for descriptor labels (RANGE, LADDER, SHELF)
COL_RANGE_LABEL_X  = 32
COL_LADDER_LABEL_X = 165
COL_SHELF_LABEL_X  = 304

# X positions for large numbers
COL_RANGE_VALUE_X  = 12
COL_LADDER_VALUE_X = 148
COL_SHELF_VALUE_X  = 281

ROW_LABEL_Y  = 42       # Y position for small descriptor text
ROW_VALUE_Y  = 79       # Y position for large number

FONT_SMALL   = 24       # Descriptor label height (dots)
FONT_LARGE   = 112      # Value number height (dots)

# Thin vertical dividers between columns
DIVIDER_1_X  = 135      # Between Range and Ladder
DIVIDER_2_X  = 271      # Between Ladder and Shelf


# ─────────────────────────────────────────────
# ZPL LABEL BUILDER
# ─────────────────────────────────────────────

def build_label(range_side: str, ladder: int, shelf: int) -> str:
    """
    Builds one ZPL label block for the given location.
    Entire block (descriptor + gap + large number) is vertically
    centered on the label as a unit.

    Padding logic:
      - Ladder: zero-padded to 2 digits (01–58)
      - Shelf:  zero-padded to 2 digits (01–26)
      - Range:  printed as-is (e.g., "5L")
    """
    ladder_str = f"{ladder:02d}"
    shelf_str  = f"{shelf:02d}"

    zpl = f"""^XA
^PW{LABEL_WIDTH_DOTS}
^LL{LABEL_HEIGHT_DOTS}
^LH0,0
^CI28
^FO{COL_RANGE_LABEL_X},{ROW_LABEL_Y}^A0N,{FONT_SMALL},{FONT_SMALL}^FDRANGE^FS
^FO{COL_RANGE_VALUE_X},{ROW_VALUE_Y}^A0N,{FONT_LARGE},{FONT_LARGE}^FD{range_side}^FS
^FO{DIVIDER_1_X},0^GB1,{LABEL_HEIGHT_DOTS},1^FS
^FO{COL_LADDER_LABEL_X},{ROW_LABEL_Y}^A0N,{FONT_SMALL},{FONT_SMALL}^FDLADDER^FS
^FO{COL_LADDER_VALUE_X},{ROW_VALUE_Y}^A0N,{FONT_LARGE},{FONT_LARGE}^FD{ladder_str}^FS
^FO{DIVIDER_2_X},0^GB1,{LABEL_HEIGHT_DOTS},1^FS
^FO{COL_SHELF_LABEL_X},{ROW_LABEL_Y}^A0N,{FONT_SMALL},{FONT_SMALL}^FDSHELF^FS
^FO{COL_SHELF_VALUE_X},{ROW_VALUE_Y}^A0N,{FONT_LARGE},{FONT_LARGE}^FD{shelf_str}^FS
^XZ
"""
    return zpl


# ─────────────────────────────────────────────
# GENERATE ALL LABELS FOR A RANGE SIDE
# ─────────────────────────────────────────────

def generate_labels(range_side=None, num_ladders=None, num_shelves=None,
                    ladder_start=None, shelf_start=None, special_shelves=None) -> str:
    """
    Generates all labels for the configured range side.
    Iterates: Ladder (outer) → Shelf (inner)
    Accepts overrides for batch mode.
    """
    rs  = range_side     or RANGE_SIDE
    nl  = num_ladders    or NUM_LADDERS
    ns  = num_shelves    or NUM_SHELVES
    ls  = ladder_start   or LADDER_START
    ss  = shelf_start    or SHELF_START
    sp  = special_shelves if special_shelves is not None else SPECIAL_SHELVES

    all_zpl = ""
    total   = 0

    for ladder in range(ls, ls + nl):
        shelf_count = sp.get(ladder, ns)
        for shelf in range(ss, ss + shelf_count):
            all_zpl += build_label(rs, ladder, shelf)
            total += 1

    last_ladder = ls + nl - 1
    print(f"  Range Side : {rs}")
    print(f"  Ladders    : {ls} – {last_ladder}")
    if sp:
        print(f"  Shelves    : {ns} standard, {len(sp)} ladder(s) with special counts")
    else:
        print(f"  Shelves    : {ss} – {ss + ns - 1}")
    print(f"  Total labels: {total}")
    return all_zpl


# ─────────────────────────────────────────────
# BATCH MODE
# Generates all range side ZPL files at once.
# Run with: python zebra_sequential_labels.py --batch
# ─────────────────────────────────────────────

def run_batch():
    """
    Iterates through all BATCH_JOBS and generates a ZPL file for each.
    """
    print("=" * 50)
    print("  BATCH MODE — Generating all range side ZPL files")
    print("=" * 50)

    total_labels = 0
    files_written = []

    for job in BATCH_JOBS:
        rs, nl, ns, ls, sp, suffix = job
        output_file = f"labels_{rs}{suffix}.zpl"

        print(f"\nGenerating {output_file}...")
        all_zpl = generate_labels(
            range_side=rs,
            num_ladders=nl,
            num_shelves=ns,
            ladder_start=ls,
            special_shelves=sp
        )

        with open(output_file, "w") as f:
            f.write(all_zpl)

        label_count = all_zpl.count("^XA")
        total_labels += label_count
        files_written.append((output_file, label_count))
        print(f"  ✔ Saved → {output_file}")

    print("\n" + "=" * 50)
    print("  BATCH COMPLETE")
    print("=" * 50)
    for fname, count in files_written:
        print(f"  {fname:<30} {count:>5} labels")
    print(f"\n  Total labels across all files: {total_labels}")
    print("=" * 50)


# ─────────────────────────────────────────────
# PREVIEW MODE
# Prints key labels to the console to verify
# sequence logic without opening the .zpl file.
# Run with: python zebra_sequential_labels.py --preview
# ─────────────────────────────────────────────

def preview_labels():
    """
    Prints a spot-check of key labels to the console:
      - First label
      - Last label of Ladder 1 (shelf rollover check)
      - First label of Ladder 2 (ladder increment check)
      - Last label of the entire job
      - If SPECIAL_SHELVES is set: first and last shelf of
        the first special ladder, to verify flat file counts
    """
    last_ladder      = LADDER_START + NUM_LADDERS - 1
    first_shelf_max  = SHELF_START + SPECIAL_SHELVES.get(LADDER_START, NUM_SHELVES) - 1
    last_shelf_max   = SHELF_START + SPECIAL_SHELVES.get(last_ladder, NUM_SHELVES) - 1

    total = sum(
        SPECIAL_SHELVES.get(l, NUM_SHELVES)
        for l in range(LADDER_START, LADDER_START + NUM_LADDERS)
    )

    checks = [
        ("First label",                          LADDER_START,     SHELF_START),
        (f"Last shelf on Ladder {LADDER_START:02d}",   LADDER_START,     first_shelf_max),
        (f"First shelf on Ladder {LADDER_START+1:02d}", LADDER_START + 1, SHELF_START),
        ("Last label",                           last_ladder,      last_shelf_max),
    ]

    # Insert special ladder spot-checks if applicable
    if SPECIAL_SHELVES:
        first_special     = min(SPECIAL_SHELVES.keys())
        special_shelf_max = SHELF_START + SPECIAL_SHELVES[first_special] - 1
        checks.insert(3, (f"First shelf on special Ladder {first_special:02d}", first_special, SHELF_START))
        checks.insert(4, (f"Last shelf on special Ladder {first_special:02d}",  first_special, special_shelf_max))

    print("=" * 50)
    print(f"  PREVIEW — Range Side: {RANGE_SIDE}")
    print(f"  Ladders: {LADDER_START}–{last_ladder}  |  Shelves: {SHELF_START}–{SHELF_START + NUM_SHELVES - 1}")
    if SPECIAL_SHELVES:
        print(f"  Special ladders: {len(SPECIAL_SHELVES)} ladder(s) with higher shelf counts")
    print(f"  Total labels: {total}")
    print("=" * 50)

    for label, ladder, shelf in checks:
        print(f"\n  ✔ {label}")
        print(f"    ┌─────────────────────────────┐")
        print(f"    │ RNG: {RANGE_SIDE:<5}  LDR: {ladder:02d}  SHF: {shelf:02d} │")
        print(f"    └─────────────────────────────┘")

    print("\n" + "=" * 50)
    print(f"  Sequence logic looks correct if:")
    print(f"  • First label  → {RANGE_SIDE} / {LADDER_START:02d} / {SHELF_START:02d}")
    print(f"  • Shelf resets → {RANGE_SIDE} / {LADDER_START:02d} / {first_shelf_max:02d} then {RANGE_SIDE} / {LADDER_START+1:02d} / {SHELF_START:02d}")
    print(f"  • Last label   → {RANGE_SIDE} / {last_ladder:02d} / {last_shelf_max:02d}")
    print("=" * 50)


# ─────────────────────────────────────────────
# PNG PREVIEW MODE
# Fetches rendered label PNGs from Labelary API.
# Run with: python zebra_sequential_labels.py --png
# ─────────────────────────────────────────────

def fetch_png(zpl: str, filename: str):
    """Sends a single ZPL label to the Labelary API and saves it as a PNG."""
    clean_zpl = "\n".join(line for line in zpl.strip().splitlines() if line.strip())
    url = "http://api.labelary.com/v1/printers/8dpmm/labels/2x1/0/"
    data = clean_zpl.encode("utf-8")
    req  = urllib.request.Request(url, data=data, headers={"Accept": "image/png"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filename, "wb") as f:
                f.write(response.read())
        print(f"  Saved → {filename}")
    except urllib.error.HTTPError as e:
        print(f"  ✘ Could not reach Labelary API: {e.reason}")
        print(f"    (Check your internet connection and try again)")
    except Exception as e:
        print(f"  ✘ Unexpected error: {e}")


def preview_png():
    """
    Fetches 4 spot-check label PNGs from the Labelary API:
      - First label
      - Last shelf on first ladder (rollover check)
      - First shelf on second ladder (increment check)
      - Last label
    """
    last_ladder     = LADDER_START + NUM_LADDERS - 1
    first_shelf_max = SHELF_START + SPECIAL_SHELVES.get(LADDER_START, NUM_SHELVES) - 1
    last_shelf_max  = SHELF_START + SPECIAL_SHELVES.get(last_ladder,  NUM_SHELVES) - 1

    previews = [
        (f"preview_{RANGE_SIDE}_first_label.png",    LADDER_START,     SHELF_START),
        (f"preview_{RANGE_SIDE}_shelf_rollover.png",  LADDER_START,     first_shelf_max),
        (f"preview_{RANGE_SIDE}_ladder_increment.png",LADDER_START + 1, SHELF_START),
        (f"preview_{RANGE_SIDE}_last_label.png",      last_ladder,      last_shelf_max),
    ]

    print("=" * 50)
    print(f"  LABELARY PNG PREVIEW — Range Side: {RANGE_SIDE}")
    print(f"  Fetching {len(previews)} spot-check labels from Labelary API...")
    print("=" * 50)

    for filename, ladder, shelf in previews:
        print(f"\n  Rendering {RANGE_SIDE} / {ladder:02d} / {shelf:02d} → {filename}")
        zpl = build_label(RANGE_SIDE, ladder, shelf)
        fetch_png(zpl, filename)
        time.sleep(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n{'=' * 50}")
    print(f"  Done! Open the PNG files in your current folder")
    print(f"  ({script_dir})")
    print("=" * 50)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--batch" in args:
        run_batch()

    elif "--preview" in args:
        preview_labels()

    elif "--png" in args:
        preview_png()

    else:
        # Standard single-job run
        OUTPUT_FILE = f"labels_{RANGE_SIDE}{FILE_SUFFIX}.zpl"
        print("=" * 50)
        print(f"  Generating labels for Range Side: {RANGE_SIDE}")
        print("=" * 50)
        all_zpl = generate_labels()
        with open(OUTPUT_FILE, "w") as f:
            f.write(all_zpl)
        print(f"\n  ✔ Saved → {OUTPUT_FILE}")

        if PRINT_DIRECTLY:
            print(f"\n  Sending to printer at {PRINTER_IP}:{PRINTER_PORT}...")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((PRINTER_IP, PRINTER_PORT))
                    s.sendall(all_zpl.encode("utf-8"))
                print("  ✔ Sent to printer successfully!")
            except Exception as e:
                print(f"  ✘ Could not connect to printer: {e}")
