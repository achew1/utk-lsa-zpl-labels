"""
Zebra Library Shelf Label Generator
=====================================
Designed for high-density library storage facilities.
Generates ZPL labels for a single Range Side per job.

Label size: 1" H x 2" W @ 203 dpi = 203 (H) x 406 (W) dots

Label layout:
  ┌──────────────────────────────────────┐
  │  RNG   5L  │  LDR  04  │  SHF  07   │
  │  (small)   │  (small)  │  (small)   │
  │    5L      │    04     │    07      │
  │  (large)   │  (large)  │  (large)   │
  └──────────────────────────────────────┘
  Large bold numbers dominate for easy wayfinding.
  Small text labels sit above each number.
  The entire block (descriptor + gap + number) is
  vertically centered on the label as a unit.

Usage:
  Normal run:   python zebra_sequential_labels.py
  Preview mode: python zebra_sequential_labels.py --preview
  Labelary PNG: python zebra_sequential_labels.py --png
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
NUM_LADDERS  = 58       # Range 5L has 58 ladders
NUM_SHELVES  = 15       # Range 5L has 15 shelves per ladder

LADDER_START = 1        # Starting ladder number (usually 1)
SHELF_START  = 1        # Starting shelf number (usually 1)

# Label dimensions @ 203 dpi
LABEL_WIDTH_DOTS  = 406     # 2 inches
LABEL_HEIGHT_DOTS = 203     # 1 inch

# Output filename (auto-named by range side)
OUTPUT_FILE = f"labels_{RANGE_SIDE}.zpl"

# Optional: send directly to a networked Zebra printer
PRINT_DIRECTLY = False
PRINTER_IP     = "192.168.1.100"
PRINTER_PORT   = 9100


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
#   FONT_SMALL  = 18 dots tall
#   GAP         = 12 dots (space between descriptor and number)
#   FONT_LARGE  = 112 dots tall
#   Total block = 18 + 12 + 112 = 142 dots
#   ROW_LABEL_Y = (203 - 142) / 2 = 30.5 ≈ 31  (top of block)
#   ROW_VALUE_Y = 31 + 18 + 12 = 61             (large number)

COL_RANGE_X  = 10       # Left edge of Range column
COL_LADDER_X = 148      # Left edge of Ladder column
COL_SHELF_X  = 286      # Left edge of Shelf column

ROW_LABEL_Y  = 31       # Y position for small descriptor text
ROW_VALUE_Y  = 61       # Y position for large number (block vertically centered)

FONT_SMALL   = 18       # Descriptor label height (dots)
FONT_LARGE   = 112      # Value number height (dots)

# Thin vertical dividers between columns
DIVIDER_1_X  = 140      # Between Range and Ladder
DIVIDER_2_X  = 278      # Between Ladder and Shelf


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
      - Shelf:  zero-padded to 2 digits (01–15)
      - Range:  printed as-is (e.g., "5L")
    """
    ladder_str = f"{ladder:02d}"    # Zero-padded: 01 … 58
    shelf_str  = f"{shelf:02d}"     # Zero-padded: 01 … 15

    zpl = f"""^XA
^PW{LABEL_WIDTH_DOTS}
^LL{LABEL_HEIGHT_DOTS}
^LH0,0
^CI28
^FO{COL_RANGE_X},{ROW_LABEL_Y}^A0N,{FONT_SMALL},{FONT_SMALL}^FDRNG^FS
^FO{COL_RANGE_X},{ROW_VALUE_Y}^A0N,{FONT_LARGE},{FONT_LARGE}^FD{range_side}^FS
^FO{DIVIDER_1_X},0^GB1,{LABEL_HEIGHT_DOTS},1^FS
^FO{COL_LADDER_X},{ROW_LABEL_Y}^A0N,{FONT_SMALL},{FONT_SMALL}^FDLDR^FS
^FO{COL_LADDER_X},{ROW_VALUE_Y}^A0N,{FONT_LARGE},{FONT_LARGE}^FD{ladder_str}^FS
^FO{DIVIDER_2_X},0^GB1,{LABEL_HEIGHT_DOTS},1^FS
^FO{COL_SHELF_X},{ROW_LABEL_Y}^A0N,{FONT_SMALL},{FONT_SMALL}^FDSHF^FS
^FO{COL_SHELF_X},{ROW_VALUE_Y}^A0N,{FONT_LARGE},{FONT_LARGE}^FD{shelf_str}^FS
^XZ
"""
    return zpl


