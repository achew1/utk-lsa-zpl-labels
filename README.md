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
├── labels_{RANGE_SIDE}.zpl               # e.g., labels_5L.zpl, labels_3R.zpl
├── preview_{RANGE_SIDE}_first_label.png  # e.g., preview_5L_first_label.png
├── preview_{RANGE_SIDE}_last_label.png   # e.g., preview_5L_last_label.png
└── ...
```

> 💡 The `{RANGE_SIDE}` portion of each filename updates automatically based on whatever `RANGE_SIDE` is set to in the script — you don't need to rename anything manually.

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

The `.zpl` file will now be visible in your `Caia Labels` folder in File Explorer. **You don't need to open it** — just leave it there and send it to the printer using one of the methods below.

> 💡 A `.zpl` file is just a plain text file with printer instructions inside. Zebra printers know how to read it and turn it into printed labels.

---

## 🔍 Testing Labels Online

Before sending a job to the printer, you can visually verify label layout using either of these free online tools. Both work directly in your browser — no installation needed.

---

### Tool 1 — ZPL Printer Online (Recommended for Full Job Testing)
**[zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net/)**

This tool lets you **upload a `.zpl` file directly** and renders all labels for preview — great for checking a full job before printing.

#### Step-by-step:
1. Generate your `.zpl` file first by running `python zebra_sequential_labels.py`
2. Open **[zplprinter.azurewebsites.net](https://zplprinter.azurewebsites.net/)** in your browser
3. Click **Choose File** (or the upload button) and select your `.zpl` file from your `Caia Labels` folder
4. Set the label size to **2" × 1"** and DPI to **203** if prompted
5. Click **Print** or **Render** — all labels will display on screen for you to scroll through and verify

✔ What to check — verify that the labels show your configured Range Side, that shelves count up correctly to your configured NUM_SHELVES, that the ladder increments when the shelf resets, and that the last label matches your configured NUM_LADDERS / NUM_SHELVES.

---

### Tool 2 — Labelary Viewer (Quick Single Label Check)
**[labelary.com/viewer.html](http://labelary.com/viewer.html)**

Best for pasting a single label block to quickly check layout and font sizing.

#### Step-by-step:
1. Copy a single `^XA...^XZ` block from your `.zpl` file (or write one manually)
2. Open **[labelary.com/viewer.html](http://labelary.com/viewer.html)** in your browser
3. Paste the ZPL into the text box on the left
4. Set **Width** to `2.00 in`, **Height** to `1.00 in`, and **DPI** to `203`
5. Click **Refresh** — the label renders on the right

✔ What to check — same as above, but for a single label only.

---

## 🖨️ Printing the Labels

### Before You Print — Printer Setup Checklist
- ✅ Load **1" × 2" label stock** into the printer
- ✅ Calibrate the printer so it detects the label gap:
  - Hold the **Feed** button for ~2 seconds until the printer feeds a few labels and stops
  - The status light should return to **solid green** when calibration is complete
- ✅ Confirm the printer is powered on and the status light is **solid green**
- ✅ Confirm the printer is connected to your network

---

### Finding the Printer's IP Address

You will need the printer's IP address for both printing options below. To find it:

1. Make sure the printer is **powered on** and **loaded with label stock**
2. Hold the **Feed button** for approximately **5 seconds** until the printer prints a configuration label automatically
3. Look for the **IP Address** on the printed label (it will look like `192.168.X.XXX`)

> ⚠️ If the IP address shows as `0.0.0.0`, the printer has not been assigned a network address yet. Connect it to your network via ethernet and try again, or contact your IT department to assign it a static IP.

Once you have the IP address, commit it to the README or the script comments so you don't have to look it up again:
```bash
git add zebra_sequential_labels.py
git commit -m "Set printer IP to 192.168.X.XXX"
```

---

### Option A — Direct Print via Script (Recommended)

This is the easiest method — the script generates the ZPL and sends it to the printer automatically in one step.

#### Setup (one time only):
1. Open `zebra_sequential_labels.py` in a text editor
2. Find these two lines near the top:
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

#### To print:
```
python zebra_sequential_labels.py
```
The script will generate the ZPL and send it directly to the printer. Labels will begin printing immediately.

---

### Option B — Manual Send via Command Line

Use this method if you have already generated the `.zpl` file and want to send it to the printer without running the full script, or if you prefer not to modify the script.

#### In your cmd window:
```
copy labels_{RANGE_SIDE}.zpl \\192.168.X.XXX\ZPL
```

Replace `{RANGE_SIDE}` with your actual range side (e.g., `labels_5L.zpl`) and `192.168.X.XXX` with your printer's IP address. The printer will begin printing immediately.

> 💡 This method works with any already-generated `.zpl` file and requires no changes to the script.

---

## 🗂️ After Printing — File Management

Once a range side job is complete:

1. **Update the Range Side Reference Table** in this README — mark the range side as ✅ Complete and fill in the ladder, shelf, and total label counts
2. **Archive the `.zpl` file** if you want a record of the exact labels printed — move it to an `archive/` subfolder:
   ```
   archive/
   ├── labels_5L.zpl
   ├── labels_3R.zpl
   └── ...
   ```
3. **Or delete the `.zpl` file** if you don't need it — it can always be regenerated by running the script again with the same configuration
4. **Commit the README update** to Git so the status table stays current:
   ```bash
   git add README.md
   git commit -m "Mark 5L as complete - 58 ladders, 15 shelves, 870 labels"
   ```

> 💡 If you choose to archive `.zpl` files, add `archive/*.zpl` to your `.gitignore` instead of `*.zpl` so the archive folder is tracked by Git but the files inside are not.

---

## 🔧 Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `python` not recognized | Python not installed or not in PATH | Reinstall Python and check "Add to PATH" |
| Labels print in wrong order | Loop logic issue | Run `--preview` and verify rollover behavior |
| Labels are blank | Wrong label size loaded | Confirm 1" × 2" stock is loaded |
| Printer not found | Wrong IP address | Reprint config label and verify IP |
| Labels misaligned | Printer needs calibration | Hold Feed ~2 seconds to recalibrate |
| `Bad Request` from Labelary | ZPL formatting issue | Check for extra blank lines in ZPL |
| `Too Many Requests` from Labelary | Rate limited | Wait a few seconds and try again |
