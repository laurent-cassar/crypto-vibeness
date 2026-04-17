#!/usr/bin/env python3
"""
Data Encryption Module for Client-Server Communication
Provides symmetric encryption (AES) for secure message exchange
"""

from cryptography.fernet import Fernet
#from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import *
import os
import base64

class EncryptionManager:
    """Manages encryption and decryption of messages"""
    
    def __init__(self, shared_key=None):
        """
        Initialize the encryption manager
        
        Args:
            shared_key: Pre-shared symmetric key (bytes). If None, generates a new one.
        """
        if shared_key:
            self.shared_key = shared_key
        else:
            self.shared_key = Fernet.generate_key()
        
        self.cipher = Fernet(self.shared_key)
    
    @staticmethod
    def generate_key():
        """Generate a new random encryption key"""
        return Fernet.generate_key()
    
    @staticmethod
    def derive_key_from_password(password, salt=None):
        """
        Derive an encryption key from a password using PBKDF2
        
        Args:
            password: The password string
            salt: Optional salt (bytes). If None, generates a new one.
            
        Returns:
            Tuple of (key, salt) both as bytes
        """
        if salt is None:
            salt = os.urandom(16)
        
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        derived = kdf.derive(password)
        key = base64.urlsafe_b64encode(derived)
        
        return key, salt
    
    def encrypt_message(self, message):
        """
        Encrypt a message
        
        Args:
            message: String message to encrypt
            
        Returns:
            Encrypted message as bytes
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        encrypted = self.cipher.encrypt(message)
        return encrypted
    
    def decrypt_message(self, encrypted_message):
        """
        Decrypt a message
        
        Args:
            encrypted_message: Encrypted message as bytes
            
        Returns:
            Decrypted message as string
        """
        decrypted = self.cipher.decrypt(encrypted_message)
        return decrypted.decode('utf-8')
    
    def get_key(self):
        """Get the current shared key"""
        return self.shared_key
