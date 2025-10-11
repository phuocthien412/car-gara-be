import os
from src.constants.dir import UPLOAD_IMAGE_DIR, UPLOAD_IMAGES_DIR, UPLOAD_FILE_DIR, UPLOAD_FILES_DIR, LOGS_DIR, UPLOAD_DOCUMENTS_DIR

folders = [UPLOAD_IMAGE_DIR, UPLOAD_IMAGES_DIR, UPLOAD_FILE_DIR, UPLOAD_FILES_DIR, LOGS_DIR, UPLOAD_DOCUMENTS_DIR]

def init_folder():
  for folder in folders:
    if not os.path.exists(folder):
      os.makedirs(folder, exist_ok=True)
      print(f"✅ Created directory: {folder}")