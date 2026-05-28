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
Generates the full ZPL file for the configured range side (e.g., `labels_5L.zpl`). Send this file to the Zebra printer using one of the methods below.

---

## 🖨️ Printing the Labels — Step by Step

### Before You Print — Printer Setup Checklist
1. **Load the correct label stock** — 1" H × 2" W labels. Make sure the roll is loaded correctly per your printer model's manual.
2. **Calibrate the printer** — After loading new label stock, most Zebra printers need to be calibrated so they detect the label size correctly:
   - Hold the **Feed** button for ~2 seconds until the printer flashes, then release.
   - The printer will feed a few labels and detect the gap between them automatically.
3. **Confirm the printer is online** — The status light should be solid green. Flashing or amber usually means a paper or ribbon issue.

---

### Option A — Direct Network Print (Recommended)

This is the fastest method if your printer is connected to your facility's network (Wi-Fi or ethernet).

#### Step 1 — Find the Printer's IP Address
The easiest way is to print a **configuration label** directly from the printer itself:
1. Make sure the printer is powered on and has label stock loaded
2. Hold the **Feed** button for approximately **5 seconds** until the printer starts printing automatically
3. A configuration label will print — the **IP address** will be listed on it
   - It will look something like: `192.168.1.100`

> 💡 If the IP shows as `0.0.0.0` the printer hasn't been assigned a network address yet — connect it to your network via ethernet or Wi-Fi and try again, or check with your IT department.

Alternatively, your IT department or network router's admin page can show you the IP address assigned to the printer.

#### Step 2 — Update the Script with the Printer's IP
Open `zebra_sequential_labels.py` and find these two lines near the top of the `CONFIGURATION` section:

```python
PRINT_DIRECTLY = False
PRINTER_IP     = "192.168.1.100"
```

Change them to:

```python
PRINT_DIRECTLY = True
PRINTER_IP     = "192.168.X.XXX"   # ← Replace with your printer's actual IP address
PRINTER_PORT   = 9100              # ← Leave this as 9100 (standard Zebra port)
```

> 💡 **Tip:** Once you have set the correct IP, commit this change to Git so you don't have to look it up again. Just remember to set `PRINT_DIRECTLY = False` when generating ZPL files without printing.

#### Step 3 — Generate and Print
Run the script normally:
```
python zebra_sequential_labels.py
```
The script will generate the ZPL and send it directly to the printer over the network. The printer should begin printing immediately.

---

### Option B — Manual File Transfer via Zebra Setup Utilities

Use this method if you can't print directly over the network, or if you want more control over the print job.

#### Step 1 — Install Zebra Setup Utilities (ZSU)
Download it free from Zebra's website:
👉 [zebra.com/us/en/support-downloads/software/printer-software/zebra-setup-utility.html](https://www.zebra.com/us/en/support-downloads/software/printer-software/zebra-setup-utility.html)

Install and open it. It will detect your connected Zebra printer automatically (USB or network).

#### Step 2 — Generate the ZPL File
Make sure `PRINT_DIRECTLY = False` in the script, then run:
```
python zebra_sequential_labels.py
```
This creates the `.zpl` file (e.g., `labels_5L.zpl`) in your project folder.

#### Step 3 — Send to Printer via ZSU
1. Open **Zebra Setup Utilities**
2. Select your printer from the list
3. Click **"Open Printer Tools"**
4. Go to the **"Action"** tab
5. Click **"Send file to printer"**
6. Browse to and select your `.zpl` file
7. Click **Send** — the printer will begin printing

---

### Option C — Copy via USB Drive

If the printer has a USB host port (a full-size USB-A port on the printer itself):

1. Copy the `.zpl` file to the root of a USB drive
2. Plug the USB drive into the printer
3. The printer should detect and print the file automatically

> ⚠️ Not all Zebra models support this. Check your printer's manual.

---

### Option D — Windows Port (Advanced)

If the printer is shared on the network as a Windows printer:

```
copy /b labels_5L.zpl \\printername\sharename
```

Or if connected via USB and mapped to a port (e.g., `LPT1`):
```
copy /b labels_5L.zpl LPT1
```

---

## 🔁 Partial Reprints

If you need to reprint labels for a specific ladder range (e.g., Ladders 12–15 got damaged):

1. Set `LADDER_START = 12` in the configuration
2. Set `NUM_LADDERS = 4` (to cover ladders 12, 13, 14, 15)
3. Run the script — it will generate only those labels

---

## 🗂️ Git Workflow

### Initial Setup
```bash
git init
git add zebra_sequential_labels.py README.md .gitignore
git commit -m "Initial commit - Range 5L configuration"
```

### Committing Each Range Side
```bash
# After updating config for a new range side:
git add zebra_sequential_labels.py README.md
git commit -m "Configure and complete Range 3R - 12 ladders x 8 shelves"
```

### Recommended Commit Message Format
```
Configure Range {SIDE} - {LADDERS} ladders x {SHELVES} shelves
```

---

## 🧪 Testing Checklist (Per Range Side)

Before every print run, work through this checklist:

- [ ] Updated `RANGE_SIDE`, `NUM_LADDERS`, `NUM_SHELVES` in the script
- [ ] Ran `--preview` and confirmed first/last/rollover labels are correct
- [ ] Ran `--png` and visually confirmed label layout
- [ ] Printer is online (solid green status light)
- [ ] Correct label stock loaded and printer calibrated
- [ ] Updated the Range Side Reference Table in this README
- [ ] Committed the configuration to Git

---

*Last updated: Range 5L — 58 ladders × 15 shelves = 870 labels*