# ─────────────────────────────────────────────
# GENERATE ALL LABELS FOR THIS RANGE SIDE
# ─────────────────────────────────────────────

def generate_labels() -> str:
    """
    Generates all labels for the configured range side.
    Iterates: Ladder (outer) → Shelf (inner)
    So labels print in physical order:
      5L-01-01, 5L-01-02 ... 5L-01-15, 5L-02-01 ...
    Labels for Range 5L: 58 ladders × 15 shelves = 870 total
    """
    all_zpl = ""
    total = 0

    for ladder in range(LADDER_START, LADDER_START + NUM_LADDERS):
        for shelf in range(SHELF_START, SHELF_START + NUM_SHELVES):
            all_zpl += build_label(RANGE_SIDE, ladder, shelf)
            total += 1

    print(f"Range Side : {RANGE_SIDE}")
    print(f"Ladders    : {LADDER_START} – {LADDER_START + NUM_LADDERS - 1}")
    print(f"Shelves    : {SHELF_START} – {SHELF_START + NUM_SHELVES - 1}")
    print(f"Total labels generated: {total}")
    return all_zpl


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
    """
    last_shelf  = SHELF_START + NUM_SHELVES - 1
    last_ladder = LADDER_START + NUM_LADDERS - 1

    checks = [
        ("First label",                  LADDER_START,     SHELF_START),
        (f"Last shelf on Ladder {LADDER_START:02d}",  LADDER_START,     last_shelf),
        (f"First shelf on Ladder {LADDER_START+1:02d}", LADDER_START + 1, SHELF_START),
        ("Last label",                   last_ladder,      last_shelf),
    ]

    print("=" * 45)
    print(f"  PREVIEW — Range Side: {RANGE_SIDE}")
    print(f"  Ladders: {LADDER_START}–{last_ladder}  |  Shelves: {SHELF_START}–{last_shelf}")
    print(f"  Total labels: {NUM_LADDERS * NUM_SHELVES}")
    print("=" * 45)

    for description, ladder, shelf in checks:
        ladder_str = f"{ladder:02d}"
        shelf_str  = f"{shelf:02d}"
        print(f"\n  ✔ {description}")
        print(f"    ┌─────────────────────────────┐")
        print(f"    │ RNG: {RANGE_SIDE:<4}  LDR: {ladder_str}  SHF: {shelf_str} │")
        print(f"    └─────────────────────────────┘")

    print("\n" + "=" * 45)
    print("  Sequence logic looks correct if:")
    print(f"  • First label  → {RANGE_SIDE} / {LADDER_START:02d} / {SHELF_START:02d}")
    print(f"  • Shelf resets → {RANGE_SIDE} / {LADDER_START:02d} / {last_shelf:02d}"
          f" then {RANGE_SIDE} / {LADDER_START+1:02d} / {SHELF_START:02d}")
    print(f"  • Last label   → {RANGE_SIDE} / {last_ladder:02d} / {last_shelf:02d}")
    print("=" * 45)


# ─────────────────────────────────────────────
# LABELARY PNG MODE
# Fetches a rendered PNG preview of key labels
# from the Labelary API and saves them locally.
# Run with: python zebra_sequential_labels.py --png
# ─────────────────────────────────────────────

def fetch_labelary_png(zpl: str, filename: str):
    """
    Sends a single ZPL label to the Labelary API and saves it as a PNG.
    API endpoint: http://api.labelary.com/v1/printers/8dpmm/labels/{w}x{h}/0/
    Uses 8dpmm (= 203 dpi), dimensions in inches.
    """
    width_in  = LABEL_WIDTH_DOTS  / 203   # = 2.0
    height_in = LABEL_HEIGHT_DOTS / 203   # = 1.0

    url = f"http://api.labelary.com/v1/printers/8dpmm/labels/{width_in}x{height_in}/0/"

    try:
        zpl_clean = "\n".join(
            line for line in zpl.strip().splitlines() if line.strip()
        )
        data = zpl_clean.encode("utf-8")

        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Accept", "image/png")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        with urllib.request.urlopen(req, timeout=10) as response:
            png_data = response.read()

        with open(filename, "wb") as f:
            f.write(png_data)

        print(f"  ✔ Saved: {filename}")

    except urllib.error.HTTPError as e:
        print(f"  ✘ Could not reach Labelary API: {e.reason}")
        print(f"    (Check your internet connection and try again)")
    except urllib.error.URLError as e:
        print(f"  ✘ Could not reach Labelary API: {e.reason}")
        print(f"    (Check your internet connection and try again)")


def preview_png():
    """
    Fetches PNG previews of 4 spot-check labels from the Labelary API.
    """
    last_shelf  = SHELF_START + NUM_SHELVES - 1
    last_ladder = LADDER_START + NUM_LADDERS - 1

    checks = [
        (LADDER_START,     SHELF_START,  f"preview_{RANGE_SIDE}_first_label.png"),
        (LADDER_START,     last_shelf,   f"preview_{RANGE_SIDE}_shelf_rollover.png"),
        (LADDER_START + 1, SHELF_START,  f"preview_{RANGE_SIDE}_ladder_increment.png"),
        (last_ladder,      last_shelf,   f"preview_{RANGE_SIDE}_last_label.png"),
    ]

    print("=" * 45)
    print(f"  LABELARY PNG PREVIEW — Range Side: {RANGE_SIDE}")
    print(f"  Fetching 4 spot-check labels from Labelary API...")
    print("=" * 45)

    for ladder, shelf, filename in checks:
        ladder_str = f"{ladder:02d}"
        shelf_str  = f"{shelf:02d}"
        print(f"\n  Rendering {RANGE_SIDE} / {ladder_str} / {shelf_str} → {filename}")
        zpl = build_label(RANGE_SIDE, ladder, shelf)
        fetch_labelary_png(zpl, filename)
        time.sleep(1)   # Avoid rate limiting

    print("\n" + "=" * 45)
    print(f"  Done! Open the PNG files in your current folder")
    print(f"  ({os.getcwd()})")
    print("=" * 45)


# ─────────────────────────────────────────────
# SEND TO PRINTER
# ─────────────────────────────────────────────

def send_to_printer(zpl: str):
    """
    Sends ZPL data directly to a networked Zebra printer via TCP/IP.
    Requires PRINT_DIRECTLY = True and a valid PRINTER_IP.
    """
    print(f"\nSending to printer at {PRINTER_IP}:{PRINTER_PORT}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((PRINTER_IP, PRINTER_PORT))
            s.sendall(zpl.encode("utf-8"))
        print("✔ Print job sent successfully!")
    except Exception as e:
        print(f"✘ Failed to send to printer: {e}")
        print("  Check that the printer is on and the IP address is correct.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":

    if "--preview" in sys.argv:
        preview_labels()

    elif "--png" in sys.argv:
        preview_png()

    else:
        print(f"\nGenerating labels for Range Side: {RANGE_SIDE}")
        print("-" * 45)
        zpl = generate_labels()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(zpl)
        print(f"✔ Saved: {OUTPUT_FILE}")

        if PRINT_DIRECTLY:
            send_to_printer(zpl)
        else:
            print(f"\nTo print, either:")
            print(f"  1. Set PRINT_DIRECTLY = True and re-run, or")
            print(f"  2. Send {OUTPUT_FILE} to the printer manually")
