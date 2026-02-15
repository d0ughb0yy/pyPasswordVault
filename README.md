# pyPasswordVault

A command-line password manager for learning secure Python development and cryptographic implementation.

## What This Is

This project implements a local password manager using AES-256-CBC encryption. It focuses on secure coding practices and demonstrates how to properly handle sensitive data in Python. The code includes detailed comments explaining security decisions and vulnerabilities that were fixed during development.

## Features

- AES-256-CBC encryption for stored credentials
- Unique initialization vector (IV) generated for each entry
- Constant-time password comparison to prevent timing attacks
- Exact case-sensitive matching for all credentials (no lowercase transformations)
- SQLite database for local storage
- Simple command-line interface

## Installation

```bash
git clone https://github.com/yourusername/pyPasswordVault.git
cd pyPasswordVault
pip install -r requirements.txt
```

## Setup

Create a .env file in the project root:

```
MASTER_PASS=your_strong_master_password_here
SALT=your_random_32_byte_salt_here
```

To generate a salt:

```python
import os
print(os.urandom(32))
```

Keep this file private and never commit it to version control.

## Usage

Add a new password:
```bash
python pypass.py -f add -n GitHub -u myemail@gmail.com -p SuperSecret123!
```

View stored passwords for an account:
```bash
python pypass.py -f view -n GitHub
```

Search by email address:
```bash
python pypass.py -f search -u myemail@gmail.com
```

Delete an entry:
```bash
python pypass.py -f delete -n GitHub -u myemail@gmail.com -p SuperSecret123!
```

## Security Fixes

**Timing Attack Vulnerability**: Initial code used standard string comparison (==) for password verification. This leaks timing information that could allow an attacker to guess the password character by character. Fixed by using hmac.compare_digest() for constant-time comparison.

**IV Reuse**: Initial code created one cipher at the module level and reused it for all encryptions. This meant the same IV was used every time, which breaks AES-CBC security. Fixed by generating a new cipher with a random IV for each encryption operation.

**Case-Insensitive Matching**: This is wrong for a password manager - Secret123 and secret123 should be different passwords. Fixed by using exact string matching.

**Database Connection Leaks**: The connection close() calls were inside loops or missing entirely. Fixed by using Python context managers to ensure connections always get closed.

## Learning Resources

This project helped me to learn:

- How timing attacks work and how to prevent them
- Proper IV management in AES encryption
- Why exact matching matters for credential storage
- Secure database connection handling

## Important Reminders

1. Never commit your .env file - it contains your master password
2. Back up your data/accounts.db file regularly
3. Use a strong master password - it protects everything
4. Review the code to understand how the security works

