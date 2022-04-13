from os.path import exists, join, realpath
from os import makedirs
import pandas as pd
import csv

root_data_dir = join(realpath('..'), 'data', 'original')


def loadData(csv_file_path):
    dataset_path = join(root_data_dir, csv_file_path)
    data = pd.read_csv(dataset_path, encoding="utf-8")
    data = data.fillna(method="ffill")
    return data


class SentenceGetter(object):

    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
        agg_func = lambda s: [(w, t) for w, t in zip(s["Word"].values.tolist(),
                                                     s["Final"].values.tolist())]
        self.grouped = self.data.groupby("Sentence #").apply(agg_func)
        self.sentences = [s for s in self.grouped]

    def get_next(self):
        try:
            s = self.grouped["Sentence: {}".format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None


def save_to_file(data, dest_folder, filename):

    with open(join(realpath('.'), dest_folder, filename), 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Sentence #','Word', 'Tag'])

    for si, sent in enumerate(data):
        words = [item[0] for item in sent]
        tags = [item[1] for item in sent]

        lines = []
        [lines.append(['Sentence: {}'.format(si), w, t]) if i == 0 else lines.append(["", w, t])
         for i, w, t in zip(range(len(words)), words, tags)]

        with open(join(realpath('.'), dest_folder, filename), 'a', encoding='utf8', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(lines)


from random import shuffle

if __name__ == '__main__':
    sheets_path = join(realpath('.'), 'sheets')
    output_dir = join(realpath('.'), 'final_NER')
    if not exists(output_dir):
        makedirs(output_dir)

    # the entire sentences from different data sources
    sentences = []

    # load missing
    csv_file_path = join(sheets_path, 'missing', 'missing_filled.csv')
    data = loadData(csv_file_path)
    getter = SentenceGetter(data)
    current_sentences = getter.sentences
    sentences = sentences + current_sentences

    # load matches and mismatches
    csv_file_paths = ['Nora-Leila.csv', 'Felicitas-Sheeba.csv']
    dirs = ['mismatches', 'matches']

    for current_dir in dirs:
        for csv_file_path in csv_file_paths:
            # print(csv_file_path)
            print(join(sheets_path, current_dir, csv_file_path))
            data = loadData(join(sheets_path, current_dir, csv_file_path))
            # print(data.head(10))

            getter = SentenceGetter(data)
            current_sentences = getter.sentences

            sentences = sentences + current_sentences

    ln = len(sentences)

    shuffle(sentences)

    train_sentences = sentences[0:int(0.8 * ln)]
    save_to_file(train_sentences, output_dir, 'train.csv')

    test_sentences = sentences[int(0.8 * ln):int(0.9 * ln)]
    save_to_file(test_sentences, output_dir, 'test.csv')

    val_sentences = sentences[int(0.9 * ln)::]
    save_to_file(val_sentences, output_dir, 'val.csv')

    # log some statistics
    print('Total #Sentences: {}'.format(ln))

    print('Train #Sentences: {}'.format(len(train_sentences)))
    print('Val #Sentences: {}'.format(len(val_sentences)))
    print('Test #Sentences: {}'.format(len(test_sentences)))
