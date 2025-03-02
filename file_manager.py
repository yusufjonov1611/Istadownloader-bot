import os
import glob

DOWNLOADS_FOLDER = "downloads/"

def cleanup_old_files():
    """Yuklangan eski fayllarni o‘chirish."""
    files = glob.glob(os.path.join(DOWNLOADS_FOLDER, "*"))
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Faylni o‘chirib bo‘lmadi: {file}, Xatolik: {e}")

def delete_file(file_path):
    """Berilgan faylni o‘chirish."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Faylni o‘chirib bo‘lmadi: {file_path}, Xatolik: {e}")
