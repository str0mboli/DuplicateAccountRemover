"""
Duplicate Account Remover

This script helps identify already-investigated users across security alerts.
Users can paste new accounts directly - the script automatically tracks all
accounts in a daily master file and identifies which ones have been seen before.

Usage:
    python duplicate_remover.py

    Option 1: Paste accounts directly when prompted
    Option 2: Load from a text file

Output:
    - Console: Shows NEW accounts (first time seen) vs ALREADY SEEN (duplicates)
    - Daily master file: all_accounts_YYYY-MM-DD.txt (resets each day)
    - Output file: unique_accounts_YYYY-MM-DD.txt (new accounts only)
"""

import re
import os

from collections import Counter
from datetime import datetime


def get_master_file():
    """Get today's master file name (resets daily)."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    return f"all_accounts_{date_str}.txt"


def normalize_account(text):
    """
    Normalize a single account string.

    Removes invisible characters, converts to lowercase, strips whitespace.
    """
    # Remove all non-printable and invisible characters
    # Keep only: letters, numbers, @, ., -, _, and standard space
    account = re.sub(r'[^\w@.\-\s]', '', text)
    account = account.strip().lower()
    return ' '.join(account.split()) if account else None


def read_accounts(filepath):
    """
    Read and normalize accounts from a text file.

    Args:
        filepath (str): Path to the input text file containing accounts.

    Returns:
        list: List of lowercase account strings with whitespace stripped.

    Note:
        - Empty lines are skipped
        - All accounts are converted to lowercase for case-insensitive comparison
        - Hidden/invisible characters are removed
    """
    accounts = []
    if not os.path.exists(filepath):
        return accounts

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            account = normalize_account(line)
            if account:
                accounts.append(account)
    return accounts


def get_new_accounts_from_input():
    """
    Get accounts from user - either by pasting or loading from file.

    Returns:
        list: List of normalized account strings.
    """
    print("\nHow would you like to add accounts?")
    print("  1. Paste accounts directly")
    print("  2. Load from a file")
    choice = input("\nEnter choice (1 or 2): ").strip()

    accounts = []

    if choice == "1":
        print("\nPaste accounts below (one per line).")
        print("When done, enter a blank line:\n")
        while True:
            line = input()
            if not line.strip():
                break
            account = normalize_account(line)
            if account:
                accounts.append(account)
    elif choice == "2":
        filepath = input("\nEnter path to accounts file: ").strip()
        filepath = filepath.strip('"').strip("'")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    account = normalize_account(line)
                    if account:
                        accounts.append(account)
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
    else:
        print("Invalid choice.")

    return accounts


def append_to_master(accounts):
    """
    Append new accounts to the master tracking file.
    """
    with open(get_master_file(), 'a', encoding='utf-8') as f:
        for account in accounts:
            f.write(account + '\n')


def main():
    """
    Main entry point for the duplicate account remover script.

    Workflow:
        1. Load existing master list of all previously seen accounts
        2. Get new accounts from user (paste or file)
        3. Check which new accounts have been seen before
        4. Display results and save new accounts to output file
        5. Update master list with all new accounts

    Raises:
        FileNotFoundError: If the specified input file does not exist.
    """
    # Display script header
    print("\n" + "=" * 50)
    print("DUPLICATE ACCOUNT REMOVER")
    print("=" * 50)

    # Step 1: Load existing master list (resets daily)
    master_file = get_master_file()
    existing_accounts = set(read_accounts(master_file))
    if existing_accounts:
        print(f"\nLoaded {len(existing_accounts)} accounts seen today.")
    else:
        print("\nStarting fresh for today.")

    # Step 2: Get new accounts from user
    new_accounts = get_new_accounts_from_input()

    if not new_accounts:
        print("\nNo accounts provided.")
        input("\nPress Enter to exit...")
        return

    print(f"\nProcessing {len(new_accounts)} accounts...")

    # Step 3: Check which are new vs already seen
    new_unique = []
    already_seen = []

    for account in new_accounts:
        if account in existing_accounts:
            already_seen.append(account)
        else:
            if account not in new_unique:  # Avoid duplicates within this batch
                new_unique.append(account)
            existing_accounts.add(account)  # Track for duplicate detection within batch

    # Step 4: Display results
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)

    print(f"\nAccounts processed: {len(new_accounts)}")
    print(f"NEW accounts (need investigation): {len(new_unique)}")
    print(f"ALREADY SEEN (skip): {len(already_seen)}")

    print("\n" + "-" * 50)
    print("NEW ACCOUNTS (Need investigation)")
    print("-" * 50)
    if new_unique:
        for account in sorted(new_unique):
            print(f"  {account}")
    else:
        print("  (none - all accounts were previously seen)")

    print("\n" + "-" * 50)
    print("ALREADY SEEN (Already investigated)")
    print("-" * 50)
    if already_seen:
        # Count occurrences in this batch
        seen_counts = Counter(already_seen)
        for account, count in sorted(seen_counts.items()):
            if count > 1:
                print(f"  {account} (appeared {count} times in this batch)")
            else:
                print(f"  {account}")
    else:
        print("  (none - all accounts are new)")
    print()

    # Step 5: Save new unique accounts to dated output file
    if new_unique:
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_path = f"unique_accounts_{date_str}.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            for account in sorted(new_unique):
                f.write(account + '\n')
        print(f"New accounts saved to: {output_path}")

    # Step 6: Append ALL new accounts to master list (including duplicates for tracking)
    append_to_master(new_accounts)
    print(f"Master list updated: {get_master_file()}")
    print()

    input("\nPress Enter to exit...")


# Standard Python idiom: only run main() when script is executed directly,
# not when imported as a module
if __name__ == "__main__":
    main()
