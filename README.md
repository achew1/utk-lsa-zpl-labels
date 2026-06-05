# 📚 Library Shelf Label Generator
### Zebra ZPL Label Generator for High-Density Library Storage

---

## Overview

This tool generates ZPL (Zebra Programming Language) label files for a high-density library storage facility with the following structure:

- **9 Ranges**, each with a **Left (L) and Right (R) side** = 18 range sides total
- Each range side has a configurable number of **Ladders**
- Each ladder has a configurable number of **Shelves**
- Some ladders contain **flat file drawers** and have a higher shelf count than the standard for that range side

Labels are printed on **1" H × 2" W** stock at **203 dpi** and are designed for easy wayfinding — large bold numbers for Range, Ladder, and Shelf, with small descriptor text centered above each. The entire block is vertically centered on the label.

```
┌────────────┬────────────┬────────────┐
│   RANGE    │   LADDER   │   SHELF    │  ← small descriptor (24pt), centered above number
│    5L      │    04      │    07      │  ← large bold value  (112pt)
└────────────┴────────────┴────────────┘
```

Vertical centering is calculated as a unit — the entire block (descriptor + gap + number) is centered together:
- Descriptor height = 24 dots
- Gap between descriptor and number = 13 dots
- Number height = 112 dots
- Total block height = 24 + 13 + 112 = **149 dots**
- Top margin = (203 − 149) / 2 = **~27 dots**
- Descriptor starts at Y = **42 dots**
- Large number starts at Y = **79 dots**
- Bottom of number = 79 + 112 = **191 dots** → bottom margin = **12 dots**

Each column is divided by thin vertical lines, with descriptor text and numbers independently positioned per column for precise visual centering.

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
├── labels_{RANGE_SIDE}_{SUFFIX}.zpl      # e.g., labels_8L_part1.zpl (for partial runs)
├── preview_{RANGE_SIDE}_first_label.png
├── preview_{RANGE_SIDE}_last_label.png
└── ...
```

> 💡 The `{RANGE_SIDE}` portion of each filename updates automatically based on whatever `RANGE_SIDE` is set to in the script — you don't need to rename anything manually.

> 💡 Generated `.zpl` and `.png` files are not committed to the repo because they are run locally on a separate machine. They can be regenerated at any time by running the script. A `.gitignore` is not needed for this reason.

---

## ⚙️ Configuration — What to Change Per Job

All job-specific settings are at the **top of the script** under the `CONFIGURATION` section. For most range sides you only need to edit **four values**:

```python
# ─────────────────────────────────────────────
# CONFIGURATION — Edit this section per job
# ─────────────────────────────────────────────

