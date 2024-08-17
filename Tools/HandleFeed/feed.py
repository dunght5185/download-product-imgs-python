import re

def replace_line_breaks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        new_lines.append(line.replace('\n', '. ') if line != '\n' else line)

    with open(filename, 'w') as file:
        file.writelines(new_lines)

replace_line_breaks('allofcheapfeed.csv')