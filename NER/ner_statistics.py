from os.path import exists, join, realpath
from os import makedirs, listdir
import pandas as pd
import csv

# QEMP
# root_data_dir = join(realpath('.'), 'QEMP_BIO_data')
# tags = ['Environment', 'Material', 'Process', 'Quality']

# BiodivNER
root_data_dir = join(realpath('.'), 'final_NER')
tags = ['Environment', 'Organism', 'Matter', 'Phenomena', 'Quality', 'Location']

#COPIOUS
# root_data_dir = join(realpath('.'), 'COPIOUS')
# tags = ['GeographicalLocation', 'Taxon', 'Person', 'TemporalExpression', 'Habitat']

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
                                                     s["Tag"].values.tolist())]
        self.grouped = self.data.groupby("Sentence #").apply(agg_func)
        self.sentences = [s for s in self.grouped]

    def get_next(self):
        try:
            s = self.grouped["Sentence: {}".format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None

if __name__ == '__main__':
    csv_file_paths = listdir(root_data_dir)
    print(root_data_dir)

    my_dict = {}
    tags_keywords = {}
    unique_tags_keywords = {}

    [my_dict.update({t: 0}) for t in tags]
    [tags_keywords.update({t: []}) for t in tags]
    [unique_tags_keywords.update({t: 0}) for t in tags]

    all_sentences, keywords = [], []
    all_words = 0

    for csv_file_path in csv_file_paths:
        # print(csv_file_path)
        data = loadData(csv_file_path)
        # print(data.head(10))

        getter = SentenceGetter(data)
        sentences = getter.sentences
        all_sentences += sentences

        for sent in sentences:
            sent_tags = [item[1].replace('B-', '') for item in sent if item[1] != 'O' and 'I-' not in item[1]]
            keywords += [(item[0], item[1]) for item in sent if 'B-' in item[1] or 'I-' in item[1]]

            keyword = ''
            tag = ''
            for item in sent:
                try:
                    if 'B-' in item[1]:
                        keyword = item[0]
                        tag = item[1].replace('B-', '')
                    elif 'I-' in item[1]:
                        keyword += ' ' + item[0]
                    elif 'O' in item[1]:
                        if keyword != '':
                            tags_keywords[tag] += [keyword]
                            keyword = ''
                            tag = ''
                except KeyError:
                    print(keyword, tag)

            all_words += len([_ for _ in sent])
            for t in sent_tags:
                my_dict[t] += 1

    # normalize tags_keywords
    for key, val in tags_keywords.items():
        keywords = [w.lower() for w in val]
        keywords = list(set(keywords))
        unique_tags_keywords[key] = len(keywords)

    print('#Sentence: {}'.format(len(all_sentences)))
    print('#Words: {}'.format(all_words))
    mentions = sum([v for v in my_dict.values()])
    print('#Mentions: {}'.format(mentions))
    unique_mentions = sum([v for v in unique_tags_keywords.values()])
    print('#Unique Mentions: {}'.format(unique_mentions))

    print('Entire Distribution:')
    print(my_dict)

    print('Unique Distribution:')
    print(unique_tags_keywords)
    print('#Keywords:')
    for k, v in tags_keywords.items():
        tags_keywords[k] = list(set([i.lower() for i in v]))
    print(tags_keywords)