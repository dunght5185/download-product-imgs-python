from PIL import Image
import os

def counter_imgs_in_path(folder_path):
    counter = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                image_path = os.path.join(root, file)
                counter += 1
    print(f"{counter}")

folder_path = "Images"
counter_imgs_in_path(folder_path)