RANGE_SIDE   = "5L"     # ← Change this: "2R", "3L", "3R" ... "7R", "8L"
NUM_LADDERS  = 58       # ← Change this: number of ladders on this side
NUM_SHELVES  = 16       # ← Change this: default shelves per ladder
LADDER_START = 1        # ← Usually stays at 1 (unless reprinting a partial run)
```

> 💡 The values shown above (`5L`, `58`, `16`) are the settings for **Range 5L** and are included as a working example. Every time you start a new range side job, update all relevant values to match that range side's actual numbers.

For range sides with **flat file drawers** (some ladders have more shelves than others), also set `SPECIAL_SHELVES`:

```python
SPECIAL_SHELVES = {2:26, 4:26, 6:26}   # ← Ladder numbers that have a different shelf count
```

For range sides that require **multiple runs** (e.g., 8L), also set `FILE_SUFFIX`:

```python
FILE_SUFFIX = "_part1"   # ← Appended to the output filename: labels_8L_part1.zpl
```

---

### About `SPECIAL_SHELVES`

`SPECIAL_SHELVES` allows specific ladders to have a different shelf count than the default `NUM_SHELVES`. This is used for ladders that contain flat file drawers, which typically add extra shelves above the standard count.

```python
# Example for Row 5R:
# Most ladders have 14 shelves, but ladders with flat files have 26
SPECIAL_SHELVES = {
    2:26, 4:26, 6:26, 8:26, 10:26, 12:26, 14:26,
    16:26, 18:26, 20:26, 21:26, 22:26, 24:26, 26:26
}
```

Any ladder number **not listed** in `SPECIAL_SHELVES` will automatically use `NUM_SHELVES`. Leave it as `{}` for range sides with a uniform shelf count.

---

### About `LADDER_START`

`LADDER_START` controls which ladder number the script begins counting from. In most cases this stays at `1`. However, if a print job is interrupted partway through (e.g., a label jam at Ladder 23), you can reprint just the remaining labels without reprinting the entire range side:

1. Set `LADDER_START = 23` (or wherever the jam occurred)
2. Run the script — it will generate labels from Ladder 23 to the end only
3. Reset `LADDER_START = 1` when done so it's ready for the next job

> ⚠️ Double-check which ladder was the last successfully printed before setting `LADDER_START` for a partial reprint.

---

### About `FILE_SUFFIX`

`FILE_SUFFIX` appends a custom string to the output filename. This is needed when a range side must be generated in multiple runs (e.g., **8L**, which has ladders 1–6 and 50–54 but nothing in between due to skeletonized structure).

**8L Run 1:**
```python
RANGE_SIDE   = "8L"
NUM_LADDERS  = 6
LADDER_START = 1
NUM_SHELVES  = 16
FILE_SUFFIX  = "_part1"    # → labels_8L_part1.zpl
```

**8L Run 2:**
```python
RANGE_SIDE   = "8L"
NUM_LADDERS  = 5
LADDER_START = 50
NUM_SHELVES  = 16
FILE_SUFFIX  = "_part2"    # → labels_8L_part2.zpl
```

Send both files to the printer separately. Reset `FILE_SUFFIX = ""` when done.

---

### Range Side Configuration Reference

Use the table below when configuring each job. `SPECIAL_SHELVES` values are listed in shorthand — refer to the full dictionary format shown above.

> 💡 Range sides marked **"Future growth — no shelving"** do not currently have shelving installed. Labels will be generated when shelving is added in future years.

| Range Side | `NUM_LADDERS` | `NUM_SHELVES` | `SPECIAL_SHELVES` | Est. Labels | Status |
|------------|---------------|---------------|-------------------|-------------|--------|
| 1L         | —             | —             | —                 | —           | 🔲 Future growth — no shelving |
| 1R         | —             | —             | —                 | —           | 🔲 Future growth — no shelving |
| 2L         | —             | —             | —                 | —           | 🔲 Future growth — no shelving |
| 2R         | 7             | 17            | `{}`              | 119         | ⬜ Not yet printed |
| 3L         | 58            | 18            | `{}`              | 1,044       | ⬜ Not yet printed |
| 3R         | 58            | 16            | `{}`              | 928         | ⬜ Not yet printed |
| 4L         | 58            | 16            | `{}`              | 928         | ⬜ Not yet printed |
| 4R         | 58            | 16            | `{}`              | 928         | ⬜ Not yet printed |
| 5L         | 58            | 16            | `{}`              | 928         | ⬜ Not yet printed |
| 5R         | 54            | 14            | `{2,4,6,8,10,12,14,16,18,20,21,22,24,26: 26}` | 924 | ⬜ Not yet printed |
| 6L         | 54            | 14            | `{1,3,5,7,9,11,13,15,17,19,21,23,25,27: 25}` | 910 | ⬜ Not yet printed |
| 6R         | 54            | 14            | `{2,6,8,10,12,14,16,18,20,22,25,27: 25}` | 888 | ⬜ Not yet printed |
| 7L         | 54            | 14            | `{5,7,9,11,13,15,17,19: 25}` | 844 | ⬜ Not yet printed |
| 7R         | 54            | 16            | `{1,3,5,7,9,11,13: 25}` | 927 | ⬜ Not yet printed |
| 8L         | 11 (1–6, 50–54) | 16          | `{}`              | 176         | ⬜ Not yet printed (2 part runs) |
| 8R         | —             | —             | —                 | —           | 🔲 Future growth — no shelving |
| 9L         | —             | —             | —                 | —           | 🔲 Future growth — no shelving |
| 9R         | —             | —             | —                 | —           | 🔲 Future growth — no shelving |

After completing each print job, update the status column:
- ⬜ Not yet printed
- 🟡 ZPL generated, not yet printed
- ✅ Printed and applied
- 🔲 Future growth — no shelving

Suggested Git commit after each job:
```bash
git add README.md
git commit -m "Mark [RANGE_SIDE] as printed"
```

---

## 🖥️ Usage

### Step 1 — Open a Terminal in Your Labels Folder
1. Open **File Explorer** and navigate to your `Caia Labels` folder
2. Click the **address bar** at the top
3. Type `cmd` and hit Enter

### Step 2 — Run the Script

#### Option 1 — Preview Mode (spot-check sequence logic, no files created)
```
python zebra_sequential_labels.py --preview
```
Prints first, rollover, and last labels to the console. Verify:
- First label → `{RANGE_SIDE} / 01 / 01`
- Shelf resets and ladder increments correctly at rollover
- Last label → `{RANGE_SIDE} / {last ladder} / {last shelf}`
- Total label count = `NUM_LADDERS × NUM_SHELVES` (adjusted for any `SPECIAL_SHELVES`)

**Example — if configured for 3R (58 ladders, 16 shelves):**
```
First label  → 3R / 01 / 01
Shelf resets → 3R / 01 / 16 then 3R / 02 / 01
Last label   → 3R / 58 / 16
Total labels : 928
```

#### Option 2 — PNG Preview (visual spot-check via Labelary API)
```
python zebra_sequential_labels.py --png
```
Fetches 4 rendered PNG images from the Labelary API and saves them in your folder. Open them like any photo to visually confirm the label layout. PNG filenames include the current `{RANGE_SIDE}` — e.g., `preview_3R_first_label.png`.

#### Option 3 — Generate ZPL File (ready to print)
```
python zebra_sequential_labels.py
```
Generates the full ZPL file for the configured range side (e.g., `labels_5L.zpl`). You'll see a confirmation in the terminal:
```
Range Side : 5L
Ladders    : 1 – 58
Shelves    : 1 – 16
Total labels generated: 928
```
The `.zpl` file will appear in your `Caia Labels` folder.

#### Option 4 — Batch Mode (generate ALL range side ZPL files at once)
```
python zebra_sequential_labels.py --batch
```
Generates ZPL files for every configured range side in one run. All files appear in your `Caia Labels` folder. Output will look like:
```
Generating labels_2R.zpl...
  Range Side : 2R
  Ladders    : 1 – 7
  Shelves    : 1 – 17
  Total labels: 119

