import os
from PIL import Image
import pillow_avif

# Define the parent directory
parent_dir = './Images/Lesliespool/Lesliespool20240620'

# Loop over each subdirectory in the parent directory
for subdir, dirs, files in os.walk(parent_dir):
    for file in files:
        # Check if the file is an AVIF image
        if file.endswith('.avif'):
            # Construct the full file path
            file_path = os.path.join(subdir, file)
            
            # Open the image and convert it to JPEG
            img = Image.open(file_path)
            img = img.resize((600, 600))  # Resize the image to 600x600
            output_path = file_path.rsplit('.', 1)[0] + '.png'
            img.save(output_path)
            print(f'Converted {file_path} to {output_path} \n')
            
            # Remove the original AVIF image
            os.remove(file_path)