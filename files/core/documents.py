import os
import logging
import pytesseract
from PIL import Image
import re

# Configure logging for documents module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
                except Exception as e:
                    logger.error(f"Error processing document {path}: {str(e)}")
                    continue
        return count, sensitive