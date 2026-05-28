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

> 💡 Add `*.zpl` and `*.png` to your `.gitignore` to keep the repo clean (the test file is committed separately as a permanent reference).

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

Best for quickly checking a single label's layout without generating a full file.

1. Go to [labelary.com/viewer.html](http://labelary.com/viewer.html)
2. Paste a single `^XA...^XZ` ZPL block into the text box
3. Set **Width** to `2.00 in`, **Height** to `1.00 in`, **DPI** to `203`
4. Click **Refresh** to render

---

## 🚀 Usage

### Step 1 — Navigate to Your Project Folder
1. Click the **File Explorer** icon on your taskbar (the yellow folder icon)
2. Find and open your `Caia Labels` folder
3. Click the **address bar** at the top of File Explorer (where it shows the folder path)
4. Type `cmd` and hit **Enter** — a black terminal window will open already pointed at your folder ✅

### Step 2 — Choose What to Run

Type one of the following commands and hit **Enter**:

---

### Option 1 — Preview Mode (Console Spot-Check)
```
python zebra_sequential_labels.py --preview
```
Prints a text summary of the first label, last label, and ladder rollover point to the console. **No files are created.** Use this first to verify sequence logic.

✔ What to check — values should match whatever is configured in the script:
- First label shows **your configured Range Side** / **01** / **01**
- Shelf counts up correctly from **01** to your configured **NUM_SHELVES**
- Shelf resets to **01** and Ladder increments by 1 after reaching **NUM_SHELVES**
- Last label shows **your configured Range Side** / **NUM_LADDERS** / **NUM_SHELVES**

> **Example:** If `RANGE_SIDE = "3R"`, `NUM_LADDERS = 12`, `NUM_SHELVES = 8`:
> - First label → `3R / 01 / 01`
> - Shelf resets → `3R / 01 / 08` then `3R / 02 / 01`
> - Last label → `3R / 12 / 08`

---

### Option 2 — PNG Preview Mode (Visual Check via Labelary API)
```
python zebra_sequential_labels.py --png
```
Fetches 4 rendered PNG label images from the [Labelary API](http://labelary.com) and saves them in your `Caia Labels` folder. **Requires internet.** Use this to visually confirm label layout before printing.

Saves four files — the `{RANGE_SIDE}` portion of each filename reflects whatever is configured in the script:
- `preview_{RANGE_SIDE}_first_label.png`
- `preview_{RANGE_SIDE}_shelf_rollover.png`
- `preview_{RANGE_SIDE}_ladder_increment.png`
- `preview_{RANGE_SIDE}_last_label.png`

To view them, simply open your `Caia Labels` folder in File Explorer and double-click any `.png` file — they open like normal photos.

✔ What to check — all four images should show **your configured Range Side**, with Ladder and Shelf values matching the expected sequence for your job.

---

### Option 3 — Generate ZPL File (Ready to Print)
```
python zebra_sequential_labels.py
```

#### What this does, step by step:
1. The script loops through every Ladder and Shelf combination for the configured range side
2. For each combination, it builds a ZPL text block — one per label
3. All label blocks are joined together into one large block of text
4. That text is saved as a `.zpl` file (e.g., `labels_5L.zpl`) in your `Caia Labels` folder

You'll see a confirmation in the terminal when it's done — it will show your configured Range Side, Ladder range, Shelf range, and total label count. Verify that the total equals **NUM_LADDERS × NUM_SHELVES**.

The `.zpl` file will now be visible in your `Caia Labels` folder in File Explorer — you don't need to open it. Just send it to the printer using one of the methods below.

---

## 🖨️ Printing the Labels

### Before You Print — Printer Setup Checklist
- ✅ Printer is powered on and connected to the network
- ✅ **1" × 2" label stock** is loaded correctly
- ✅ Printer is calibrated — hold the **Feed** button for ~2 seconds until it advances and cuts cleanly
- ✅ Status light is **solid green** (not blinking)

> ⚠️ **Always run the test file first** (`test_labels_TL_3x3.zpl`) when using a new printer or new label stock before printing a full range side job. See **Testing Before a Full Print Run** above.

---

### Finding Your Printer's IP Address

Both printing options below require knowing the printer's IP address. Here's how to find it:

1. Make sure the printer is **powered on** and connected to the network
2. Hold the **Feed** button for **~5 seconds** until the printer prints a configuration label automatically
3. Look for the **IP Address** line on the printed label (e.g., `192.168.1.100`)

> ⚠️ If the IP address shows as `0.0.0.0`, the printer has not been assigned a network address yet. Contact your IT department to have it assigned a static IP on your network.

Once you have the IP address, write it here for reference: **Printer IP: _______________**

> 💡 Once confirmed, update `PRINTER_IP` in the script and commit the change to Git so you never have to look it up again:
> ```
> git add zebra_sequential_labels.py
> git commit -m "Set confirmed printer IP address"
> ```

---

### Option A — Direct Print via Python Script (Recommended)

This is the easiest method — the script generates the ZPL and sends it to the printer in one step.

1. Open `zebra_sequential_labels.py` in a text editor
2. Find these two lines near the top of the file:
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
5. Run the script:
   ```
   python zebra_sequential_labels.py
   ```
The script will generate the labels and send them directly to the printer automatically.

---

### Option B — Manual Send via Command Line (No Python Required)

If you have already generated a `.zpl` file and just want to send it to the printer directly, use this one-line command in your terminal:

```
copy labels_5L.zpl \\192.168.X.XXX\ZPL
```

Replace `192.168.X.XXX` with your printer's actual IP address, and `labels_5L.zpl` with the name of your generated file. The printer will start printing immediately.

> 💡 This method also works for the test file:
> ```
> copy test_labels_TL_3x3.zpl \\192.168.X.XXX\ZPL
> ```

---

## ✅ After Printing

Once a range side job is complete:

1. **Update the Range Side Reference Table** in this README — fill in Ladders, Shelves, Total Labels, and mark it ✅ Complete
2. **Archive or delete the `.zpl` file** — it can always be regenerated by running the script again. If you want to keep it for reference, move it to an `archive/` folder
3. **Commit the README update to Git:**
   ```
   git add README.md
   git commit -m "✅ Range 5L complete — 58 ladders, 15 shelves, 870 labels"
   ```

---

## 🔧 Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `python` not recognized | Python not installed or not in PATH | Reinstall Python and check "Add to PATH" |
| Labels print misaligned | Printer not calibrated | Hold Feed button ~2 seconds to recalibrate |
| Labels cut in wrong place | Wrong label size in printer settings | Confirm 1" × 2" stock is loaded |
| `copy` command fails | Wrong IP or printer offline | Double-check IP from config label; confirm network connection |
| Labelary API error | Rate limit or internet issue | Wait 30 seconds and try again |
| Wrong label count | `LADDER_START` not reset to 1 | Set `LADDER_START = 1` and regenerate |

---

## 🗂️ Git Workflow

```bash
# First time setup
git init
git add zebra_sequential_labels.py README.md .gitignore test_labels_TL_3x3.zpl
git commit -m "Initial commit - Range 5L configuration"

# After each range side job
git add README.md
git commit -m "✅ Range 3R complete — 12 ladders, 8 shelves, 96 labels"

# After any script changes
git add zebra_sequential_labels.py
git commit -m "Update config for Range 3R"
```
