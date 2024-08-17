from PIL import Image
import os
import traceback

def resize_image(image_path, size=(600, 600)):
    try:
        # Create a new image with white background
        background = Image.new('RGB', size, (255, 255, 255))

        # Open the product image
        img = Image.open(image_path)

        # Calculate the new size while maintaining the aspect ratio
        img.thumbnail(size, Image.LANCZOS)
        img_width, img_height = img.size

        # Calculate the position to paste the product image
        bg_width, bg_height = background.size
        position = ((bg_width - img_width) // 2, (bg_height - img_height) // 2)

        # Paste the product image onto the background
        background.paste(img, position)

        # Save the resulting image
        background.save(image_path)
        print(f"Resized image {image_path} to {img.size}")
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")
        traceback.print_exc()  # Print the full traceback

def resize_images_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                image_path = os.path.join(root, file)
                resize_image(image_path)

folder_path = "../../Images/Homedeport"
resize_images_in_folder(folder_path)