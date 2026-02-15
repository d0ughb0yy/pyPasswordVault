## FIXES

Since I'm not an expert on cryptography and cybersecurity, I decided to use this project as a learning point and
document my vulnerabilities and how I fixed them.

### Security Fixes

#### Critical

- **Timing Attack Prevention**: Replaced `!=` password comparison with `hmac.compare_digest()` in authentication system
  - Original code used standard comparison which leaks timing information
  - New implementation uses constant-time comparison to prevent timing attacks
  - File: `src/utils.py`

- **IV Reuse Vulnerability**: Fixed catastrophic IV reuse in AES encryption
  - Original code created single cipher at module level, reused for all encryptions
  - New code generates new cipher with random IV for each encryption operation
  - This prevented identical plaintexts from producing identical ciphertexts
  - File: `src/crypto.py`

- **Case-Insensitive Password Matching**: Removed `.lower()` from password comparisons
  - Original code treated "Secret123" and "secret123" as identical
  - Reduced password entropy by 26x (62^8 to 36^8)
  - All password comparisons now use exact case-sensitive matching
  - File: `src/db.py`

- **Case-Insensitive Email Matching**: Removed `.lower()` from email comparisons
  - Password manager standards require exact matching for all credentials
  - Prevents accidental matching of different accounts
  - Files: `src/db.py` (search_by_email, delete_entry)

#### High

- **Database Connection Leaks**: Fixed connection management issues
  - Original code had `conn.close()` inside loop (closed after first iteration)
  - delete_entry was missing connection close entirely
  - New implementation uses context managers (`@contextmanager`) for guaranteed cleanup
  - File: `src/db.py`