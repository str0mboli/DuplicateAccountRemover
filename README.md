# Duplicate Account Remover

A Python script that helps identify already-investigated users across security alerts. Track accounts throughout the day - the script automatically detects duplicates and shows which accounts are new vs already seen.

## Requirements

- Python 3.6 or higher

## How to Run

### Option 1: Command Line

```powershell
cd "path\to\script\folder"
python duplicate_remover.py
```

### Option 2: Double-Click

Navigate to the folder containing `duplicate_remover.py` and double-click it.

## Usage

1. Run the script
2. Choose how to add accounts:
   - **Option 1**: Paste accounts directly (one per line, then press Enter on a blank line)
   - **Option 2**: Load from a text file (enter the file path or drag and drop)
3. View results showing NEW accounts vs ALREADY SEEN
4. Repeat throughout the day - the script remembers all accounts you've processed

## Input Format

Plain text file with one account (email) per line:

```
john.doe@company.com
jane.smith@company.com
bob.wilson@company.com
```

## Output

The script produces:

- **Console output**: Shows NEW accounts (need investigation) vs ALREADY SEEN (skip)
- **Daily master file**: `all_accounts_YYYY-MM-DD.txt` - tracks all accounts seen today (resets each day)
- **Output file**: `unique_accounts_YYYY-MM-DD.txt` - new accounts only

## Example

**First run with 5 accounts:**
```
Accounts processed: 5
NEW accounts (need investigation): 5
ALREADY SEEN (skip): 0
```

**Second run with 3 accounts (2 were already seen):**
```
Accounts processed: 3
NEW accounts (need investigation): 1
ALREADY SEEN (skip): 2

NEW ACCOUNTS (Need investigation)
  newuser@company.com

ALREADY SEEN (Already investigated)
  john.doe@company.com
  jane.smith@company.com
```

## Notes

- The master list resets automatically each day (no manual cleanup needed)
- Accounts are normalized (case-insensitive, invisible characters removed)
- Press Enter to close the terminal window when done
