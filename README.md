# 📚 Library Shelf Label Generator
### Zebra ZPL Label Generator for High-Density Library Storage

---

## Overview

This tool generates ZPL (Zebra Programming Language) label files for a high-density library storage facility with the following structure:

- **9 Ranges**, each with a **Left (L) and Right (R) side** = 18 range sides total
- Each range side has a configurable number of **Ladders**
- Each ladder has a configurable number of **Shelves**

Labels are printed on **1" H × 2" W** stock at **203 dpi** and are designed for easy wayfinding — large bold numbers for Range, Ladder, and Shelf, with small descriptor text above each. The entire block is vertically centered on the label.

```
┌────────────┬────────────┬────────────┐
│  RNG       │  LDR       │  SHF       │  ← small descriptor (18pt)
│  5L        │  04        │  07        │  ← large bold value  (112pt)
└────────────┴────────────┴────────────┘
```

Vertical centering is calculated as a unit — the entire block (descriptor + gap + number) is centered together:
- Total block height = 18 (descriptor) + 12 (gap) + 112 (number) = **142 dots**
- Top of block = (203 − 142) / 2 = **31 dots**
- Large number starts at = 31 + 18 + 12 = **61 dots**

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
├── zebra_sequential_labels.py        # Main label generator script
├── test_labels_TL_3x3.zpl            # 9-label test file (TL range, 3 ladders × 3 shelves)
└── README.md                         # This file
```

Generated output files (not committed to Git):
```
├── labels_{RANGE_SIDE}.zpl               # e.g., labels_5L.zpl, labels_3R.zpl
├── preview_{RANGE_SIDE}_first_label.png  # e.g., preview_5L_first_label.png
├── preview_{RANGE_SIDE}_last_label.png   # e.g., preview_5L_last_label.png
└── ...
```

> 💡 The `{RANGE_SIDE}` portion of each filename updates automatically based on whatever `RANGE_SIDE` is set to in the script — you don't need to rename anything manually.

> 💡 Generated `.zpl` and `.png` files are not committed to the repo because they are run locally on a separate machine. They can be regenerated at any time by running the script. A `.gitignore` is not needed for this reason.

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

> 💡 The values shown above (`5L`, `58`, `15`) are the settings for **Range 5L** and are included as a working example. Every time you start a new range side job, update all four values to match that range side's actual numbers.

> 💡 Each time you change these values for a new range side, all previews, checks, and output files will automatically reflect the new configuration — the expected label content always matches whatever is set here.

---

### About `LADDER_START`

`LADDER_START` controls which ladder number the script begins counting from. In most cases this stays at `1`. However, if a print job is interrupted partway through (e.g., a label jam at Ladder 23), you can reprint just the remaining labels without reprinting the entire range side:

1. Set `LADDER_START = 23` (or wherever the jam occurred)
2. Run the script — it will generate labels from Ladder 23 to the end only
3. Reset `LADDER_START = 1` when done so it's ready for the next job

> ⚠️ Double-check which ladder was the last successfully printed before setting `LADDER_START` for a partial reprint.

---

### Range Side Reference Table

Update this table as each range side is confirmed and printed. After completing a job, mark it ✅ Complete and fill in the ladder, shelf, and total label counts so there is a permanent record of every job.

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

## 🧪 Testing Before a Full Print Run

Before printing any range side — and especially when setting up on a **new printer or new label stock** — always run a test print first using the included test file.

### Why Test First?
A 9-label test print confirms everything is working before committing to a full run (which could be 800+ labels):

| What It Confirms | Details |
|---|---|
| ✅ Printer connection | Network/IP is working correctly |
| ✅ Print quality | Darkness, clarity, and resolution look good |
| ✅ Label calibration | Labels feed and cut at the right position |
| ✅ Label stock size | 1" × 2" stock is loaded and detected correctly |
| ✅ Adhesive | Sticks properly to your shelving material |
| ✅ Font size & layout | Large numbers are readable at a glance in real life |
| ✅ Sequence logic | Ladder rollover and zero-padding are correct |

### The Test File
The file `test_labels_TL_3x3.zpl` is included in the repo and contains **9 labels** using range side `TL` (Test Left) — a two-character value just like real range sides (`5L`, `3R`, etc.) so the font size and column spacing are identical to production labels.

Expected sequence:
```
TL / 01 / 01 → TL / 01 / 02 → TL / 01 / 03
TL / 02 / 01 → TL / 02 / 02 → TL / 02 / 03   ← ladder rollover
TL / 03 / 01 → TL / 03 / 02 → TL / 03 / 03   ← ladder rollover
```

### How to Run the Test
Send `test_labels_TL_3x3.zpl` to the printer using whichever method you prefer (see **Printing the Labels** below). Verify that:
- All 9 labels print cleanly with no smearing or misalignment
- The three columns are clear and well-spaced
- The large numbers are easy to read
- The ladder rolls over correctly from `01` to `02` to `03`

> 💡 Keep a few printed test labels on hand as a physical reference for quality comparison when switching to new label stock.

---

## 🔍 Testing Labels Online

Before sending to the printer, visually verify your labels using one of these free online tools:

### Option 1 — ZPL Printer Online (Recommended — Upload Full File)
**[zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net)**

This tool lets you upload a `.zpl` file directly and preview all labels in one go — great for checking the full sequence.

1. Generate your ZPL file first (see **Option 3** in Usage below)
2. Go to [zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net)
3. Click **Choose File** and select your `.zpl` file (e.g., `labels_5L.zpl` or `test_labels_TL_3x3.zpl`)
4. Click **Print / Preview**
5. Scroll through the rendered labels and verify:
   - Range side matches your configured `RANGE_SIDE`
   - First label shows `{RANGE_SIDE} / 01 / 01`
   - Shelf counts up to `{NUM_SHELVES}` then resets to `01`
   - Ladder increments correctly on each reset
   - Last label shows `{RANGE_SIDE} / {NUM_LADDERS} / {NUM_SHELVES}`
   - Total label count equals `NUM_LADDERS × NUM_SHELVES`

For example, if configured for Range `3R` with 10 ladders and 8 shelves:
- First label → `3R / 01 / 01`
- Shelf resets → `3R / 01 / 08` then `3R / 02 / 01`
- Last label → `3R / 10 / 08`
- Total → 80 labels

### Option 2 — Labelary Viewer (Quick Single Label Check)
**[labelary.com/viewer.html](http://labelary.com/viewer.html)**

Best for quickly checking a single label's layout by pasting ZPL directly.

1. Copy a single `^XA...^XZ` block from your ZPL file
2. Paste it into the text box
3. Set size to **2.00 in × 1.00 in** and DPI to **203**
4. Click **Refresh**

---

## 🚀 Usage

### Step 1 — Navigate to Your Script Folder
1. Open **File Explorer** and navigate to the folder containing `zebra_sequential_labels.py`
2. Click the **address bar** at the top of File Explorer
3. Type `cmd` and hit **Enter** — a terminal window opens in that folder

### Option 1 — Preview Mode (Console Spot-Check)
```
python zebra_sequential_labels.py --preview
```
Prints a text spot-check of key labels (first, rollover, last) directly in the terminal — no files created. Verify that:
- First label matches `{RANGE_SIDE} / 01 / 01`
- Shelf resets and ladder increments correctly at the rollover
- Last label matches `{RANGE_SIDE} / {NUM_LADDERS} / {NUM_SHELVES}`
- Total label count equals `NUM_LADDERS × NUM_SHELVES`

### Option 2 — PNG Preview (Visual Check via Labelary API)
```
python zebra_sequential_labels.py --png
```
Fetches 4 rendered label images from the Labelary API and saves them as PNG files in the same folder. Open them like any photo in File Explorer — they show exactly what the printed labels will look like.

| File | What it shows |
|---|---|
| `preview_{RANGE_SIDE}_first_label.png` | First label of the job |
| `preview_{RANGE_SIDE}_shelf_rollover.png` | Last shelf on Ladder 01 |
| `preview_{RANGE_SIDE}_ladder_increment.png` | First shelf on Ladder 02 |
| `preview_{RANGE_SIDE}_last_label.png` | Last label of the job |

> 💡 Requires an internet connection to reach the Labelary API.

### Option 3 — Generate ZPL File (Ready to Print)
```
python zebra_sequential_labels.py
```
This runs the script and generates a `.zpl` file (e.g., `labels_5L.zpl`) in the same folder as the script. Here's what happens under the hood:

1. The script loops through every combination of Ladder and Shelf for the configured range side
2. Each combination is built into a ZPL text block (`^XA...^XZ`)
3. All blocks are joined together and written to `labels_{RANGE_SIDE}.zpl`

When it finishes you'll see a summary in the terminal:
```
Range Side : 5L
Ladders    : 1 – 58
Shelves    : 1 – 15
Total labels generated: 870
```
The `.zpl` file will appear in the same folder as the script — send this file to the Zebra printer using one of the methods below.

---

## 🖨️ Printing the Labels

### Printer Setup Checklist
Before printing, make sure:
- [ ] 1" × 2" label stock is loaded correctly
- [ ] Printer is calibrated — hold the **Feed** button ~2 seconds until it auto-feeds and detects the label gap
- [ ] Status light is **solid green** (ready)
- [ ] Printer is connected to the network
- [ ] You have run the **test file** (`test_labels_TL_3x3.zpl`) first to confirm everything looks correct

---

### Finding the Printer's IP Address
Both printing options below require the printer's IP address. To find it:

1. Hold the **Feed** button on the printer for **~5 seconds** until it prints a configuration label automatically
2. Look for the **IP Address** line on that printed label (e.g., `192.168.1.100`)
3. If the IP shows as `0.0.0.0`, the printer hasn't been assigned a network address yet — contact IT to assign it a static IP

> 💡 Once confirmed, update `PRINTER_IP` in the script and commit the change to Git so it's saved for future jobs.

---

### Option A — Direct Network Print via Script (Recommended)
The easiest method — the script generates the ZPL and sends it to the printer in one step.

1. Open `zebra_sequential_labels.py` and find these two lines near the top:
```python
PRINT_DIRECTLY = False
PRINTER_IP     = "192.168.1.100"
```
2. Change them to:
```python
PRINT_DIRECTLY = True
PRINTER_IP     = "192.168.X.XXX"   # ← your printer's actual IP address
```
3. Save the file and run:
```
python zebra_sequential_labels.py
```
The script will generate the ZPL and send it directly to the printer over the network. Labels will start printing immediately.

---

### Option B — Manual Send via Command Line
If you prefer to send an already-generated `.zpl` file manually without running the script, use this command in your terminal:

```
copy labels_5L.zpl \\192.168.X.XXX\ZPL
```
Replace `192.168.X.XXX` with your printer's actual IP address and `labels_5L.zpl` with your actual filename. The printer will start printing immediately.

This method also works for the test file:
```
copy test_labels_TL_3x3.zpl \\192.168.X.XXX\ZPL
```

> 💡 No Python required for this method — useful as a backup if the script isn't available.

---

## 📦 After Printing

1. **Update the Range Side Reference Table** in this README — mark the range side ✅ Complete and fill in the ladder, shelf, and total label counts
2. **Commit the update to Git:**
```
git add README.md
git commit -m "Mark {RANGE_SIDE} complete - {NUM_LADDERS} ladders x {NUM_SHELVES} shelves"
git push
```
3. **Archive or delete the generated `.zpl` file** — it can be regenerated at any time by running the script, so there's no need to keep it unless you want a local backup

---

## 🛠️ Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `python` not recognized | Python not installed or not in PATH | Reinstall Python and check "Add to PATH" |
| Labels print misaligned | Printer needs calibration | Hold Feed ~2 seconds to recalibrate |
| Labels cut in wrong place | Wrong label size detected | Confirm 1" × 2" stock is loaded; recalibrate |
| `Could not reach Labelary API` | No internet / API down | Check connection; try again later |
| Printer not responding | Wrong IP or not on network | Reprint config label to confirm IP |
| `0.0.0.0` shown as IP | No network address assigned | Contact IT to assign a static IP |
