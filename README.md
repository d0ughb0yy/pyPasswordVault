# pyPasswordManager

## Description

Password manager written in Python that encrypts and stores account credentials using AES
encryption and SQLite for local storage.

### Features

* Encryption of email and password data using pycryptodome library
* SQLite database for storing account names, usernames and encrypted passwords
* Create, view, search and delete entries from the command line

## About

You MUST add a .env file to the directory with the MASTER_PASS and SALT entries.\
*Example:*
```
MASTER_PASS=4q7$oOJlH80!
SALT=b'\x19\xb6\x9ec0Xu\x9fghz\x08\xc4\xc4$@]\xd2B\xc9|wk\x1a\xb1\xc9\xbb"1\x1f\x8a\xd3'
```

**Install requirements**:\
`pip install -r requirements.txt`

### Usage

Add an entry to the database:\
`python3 pypass.py -f add -n Google -u test@gmail.com -p password123`

Query by account name:\
`python3 pypass.py -f view -n Google`

Query by email:\
`python3 pypass.py -f search -u test@gmail.com`

Delete specific entry:\
`python3 pypass.py -f delete -n Facebook -u test@gmail.com -p password123`
