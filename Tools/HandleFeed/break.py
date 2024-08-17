def count_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return len(lines)

import re

def replace_line_breaks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if re.search(r'\n(?!\s*US::United States \(US\) Free shipping US:0 USD)', line):
            new_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(new_lines)

filename = 'allofcheapfeed_20240425.csv'
replace_line_breaks(filename)