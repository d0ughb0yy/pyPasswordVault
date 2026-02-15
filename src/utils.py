"""Shared utilities for authentication and validation."""

import hmac
import os
import sys
from typing import Optional

from dotenv import load_dotenv
from Crypto.Protocol.KDF import PBKDF2

load_dotenv()


def verify_master_password() -> bool:
    """Verify master password against environment variable using constant-time comparison.
    
    VULNERABILITY FIXED:
    The original code used '!=' for password comparison (pypass.py lines 39, 49, 60, 70):
        if user_check != os.getenv("MASTER_PASS"):
    
    This is vulnerable to TIMING ATTACKS. The '!=' operator returns False immediately 
    when it finds a mismatch, which leaks timing information. Attackers can measure 
    response times to guess the password character by character.
    
    THE FIX:
    hmac.compare_digest() performs a constant-time comparison. It compares ALL 
    characters regardless of mismatches, ensuring the comparison takes the same 
    amount of time whether the password is 1% or 99% correct.
    
    Returns:
        bool: True if password is correct, False otherwise.
    """
    master_pass = os.getenv("MASTER_PASS")
    if not master_pass:
        print("[✗] MASTER_PASS not set in environment")
        return False
    
    user_input = input("Please enter master password: ")
    
    # Use constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(user_input, master_pass):
        print("[!] Wrong password try again")
        return False
    
    return True


def require_auth() -> None:
    """Require authentication or exit the program.
    
    This eliminates the code duplication that existed in the original pypass.py,
    where the same authentication block was repeated 4 times across lines 39-41,
    49-51, 60-62, and 70-72.
    
    Centralizing authentication ensures:
    1. Consistent error messages
    2. Single point of maintenance
    3. No risk of inconsistent behavior between operations
    """
    if not verify_master_password():
        sys.exit(1)


def get_encryption_key() -> Optional[bytes]:
    """Derive encryption key from environment using PBKDF2.
    
    VULNERABILITY AVOIDED:
    The original code in crypto.py (line 13) derived the key at module import time:
        key = PBKDF2(MASTER, SALT, dkLen=32)
    
    This meant:
    1. Key was created even if not needed (e.g., running --help)
    2. Key existed in memory throughout entire program lifetime
    3. If MASTER or SALT env vars were missing, the error was cryptic
    
    THE FIX:
    Derive keys only when needed, with proper error handling for missing
    environment variables.
    
    Returns:
        bytes: 32-byte encryption key, or None if environment not configured.
    """
    master = os.getenv("MASTER_PASS")
    salt = os.getenv("SALT")
    
    if not master or not salt:
        print("[✗] MASTER_PASS or SALT not set in environment")
        return None
    
    # Handle salt that might be stored as a string representation of bytes
    if isinstance(salt, str):
        if salt.startswith("b'") and salt.endswith("'"):
            # It's a string representation of bytes like "b'\\x00\\x01...'"
            try:
                salt = eval(salt)
            except:
                salt = salt.encode()
        else:
            salt = salt.encode()
    
    return PBKDF2(master, salt, dkLen=32)
