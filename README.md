# 📚 Library Shelf Label Generator
### Zebra ZPL Label Generator for High-Density Storage Facilities

**Last Updated:** June 2026

---

## Overview

This tool generates ZPL (Zebra Programming Language) label files for high-density storage facilities. It was originally built for a 9-range library storage facility, but is fully customizable to any size facility — any number of ranges, sides, ladders, or shelves.

The examples and configuration tables in this README reflect the specific facility it was built for:
- **9 Ranges**, each with a **Left (L) and Right (R) side** = 18 range sides total
- Each range side has a configurable number of **Ladders**
- Each ladder has a configurable number of **Shelves**
- Some ladders contain **flat file drawers** and have a higher shelf count than the standard for that range side

To adapt this tool to your own facility, see the **Customizing for Your Facility** section below.

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

> 💡 **Python version:** Make sure you install **Python 3** (not Python 2). When the installer asks about adding Python to PATH, say **Yes**. After installing, verify by opening a terminal and typing `python --version` — you should see `Python 3.x.x`.

---

## File Structure

```
caia-labels/
│
├── zebra_sequential_labels.py        # Main label generator script
├── test_labels_TL_3x3.zpl            # 9-label test file (TL range, 3 ladders × 3 shelves)
├── facility_reference.xlsx           # Fillable reference spreadsheet for your facility
└── README.md                         # This file
```

Generated output files (kept locally, not shared):
```
├── labels_{RANGE_SIDE}.zpl               # e.g., labels_5L.zpl, labels_3R.zpl
├── labels_{RANGE_SIDE}_{SUFFIX}.zpl      # e.g., labels_8L_part1.zpl (for partial runs)
├── reprint_{RANGE_SIDE}_L{LL}_S{SS}.zpl  # e.g., reprint_5L_L23_S07.zpl (single label reprints)
├── preview_{RANGE_SIDE}_first_label.png
├── preview_{RANGE_SIDE}_last_label.png
└── ...
```

> 💡 The `{RANGE_SIDE}` portion of each filename updates automatically based on whatever `RANGE_SIDE` is set to in the script — you don't need to rename anything manually.

> 💡 Generated `.zpl` and `.png` files are not shared because they are run locally on a separate machine. They can be regenerated at any time by running the script. 

---

## Customizing for Your Facility

This tool is not limited to a 9-range facility — it can be adapted to any storage layout. Here is what each configuration value means and how to change it:

### Label Size and DPI
If your label stock or printer DPI is different, update these values near the top of the script:

```python
LABEL_WIDTH_DOTS  = 402     # Label width in dots  (width in inches × DPI)
LABEL_HEIGHT_DOTS = 203     # Label height in dots (height in inches × DPI)
```

> 💡 **Example:** A 2" × 1" label at 203 dpi = 402 dots wide × 203 dots tall.
> For 300 dpi labels, multiply your label dimensions by 300 instead.

### Location Naming
The three columns on the label are currently labeled **RANGE**, **LADDER**, and **SHELF**. If your facility uses different terminology (e.g., Aisle, Bay, Level), update these lines in the `build_label()` function:

```python
^FDRANGE^FS    ← change RANGE to your term
^FDLADDER^FS   ← change LADDER to your term
^FDSHELF^FS    ← change SHELF to your term
```

### Number of Location Levels
The current design uses **three levels** (Range → Ladder → Shelf). If your facility only needs two levels, or needs four, the `build_label()` function can be modified to add or remove columns. Contact your developer or refer to the ZPL documentation for guidance.

### Range Side Naming Convention
The current facility uses names like `1L`, `1R`, `2L`, `2R`, etc. You can use any naming convention — just set `RANGE_SIDE` to whatever string you want to appear on the label:

```python
RANGE_SIDE = "A1"    # or "ROW1", "SEC-A", "1N", etc.
```

### Batch Mode
The `BATCH_JOBS` list at the top of the script contains all pre-configured range sides for this facility. To adapt it for a different facility, replace the entries with your own range sides and their corresponding ladder and shelf counts.

---

## 💾 Managing Your Files Locally

### Core Files — Keep These Safe
There are three files that make this tool work. Keep them together in a dedicated folder (e.g., a `Labels` folder on your Desktop or a shared network drive):

| File | What It Is |
|---|---|
| `zebra_sequential_labels.py` | The main script — this is the brain of the tool |
| `README.md` | This documentation file |
| `test_labels_TL_3x3.zpl` | A 9-label test file for verifying the printer |
| `facility_reference.xlsx` | Your fillable reference spreadsheet |

