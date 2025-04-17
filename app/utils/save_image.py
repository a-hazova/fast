import os
import shutil
from app.settings import settings

MEDIA_DIR = settings.get_media_dir()


def save_image(image: bytes, user_id, file_name):
    image_dir = os.path.join(MEDIA_DIR, f"{user_id}")
    os.makedirs(image_dir, exist_ok=True)
    
    image_path = os.path.join(image_dir, f"{file_name}").replace(' ', '_')

    with open(image_path, 'wb') as buffer:
        shutil.copyfileobj(image, buffer)
    return image_path
