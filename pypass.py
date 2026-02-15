"""CLI entry point for password manager."""

import argparse
import sys

from src.utils import require_auth
from src.crypto import UserAccount, encrypt
from src.db import (
    insert_into_db,
    view_entry,
    search_by_email,
    delete_entry
)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="pyPass Password Manager",
        description="Password manager that stores your encrypted data in a SQLite local file",
    )
    parser.add_argument(
        "-f", "--function",
        help="Function to perform: add, view, search or delete",
        required=True,
        type=str,
        choices=["add", "view", "search", "delete"],
    )
    parser.add_argument(
        "-n", "--name",
        help="Name of the account",
        type=str
    )
    parser.add_argument(
        "-u", "--username",
        help="Username used in the account",
        type=str
    )
    parser.add_argument(
        "-p", "--password",
        help="Password for the account",
        type=str
    )
    return parser


def handle_view(args) -> None:
    """Handle view function.
    """
    require_auth()
    
    if not args.name:
        print("[!] Name required for view operation")
        sys.exit(1)
    
    view_entry(args.name)


def handle_add(args) -> None:
    """Handle add function.
    """
    require_auth()
    
    if not all([args.name, args.username, args.password]):
        print("[!] Name, username, and password required for add operation")
        sys.exit(1)
    
    user = UserAccount(
        name=args.name,
        email=args.username,
        password=args.password
    )
    encrypted_user = encrypt(user)
    insert_into_db(encrypted_user)
    print(f"[✓] Entry added for {args.name}")


def handle_search(args) -> None:
    """Handle search function.
    """
    require_auth()
    
    if not args.username:
        print("[!] Username/email required for search operation")
        sys.exit(1)
    
    search_by_email(args.username)


def handle_delete(args) -> None:
    """Handle delete function.
    """
    require_auth()
    
    if not all([args.name, args.username, args.password]):
        print("[!] Name, username, and password required for delete operation")
        sys.exit(1)
    
    success = delete_entry(args.username, args.password, args.name)
    if success:
        print(f"[✓] Entry deleted successfully")
    else:
        print(f"[✗] Failed to delete entry")


def main() -> None:

    parser = create_parser()
    args = parser.parse_args()
    
    # Route to appropriate handler
    handlers = {
        "view": handle_view,
        "add": handle_add,
        "search": handle_search,
        "delete": handle_delete,
    }
    
    handler = handlers.get(args.function)
    if handler:
        handler(args)
    else:
        print(f"[!] Unknown function: {args.function}")
        sys.exit(1)


if __name__ == "__main__":
    main()
