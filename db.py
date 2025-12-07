import sqlite3
import os

from crypto import decrypt, UserAccount


def check_for_db():
    """Checks for presence of accounts.db file in the working directory,
    if the file is not present it creates it and initializes columns"""
    if os.path.exists("accounts.db"):
        pass
    else:
        conn = sqlite3.connect("accounts.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE accounts (
                    name text,
                    email text,
                    password text,
                    iv text
                    )"""
        )
        conn.commit()


def insert_into_db(enc_user_object):
    """Checks if the local storage exists if not it creates it,
    it takes the encrypted UserAccount object and stores it in a db file"""
    # Create an accounts.db file if it's not created and initialize the accounts table inside
    check_for_db()
    connection = sqlite3.connect("accounts.db")
    db_con = connection.cursor()
    db_con.execute(
        "INSERT INTO accounts VALUES(?, ?, ?, ?)",
        (
            enc_user_object.name,
            enc_user_object.email,
            enc_user_object.password,
            enc_user_object.iv,
        ),
    )
    connection.commit()
    connection.close()


def view_entry(acc_name_input):
    """Checks for the name of the service from acc_name_input in the local storage,
    if it exists it decrypts the content and prints out the user account info"""
    if os.path.exists("accounts.db"):
        # Connect
        view_conn = sqlite3.connect("accounts.db")
        vc = view_conn.cursor()

        # Execute SELECT statement
        vc.execute("SELECT * FROM accounts WHERE name=?", (acc_name_input,))
        view_conn.commit()

        # Store everything in a db_dump variable
        db_dump = vc.fetchall()
        # Iterate through the list of tuples
        for user_info in db_dump:
            user_tuple = user_info
            # Extracts the values from every tuple and stores them into a UserAccount class
            encrypted_user = UserAccount(
                user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3]
            )
            decrypted_user = decrypt(encrypted_user)
            view_conn.close()
            print(
                f"""Account: {decrypted_user.name}\nEmail: {decrypted_user.email}\nPassword: {decrypted_user.password}"""
            )
            print("=========================")
    else:
        print("Accounts file is missing.")
        print("Add an entry with --add first")


def search_by_email(email):
    if os.path.exists("accounts.db"):
        # Connect
        view_conn = sqlite3.connect("accounts.db")
        vc = view_conn.cursor()

        # Fetch all from accounts.db
        vc.execute("SELECT * FROM accounts")
        view_conn.commit()

        db_dump = vc.fetchall()
        for creds in db_dump:
            encrypted_creds = UserAccount(creds[0], creds[1], creds[2], creds[3])
            decrypted_creds = decrypt(encrypted_creds)

            if decrypted_creds.email.lower() == email.lower():
                print(
                    f"Account: {decrypted_creds.name}\nEmail: {decrypted_creds.email}\nPassword: {decrypted_creds.password}"
                )
                found = True
                break

        else:
            print(f"No account found for email: {email}")

def delete_entry(email, password, accName):
    if os.path.exists("accounts.db"):
        # Connect
        view_conn = sqlite3.connect("accounts.db")
        vc = view_conn.cursor()

        # Fetch all encrypted accounts from accounts.db
        vc.execute("SELECT * FROM accounts")
        view_conn.commit()

        db_dump = vc.fetchall()
        for creds in db_dump:
            encrypted_creds = UserAccount(creds[0], creds[1], creds[2], creds[3])
            decrypted_creds = decrypt(encrypted_creds)

            if decrypted_creds.email.lower() == email.lower() and decrypted_creds.password.lower() == password.lower() and decrypted_creds.name == accName:
                vc.execute("DELETE FROM accounts WHERE email=? AND password=?", (encrypted_creds.email, encrypted_creds.password))
                view_conn.commit()