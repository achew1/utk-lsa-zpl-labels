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

✔ What to check:
- First label matches `{RANGE_SIDE} / 01 / 01`
- Shelf resets to `01` after reaching `NUM_SHELVES`
- Ladder increments correctly on shelf rollover
- Last label matches `{RANGE_SIDE} / {NUM_LADDERS} / {NUM_SHELVES}`

---

### Option 2 — PNG Preview Mode (Visual Check)
```
python zebra_sequential_labels.py --png
```
Fetches 4 rendered PNG label images from the [Labelary API](http://labelary.com) and saves them in your `Caia Labels` folder. **Requires internet.** Use this to visually confirm label layout before printing.

Saves:
- `preview_{RANGE_SIDE}_first_label.png`
- `preview_{RANGE_SIDE}_shelf_rollover.png`
- `preview_{RANGE_SIDE}_ladder_increment.png`
- `preview_{RANGE_SIDE}_last_label.png`

To view them, simply open your `Caia Labels` folder in File Explorer and double-click any `.png` file — they open like normal photos.

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

You'll see this confirmation in the terminal when it's done:
```
Range Side : 5L
Ladders    : 1 – 58
Shelves    : 1 – 15
Total labels generated: 870
```

The file `labels_5L.zpl` will now be visible in your `Caia Labels` folder in File Explorer. **You don't need to open it** — just leave it there and send it to the printer using one of the methods below.

> 💡 A `.zpl` file is just a plain text file with printer instructions inside. Zebra printers know how to read it and turn it into printed labels.

---

## 🖨️ Printing the Labels — Step by Step

### Before You Print — Printer Setup Checklist
1. **Load the correct label stock** — 1" H × 2" W labels. Make sure the roll is loaded correctly per your printer model's manual.
2. **Calibrate the printer** — After loading new label stock, most Zebra printers need to be calibrated so they detect the label size correctly:
   - Hold the **Feed** button for ~2 seconds until the printer flashes, then release.
   - The printer will feed a few labels and detect the gap between them automatically.
3. **Confirm the printer is online** — The status light should be solid green. Flashing or amber usually means a paper or ribbon issue.

---

### Finding the Printer's IP Address

You'll need the printer's IP address for both Option A (direct print) and Option B (manual send). The easiest way is to print a **configuration label** directly from the printer:

1. Make sure the printer is powered on and has label stock loaded
2. Hold the **Feed** button for approximately **5 seconds** until the printer starts printing automatically
3. A configuration label will print — the **IP address** will be listed on it
   - It will look something like: `192.168.1.100`

> 💡 If the IP shows as `0.0.0.0`, the printer hasn't been assigned a network address yet — connect it to your network via ethernet or Wi-Fi and try again, or check with your IT department.

Alternatively, your IT department or network router's admin page can show you the IP address assigned to the printer.

---

### Option A — Direct Network Print via Script (Recommended)

This method generates the ZPL **and** sends it to the printer automatically in one step.

#### Step 1 — Update the Script with the Printer's IP
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

#### Step 2 — Generate and Print
Open a terminal in your `Caia Labels` folder (see Step 1 under Usage above) and run:
```
python zebra_sequential_labels.py
```
The script will generate the ZPL and send it directly to the printer over the network. The printer should begin printing immediately.

---

### Option B — Manual Send via Command Line (No Python Required)

This method is a great backup if you already have a `.zpl` file generated and just want to send it to the printer without running the script again. It uses a built-in Windows command — no extra software needed.

#### Step 1 — Generate the ZPL File
If you haven't already, run the script to generate the file:
```
python zebra_sequential_labels.py
```
This creates `labels_5L.zpl` in your `Caia Labels` folder.

#### Step 2 — Send the File to the Printer
In your terminal, type the following and hit **Enter** (replace the IP with your printer's actual address):
```
copy labels_5L.zpl \\192.168.X.XXX\ZPL
```
The printer will receive the file and begin printing immediately.

> 💡 The `\\IP\ZPL` format is a standard Windows network path that Zebra printers recognize on port 9100. No additional setup is needed on the printer side.

---

### Option C — Zebra Setup Utilities (ZSU)

Use this method if you prefer a graphical interface or need more control over the print job.

#### Step 1 — Install Zebra Setup Utilities (ZSU)
Download it free from Zebra's website:
👉 [zebra.com/us/en/support-downloads/software/printer-software/zebra-setup-utility.html](https://www.zebra.com/us/en/support-downloads/software/printer-software/zebra-setup-utility.html)

Install and open it. It will detect your connected Zebra printer automatically (USB or network).

#### Step 2 — Generate the ZPL File
Make sure `PRINT_DIRECTLY = False` in the script, then run:
```
python zebra_sequential_labels.py
```

#### Step 3 — Send to Printer via ZSU
1. Open **Zebra Setup Utilities**
2. Select your printer from the list
3. Click **Open Printer Tools**
4. Go to the **Action** tab
5. Click **Send file to printer** and browse to your `labels_5L.zpl` file
6. Click **Send** — the printer will begin printing

---

### Option D — USB Drive (If Printer Has a USB Host Port)

Some Zebra printers have a **USB host port** (the kind you plug a USB drive into, not the kind you plug into a computer). If yours does:

1. Generate the `.zpl` file using the script
2. Copy `labels_5L.zpl` to a USB drive
3. Plug the USB drive into the printer's host port
4. The printer should detect and print the file automatically

Check your printer's manual to confirm if this feature is supported and how to enable it.

---

## 🔁 Git Workflow — Tracking Changes Across Range Sides

After completing each range side, commit the changes so you have a full history:

```bash
# Stage your changes
git add zebra_sequential_labels.py README.md

# Commit with a descriptive message
git commit -m "Complete Range 5L — 58 ladders, 15 shelves, 870 labels"
```

### Suggested Commit Messages
```
Initial commit - project setup
Complete Range 1L - XX ladders, XX shelves, XXX labels
Complete Range 1R - XX ladders, XX shelves, XXX labels
...
```

> 💡 The `.zpl` and `.png` files are excluded from Git via `.gitignore` — they can always be regenerated by running the script.

---

## 🔄 Partial Reprints

If you need to reprint starting from a specific ladder (e.g., labels were damaged starting at Ladder 12):

```python
LADDER_START = 12    # ← Start from Ladder 12
NUM_LADDERS  = 47    # ← Remaining ladders (58 - 12 + 1 = 47)
```

This generates only the labels you need without reprinting the whole range side.

---

## 🔍 Troubleshooting

| Problem | Solution |
|---|---|
| `python` not recognized | Reinstall Python and make sure "Add to PATH" is checked |
| Labelary PNG fails | Check internet connection; try again after 30 seconds |
| Printer not responding | Confirm IP address by printing a config label (hold Feed ~5 seconds) |
| Labels printing wrong size | Recalibrate printer (hold Feed ~2 seconds after loading stock) |
| `0.0.0.0` shown as IP | Printer not assigned a network address — check network/IT |
