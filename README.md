# 📚 Library Shelf Label Generator
### Zebra ZPL Label Generator for High-Density Library Storage

---

## Overview

This tool generates ZPL (Zebra Programming Language) label files for a high-density library storage facility with the following structure:

- **9 Ranges**, each with a **Left (L) and Right (R) side** = 18 range sides total
- Each range side has a configurable number of **Ladders**
- Each ladder has a configurable number of **Shelves**

Labels are printed on **1" H × 2" W** stock at **203 dpi** and are designed for easy wayfinding — large bold numbers for Range, Ladder, and Shelf, with small descriptor text above each.

```
┌────────────┬────────────┬────────────┐
│  RNG       │  LDR       │  SHF       │  ← small descriptor
│  5L        │  04        │  07        │  ← large bold value
└────────────┴────────────┴────────────┘
```

---

## Requirements

- **Python 3.x** — [Download here](https://python.org)
- Internet connection (only needed for `--png` preview mode via the Labelary API)
- A networked Zebra label printer (only needed for direct printing)

No additional Python packages are required — the script uses only the standard library.

---

## File Structure

```
caia-labels/
│
├── zebra_sequential_labels.py   # Main label generator script
└── README.md                    # This file
```

Generated output files (not committed to Git):
```
├── labels_5L.zpl                # Generated ZPL file (one per range side)
├── preview_5L_first_label.png   # PNG previews from Labelary API
├── preview_5L_last_label.png
└── ...
```

> 💡 Add `*.zpl` and `*.png` to your `.gitignore` to keep the repo clean.

---

## ⚙️ Configuration — What to Change Per Job

All job-specific settings are at the **top of the script** under the `CONFIGURATION` section. You only need to edit **four values** per range side:

```python
# ─────────────────────────────────────────────
# CONFIGURATION — Edit this section per job
# ─────────────────────────────────────────────

RANGE_SIDE   = "5L"     # ← Change this: "1L", "1R", "2L" ... "9R"
NUM_LADDERS  = 58       # ← Change this: number of ladders on this side
NUM_SHELVES  = 15       # ← Change this: number of shelves per ladder
LADDER_START = 1        # ← Usually stays at 1 (unless reprinting a partial run)
```

### Range Side Reference Table

Update this table as each range side is confirmed and printed:

| Range Side | Ladders | Shelves | Total Labels | Status |
|------------|---------|---------|--------------|--------|
| 1L         |         |         |              | ⬜ Pending |
| 1R         |         |         |              | ⬜ Pending |
| 2L         |         |         |              | ⬜ Pending |
| 2R         |         |         |              | ⬜ Pending |
| 3L         |         |         |              | ⬜ Pending |
| 3R         |         |         |              | ⬜ Pending |
| 4L         |         |         |              | ⬜ Pending |
| 4R         |         |         |              | ⬜ Pending |
| 5L         | 58      | 15      | 870          | ✅ Complete |
| 5R         |         |         |              | ⬜ Pending |
| 6L         |         |         |              | ⬜ Pending |
| 6R         |         |         |              | ⬜ Pending |
| 7L         |         |         |              | ⬜ Pending |
| 7R         |         |         |              | ⬜ Pending |
| 8L         |         |         |              | ⬜ Pending |
| 8R         |         |         |              | ⬜ Pending |
| 9L         |         |         |              | ⬜ Pending |
| 9R         |         |         |              | ⬜ Pending |

---

## 🚀 Usage

Open a terminal (`cmd`) in the project folder and run one of the following:

### 1. Preview Mode (Console Spot-Check)
```
python zebra_sequential_labels.py --preview
```
Prints a text summary of the first label, last label, and ladder rollover point to the console. **No files are created.** Use this first to verify sequence logic.

✔ What to check:
- First label matches `{RANGE_SIDE} / 01 / 01`
- Shelf resets to `01` after reaching `NUM_SHELVES`
- Ladder increments correctly on shelf rollover
- Last label matches `{RANGE_SIDE} / {NUM_LADDERS} / {NUM_SHELVES}`

---

### 2. PNG Preview Mode (Visual Check)
```
python zebra_sequential_labels.py --png
```
Fetches 4 rendered PNG label images from the [Labelary API](http://labelary.com) and saves them in the current folder. **Requires internet.** Use this to visually confirm label layout before printing.

Saves:
- `preview_{RANGE_SIDE}_first_label.png`
- `preview_{RANGE_SIDE}_shelf_rollover.png`
- `preview_{RANGE_SIDE}_ladder_increment.png`
- `preview_{RANGE_SIDE}_last_label.png`

---

### 3. Generate ZPL File (Ready to Print)
```
python zebra_sequential_labels.py
```
Generates the full ZPL file for the configured range side (e.g., `labels_5L.zpl`). Send this file to the Zebra printer.

---

## 🖨️ Sending to the Printer

**Option A — Network (Direct Print)**
Set `PRINT_DIRECTLY = True` and enter the printer's IP in the script:
```python
PRINT_DIRECTLY = True
PRINTER_IP     = "192.168.1.100"   # ← Your printer's IP address
PRINTER_PORT   = 9100
```
Then run the script normally — it will send the job automatically.

**Option B — File Transfer**
Copy the `.zpl` file to the printer via USB or Zebra Setup Utilities.

---

## 🏷️ Label Layout Details

| Property | Value |
|----------|-------|
| Label width | 2 inches (406 dots @ 203 dpi) |
| Label height | 1 inch (203 dots @ 203 dpi) |
| Font - descriptor | 18 dots (small, above each value) |
| Font - value | 80 dots (large, vertically centered) |
| Columns | Range \| Ladder \| Shelf (divided by thin lines) |
| Ladder padding | 2 digits (01–99) |
| Shelf padding | 2 digits (01–99) |

---

## 🌿 Recommended Git Workflow

### Initial Setup
```bash
git init
git add zebra_sequential_labels.py README.md
git commit -m "Initial commit - Range 5L configuration"
```

### Creating a `.gitignore`
Create a file named `.gitignore` in the project folder with:
```
*.zpl
*.png
__pycache__/
```

### Per Range Side Workflow
```bash
# 1. Edit RANGE_SIDE, NUM_LADDERS, NUM_SHELVES in the script
# 2. Preview and verify
# 3. Generate and print
# 4. Commit the configuration change
git add zebra_sequential_labels.py README.md
git commit -m "Configure and complete Range 5R - 54 ladders, 15 shelves"
```

This way, every range side's settings are saved in Git history and can be reviewed or re-run at any time.

---

## 🔁 Reprinting a Partial Run

If you need to reprint from a specific ladder (e.g., Ladder 12 onwards after a jam):

```python
LADDER_START = 12    # ← Start from ladder 12
NUM_LADDERS  = 47    # ← Remaining ladders (58 - 11 = 47)
```

This generates only the remaining labels without reprinting the ones already applied.

---

## 📞 Support / Notes

- ZPL reference: [Zebra ZPL Manual](https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf)
- Label previewer: [Labelary Online Viewer](http://labelary.com/viewer.html)
- Python download: [python.org](https://python.org)
