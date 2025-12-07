# pyPasswordManager

## Description

Password manager written in python that encrypts and stores account credentials using AES
encryption and SQLite for local storage.

### Features

* Encryption of email and password data using pycryptodome library
* SQLite database for storing account names, usernames and encrypted passwords
* Create, view, search and delete entries from the command line

## Usage

Add an entry to the database:\
`python3 pypass.py -f add -n Google -u test@gmail.com -p password123`

Query by account name:\
`python3 pypass.py -f view -n Google`

Query by email:\
`python3 pypass.py -f search -u test@gmail.com`

Delete specific entry:\
`python3 pypass.py -f delete -n Facebook -u test@gmail.com -p password123`

## To-Do
* Add master password check
