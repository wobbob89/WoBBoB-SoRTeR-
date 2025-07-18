# WoBBoB WiZArD

The ultimate AI-powered desktop organiser for files, photos, documents, and music.  
Sorts, detects duplicates, recognises faces, filters NSFW, restores points, manages music, scans documents, encrypts, and more—all in a beautiful PyQt5 interface.

**Features:**
- Smart AI-driven file organisation
- Duplicate detection and review
- Restore points for undo/redo
- Facial recognition in photos
- **Production-ready NSFW filtering** using NudeNet (local, MIT-licensed)
- Music organisation (metadata, tag editing, playlists)
- Document OCR and sensitive data detection
- **Secure AES-GCM encryption** for file protection
- Logging, analytics, **enterprise-grade plugin system**
- Modern PyQt5 UI: drag-and-drop, previews, dashboard

## Installation

### Quick Start
```bash
pip install -r requirements.txt
python wizard_main.py
```

### Plugin System Setup

WoBBoB-SoRTeR- includes a production-ready plugin system with built-in NSFW detection and encryption capabilities.

#### NSFW Detection Plugin
- **Technology:** NudeNet (MIT-licensed, local processing)
- **Privacy:** No data sent to external services
- **Performance:** ~1 second per image after initial model load
- **Setup:** Automatically downloads model on first use

#### Encryption Plugin
- **Security:** AES-GCM 256-bit encryption with PBKDF2 key derivation
- **Standards:** OWASP-compliant cryptographic practices
- **Features:** File and in-memory encryption/decryption
- **Performance:** ~50-100 MB/s encryption speed

### System Requirements
- Python 3.8+
- 4GB RAM minimum (8GB recommended for NSFW detection)
- 500MB free disk space for models
- OpenCV-compatible system

## Plugin Usage

### NSFW Detection
```python
from plugins.nsfw import is_nsfw

# Check if image contains NSFW content
if is_nsfw("/path/to/image.jpg"):
    print("NSFW content detected!")
```

### File Encryption
```python
from plugins.encryption import encrypt_file, decrypt_file

# Encrypt a file
encrypt_file("/path/to/file.txt", "/path/to/file.enc", "password")

# Decrypt a file
decrypt_file("/path/to/file.enc", "/path/to/file.txt", "password")
```

**Structure:**
- `wizard_main.py` — Main entry
- `core/` — Logic and AI
- `ui/` — PyQt5 interface
- `plugins/` — Production-ready plugins (NSFW, encryption)
  - `nsfw.py` — NudeNet NSFW detection
  - `encryption.py` — AES-GCM encryption
- `resources/` — Icons, config
- `tests/` — Unit tests
- `PLUGIN_API.md` — Complete plugin documentation

## Plugin API

The plugin system provides three main hooks:

1. **`is_nsfw(image_path)`** - Detect NSFW content in images
2. **`encrypt_file(input_path, output_path, password)`** - Encrypt files
3. **`decrypt_file(input_path, output_path, password)`** - Decrypt files

See `PLUGIN_API.md` for complete documentation and examples.

## Security & Privacy

- **Local Processing:** NSFW detection runs entirely on your machine
- **No Data Transmission:** No files or metadata sent to external services
- **Encryption Standards:** Uses industry-standard AES-GCM encryption
- **Open Source:** All components use MIT or compatible licenses

## Troubleshooting

### NSFW Detection Issues
- Ensure you have 4GB+ RAM available
- First-time model download may take several minutes
- Check internet connection for initial model download

### Encryption Issues
- Verify password accuracy (case-sensitive)
- Ensure sufficient disk space for encrypted files
- Check file permissions for input/output paths

MIT License