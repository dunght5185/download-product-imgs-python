from PIL import Image
import os

def resize_image(image_path, size=(600, 600)):
    try:
        # Create a new image with white background
        background = Image.new('RGB', size, (255, 255, 255))

        # Open and resize the product image
        img = Image.open(image_path)
        img.thumbnail(size, Image.LANCZOS)

        # Calculate the position to paste the product image
        img_width, img_height = img.size
        print(img.size)
        bg_width, bg_height = background.size
        position = ((bg_width - img_width) // 2, (bg_height - img_height) // 2)

        # Paste the product image onto the background
        background.paste(img, position)

        # Save the resulting image
        background.save(image_path)
        print(f"Resized image {image_path} to {size}")
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")

def resize_images_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                resize_image(image_path)

folder_path = "Images/Kohls/1"
resize_images_in_folder(folder_path)