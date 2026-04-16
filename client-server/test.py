#!/usr/bin/env python3
"""
Test script for Client-Server communication
"""

import socket
import time
import subprocess
import sys
import os

HOST = 'localhost'
PORT = 5000


def send_test_message(message):
    """Send a test message to the server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall((message + '\n').encode('utf-8'))
        sock.close()
        print(f"✓ Message sent: {message}")
    except Exception as e:
        print(f"✗ Failed to send message: {e}")
        return False
    return True


def test_communication():
    """Test the client-server communication"""
    print("[TEST] Starting Client-Server Communication Test\n")
    
    test_messages = [
        "Hello Server!",
        "This is a test message",
        "Client-Server communication is working!"
    ]
    
    time.sleep(1)  # Wait for server to be ready
    
    print("[INFO] Sending test messages to server...\n")
    for msg in test_messages:
        if send_test_message(msg):
            time.sleep(0.5)
    
    print("\n[INFO] Check the server output above for received messages")
    print("[TEST] Test completed!\n")


if __name__ == "__main__":
    test_communication()