Generating labels_3L.zpl...
  ...

Batch complete! 13 files generated.
```

> 💡 Batch configurations are stored in the `BATCH_JOBS` list near the top of the script. Update that list when new range sides are added.

---

## 🧪 Testing Before a Full Print Run

**Always test on a new printer or new label stock before committing to a full run.**

### Test File
The file `test_labels_TL_3x3.zpl` contains **9 labels** (3 ladders × 3 shelves) using the range name `TL` (Test Left). `TL` is two characters — the same as any real range side (`5L`, `3R`, etc.) — so the font size and layout are identical to production labels.

Use this file to verify:
- ✅ Printer network connection and IP are working
- ✅ Print quality and darkness are acceptable
- ✅ Label calibration is correct (no misaligned cuts)
- ✅ 1" × 2" label stock is the correct size
- ✅ Font is large and readable in real life
- ✅ Three-column layout is clear and well-spaced
- ✅ Adhesive works on your shelving material
- ✅ Ladder rollover sequence is correct (`TL/01/03` → `TL/02/01`)

> 💡 Run the test file whenever setting up on a new printer or using a new batch of label stock.

---

## 🔍 Testing Labels Online

Before printing, preview labels visually using one of these free tools:

### Option A — ZPL Printer Online (recommended for full file upload)
**[zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net)**

1. Run `python zebra_sequential_labels.py` to generate the `.zpl` file
2. Open the website
3. Click **Upload** and select your `.zpl` file
4. Scroll through the rendered labels and verify:
   - First label shows correct Range, Ladder 01, Shelf 01
   - Ladder rollover is correct
   - Last label shows correct final ladder and shelf numbers
   - Layout, font size, and spacing look correct

### Option B — Labelary Viewer (recommended for quick single-label paste)
**[labelary.com/viewer.html](http://labelary.com/viewer.html)**

1. Paste a single `^XA...^XZ` label block into the text box
2. Set width to `2.00 in`, height to `1.00 in`, DPI to `203`
3. Click Refresh

> 💡 Labelary is the more accurate renderer of the two for verifying precise font positioning.

---

## 🖨️ Printing the Labels

### Printer Setup Checklist
Before starting any print job:
- [ ] Load **1" × 2" label stock** (labels oriented horizontally)
- [ ] **Calibrate** the printer — hold the Feed button ~2 seconds until it advances and stops; this ensures it detects the label gap correctly
- [ ] Confirm the **status light is solid green**
- [ ] Run the **test file** (`test_labels_TL_3x3.zpl`) to verify print quality before a full run

---

### Finding the Printer's IP Address

Both printing options below require the printer's IP address. To find it:

1. Make sure the printer is **powered on** and connected to the network
2. Hold the **Feed button** for approximately **5 seconds** until the printer prints a configuration label automatically
3. Look for the **IP Address** field on the printed label (e.g., `192.168.1.100`)

> ⚠️ If the IP shows as `0.0.0.0`, the printer has not been assigned a network address yet. Contact your IT department to ensure it is connected to the network and has been assigned an IP.

Once you have the IP address, **update the script** so you don't have to look it up again:
```python
PRINT_DIRECTLY = True
PRINTER_IP     = "192.168.X.XXX"   # ← Enter your printer's actual IP here
```
Then commit this change to Git:
```bash
git add zebra_sequential_labels.py
git commit -m "Add confirmed printer IP address"
```

---

### Option A — Direct Network Print (Recommended)
Set `PRINT_DIRECTLY = True` and `PRINTER_IP` in the script, then run:
```
python zebra_sequential_labels.py
```
The script generates the ZPL and sends it directly to the printer in one step.

---

### Option B — Manual Send via Command Line
If you already have a generated `.zpl` file and want to send it without running the script, use the Windows `copy` command:

```
copy labels_5L.zpl \\192.168.X.XXX\ZPL
```

Replace `192.168.X.XXX` with your printer's actual IP address and `labels_5L.zpl` with the file you want to send. The printer will start printing immediately.

This method works without Python and is a useful backup if the script ever has issues.

**To send the test file:**
```
copy test_labels_TL_3x3.zpl \\192.168.X.XXX\ZPL
```

---

## 📦 After Printing

After completing a print job:

1. **Update the status table** in this README — change the range side from ⬜ to ✅
2. **Archive or delete** the generated `.zpl` file — it can be regenerated at any time by running the script
3. **Commit the README update** to Git:
```bash
git add README.md
git commit -m "Mark 5L as printed and applied"
```

---

## 🔧 Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `python` not recognized in terminal | Python not installed or not in PATH | Reinstall Python, check "Add to PATH" option |
| Script runs but no file appears | Check the terminal for error messages | Look for typos in configuration values |
| Labelary API errors (`--png`) | Rate limiting or connectivity | Wait a few seconds and try again |
| Printer not responding | Wrong IP or not connected | Reprint config label to confirm IP |
| Labels printing misaligned | Printer needs calibration | Hold Feed button ~2 seconds to recalibrate |
| Labels cutting in wrong place | Wrong label size loaded | Confirm 1" × 2" stock is installed |
