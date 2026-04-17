#!/usr/bin/env python3
"""
Encrypted Server for Client-Server Communication
Listens for incoming encrypted messages from clients and displays them
"""

import socketserver
import socket
import threading
from data_encryption import EncryptionManager
from shared_key import load_or_create_key

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

# Load or create shared encryption key
SHARED_KEY = load_or_create_key()


class ServerHandler(socketserver.StreamRequestHandler):
    """Handler for incoming client connections"""
    
    def handle(self):
        """Handle incoming connection from client"""
        client_address = self.client_address[0]
        print(f"[INFO] Client connected: {client_address}")
        
        # Initialize encryption for this client
        encryption_mgr = EncryptionManager(SHARED_KEY)
        
        try:
            while True:
                # Receive encrypted data
                encrypted_line = self.rfile.readline()
                if not encrypted_line:
                    break
                
                try:
                    # Decrypt the message
                    decrypted_message = encryption_mgr.decrypt_message(encrypted_line.strip())
                    print(f"[{client_address}]: {decrypted_message}")
                except Exception as e:
                    print(f"[ERROR] Failed to decrypt message from {client_address}: {e}")
        except ConnectionResetError:
            print(f"[INFO] Client {client_address} disconnected")
        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
        finally:
            print(f"[INFO] Closing connection with {client_address}")


class ServerHandler(socketserver.StreamRequestHandler):
    """Handler for incoming client connections"""
    
    def handle(self):
        """Handle incoming connection from client"""
        client_address = self.client_address[0]
        print(f"[INFO] Client connected: {client_address}")
        
        # Initialize encryption for this client
        encryption_mgr = EncryptionManager(SHARED_KEY)
        
        try:
            while True:
                # Receive encrypted data
                encrypted_line = self.rfile.readline()
                if not encrypted_line:
                    break
                
                try:
                    # Decrypt the message
                    decrypted_message = encryption_mgr.decrypt_message(encrypted_line.strip())
                    print(f"[{client_address}]: {decrypted_message}")
                except Exception as e:
                    print(f"[ERROR] Failed to decrypt message from {client_address}: {e}")
        except ConnectionResetError:
            print(f"[INFO] Client {client_address} disconnected")
        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
        finally:
            print(f"[INFO] Closing connection with {client_address}")


def start_server():
    """Start the server"""
    server = socketserver.ThreadingTCPServer((HOST, PORT), ServerHandler)
    print(f"[INFO] Server started on {HOST}:{PORT}")
    print(f"[INFO] Using shared encryption key from shared_key.txt")
    print("[INFO] Waiting for incoming connections...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down...")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    start_server()
