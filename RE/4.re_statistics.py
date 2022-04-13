from os.path import realpath, join
from os import listdir
import collections
import csv

if __name__  == '__main__':
    sheet_path = join(realpath('.'), 'data')
    sheets = listdir(sheet_path)

    relations, binaries = [], []
    for sheet in sheets:
        with open(join(sheet_path, sheet), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] and row[0] != '':
                    relations += [row[0]]
                if row[1] and row[1] != '-':
                    binaries += [row[1]]
    relations_counter = collections.Counter(relations)
    print(relations_counter)
    binaries_counter = collections.Counter(binaries)
    print(binaries_counter)
