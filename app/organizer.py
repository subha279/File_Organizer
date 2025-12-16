import os
import shutil
from datetime import datetime

from .undo import add_undo

FILE_TYPES = {
    "PDFs": [".pdf"],
    "Music": [".mp3"],
    "Video": [".mp4", ".mkv"],
    "Images": [".jpg", ".jpeg", ".png", ".webp"],
}


def get_unique(dest, name):
    base, ext = os.path.splitext(name)
    i = 1
    new = name
    while os.path.exists(os.path.join(dest, new)):
        new = f"{base}_{i}{ext}"
        i += 1
    return new


def organize(folder, status_cb):
    moved = 0
    for f in os.listdir(folder):
        src = os.path.join(folder, f)
        if not os.path.isfile(src):
            continue

        _, ext = os.path.splitext(f)
        ext = ext.lower()

        for cat, exts in FILE_TYPES.items():
            if ext in exts:
                month = datetime.fromtimestamp(os.path.getmtime(src)).strftime("%Y-%m")

                dest_dir = os.path.join(folder, cat, month)
                os.makedirs(dest_dir, exist_ok=True)

                new_name = get_unique(dest_dir, f)
                dest = os.path.join(dest_dir, new_name)

                shutil.move(src, dest)
                add_undo(dest, src)
                moved += 1
                status_cb(f"Moved: {f}")
                break
    return moved
