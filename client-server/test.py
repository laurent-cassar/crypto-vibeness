#!/usr/bin/env python3
"""
Test script for Encrypted Client-Server communication
"""

import socket
import time
from data_encryption import EncryptionManager
from shared_key import load_or_create_key

HOST = 'localhost'
PORT = 5000


def send_test_message(message, encryption_mgr):
    """Send an encrypted test message to the server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        # Encrypt the message
        encrypted_message = encryption_mgr.encrypt_message(message)
        sock.sendall(encrypted_message + b'\n')
        sock.close()
        print(f"✓ Message sent: {message}")
    except Exception as e:
        print(f"✗ Failed to send message: {e}")
        return False
    return True


def test_communication():
    """Test the encrypted client-server communication"""
    print("[TEST] Starting Encrypted Client-Server Communication Test\n")
    
    test_messages = [
        "Hello Server!",
        "This is an encrypted test message",
        "End-to-end encryption is working!"
    ]
    
    # Load shared encryption key
    shared_key = load_or_create_key()
    encryption_mgr = EncryptionManager(shared_key)
    
    time.sleep(1)  # Wait for server to be ready
    
    print("[INFO] Sending encrypted test messages to server...\n")
    for msg in test_messages:
        if send_test_message(msg, encryption_mgr):
            time.sleep(0.5)
    
    print("\n[INFO] Check the server output above for received messages")
    print("[TEST] Test completed!\n")


if __name__ == "__main__":
    test_communication()
