import hashlib
from pathlib import Path

def find_duplicates(directory):
    hashes = {}
    duplicates = []
    for file in Path(directory).rglob("*.*"):
        if file.is_file():
            h = hashlib.md5(file.read_bytes()).hexdigest()
            if h in hashes:
                duplicates.append((file, hashes[h]))
            else:
                hashes[h] = file
    return duplicates