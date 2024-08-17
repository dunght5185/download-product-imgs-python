from PIL import Image, ImageDraw
import os
import traceback

def resize_image(image_path, size=(600, 600)):
    try:
        # Create a new image with white background
        background = Image.new('RGB', size, (255, 255, 255))

        # Open and resize the product image
        img = Image.open(image_path)
        img.thumbnail(size, Image.LANCZOS)

        # Calculate the position to paste the product image
        img = img.resize(size)
        img_width, img_height = img.size
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


logo_path = "./Images/favicon_sgm.png"
def paste_logo_on_images(target_image_path):
    try:
        
        target_image = Image.open(target_image_path)
        smaller_dimension = min(target_image.size)
        logo_new_size = int(smaller_dimension * 0.14)
        
        
        logo = Image.open(logo_path)
        logo_aspect_ratio = logo.width / logo.height
        logo_resized = logo.resize((logo_new_size, int(logo_new_size / logo_aspect_ratio)), Image.LANCZOS)
        
        
        target_width, target_height = target_image.size
        logo_width, logo_height = logo_resized.size
        position = (0, target_height - logo_height)

        
        # if target_width == target_height:
            
        #     box_width = int(target_width * 0.325)
        #     box_height = int(target_height * 0.074)
            
        #     box_position = (target_width - box_width, target_height - box_height, target_width, target_height)
            
        #     draw = ImageDraw.Draw(target_image)
        #     draw.rectangle(box_position, fill="white")
        
        # Assuming logo_resized is in "RGBA" mode and target_image supports pasting with transparency
        if logo_resized.mode == 'RGBA':
            # Extract the alpha channel from the logo as a transparency mask
            mask = logo_resized.split()[3]  # The alpha channel is the 4th channel in "RGBA"
            target_image.paste(logo_resized, position, mask)
        else:
            # If no need for transparency, paste without a mask
            target_image.paste(logo_resized, position)

        # target_image.paste(logo_resized, position, logo_resized)
        target_image.save(target_image_path)
        print(f"Logo added to {target_image_path} and saved as {target_image_path}")
    except Exception as e:
        print(f"Error adding logo to image: {e}")



def addlogo_to_images_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                image_path = os.path.join(root, file)
                paste_logo_on_images(image_path)

folder_path = "Images/2023/12"
addlogo_to_images_in_folder(folder_path)
# resize_images_in_folder(folder_path)