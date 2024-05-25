from PIL import Image
import os

image_dir = 'static/images/exercises'

images = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

for image_file in images:
    with Image.open(os.path.join(image_dir, image_file)) as img:
        width, height = img.size
        if width != 466 or height != 375:
            new_img = img.resize((466, 375))
            new_img.save(os.path.join(image_dir, image_file))
