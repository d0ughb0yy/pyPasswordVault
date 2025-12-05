import argparse

from db import view_entry, insert_into_db, search_by_email
from crypto import UserAccount, encrypt, IV

parser = argparse.ArgumentParser(
    prog="pyPass Password Manager",
    usage="python3 pypass.py [-f (add | view) -n Google -u john@gmail.com -p Password123]",
    description="Password manager that stores your encrypted data in a sqlite local file",
)
parser.add_argument(
    "-f",
    "--function",
    help="Function to perform add or view",
    required=True,
    type=str,
    choices=["add", "view", "search"],
)
parser.add_argument("-n", "--name", help="Name of the account", type=str)
parser.add_argument("-u", "--username", help="Username used in the account", type=str)
parser.add_argument("-p", "--password", help="Password for the account", type=str)
args = parser.parse_args()

# Get account information from the command line arguments
acc_name_input = args.name
acc_username_input = args.username
acc_pass_input = args.password

# Initiate a UserAccount class with arguments
user = UserAccount(acc_name_input, acc_username_input, acc_pass_input, iv=IV)

if __name__ == "__main__":
    # Application logic for --function argument
    if args.function == "view":
        try:
            user = view_entry(acc_name_input)
        except Exception as e:
            print(f"{e}")
    elif args.function == "add":
        encrypted_user = encrypt(user)
        insert_into_db(encrypted_user)
    elif args.function == "search" and acc_name_input:
        search_by_email(acc_username_input, acc_name_input)
