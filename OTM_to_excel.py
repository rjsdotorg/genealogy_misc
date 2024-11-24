import csv
import os
import re

data_folder = r'c:\Users\<username>'
fn = r"One-to-Many Tool - Full Version _ GEDmatch.mhtml"
base = fn.split('.')[:-1 ][0]



# regular expressions for columns
re_list = [
    r'>([A-Z0-9]{7,10}[C1]{0,1})<',
    r'(.*)',
    r'k">(.*)</a',
    r'">([GEDWik]{0,7})</a',
    r'([MFU])',
    r'">([0-9\.]{1,8})</div',
    r'">([0-9\.]{1,8})</a',
    r'([0-9\.]{1,8})',
    r'([0-9\.]{1,8})',
    r'">([0-9\.]{1,8})</a',
    r'(Match)',
    r'([A-Za-z\s0-9-]*)',
    r'([0-9]{1,8})',
    r'([0-9]{1,8})',
    r'(.*)',
    r'([A-Za-z 0-9\-]{0,22})',
]

match_list = []
header = ['Kit', 'Name', 'Eail', 'GEDWiki', 'Sex', 'Autosomal Total cM', 'Autosomal Largest', 'Gen', 'X Total cM', 'X Largest', 'Source', 'Overlap', 'Age', 'Haplogroup Mt', 'Haplogroup Y']

with open(os.path.join(data_folder, fn), "r") as f:
    data = f.read()
    data = re.sub('\=\n', '', data)

# Extracting the table data
table = re.findall(r'<tbody.*?>(.*?)</tbody>', data, re.DOTALL)[0]

# Extracting the table rows
rows = re.findall(r'<tr.*?>(.*?)</tr>', table, re.DOTALL)
print(f'{len(rows)} rows matched')


for row_num, row in enumerate(rows):
    # Extracting the table data
    cols = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)[2:]
    #print(f'{len(cols)} columns matched')
    this_row = []
    for col_num, col in enumerate(cols):
        #print(col_num, re_list[col_num], len(col), col)
        if len(col)>0:
            match = re.search(re_list[col_num], col)
            if match is not None:
                this_row.append(match.group(1))
            else:
                print(f'ERR: {row_num} {this_row[0]} {col_num} {re_list[col_num]} {len(col)} "{col}"')
                this_row.append('ERR')
        else:
            this_row.append('')
    this_row.pop(this_row.index('Match'))
    #print(f'\r{row_num} {this_row[0]}', end='')

    match_list.append(this_row)
#print(match_list)

with open(os.path.join(data_folder, base + '.csv'), 'w', newline='') as csvfile:
    w = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow(header)
    w.writerows(match_list)