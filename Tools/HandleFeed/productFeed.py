import re

def clean_csv(file_path):
    # Step 1: Open the CSV file in read mode
    with open(file_path, 'r') as file:
        # Step 2: Read the content of the file
        content = file.read()

    # Step 3: Replace all newline characters with spaces
    content = content.replace('\n', ' ')

    # Step 6: Use a regular expression to add a new line before any occurrence of `xxx,simple,`
    cleaned_content = re.sub(r'(\d+,simple,)', r'\n\1', content)

    # Step 7: Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(cleaned_content)

# Example usage
clean_csv('Feeds/wc-product-export-2-8-2024-1722570380074.csv')