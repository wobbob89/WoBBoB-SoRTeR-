"""
Test suite for the encryption plugin.
"""

import os
import tempfile
import pytest
from plugins.encryption import (
    encrypt_file, decrypt_file, encrypt_data, decrypt_data,
    SecureEncryption, EncryptionError
)


class TestSecureEncryption:
    """Test the SecureEncryption class."""
    
    def test_key_derivation(self):
        """Test key derivation from password."""
        encryptor = SecureEncryption()
        salt = b'0' * 16  # Fixed salt for testing
        
        key1 = encryptor._derive_key("password", salt)
        key2 = encryptor._derive_key("password", salt)
        key3 = encryptor._derive_key("different", salt)
        
        # Same password should produce same key
        assert key1 == key2
        # Different password should produce different key
        assert key1 != key3
        # Key should be correct length
        assert len(key1) == 32  # 256 bits
    
    def test_file_encryption_decryption(self):
        """Test file encryption and decryption."""
        encryptor = SecureEncryption()
        
        # Create test data
        test_data = b"Hello, World! This is a test file."
        password = "test_password"
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(test_data)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
            encrypted_path = encrypted_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
            decrypted_path = decrypted_file.name
        
        try:
            # Test encryption
            success = encryptor.encrypt_file(input_path, encrypted_path, password)
            assert success is True
            assert os.path.exists(encrypted_path)
            
            # Encrypted file should be different from original
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            assert encrypted_data != test_data
            
            # Test decryption
            success = encryptor.decrypt_file(encrypted_path, decrypted_path, password)
            assert success is True
            assert os.path.exists(decrypted_path)
            
            # Decrypted data should match original
            with open(decrypted_path, 'rb') as f:
                decrypted_data = f.read()
            assert decrypted_data == test_data
            
        finally:
            # Clean up
            for path in [input_path, encrypted_path, decrypted_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_file_encryption_wrong_password(self):
        """Test decryption with wrong password."""
        encryptor = SecureEncryption()
        
        test_data = b"Secret data"
        password = "correct_password"
        wrong_password = "wrong_password"
        
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(test_data)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
            encrypted_path = encrypted_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
            decrypted_path = decrypted_file.name
        
        try:
            # Encrypt with correct password
            success = encryptor.encrypt_file(input_path, encrypted_path, password)
            assert success is True
            
            # Try to decrypt with wrong password
            success = encryptor.decrypt_file(encrypted_path, decrypted_path, wrong_password)
            assert success is False
            
        finally:
            for path in [input_path, encrypted_path, decrypted_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_data_encryption_decryption(self):
        """Test in-memory data encryption and decryption."""
        encryptor = SecureEncryption()
        
        test_data = b"This is sensitive data that needs encryption"
        password = "secure_password"
        
        # Encrypt data
        encrypted_data = encryptor.encrypt_data(test_data, password)
        assert encrypted_data is not None
        assert encrypted_data != test_data
        
        # Decrypt data
        decrypted_data = encryptor.decrypt_data(encrypted_data, password)
        assert decrypted_data is not None
        assert decrypted_data == test_data
    
    def test_data_encryption_wrong_password(self):
        """Test in-memory decryption with wrong password."""
        encryptor = SecureEncryption()
        
        test_data = b"Secret information"
        password = "correct_password"
        wrong_password = "wrong_password"
        
        # Encrypt with correct password
        encrypted_data = encryptor.encrypt_data(test_data, password)
        assert encrypted_data is not None
        
        # Try to decrypt with wrong password
        decrypted_data = encryptor.decrypt_data(encrypted_data, wrong_password)
        assert decrypted_data is None
    
    def test_nonexistent_file_encryption(self):
        """Test encryption of non-existent file."""
        encryptor = SecureEncryption()
        
        success = encryptor.encrypt_file("/nonexistent/file.txt", "/tmp/output.enc", "password")
        assert success is False
    
    def test_nonexistent_file_decryption(self):
        """Test decryption of non-existent file."""
        encryptor = SecureEncryption()
        
        success = encryptor.decrypt_file("/nonexistent/file.enc", "/tmp/output.txt", "password")
        assert success is False
    
    def test_invalid_encrypted_data(self):
        """Test decryption of invalid encrypted data."""
        encryptor = SecureEncryption()
        
        # Test with too short data
        result = encryptor.decrypt_data(b"short", "password")
        assert result is None
        
        # Test with corrupt data
        corrupt_data = b"x" * 100  # Not valid encrypted data
        result = encryptor.decrypt_data(corrupt_data, "password")
        assert result is None


class TestModuleFunctions:
    """Test the module-level convenience functions."""
    
    def test_encrypt_decrypt_file_functions(self):
        """Test module-level encrypt_file and decrypt_file functions."""
        test_data = b"Testing module functions"
        password = "module_test_password"
        
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(test_data)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as encrypted_file:
            encrypted_path = encrypted_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as decrypted_file:
            decrypted_path = decrypted_file.name
        
        try:
            # Test module-level functions
            success = encrypt_file(input_path, encrypted_path, password)
            assert success is True
            
            success = decrypt_file(encrypted_path, decrypted_path, password)
            assert success is True
            
            # Verify data
            with open(decrypted_path, 'rb') as f:
                decrypted_data = f.read()
            assert decrypted_data == test_data
            
        finally:
            for path in [input_path, encrypted_path, decrypted_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_encrypt_decrypt_data_functions(self):
        """Test module-level encrypt_data and decrypt_data functions."""
        test_data = b"Module data encryption test"
        password = "data_test_password"
        
        # Test module-level functions
        encrypted_data = encrypt_data(test_data, password)
        assert encrypted_data is not None
        
        decrypted_data = decrypt_data(encrypted_data, password)
        assert decrypted_data == test_data
    
    def test_password_types(self):
        """Test that both string and bytes passwords work."""
        test_data = b"Testing password types"
        string_password = "string_password"
        bytes_password = b"bytes_password"
        
        # Test string password
        encrypted1 = encrypt_data(test_data, string_password)
        decrypted1 = decrypt_data(encrypted1, string_password)
        assert decrypted1 == test_data
        
        # Test bytes password
        encrypted2 = encrypt_data(test_data, bytes_password)
        decrypted2 = decrypt_data(encrypted2, bytes_password)
        assert decrypted2 == test_data
        
        # Different password types should produce different results
        assert encrypted1 != encrypted2
    
    def test_empty_data(self):
        """Test encryption of empty data."""
        empty_data = b""
        password = "empty_test"
        
        encrypted = encrypt_data(empty_data, password)
        assert encrypted is not None
        
        decrypted = decrypt_data(encrypted, password)
        assert decrypted == empty_data
    
    def test_large_data(self):
        """Test encryption of large data."""
        large_data = b"A" * 1000000  # 1MB of data
        password = "large_test"
        
        encrypted = encrypt_data(large_data, password)
        assert encrypted is not None
        
        decrypted = decrypt_data(encrypted, password)
        assert decrypted == large_data