### Generated Files — Temporary
Every time you run the script it creates `.zpl` files (and optionally `.png` preview images) in the same folder. These are:
- ✅ Safe to keep for reference
- ✅ Safe to delete — they can be regenerated anytime by running the script
- ❌ Not needed to back up — the script is what matters

### Backups
**Make a backup copy of your core files** in at least one additional location:
- A USB drive stored with the printer
- A shared network folder
- A cloud storage folder (OneDrive, Google Drive, etc.)

> ⚠️ **Do not modify the script** unless you are familiar with Python. If changes are needed (new range sides, different label sizes, etc.), contact whoever originally set this up.

### Mac and Linux Users
All terminal instructions in this README use Windows `cmd`. If you are on a **Mac or Linux** machine:
- Open **Terminal** instead of cmd
- Use `python3` instead of `python` in all commands
- Everything else works the same way

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

`FILE_SUFFIX` appends a custom string to the output filename. This is needed when a range side must be generated in multiple runs (e.g., **8L**, which has ladders 1–6 and 50–54 with a gap of uninstalled shelving in between):

```
Run 1 → FILE_SUFFIX = "_part1"  →  labels_8L_part1.zpl  (ladders 1–6)
Run 2 → FILE_SUFFIX = "_part2"  →  labels_8L_part2.zpl  (ladders 50–54)
```

Leave as `""` for standard naming (e.g., `labels_5L.zpl`).

---

## 🚀 Usage

### Step 1 — Open a Terminal in Your Labels Folder

1. Open **File Explorer** and navigate to your `Labels` folder
2. Click the **address bar** at the top of the window (where the folder path is shown)
3. Type `cmd` and press **Enter**
4. A black terminal window will open, already pointed at your Labels folder ✅

> 💡 **Mac/Linux:** Open **Terminal**, then use the `cd` command to navigate to your Labels folder. For example: `cd ~/Desktop/Labels`

---

### Option 1 — Preview Mode (Text Spot-Check, No Files Created)

```
python zebra_sequential_labels.py --preview
```

This prints a text summary directly in the terminal window showing the first label, the last shelf on Ladder 01, the first shelf on Ladder 02, and the last label. No files are created. Use this to quickly confirm the sequence logic is correct before generating the full file.

**What you should see** (example for Range 5L, 58 ladders, 16 shelves):
```
=============================================
  PREVIEW — Range Side: 5L
  Ladders: 1–58  |  Shelves: 1–16
  Total labels: 928
=============================================

  ✔ First label
    ┌─────────────────────────────┐
    │ RNG: 5L    LDR: 01  SHF: 01 │
    └─────────────────────────────┘

  ✔ Last shelf on Ladder 01
    ┌─────────────────────────────┐
    │ RNG: 5L    LDR: 01  SHF: 16 │
    └─────────────────────────────┘

  ✔ First shelf on Ladder 02
    ┌─────────────────────────────┐
    │ RNG: 5L    LDR: 02  SHF: 01 │
    └─────────────────────────────┘

  ✔ Last label
    ┌─────────────────────────────┐
    │ RNG: 5L    LDR: 58  SHF: 16 │
    └─────────────────────────────┘
```

Verify that:
- **First label** matches your `RANGE_SIDE` / `01` / `01`
- **Shelf resets** correctly at the ladder rollover
- **Last label** matches your `RANGE_SIDE` / last ladder / last shelf
- **Total label count** equals `NUM_LADDERS × NUM_SHELVES` (adjusting for any `SPECIAL_SHELVES`)

---

### Option 2 — PNG Preview (Visual Spot-Check via Labelary API)

```
python zebra_sequential_labels.py --png
```

This reaches out to the Labelary API over the internet and saves **4 PNG image files** in your Labels folder — one for the first label, one for the last shelf on Ladder 01, one for the first shelf on Ladder 02, and one for the last label.

**After running**, open your Labels folder in File Explorer — you will see files like:
- `preview_5L_first_label.png`
- `preview_5L_shelf_rollover.png`
- `preview_5L_ladder_increment.png`
- `preview_5L_last_label.png`

Double-click any of them to open and view like a normal photo.

> 💡 The `5L` portion of each filename reflects whatever `RANGE_SIDE` is currently set to in the script.

> ⚠️ This mode requires an internet connection. If it fails, check your connection and try again. There is a short pause between each request to avoid rate limiting.

