"""Database operations with proper connection management."""

import sqlite3
import os
from typing import Optional, List
from contextlib import contextmanager

from .crypto import decrypt, UserAccount

DB_PATH = "data/accounts.db"


@contextmanager
def get_db_connection():
    """Context manager for database connections.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Initialize database if it doesn't exist."""
    if os.path.exists(DB_PATH):
        return
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE accounts (
                name TEXT,
                email BLOB,
                password BLOB,
                iv BLOB
            )
        """)


def insert_into_db(user: UserAccount) -> bool:
    """Insert encrypted entry into database.
    
    Args:
        user: UserAccount with encrypted email, password, and IV
        
    Returns:
        True on success
    """
    init_db()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts VALUES (?, ?, ?, ?)",
            (user.name, user.email, user.password, user.iv)
        )
        return True


def view_entry(name: str) -> None:
    """View and print all entries matching name.
    """
    if not os.path.exists(DB_PATH):
        print("Accounts file is missing.")
        print("Add an entry with --add first")
        return
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE name = ?", (name,))
        
        found = False
        for row in cursor.fetchall():
            try:
                encrypted = UserAccount(
                    name=row[0],
                    email=row[1],
                    password=row[2],
                    iv=row[3]
                )
                decrypted = decrypt(encrypted)
                
                print(f"Account: {decrypted.name}")
                print(f"Email: {decrypted.email}")
                print(f"Password: {decrypted.password}")
                print("=========================")
                found = True
            except Exception as e:
                print(f"Error decrypting entry: {e}")
        
        if not found:
            print(f"No entries found for: {name}")


def search_by_email(email: str) -> None:
    """Search entries by email.
    """
    if not email:
        print("[!] No email/username provided...Exiting [!]")
        return
    
    if not os.path.exists(DB_PATH):
        print("Accounts file is missing.")
        return
    
    found = False
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        
        for row in cursor.fetchall():
            try:
                encrypted = UserAccount(
                    name=row[0],
                    email=row[1],
                    password=row[2],
                    iv=row[3]
                )
                decrypted = decrypt(encrypted)
                
                # EXACT MATCH: Case-sensitive comparison (password manager standard)
                if decrypted.email == email:
                    print(f"Account: {decrypted.name}")
                    print(f"Email: {decrypted.email}")
                    print(f"Password: {decrypted.password}")
                    found = True
                    break
            except Exception:
                continue
        
        if not found:
            print(f"No account found for email: {email}")


def delete_entry(email: str, password: str, name: str) -> bool:
    """Delete specific entry after verification.
    """
    if not all([email, password, name]):
        print("[!] Missing required fields for deletion")
        return False
    
    if not os.path.exists(DB_PATH):
        print("Accounts file is missing.")
        return False
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        
        for row in cursor.fetchall():
            try:
                encrypted = UserAccount(
                    name=row[0],
                    email=row[1],
                    password=row[2],
                    iv=row[3]
                )
                decrypted = decrypt(encrypted)
                
                # FIXED: All comparisons use EXACT matching (password manager standard)
                # Email and password must match character-for-character including case
                if (decrypted.name == name and 
                    decrypted.email == email and  # EXACT match, no .lower()
                    decrypted.password == password):  # EXACT match, no .lower()
                    
                    cursor.execute(
                        "DELETE FROM accounts WHERE email = ? AND password = ?",
                        (encrypted.email, encrypted.password)
                    )
                    return True
            except Exception:
                continue
        
        print(f"No matching account found")
        return False
