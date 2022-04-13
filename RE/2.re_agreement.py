from os.path import join, realpath
from sklearn.metrics import cohen_kappa_score as agreement
import numpy as np
import csv

if __name__ == '__main__':

    data_path = join(realpath('.'), 'data', '[BiodivBERT-RE] Annotation - double-annotation.csv')
    nora, leila = [], []
    with open(data_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            if i == 51:
                break
            if row[0] == '-':
                continue
            nora += [row[1]]
            leila += [row[2]]

        score = agreement(nora, leila)
        print(score)
        print(len(nora))
