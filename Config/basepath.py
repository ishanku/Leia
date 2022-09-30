from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.join(BASE_DIR, "../")

print("------------         Base Directory From basepath.py     ------------")
print(BASE_DIR)

