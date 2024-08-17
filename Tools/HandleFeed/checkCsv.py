import csv
import difflib

def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def filter_csv_by_text(text_file_path, csv_file_path, output_csv_file_path):
    # Step 1: Read lines from the text file
    with open(text_file_path, 'r') as text_file:
        text_lines = text_file.readlines()

    # Step 2: Open the CSV file and the output CSV file
    with open(csv_file_path, 'r') as csv_file, open(output_csv_file_path, 'w', newline='') as output_csv_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(output_csv_file)

        # Step 3: Iterate over each line in the CSV file
        for csv_row in csv_reader:
            if len(csv_row) < 5:
                continue  # Skip rows that don't have at least 5 columns

            csv_text = csv_row[4]  # Get the text from column 4

            # Step 4: Compare with each line in the text file
            for text_line in text_lines:
                text_line = text_line.strip()
                if 0.7 <= similarity(text_line, csv_text) <= 1.0:
                    # Step 5: Change value at column 5 from '-1' to '1' if necessary
                    # if csv_row[4] == '\'-1':
                    #     csv_row[4] = '1'
                    
                    # Step 6: Write the matching CSV row to the output file
                    csv_writer.writerow(csv_row)
                    break  # Stop checking other text lines once a match is found

# Example usage
filter_csv_by_text('Feeds/filter.txt', 'Feeds/inyoustorefeed_20240805.csv', 'Feeds/Linhtinh.csv')