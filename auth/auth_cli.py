#!/usr/bin/env python3
"""
Simple CLI authentication.
- Prompts for username and password (password not echoed).
- Password policy: min 8 chars, at least 1 uppercase, 1 digit, 1 special char.
- On successful connection, stores username and SHA-256(password) in ../userbase.txt if username not present.
- If username exists, verifies the password matches the stored hash.

Usage: python3 auth/auth_cli.py
"""

import getpass
import hashlib
import os
import re
import sys

# Path to userbase.txt in repository root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
USERBASE_PATH = os.path.join(BASE_DIR, 'userbase.txt')

PW_POLICY_REGEX = re.compile(r'^(?=.{8,})(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$')


def hash_password(password: str) -> str:
    """Return hex SHA-256 of the password."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def load_userbase(path: str) -> dict:
    """Return dict username -> password_hash"""
    users = {}
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                username, pw_hash = line.split(':', 1)
                users[username] = pw_hash
    return users


def save_userbase_entry(path: str, username: str, pw_hash: str) -> None:
    """Append a new user entry to the userbase file."""
    # Ensure directory exists
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{username}:{pw_hash}\n")


def valid_password(password: str) -> bool:
    return bool(PW_POLICY_REGEX.match(password))


def getpass_masked(prompt='Password: '):
    """Read a password from stdin, displaying '*' for each character (Unix only)."""
    import sys
    import termios
    import tty

    sys.stdout.write(prompt)
    sys.stdout.flush()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    password_chars = []
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ('\r', '\n'):
                break
            if ch == '\x03':
                # Ctrl-C
                raise KeyboardInterrupt
            if ch == '\x7f':
                # Backspace/delete
                if password_chars:
                    password_chars.pop()
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                continue
            password_chars.append(ch)
            sys.stdout.write('*')
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    sys.stdout.write('\n')
    return ''.join(password_chars)


def prompt_credentials():
    username = input('Username: ').strip()
    if not username:
        print('Username cannot be empty.')
        sys.exit(1)
    password = getpass_masked('Password: ')
    return username, password


def main():
    print('--- Simple Auth CLI ---')
    username, password = prompt_credentials()

    if not valid_password(password):
        print('Password does not meet policy: min 8 chars, at least 1 uppercase, 1 digit and 1 special character.')
        sys.exit(1)

    users = load_userbase(USERBASE_PATH)
    pw_hash = hash_password(password)

    if username in users:
        if users[username] == pw_hash:
            print(f'Welcome back, {username}! Authentication successful.')
        else:
            print('Authentication failed: password does not match.')
            sys.exit(1)
    else:
        save_userbase_entry(USERBASE_PATH, username, pw_hash)
        print(f'User {username} registered and authenticated. Entry stored in userbase.txt (password stored as SHA-256 hash).')


if __name__ == '__main__':
    main()