---

### Option 3 — Generate ZPL File (Ready to Print)

```
python zebra_sequential_labels.py
```

This generates the full ZPL file for the configured range side. The file will appear in your Labels folder — for example, `labels_5L.zpl`.

**What you should see in the terminal:**
```
  Range Side : 5L
  Ladders    : 1 – 58
  Shelves    : 1 – 16
  Total labels generated: 928

  ZPL written to: labels_5L.zpl
```

Verify that the total label count matches your expected number before sending to the printer. The `.zpl` file is now ready to upload to the online preview tool or send to the printer.

---

### Option 4 — Batch Mode (Generate All Range Sides at Once)

```
python zebra_sequential_labels.py --batch
```

This generates all pre-configured range side ZPL files in one run. All files will appear in your Labels folder. This is useful when setting up a new facility or regenerating all files after any configuration changes.

**What you should see:**
```
  ============================================
  BATCH MODE — Generating all range sides
  ============================================

  [1/13]  2R  →  labels_2R.zpl          119 labels
  [2/13]  3L  →  labels_3L.zpl        1,044 labels
  [3/13]  3R  →  labels_3R.zpl          928 labels
  ...
  [13/13] 8L  →  labels_8L_part2.zpl     80 labels

  ============================================
  Batch complete! 13 files generated.
  ============================================
```

---

### Option 5 — Single Label Reprint

```
python zebra_sequential_labels.py --single RANGE LADDER SHELF
```

This generates a single label ZPL file for one specific location. Replace `RANGE`, `LADDER`, and `SHELF` with the actual values you need.

**Example** — reprint the label for Range 5L, Ladder 23, Shelf 07:
```
python zebra_sequential_labels.py --single 5L 23 07
```

This creates a file called `reprint_5L_L23_S07.zpl` in your Labels folder. Upload it to the online preview tool to verify it looks correct, then send it to the printer.

---

## 🔍 Testing Labels Online

Before committing to a full print run, use one of these free online tools to visually preview your labels:

### Option A — ZPL Printer Online (Recommended for Full File Preview)
**URL:** [zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net)

This tool lets you upload a `.zpl` file directly and preview all labels at once.

**Step by step:**
1. Open your browser and go to [zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net)
2. Click the **Upload** or **Choose File** button on the page
3. Navigate to your Labels folder and select the `.zpl` file you want to preview (e.g., `labels_5L.zpl` or `test_labels_TL_3x3.zpl`)
4. The labels will render on screen — use the navigation arrows to scroll through them
5. Verify:
   - The first label shows the correct Range Side, `01`, `01`
   - The RANGE / LADDER / SHELF words are visible and centered above the numbers
   - The numbers are large and easy to read
   - The layout looks clean and properly centered
   - The sequence increments correctly as you page through

