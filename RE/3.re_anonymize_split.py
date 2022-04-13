from os.path import realpath, join, exists
from os import listdir, makedirs
import csv
import random


def save_to_file(lines, dest_folder, filename):
    with open(join(realpath('.'), dest_folder, filename), 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(lines)


def create_bin_corpus():
    sheet_path = join(realpath('.'), 'data')
    sheets = listdir(sheet_path)

    bin_corpus = []
    for sheet in sheets:
        with open(join(sheet_path, sheet), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i % 2 == 0:
                    relation = row[0]
                    bin_re = row[1]
                    sent = row[2:]
                else:
                    tags = row[2:]
                    assert len(sent) == len(tags)
                    anonymize = []
                    for w, t in zip(sent, tags):
                        if t == 'O':
                            anonymize += [w]
                        elif 'B-' in t:
                            anonymize += ['@{}$'.format(t.replace('B-', '').upper())]
                        else:
                            pass  # ignore I-
                    # save binary mode
                    bin_corpus += [[bin_re] + [' '.join(anonymize)]]
    return bin_corpus


def create_multi_re_corpus():
    sheet_path = join(realpath('.'), 'data')
    sheets = listdir(sheet_path)

    mutli_corpus = []
    for sheet in sheets:
        with open(join(sheet_path, sheet), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i % 2 == 0:
                    relation = row[0]
                    if not relation:
                        relation = 'NA'
                    # bin_re = row[1]
                    sent = row[2:]
                else:
                    tags = row[2:]
                    assert len(sent) == len(tags)
                    anonymize = []
                    for w, t in zip(sent, tags):
                        if t == 'O':
                            anonymize += [w]
                        elif 'B-' in t:
                            anonymize += ['@{}$'.format(t.replace('B-', '').upper())]
                        else:
                            pass  # ignore I-
                    # save binary mode
                    mutli_corpus += [[relation] + [' '.join(anonymize)]]
    return mutli_corpus


def sets_split(dest_dir, corpus):
    random.shuffle(corpus)

    # train test split
    train_sentences = corpus[0:int(0.8 * ln)]
    save_to_file(train_sentences, dest_dir, 'train.csv')

    test_sentences = corpus[int(0.8 * ln):int(0.9 * ln)]
    save_to_file(test_sentences, dest_dir, 'test.csv')

    val_sentences = corpus[int(0.9 * ln)::]
    save_to_file(val_sentences, dest_dir, 'val.csv')


if __name__ == '__main__':
    root_data_dir = join(realpath('.'), 'data')

    # dest_dir = join(realpath('.'), 'bin_BiodivRE')
    # if not exists(dest_dir):
    #     makedirs(dest_dir)
    #
    # bin_corpus = create_bin_corpus()
    #
    # ln = len(bin_corpus)
    # print(ln)

    # sets_split(dest_dir, bin_corpus)

    dest_dir = join(realpath('.'), 'multi_BiodivRE')
    if not exists(dest_dir):
        makedirs(dest_dir)

    mutli_corpus = create_multi_re_corpus()

    ln = len(mutli_corpus)
    print(ln)

    sets_split(dest_dir, mutli_corpus)
