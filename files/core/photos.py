import os
import face_recognition
from PIL import Image
import numpy as np

class PhotoManager:
    def __init__(self, folder):
        self.folder = folder

    def analyse_photos(self):
        faces_found = 0
        nsfw_count = 0
        for root, dirs, files in os.walk(self.folder):
            for name in files:
                path = os.path.join(root, name)
                try:
                    img = face_recognition.load_image_file(path)
                    faces = face_recognition.face_locations(img)
                    if faces:
                        faces_found += 1
                    if self.nsfw_scan(path):
                        nsfw_count += 1
                except Exception:
                    pass
        return faces_found, nsfw_count

    def nsfw_scan(self, path):
        """Scan image for NSFW content using the plugin."""
        try:
            # Import the NSFW plugin
            from plugins.nsfw import is_nsfw
            return is_nsfw(path)
        except Exception as e:
            # Log error but don't crash
            import logging
            logging.warning(f"NSFW scanning failed for {path}: {e}")
            return False