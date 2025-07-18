# Plugin API Documentation

WoBBoB-SoRTeR- includes a production-ready plugin system with three main plugin hooks for NSFW detection and file encryption/decryption.

## Available Plugin Hooks

### 1. NSFW Detection (`plugins/nsfw.py`)

**Function:** `is_nsfw(image_path: str, threshold: float = 0.6) -> bool`

Detects NSFW (Not Safe For Work) content in images using NudeNet, an open-source, MIT-licensed deep learning model.

**Parameters:**
- `image_path` (str): Path to the image file to analyze
- `threshold` (float, optional): Confidence threshold (0.0-1.0) for NSFW detection. Default: 0.6

**Returns:**
- `bool`: True if NSFW content is detected, False otherwise

**Example:**
```python
from plugins.nsfw import is_nsfw

# Check if an image contains NSFW content
if is_nsfw("/path/to/image.jpg"):
    print("NSFW content detected!")
else:
    print("Image is safe")

# Use custom threshold
if is_nsfw("/path/to/image.jpg", threshold=0.8):
    print("High confidence NSFW content detected!")
```

**Advanced Function:** `get_detection_details(image_path: str) -> Dict[str, Any]`

Returns detailed detection results for debugging and analysis.

**Example:**
```python
from plugins.nsfw import get_detection_details

details = get_detection_details("/path/to/image.jpg")
print(f"Detections: {details}")
```

### 2. File Encryption (`plugins/encryption.py`)

**Function:** `encrypt_file(input_path: str, output_path: str, password: Union[str, bytes]) -> bool`

Encrypts a file using AES-GCM authenticated encryption with PBKDF2 key derivation.

**Parameters:**
- `input_path` (str): Path to the file to encrypt
- `output_path` (str): Path where encrypted file will be saved
- `password` (str or bytes): Password for encryption

**Returns:**
- `bool`: True if encryption was successful, False otherwise

**Example:**
```python
from plugins.encryption import encrypt_file

# Encrypt a file
if encrypt_file("/path/to/document.pdf", "/path/to/document.pdf.enc", "my_password"):
    print("File encrypted successfully!")
else:
    print("Encryption failed!")
```

### 3. File Decryption (`plugins/encryption.py`)

**Function:** `decrypt_file(input_path: str, output_path: str, password: Union[str, bytes]) -> bool`

Decrypts a file that was encrypted using the `encrypt_file` function.

**Parameters:**
- `input_path` (str): Path to the encrypted file
- `output_path` (str): Path where decrypted file will be saved
- `password` (str or bytes): Password for decryption

**Returns:**
- `bool`: True if decryption was successful, False otherwise

**Example:**
```python
from plugins.encryption import decrypt_file

# Decrypt a file
if decrypt_file("/path/to/document.pdf.enc", "/path/to/document.pdf", "my_password"):
    print("File decrypted successfully!")
else:
    print("Decryption failed! Check password.")
```

## Additional Encryption Functions

### In-Memory Data Encryption/Decryption

**Function:** `encrypt_data(data: bytes, password: Union[str, bytes]) -> Optional[bytes]`

Encrypts data in memory without writing to disk.

**Function:** `decrypt_data(encrypted_data: bytes, password: Union[str, bytes]) -> Optional[bytes]`

Decrypts data in memory.

**Example:**
```python
from plugins.encryption import encrypt_data, decrypt_data

# Encrypt data in memory
data = b"sensitive information"
encrypted = encrypt_data(data, "my_password")

# Decrypt data in memory
decrypted = decrypt_data(encrypted, "my_password")
print(decrypted)  # b"sensitive information"
```

## Security Features

### NSFW Detection
- Uses NudeNet, an open-source, MIT-licensed model
- Local processing (no data sent to external services)
- Configurable confidence thresholds
- Comprehensive logging for debugging

### Encryption
- **Algorithm:** AES-GCM (256-bit keys)
- **Authentication:** Built-in authenticated encryption
- **Key Derivation:** PBKDF2 with SHA-256 (100,000 iterations)
- **Security:** Cryptographically secure random salt and nonce generation
- **Standard:** Follows OWASP cryptographic guidelines

## Error Handling

All plugin functions include robust error handling:
- File not found errors
- Invalid password errors
- Corrupted file detection
- Network/model loading errors
- Detailed logging for debugging

## Dependencies

### NSFW Detection
- `nudenet` - MIT-licensed NSFW detection model
- `opencv-python-headless` - Image processing
- `numpy` - Numerical operations

### Encryption
- `cryptography` - Industry-standard cryptographic library
- Built-in Python libraries (`os`, `logging`)

## Integration with Core Application

The plugins are automatically integrated with the core application:

- **Photos Manager:** Uses `is_nsfw()` for content filtering
- **File Organization:** Can integrate encryption for sensitive files
- **Settings:** Plugin status and configuration available in settings

## Performance Considerations

### NSFW Detection
- First-time model loading may take a few seconds
- Subsequent detections are fast (< 1 second per image)
- Memory usage: ~500MB when model is loaded

### Encryption
- File encryption speed: ~50-100 MB/s (depends on hardware)
- Memory usage: Processes files in chunks for large files
- CPU usage: Moderate (key derivation is intentionally slow for security)

## Plugin Development Guidelines

When extending the plugin system:

1. Follow the existing pattern of module-level convenience functions
2. Include comprehensive error handling and logging
3. Use production-ready libraries with appropriate licenses
4. Document all functions with clear docstrings
5. Include type hints for better IDE support
6. Test thoroughly with various file types and edge cases