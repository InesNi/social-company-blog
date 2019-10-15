import os
import hashlib
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user

def add_profile_pic(pic_upload, email):
    """
    Takes in image, deletes previous profile image,
    sets a new hashed path to new image and sets it as new profile image
    """
    if current_user.profile_image != 'default_profile.png':
        filepath = os.path.join(current_app.root_path, 'static/profile_pics', current_user.profile_image)
        os.remove(filepath)

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    hash_object = hashlib.md5(email.encode()).hexdigest()
    storage_filename = hash_object+'.'+ ext_type
    filepath = os.path.join(current_app.root_path, 'static/profile_pics',storage_filename)
    output_size = (200,200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename