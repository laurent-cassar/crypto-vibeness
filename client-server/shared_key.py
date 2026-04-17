#!/usr/bin/env python3
"""
Shared key management for encrypted client-server communication
"""

import os
from data_encryption import EncryptionManager

KEY_FILE = "shared_key.txt"


def load_or_create_key():
    """Load the shared key from file, or create and save a new one"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            key = f.read().strip().encode('utf-8')
        return key
    else:
        # Generate and save a new key
        key = EncryptionManager.generate_key()
        with open(KEY_FILE, 'w') as f:
            f.write(key.decode('utf-8'))
        print(f"[INFO] Generated new encryption key and saved to {KEY_FILE}")
        return key
