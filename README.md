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

> 💡 Add `labels_*.zpl` and `*.png` to your `.gitignore` to keep the repo clean (the test file is committed separately as a permanent reference).

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
   - First label shows `RANGE_SIDE / 01 / 01`
   - Shelf counts up from `01` to your configured `NUM_SHELVES`
   - Ladder increments by 1 when shelf resets
   - Last label shows `RANGE_SIDE / NUM_LADDERS / NUM_SHELVES`

### Option 2 — Labelary Viewer (Quick Single Label Check)
**[labelary.com/viewer.html](http://labelary.com/viewer.html)**

Best for quickly checking a single label's layout by pasting ZPL directly.

1. Go to [labelary.com/viewer.html](http://labelary.com/viewer.html)
2. Paste a single `^XA...^XZ` block into the text box
3. Set **Width** to `2.00 in`, **Height** to `1.00 in`, **DPI** to `203`
4. Click **Refresh**

---

## 🚀 Usage

### Step 1 — Navigate to Your Project Folder
1. Open **File Explorer** and go to your `Caia Labels` folder
2. Click the **address bar** at the top, type `cmd`, and hit **Enter**
3. A terminal window will open already pointed at that folder ✅

### Step 2 — Choose How to Run

#### Option 1 — Preview Mode (Console Spot-Check)
```
python zebra_sequential_labels.py --preview
```
Prints a text summary of 4 key labels to the console — the first label, last shelf on Ladder 01, first shelf on Ladder 02, and the last label. No files are created. Use this first to confirm sequence logic is correct.

Expected output example (will reflect your actual configured values):
```
=============================================
  PREVIEW — Range Side: 5L
  Ladders: 1–58  |  Shelves: 1–15
  Total labels: 870
=============================================
  ✔ First label
    ┌─────────────────────────────┐
    │ RNG: 5L    LDR: 01  SHF: 01 │
    └─────────────────────────────┘
  ...
```

Verify that:
- The Range Side matches what you set in the script
- The first label is `RANGE_SIDE / 01 / 01`
- Shelf counts up to `NUM_SHELVES`, then resets to `01` as Ladder increments
- The last label is `RANGE_SIDE / NUM_LADDERS / NUM_SHELVES`

#### Option 2 — PNG Preview (Visual Spot-Check via Labelary API)
```
python zebra_sequential_labels.py --png
```
Fetches 4 rendered PNG images from the Labelary API and saves them in your project folder. Open them in File Explorer like any photo to visually verify the label layout. Requires an internet connection.

The filenames update automatically based on `RANGE_SIDE` — for example, if `RANGE_SIDE = "5L"`:
- `preview_5L_first_label.png`
- `preview_5L_shelf_rollover.png`
- `preview_5L_ladder_increment.png`
- `preview_5L_last_label.png`

#### Option 3 — Generate ZPL File (Ready to Print)
```
python zebra_sequential_labels.py
```

Here's exactly what to do:

1. Open **File Explorer** and navigate to your `Caia Labels` folder
2. Click the **address bar**, type `cmd`, and hit **Enter**
3. In the terminal window, type the command above and hit **Enter**
4. You'll see output like this confirming it worked:
   ```
   Range Side : 5L
   Ladders    : 1 – 58
   Shelves    : 1 – 15
   Total labels generated: 870
   ✔ Saved: labels_5L.zpl
   ```
5. The file `labels_{RANGE_SIDE}.zpl` (e.g., `labels_5L.zpl`) will appear in your `Caia Labels` folder

The total label count should equal `NUM_LADDERS × NUM_SHELVES`. This file is what gets sent to the printer.

---

## 🖨️ Printing the Labels

### Printer Setup Checklist
Before printing, make sure:
- [ ] **Label stock is loaded** — 1" × 2" labels, loaded correctly per printer manual
- [ ] **Labels are calibrated** — hold the Feed button ~2 seconds until the printer advances and detects the label gap
- [ ] **Status light is solid green** — printer is ready
- [ ] **Run the test file first** — print `test_labels_TL_3x3.zpl` before any full job

### Finding the Printer's IP Address
Both Option A and Option B below require the printer's IP address. Here's how to find it:

1. Make sure the printer is **powered on** and connected to the network
2. Hold the **Feed button** for approximately **5 seconds** until the printer prints a configuration label automatically
3. Look for the **IP Address** line on the printed label (e.g., `192.168.1.100`)
4. If the IP shows as `0.0.0.0`, the printer has not yet been assigned a network address — contact your IT department to have it assigned a static IP

> 💡 Once confirmed, add the printer's IP to the script and commit the change to Git so you don't have to look it up again.

---

### Option A — Direct Print via Script (Recommended)
Once you have the printer's IP address:

1. Open `zebra_sequential_labels.py` in a text editor
2. Find these two lines near the top of the script:
   ```python
   PRINT_DIRECTLY = False
   PRINTER_IP     = "192.168.1.100"
   ```
3. Change them to:
   ```python
   PRINT_DIRECTLY = True
   PRINTER_IP     = "192.168.X.XXX"   # ← your printer's actual IP address
   ```
4. Save the file
5. Run the script normally:
   ```
   python zebra_sequential_labels.py
   ```
The script will generate the ZPL file **and** send it directly to the printer in one step.

---

### Option B — Manual Send via Command Line
If you've already generated a `.zpl` file and just want to send it to the printer without re-running the script, use this command in your terminal:

```
copy labels_5L.zpl \\192.168.X.XXX\ZPL
```

Replace `labels_5L.zpl` with your actual filename and `192.168.X.XXX` with your printer's IP. The printer will start printing immediately.

This also works for the test file:
```
copy test_labels_TL_3x3.zpl \\192.168.X.XXX\ZPL
```

> 💡 This method requires no Python — it's a good backup if you ever have trouble running the script.

For more detail, see: [Zebra Support — Sending ZPL Commands to a Printer](https://support.zebra.com/article/000026336)

---

### Option C — Zebra Setup Utilities
1. Download **Zebra Setup Utilities** from [zebra.com](https://www.zebra.com/us/en/support-downloads/software/printer-software/zebra-setup-utility.html)
2. Install and open the application
3. Select your printer from the list
4. Use **Open Printer Tools → Action → Send File** to select and send your `.zpl` file

---

## 📁 After Printing

### Update the Status Table
After completing each range side:
1. Open `README.md`
2. Find that range side in the **Range Side Reference Table**
3. Fill in the Ladders, Shelves, and Total Labels columns
4. Change the status from `⬜ Pending` to `✅ Complete`
5. Commit the update:
   ```
   git add README.md
   git commit -m "Mark 5L complete — 58 ladders, 15 shelves, 870 labels"
   ```

### ZPL File Management
Generated `.zpl` files (e.g., `labels_5L.zpl`) are excluded from Git by `.gitignore` — they can always be regenerated by running the script. Options after printing:
- **Delete** — safe to do since the script can regenerate any file at any time
- **Archive locally** — keep them in a separate folder outside the repo if you want a local record

> 💡 The test file `test_labels_TL_3x3.zpl` is intentionally committed to the repo and should not be deleted — it's a permanent reference for testing new printers or label stock.

---

## 🔁 Git Workflow

```bash
# Initial setup
git init
git add zebra_sequential_labels.py README.md .gitignore test_labels_TL_3x3.zpl
git commit -m "Initial commit - label generator with Range 5L configuration"

# After each range side job
git add README.md
git commit -m "Mark 3R complete — 14 ladders, 12 shelves, 168 labels"

# After any script changes
git add zebra_sequential_labels.py
git commit -m "Update font size to 112 dots for better readability"
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `python` not recognized | Make sure Python is installed and added to PATH — see [python.org](https://python.org) |
| Labels print misaligned | Recalibrate the printer — hold Feed button ~2 seconds |
| Can't connect to printer | Verify the IP address by printing a config label (hold Feed ~5 seconds) |
| Labelary API fails | Check your internet connection; try again after 30 seconds |
| Wrong label count | Double-check `NUM_LADDERS` and `NUM_SHELVES` in the script |
| Labels cut in wrong place | Check that 1" × 2" stock is loaded and printer is calibrated |
