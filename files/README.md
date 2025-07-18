# WoBBoB WiZArD

The ultimate AI-powered desktop organiser for files, photos, documents, and music.  
Sorts, detects duplicates, recognises faces, filters NSFW, restores points, manages music, scans documents, encrypts, and more—all in a beautiful PyQt5 interface.

**Features:**
- Smart AI-driven file organisation
- Duplicate detection and review
- Restore points for undo/redo
- Facial recognition in photos
- NSFW and sensitive content filtering
- Music organisation (metadata, tag editing, playlists)
- Document OCR and sensitive data detection
- Encrypted and password-protected folders
- Logging, analytics, plugin system
- Modern PyQt5 UI: drag-and-drop, previews, dashboard

**Install:**
```bash
pip install -r requirements.txt
python wizard_main.py
```

**Structure:**
- `wizard_main.py` — Main entry
- `core/` — Logic and AI
- `ui/` — PyQt5 interface
- `plugins/` — Optional plugins (e.g. NSFW, encryption)
- `resources/` — Icons, config
- `tests/` — Unit tests

MIT License