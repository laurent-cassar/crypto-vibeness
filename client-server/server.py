#!/usr/bin/env python3
"""
Simple Server for Client-Server Communication
Listens for incoming messages from clients and displays them
"""

import socketserver
import socket
import threading

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024


class ServerHandler(socketserver.StreamRequestHandler):
    """Handler for incoming client connections"""
    
    def handle(self):
        """Handle incoming connection from client"""
        client_address = self.client_address[0]
        print(f"[INFO] Client connected: {client_address}")
        
        try:
            while True:
                data = self.rfile.readline().decode('utf-8').strip()
                if not data:
                    break
                print(f"[{client_address}]: {data}")
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
