from __future__ import annotations

import sys

from src.gmail_creator.account_creator import create_single_account
from src.gmail_creator.config import CONFIG
from src.gmail_creator.ip_check import check_current_ip
from src.gmail_creator.ui import (
    create_progress,
    input_number,
    print_accounts,
    print_banner,
    print_error,
    print_info,
    print_ip_check,
    print_menu,
    print_stats,
)


def create_accounts_flow() -> None:
    count = input_number("How many accounts to create? ")
    if count <= 0:
        print_info("Invalid number.")
        return

    success = 0
    progress = create_progress()
    with progress:
        task = progress.add_task("Creating accounts...", total=count)
        for _ in range(count):
            result = create_single_account()
            if result:
                success += 1
            progress.update(task, advance=1)

    print_info(f"Done. {success}/{count} accounts created.")


def main() -> None:
    print_banner()
    if CONFIG.IP_CHECK_ENABLED:
        result = check_current_ip()
        print_ip_check(result)
        if CONFIG.IP_CHECK_BLOCK_ON_MISMATCH and not result.ok:
            print_error("Startup IP check failed. Fix proxy/IP settings before creating accounts.")
            sys.exit(1)

    while True:
        print_menu()
        choice = input_number("Select option: ")
        if choice == 1:
            create_accounts_flow()
        elif choice == 2:
            print_stats()
        elif choice == 3:
            print_info("Settings - coming soon.")
        elif choice == 4:
            print_accounts()
        elif choice == 5:
            print_info("Goodbye!")
            sys.exit(0)
        else:
            print_info("Invalid option.")


if __name__ == "__main__":
    main()
