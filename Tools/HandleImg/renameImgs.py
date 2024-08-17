import os
import glob

def rename_images_in_folder(folder_path):
    # Traverse the directory tree
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Get the full file path
            image_file = os.path.join(root, file)
            
            # Get the base name of the image file
            base_name = os.path.basename(image_file)
            
            # Check if the image name contains two "." characters
            if base_name.count('.') == 2:
                # Split the base name to remove the middle part
                parts = base_name.split('.')
                new_base_name = parts[0] + '.' + parts[-1]
                
                # Construct the full new file path
                new_image_file = os.path.join(root, new_base_name)
                
                # Rename the image file
                os.rename(image_file, new_image_file)
                print(f'Renamed: {image_file} to {new_image_file}')

# Example usage
parent_folder_path = 'Images/20240804'
rename_images_in_folder(parent_folder_path)