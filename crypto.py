import os
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import base64

# Load Environmental Variables
load_dotenv()

MASTER = os.getenv("MASTER_PASS")  # Get the main encryption password
SALT = os.getenv("SALT")  # Get the salt
key = PBKDF2(MASTER, SALT, dkLen=32)
mode = AES.MODE_CBC


# Create a class that will act as a template for a user account
class UserAccount:
    def __init__(self, acc_name, acc_email, acc_pass, iv):
        self.name = acc_name
        self.email = acc_email
        self.password = acc_pass
        self.iv = iv


cipher = AES.new(key, mode)
IV = cipher.iv


def encrypt(user_object):
    """Takes a UserAccount class and encodes the email and password
    and returns a new UserAccount class with the encrypted email and password values"""

    # Take the plain-text info and first base64 encode it and turn into bytes
    user_email_b64 = base64.b64encode(user_object.email.encode())
    user_password_b64 = base64.b64encode(user_object.password.encode())

    # Encrypt the base64 encoded email and password
    user_email_enc = cipher.encrypt(pad(user_email_b64, AES.block_size))
    user_password_enc = cipher.encrypt(pad(user_password_b64, AES.block_size))
    print(f"Encrypted email: {user_email_enc}, Encrypted Pass: {user_password_enc}")

    # Populates a new UserAccount object with encrypted values
    return UserAccount(user_object.name, user_email_enc, user_password_enc, iv=IV)


def decrypt(enc_user_object):
    """Takes an UserAccount object populated with encrypted email and password,
    It then decrypts them and returns in another UserAccount object"""

    # Declare a new cipher for decrypting with the iv from the database
    cipher_dec = AES.new(key, mode, enc_user_object.iv)

    # Unpads and decrypts into base64 encoding
    user_email_b64 = unpad(cipher_dec.decrypt(enc_user_object.email), AES.block_size)
    user_password_b64 = unpad(
        cipher_dec.decrypt(enc_user_object.password), AES.block_size
    )

    # Decode from base64 and decode from bytes
    user_em = base64.b64decode(user_email_b64).decode()
    user_pass = base64.b64decode(user_password_b64).decode()

    # Return a UserAccount object populated with decrypted account info
    return UserAccount(enc_user_object.name, user_em, user_pass, enc_user_object.iv)
