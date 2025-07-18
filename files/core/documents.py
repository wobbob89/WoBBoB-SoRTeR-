import os
import pytesseract
from PIL import Image
import re

class DocumentManager:
    def __init__(self, folder):
        self.folder = folder

    def scan_documents(self):
        count = 0
        sensitive = 0
        keywords = ["SSN", "password", "confidential", "secret"]
        for root, dirs, files in os.walk(self.folder):
            for name in files:
                path = os.path.join(root, name)
                try:
                    if path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        text = pytesseract.image_to_string(Image.open(path))
                    elif path.lower().endswith(('.txt', '.md')):
                        with open(path) as f:
                            text = f.read()
                    else:
                        text = ""
                    if any(kw in text for kw in keywords):
                        sensitive += 1
                    count += 1
                except Exception:
                    pass
        return count, sensitive