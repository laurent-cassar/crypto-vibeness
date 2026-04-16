#!/usr/bin/env python3
"""
Simple Client for Client-Server Communication
Sends messages to the server
"""

import socket
import sys

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024


def connect_and_send():
    """Connect to server and send messages"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"[INFO] Connected to server at {HOST}:{PORT}")
        print("[INFO] Type your message and press Enter")
        print("[INFO] Use '/disconnect' to quit gracefully\n")
        
        while True:
            try:
                message = input("You: ")
                
                if not message.strip():
                    continue
                
                if message.strip().lower() == '/disconnect':
                    print("[INFO] Disconnecting...")
                    break
                
                sock.sendall((message + '\n').encode('utf-8'))
            except KeyboardInterrupt:
                print("\n[INFO] Disconnecting...")
                break
            except Exception as e:
                print(f"[ERROR] Failed to send message: {e}")
                break
    
    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {HOST}:{PORT}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Connection error: {e}")
        sys.exit(1)
    finally:
        sock.close()
        print("[INFO] Disconnected from server")


if __name__ == "__main__":
    connect_and_send()
