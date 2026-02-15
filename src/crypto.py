"""Encryption and decryption utilities."""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

load_dotenv()


@dataclass
class UserAccount:
    """Data class for user account information.
    """
    name: Optional[str]
    email: Optional[bytes | str]
    password: Optional[bytes | str]
    iv: Optional[bytes] = None


def _get_key() -> bytes:
    """Derive encryption key from environment.
    """
    master = os.getenv("MASTER_PASS")
    salt = os.getenv("SALT")
    
    if not master:
        raise ValueError("MASTER_PASS environment variable not set")
    if not salt:
        raise ValueError("SALT environment variable not set")
    
    # Handle salt that might be stored as string representation of bytes
    if isinstance(salt, str):
        if salt.startswith("b'") and salt.endswith("'"):
            try:
                salt = eval(salt)
            except:
                salt = salt.encode()
        else:
            salt = salt.encode()
    
    return PBKDF2(master, salt, dkLen=32)


def encrypt(user: UserAccount) -> UserAccount:
    """Encrypt user credentials.
    Args:
        user: UserAccount with plaintext email and password
        
    Returns:
        UserAccount with encrypted email/password and the IV used
        
    Raises:
        ValueError: If email or password is missing
    """
    if not user.email or not user.password:
        raise ValueError("Email and password required for encryption")
    
    key = _get_key()
    
    # Create NEW cipher with random IV for each encryption
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    
    # Convert to bytes (removing unnecessary base64 step from original)
    email_bytes = user.email.encode() if isinstance(user.email, str) else user.email
    password_bytes = user.password.encode() if isinstance(user.password, str) else user.password
    
    # Encrypt
    email_enc = cipher.encrypt(pad(email_bytes, AES.block_size))
    password_enc = cipher.encrypt(pad(password_bytes, AES.block_size))
    
    return UserAccount(
        name=user.name,
        email=email_enc,
        password=password_enc,
        iv=iv
    )


def decrypt(user: UserAccount) -> UserAccount:
    """Decrypt user credentials using stored IV.
    
    Args:
        user: UserAccount with encrypted email/password and IV
        
    Returns:
        UserAccount with decrypted email/password
        
    Raises:
        ValueError: If IV or encrypted data is missing
    """
    if not user.iv:
        raise ValueError("IV required for decryption")
    if not user.email or not user.password:
        raise ValueError("Encrypted data required for decryption")
    
    key = _get_key()
    
    # Create cipher with the stored IV from encryption
    cipher = AES.new(key, AES.MODE_CBC, user.iv)
    
    # Decrypt
    email_bytes = unpad(cipher.decrypt(user.email), AES.block_size)
    password_bytes = unpad(cipher.decrypt(user.password), AES.block_size)
    
    return UserAccount(
        name=user.name,
        email=email_bytes.decode(),
        password=password_bytes.decode(),
        iv=user.iv
    )