### Option B — Labelary Viewer (Best for Single Label Paste)
**URL:** [labelary.com/viewer.html](http://labelary.com/viewer.html)

This tool lets you paste ZPL text directly and renders a preview immediately.

**Step by step:**
1. Open your browser and go to [labelary.com/viewer.html](http://labelary.com/viewer.html)
2. Set the **width** to `2.00 in` and **height** to `1.00 in`
3. Set the **DPI** to `203`
4. Copy a single `^XA...^XZ` block from your `.zpl` file and paste it into the text box
5. Click **Refresh** (or it may render automatically)

---

## 🧪 Testing Before a Full Print Run

**Always run a test print before printing a full range side.** The test file `test_labels_TL_3x3.zpl` is included specifically for this purpose. It prints 9 labels (3 ladders × 3 shelves) using the range name `TL` (Test Left) — two characters, just like a real range side name, so the font size and spacing are identical to production labels.

**What the test confirms:**
- ✅ The printer is connected and responding
- ✅ Print quality and darkness are acceptable
- ✅ Label calibration is correct (labels cut at the right place)
- ✅ The 1" × 2" label stock is loaded correctly
- ✅ Font size and layout look correct on a real physical label
- ✅ The adhesive sticks to your shelving material

**Run a test print whenever:**
- Setting up on a new printer
- Using a new batch of label stock
- The printer hasn't been used in a while
- Anything looks off after a calibration or setting change

---

## 🖨️ Printing the Labels

### Printer Setup Checklist
Before printing anything, confirm:
- [ ] Label stock is loaded correctly (1" × 2", positioned flush against the guides)
- [ ] The printer status light is **solid green** (not blinking or red)
- [ ] The printer has been **calibrated** — hold the Feed button for ~2 seconds until it advances a few labels and stops. This tells the printer where each label begins and ends.
- [ ] Run the **test file** (`test_labels_TL_3x3.zpl`) before any full job

---

### Finding the Printer's IP Address

Both printing methods below require the printer's IP address. Here's how to find it:

1. Make sure the printer is **powered on** and connected to the network
2. Hold the **Feed button** on the printer for approximately **5 seconds** — longer than the calibration hold — until the printer automatically prints a configuration label
3. Look at the printed label for a line that says **IP Address** — it will look something like `192.168.1.100`
4. Write this number down and enter it in the `facility_reference.xlsx` spreadsheet

> ⚠️ If the IP address shows as `0.0.0.0`, the printer has not been assigned a network address yet. Contact your IT department — the printer needs to be connected to the network and assigned an IP before it can receive print jobs.

> 💡 **Static IP Recommended:** Ask your IT department to assign a **static (fixed) IP address** to the printer so it doesn't change after a reboot. If the printer ever stops responding, check with IT to confirm the IP hasn't changed.

---

### Option A — Print Directly from the Script (Recommended)

Once you have the printer's IP address, update these two lines near the top of `zebra_sequential_labels.py`:

**Step 1 — Open the script in Notepad:**
1. Open your Labels folder in File Explorer
2. Right-click on `zebra_sequential_labels.py`
3. Click **Open with** → **Notepad**

**Step 2 — Find these two lines** (they are near the top of the file, under the `CONFIGURATION` section):
```python
PRINT_DIRECTLY = False
PRINTER_IP     = "192.168.1.100"
```

**Step 3 — Change them to:**
```python
PRINT_DIRECTLY = True
PRINTER_IP     = "192.168.X.XXX"   # ← Replace with your printer's actual IP address
```

**Step 4 — Save the file:**
- Press **Ctrl + S**
- Close Notepad

**Step 5 — Run the script:**
```
python zebra_sequential_labels.py
```

The script will generate the ZPL file and send it directly to the printer. The printer will begin printing immediately.

> 💡 Record the printer's IP address in `facility_reference.xlsx` so it's always easy to find.

---

### Option B — Manual Send via Command Line

If you have already generated a `.zpl` file and want to send it to the printer without running the script again, use this command in your terminal:

```
copy labels_5L.zpl \\192.168.X.XXX\ZPL
```

Replace `labels_5L.zpl` with the actual filename and `192.168.X.XXX` with your printer's IP address. The printer will begin printing immediately after the command completes.

**This method works for any `.zpl` file**, including single-label reprints:
```
copy reprint_5L_L23_S07.zpl \\192.168.X.XXX\ZPL
```

---

## 🔄 Reprinting Labels

Labels occasionally need to be reprinted — a label may have been applied to the wrong shelf, damaged, or lost. There are three reprint scenarios:

---

### Scenario 1 — Reprint a Single Label

Use this when you need just one specific label (e.g., Range 5L, Ladder 23, Shelf 07).

**Step 1 — Open a terminal in your Labels folder** (see Step 1 in the Usage section above)

**Step 2 — Run the single reprint command:**
```
python zebra_sequential_labels.py --single 5L 23 07
```
Replace `5L`, `23`, and `07` with the actual Range Side, Ladder number, and Shelf number you need.

**Step 3 — Verify the file was created:**
A file called `reprint_5L_L23_S07.zpl` will appear in your Labels folder.

**Step 4 — Preview it before printing:**
1. Go to [zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net)
2. Upload `reprint_5L_L23_S07.zpl`
3. Confirm the label shows the correct Range, Ladder, and Shelf

**Step 5 — Send to the printer:**
```
copy reprint_5L_L23_S07.zpl \\192.168.X.XXX\ZPL
```

---

### Scenario 2 — Reprint a Range of Labels (e.g., Several Ladders)

Use this when multiple consecutive labels need reprinting — for example, Ladders 10 through 15 on Range 5L.

**Step 1 — Open the script in Notepad** (right-click → Open with → Notepad)

**Step 2 — Update the CONFIGURATION section:**
```python
RANGE_SIDE   = "5L"     # ← The range side being reprinted
NUM_LADDERS  = 6        # ← How many ladders to reprint (15 - 10 + 1 = 6)
NUM_SHELVES  = 16       # ← Same as the original job
LADDER_START = 10       # ← The first ladder to reprint
FILE_SUFFIX  = "_reprint_L10_L15"   # ← Optional, helps identify the file
```

**Step 3 — Save the file** (Ctrl + S) and close Notepad

**Step 4 — Run the script:**
```
python zebra_sequential_labels.py --preview
```
Verify the output shows Ladder 10 as the first label and Ladder 15 as the last.

**Step 5 — Generate the file:**
```
python zebra_sequential_labels.py
```

**Step 6 — Preview, then print** using either printing method above.

**Step 7 — Reset `LADDER_START` back to `1`** and clear `FILE_SUFFIX` when done:
```python
LADDER_START = 1
FILE_SUFFIX  = ""
```

> ⚠️ Always reset `LADDER_START` to `1` after a partial reprint so the next full job generates correctly.

---

### Scenario 3 — Reprint After a Label Jam

If the printer jams mid-job, some labels may have printed and some may not. Here's how to recover:

**Step 1 — Identify the last successfully printed label.** Look at the printed labels and find the last one that came out correctly. Note its Ladder number.

**Step 2 — Open the script in Notepad** and set `LADDER_START` to the **next** ladder after the last good one. For example, if Ladder 22 was the last good label:
```python
LADDER_START = 23
```

**Step 3 — Leave all other settings the same** as the original job.

**Step 4 — Run the script** — it will generate only the remaining labels (Ladder 23 to the end).

**Step 5 — Reset `LADDER_START = 1`** when done.

---

## 📐 Label Layout Reference

```
┌────────────────────────────────────────────────┐  ← Top of label
│                                                │
│   RANGE        LADDER        SHELF             │  ← Y = 42 dots (descriptor text, 24pt)
│                                                │
│    5L     │     04     │     07                │  ← Y = 79 dots (large number, 112pt)
│           │            │                       │  ← Dividers at X = 135 and X = 271
│                                                │
└────────────────────────────────────────────────┘  ← Bottom of label
  ↑ 402 dots (2" @ 203dpi) ↑
```

**Label dimensions:** 1" H × 2" W at 203 dpi = 203 × 402 dots

**Column X positions:**

| Element | X Position |
|---|---|
| RANGE descriptor | 32 |
| RANGE value | 12 |
| Divider 1 | 135 |
| LADDER descriptor | 165 |
| LADDER value | 148 |
| Divider 2 | 271 |
| SHELF descriptor | 304 |
| SHELF value | 281 |

---

## 🏷️ Label Application Tips

- Labels are designed to be applied **vertically** on shelf uprights/ladders so the text reads when viewed from the aisle
- Apply labels at a **consistent height** on each ladder so they form a visible line when looking down the aisle
- Make sure the surface is **clean and dry** before applying — dust or moisture will reduce adhesion
- Press firmly along the full length of the label after application
- If a label needs to be removed and repositioned, do so **immediately** — adhesive sets quickly on metal shelving

---

## 🔧 Facility Reference Spreadsheet

The file `facility_reference.xlsx` is included for you to document your specific facility's configuration. It contains tabs for:

- **Facility & Printer Info** — contact info, printer model, IP address, label stock details
- **Range Side Status** — track which range sides have been printed and applied
- **Reprint Log** — record every reprint with date, location, and reason
- **Test Print Log** — record each test print
- **Notes & Change History** — document any changes over time
- **Troubleshooting** — quick reference for common issues

> 💡 Keep `facility_reference.xlsx` in your Labels folder alongside the script, and back it up along with your other core files.

---

## 🆘 Troubleshooting

| Problem | First Step |
|---|---|
| Printer not responding | Check IP address — print config label by holding Feed ~5 seconds |
| IP address shows `0.0.0.0` | Printer not connected to network — contact IT |
| IP address changed | Ask IT to assign a static IP; update `PRINTER_IP` in script |
| Labels printing misaligned | Calibrate printer — hold Feed ~2 seconds |
| Script won't run | Check Python is installed: type `python --version` in terminal |
| `python` not recognized | Python not added to PATH — reinstall Python and check "Add to PATH" |
| Wrong labels printed | Use `--single` mode to reprint just the affected label |
| Need to reprint a range | Set `LADDER_START` in script — see Reprinting section above |
| Lost label stock | See `facility_reference.xlsx` Label Stock tab for reorder details |
| Can't find the script | Check backup location listed in `facility_reference.xlsx` |
| Labelary API fails | Check internet connection; try again after a minute |
| Labels look different in preview vs. printer | Labelary is more accurate — trust the printer output |
