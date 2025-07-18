"""
Production-ready encryption/decryption plugin using cryptography library.
Uses AES-GCM for authenticated encryption providing both confidentiality and integrity.
"""

import os
import logging
from typing import Optional, Union
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag

# Configure logging
logger = logging.getLogger(__name__)

class EncryptionError(Exception):
    """Custom exception for encryption/decryption errors."""
    pass

class SecureEncryption:
    """Production-ready encryption using AES-GCM."""
    
    # Constants for encryption
    KEY_SIZE = 32  # 256-bit key
    NONCE_SIZE = 12  # 96-bit nonce for GCM
    SALT_SIZE = 16  # 128-bit salt for key derivation
    
    def __init__(self):
        self.cipher = AESGCM
    
    def _derive_key(self, password: Union[str, bytes], salt: bytes) -> bytes:
        """
        Derive encryption key from password using PBKDF2.
        
        Args:
            password: Password string or bytes
            salt: Salt bytes for key derivation
            
        Returns:
            bytes: Derived encryption key
        """
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=salt,
            iterations=100000,  # OWASP recommended minimum
        )
        return kdf.derive(password)
    
    def encrypt_file(self, input_path: str, output_path: str, password: Union[str, bytes]) -> bool:
        """
        Encrypt a file using AES-GCM.
        
        Args:
            input_path: Path to input file
            output_path: Path to output encrypted file
            password: Password for encryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                raise EncryptionError(f"Input file not found: {input_path}")
            
            # Generate random salt and nonce
            salt = os.urandom(self.SALT_SIZE)
            nonce = os.urandom(self.NONCE_SIZE)
            
            # Derive key from password
            key = self._derive_key(password, salt)
            
            # Create cipher
            cipher = self.cipher(key)
            
            # Read input file
            with open(input_path, 'rb') as f:
                plaintext = f.read()
            
            # Encrypt the data
            ciphertext = cipher.encrypt(nonce, plaintext, None)
            
            # Write encrypted file: salt + nonce + ciphertext
            with open(output_path, 'wb') as f:
                f.write(salt)
                f.write(nonce)
                f.write(ciphertext)
            
            logger.info(f"File encrypted successfully: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            # Clean up partial output file
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            return False
    
    def decrypt_file(self, input_path: str, output_path: str, password: Union[str, bytes]) -> bool:
        """
        Decrypt a file using AES-GCM.
        
        Args:
            input_path: Path to encrypted file
            output_path: Path to output decrypted file
            password: Password for decryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                raise EncryptionError(f"Input file not found: {input_path}")
            
            # Read encrypted file
            with open(input_path, 'rb') as f:
                # Read salt, nonce, and ciphertext
                salt = f.read(self.SALT_SIZE)
                nonce = f.read(self.NONCE_SIZE)
                ciphertext = f.read()
            
            if len(salt) != self.SALT_SIZE or len(nonce) != self.NONCE_SIZE:
                raise EncryptionError("Invalid encrypted file format")
            
            # Derive key from password
            key = self._derive_key(password, salt)
            
            # Create cipher
            cipher = self.cipher(key)
            
            # Decrypt the data
            try:
                plaintext = cipher.decrypt(nonce, ciphertext, None)
            except InvalidTag:
                raise EncryptionError("Invalid password or corrupted file")
            
            # Write decrypted file
            with open(output_path, 'wb') as f:
                f.write(plaintext)
            
            logger.info(f"File decrypted successfully: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            # Clean up partial output file
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            return False
    
    def encrypt_data(self, data: bytes, password: Union[str, bytes]) -> Optional[bytes]:
        """
        Encrypt data in memory.
        
        Args:
            data: Data to encrypt
            password: Password for encryption
            
        Returns:
            bytes: Encrypted data (salt + nonce + ciphertext) or None if failed
        """
        try:
            # Generate random salt and nonce
            salt = os.urandom(self.SALT_SIZE)
            nonce = os.urandom(self.NONCE_SIZE)
            
            # Derive key from password
            key = self._derive_key(password, salt)
            
            # Create cipher and encrypt
            cipher = self.cipher(key)
            ciphertext = cipher.encrypt(nonce, data, None)
            
            # Return salt + nonce + ciphertext
            return salt + nonce + ciphertext
            
        except Exception as e:
            logger.error(f"Data encryption failed: {e}")
            return None
    
    def decrypt_data(self, encrypted_data: bytes, password: Union[str, bytes]) -> Optional[bytes]:
        """
        Decrypt data in memory.
        
        Args:
            encrypted_data: Encrypted data (salt + nonce + ciphertext)
            password: Password for decryption
            
        Returns:
            bytes: Decrypted data or None if failed
        """
        try:
            if len(encrypted_data) < self.SALT_SIZE + self.NONCE_SIZE:
                raise EncryptionError("Invalid encrypted data format")
            
            # Extract salt, nonce, and ciphertext
            salt = encrypted_data[:self.SALT_SIZE]
            nonce = encrypted_data[self.SALT_SIZE:self.SALT_SIZE + self.NONCE_SIZE]
            ciphertext = encrypted_data[self.SALT_SIZE + self.NONCE_SIZE:]
            
            # Derive key from password
            key = self._derive_key(password, salt)
            
            # Create cipher and decrypt
            cipher = self.cipher(key)
            try:
                plaintext = cipher.decrypt(nonce, ciphertext, None)
                return plaintext
            except InvalidTag:
                raise EncryptionError("Invalid password or corrupted data")
            
        except Exception as e:
            logger.error(f"Data decryption failed: {e}")
            return None

# Global encryption instance
_encryptor = SecureEncryption()

def encrypt_file(input_path: str, output_path: str, password: Union[str, bytes]) -> bool:
    """
    Convenience function to encrypt a file.
    
    Args:
        input_path: Path to input file
        output_path: Path to output encrypted file
        password: Password for encryption
        
    Returns:
        bool: True if successful, False otherwise
    """
    return _encryptor.encrypt_file(input_path, output_path, password)

def decrypt_file(input_path: str, output_path: str, password: Union[str, bytes]) -> bool:
    """
    Convenience function to decrypt a file.
    
    Args:
        input_path: Path to encrypted file
        output_path: Path to output decrypted file
        password: Password for decryption
        
    Returns:
        bool: True if successful, False otherwise
    """
    return _encryptor.decrypt_file(input_path, output_path, password)

def encrypt_data(data: bytes, password: Union[str, bytes]) -> Optional[bytes]:
    """
    Convenience function to encrypt data in memory.
    
    Args:
        data: Data to encrypt
        password: Password for encryption
        
    Returns:
        bytes: Encrypted data or None if failed
    """
    return _encryptor.encrypt_data(data, password)

def decrypt_data(encrypted_data: bytes, password: Union[str, bytes]) -> Optional[bytes]:
    """
    Convenience function to decrypt data in memory.
    
    Args:
        encrypted_data: Encrypted data
        password: Password for decryption
        
    Returns:
        bytes: Decrypted data or None if failed
    """
    return _encryptor.decrypt_data(encrypted_data, password)