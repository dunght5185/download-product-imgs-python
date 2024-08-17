import re

filename = 'Feeds/sgearmartfeed_20240810.csv'

    
def clean_feed(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for index, line in enumerate(lines):
        new_lines.append(line.replace('\n', '. '))

    with open(filename, 'w', encoding="utf-8") as file:
        file.writelines(new_lines)



def format_feed(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for index, line in enumerate(lines):
        new_lines.append(line.replace(',"US:0 USD","yes"', ',"US:0 USD","yes"\n'))

    with open(filename, 'w', encoding="utf-8") as file:
        file.writelines(new_lines)

# def remove_special(filename):

#     df = pd.read_excel(filename)

#     for col in df.columns:
#         df[col] = df[col].apply(lambda x: x.encode('utf-8', 'ignore').decode('utf-8') if isinstance(x, str) else x)

#     df.to_excel('cleaned_file.xlsx', index=False)

clean_feed(filename)
format_feed(filename)
