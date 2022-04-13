from os.path import exists, join, realpath
from os import makedirs
import pandas as pd
import csv

root_data_dir = join(realpath('.'), 'data', 'original')


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


def filter_sentences(sentences, len_tags='exact'):
    re_sentences = []
    for sent in sentences:
        tags = [item[1].replace('I-', '').replace('B-', '') for item in sent]
        if len_tags == 'exact':
            if len(set(tags)) - 1 == 2:  # exclude O from unique set length
                re_sentences.append(sent)
        else:
            if len(set(tags)) - 1 > 2:  # exclude O from unique set length
                re_sentences.append(sent)
    return re_sentences


def __get_entitiy(entities, key):
    ent0_start = entities[key]['start']
    ent0_end = entities[key]['end']
    ent0 = entities[key]['entity']
    return ent0, ent0_start, ent0_end


def create_sent_variations(sent, entities, pairs):
    """

    :param sent: original sentence in tuple format (word, tag)
    :param entities: entities dictionary, holds all entity words and tags, start, end and unique tag keys
    :param pairs: all pairs that I should keep
    :return:
    """
    variations = []
    for pair in pairs:
        new_sent = [(w, 'O') for w, _ in sent]

        ent0, ent0_start, ent0_end = __get_entitiy(entities, pair[0])
        ent1, ent1_start, ent1_end = __get_entitiy(entities, pair[1])

        tmp_i = 0
        for i in range(ent0_start, ent0_end + 1):
            new_sent[i] = (new_sent[i][0], ent0[tmp_i][1])
            tmp_i += 1

        tmp_i = 0
        for i in range(ent1_start, ent1_end + 1):
            new_sent[i] = (new_sent[i][0], ent1[tmp_i][1])
            tmp_i += 1

        variations.append(new_sent)
    return variations


def create_combinations(sentences):
    all_combinations = []
    for sent in sentences:
        entities = {}
        start = -1
        for i, item in enumerate(sent):
            w = item[0]
            t = item[1]
            if 'B-' in t:
                start = i
                end = i
                entities[start] = {'entity': [(w, t)]}

            elif 'I-' in t:
                end += 1
                if start == -1:
                    print(sent)
                    break
                entities[start]['entity'].append((w, t))

            if start > -1:
                entities[start].update({'start': start, 'end': end})  # complete creation and add to entities

        # fill-in unique tag attribute
        for key, val in entities.items():
            # print(key)
            unique = list(set([v[1].replace('B-', '').replace('I-', '') for v in val['entity']]))[0]
            # if 'Location' not in unique:
            entities[key].update({'unique_tag': unique})

        # create pairs if they have different unique tags
        pairs = []
        for key1, val1 in entities.items():
            for key2, val2 in entities.items():
                if val1['unique_tag'] != val2['unique_tag']:
                    if (key2, key1) not in pairs:  # add in one direction only
                        pairs.append((key1, key2))
        sent_variations = create_sent_variations(sent, entities, pairs)
        # print(pairs)
        all_combinations.extend(sent_variations)
    return all_combinations


def save_file(sentences, save_to):
    with open(save_to, 'w+', newline='', encoding='utf-8') as file:
        for sent in sentences:
            l1 = ['?'] + [item[0] for item in sent]
            l2 = ['-'] + [item[1] for item in sent]
            # l3 = []  # skipping line

            # QUOTE_MINIMAL escaping quotes that appear in text only. Default option would escape everything
            # file could be as 3x in desk size if you selected the default option
            w = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            # w.writerows([l1, l2, l3])
            w.writerows([l1, l2])


def filter_corpus(corpus):
    corpus = [s for s in corpus if len(s) <= 512]
    new_corpus = []
    for sent in corpus:
        staring_idxs = [i for i, item in enumerate(sent) if 'B-' in item[1]]
        diff = staring_idxs[1] - staring_idxs[0]
        if diff <= 20:
            new_corpus += [sent]
    return new_corpus


from random import shuffle, sample


# def get_sample(sentences_lst):
#     """"
#     This is a dump sampling, just random 6000 samples from the entire list, list samples are equal weight.
#     """
#     shuffle(sentences_lst)
#     subset = sample(sentences_lst, 6000)
#     return subset

def get_sample(sentences_lst):
    pairs = [
        ("Organism", "Organism"),
        ("Organism", "Environment"),
        ("Organism ", "Location"),
        ("Organism ", "Phenomena"),
        ("Organism", "Matter"),
        ("Organism", "Quality"),
        ("Environment", "Environment"),
        ("Environment", "Phenomena"),
        ("Environment", "Location"),
        ("Environment", "Quality"),
        ("Phenomena", "Phenomena"),
        ("Phenomena", "Environment"),
        ("Phenomena", "Location"),
        ("Phenomena", "Quality"),
        ("Matter", "Environment"),
        ("Matter ", "Quality"),
        ("Quality", "Quality"),
        ("Quality", "Organism")
    ]

    # counter of each pair, calculates the support by the actual sentences
    # init holder dict to point to the actual sentence index
    count, taken, holder = {}, {}, {}
    for pair in pairs:
        count[pair] = 0
        taken[pair] = 0
        holder[pair] = []
    count['other'] = 0
    taken['other'] = 0
    holder['other'] = []

    for i, sent in enumerate(sentences_lst):
        sent_pair = [i[1].replace('B-', '') for i in sent if i[1] != 'O' and 'I-' not in i[1]]
        if len(sent_pair) == 2:
            sent_pair = (sent_pair[0], sent_pair[1])
            if sent_pair in pairs:
                count[sent_pair] += 1
                holder[sent_pair] += [i]
            else:
                count['other'] += 1
                holder['other'] += [i]
    print(count)
    # sample 6000 sentence as round robin fashion
    taken_idxs = []
    target = 3000
    i = 0
    for _ in range(target):
        if i < target:
            for key, val in holder.items():
                if i < target:
                    if val:
                        # take current item
                        taken_idxs += [val[0]]
                        taken[key] += 1
                        # update the values (actual remove)
                        holder[key] = val[1:]
                        i += 1
                else:
                    break
        else:
            break
    print(taken)
    print(taken_idxs)
    actual_sentence_sample = [sentences_lst[i] for i in taken_idxs]

    return actual_sentence_sample

def create_re_from(csv_path):
    data = loadData(csv_path)

    getter = SentenceGetter(data)
    sentences = getter.sentences
    print('Original sentences: {}'.format(len(sentences)))

    two_ent_sentences = filter_sentences(sentences)
    # print(len(two_ent_sentences))
    two_ent_sentences_v2 = create_combinations(two_ent_sentences)
    print('Sents with 2 entities: {}'.format(len(two_ent_sentences_v2)))

    more_ent_sentences = filter_sentences(sentences, len_tags='>2')
    all_combinations = create_combinations(more_ent_sentences)
    print('Combinations for sentences with > 2 entities: {}'.format(len(all_combinations)))

    # all = two_ent_sentences + all_combinations
    all = two_ent_sentences_v2 + all_combinations
    print('Total: {}'.format(len(all)))

    return all

if __name__ == '__main__':
    sheets_path = join(realpath('.'), 'data', 'original')
    csv_file_paths = ['Nora-Leila.csv', 'Felicitas-Sheeba.csv']
    dirs = ['matches']

    corpus = []

    # load missing
    csv_file_path = join(sheets_path, 'missing', 'missing_filled.csv')
    missing = create_re_from(csv_file_path)
    corpus += missing

    for current_dir in dirs:
        for csv_file_path in csv_file_paths:

            print(join(sheets_path, current_dir, csv_file_path))
            all = create_re_from(join(sheets_path, current_dir, csv_file_path))
            # append to the entire corpus
            corpus += all

    print("========================================================")
    print('Entire corpus sentences: {}'.format(len(corpus)))

    # filter corpus
    corpus = filter_corpus(corpus)
    print('Filtered corpus sentences: {}'.format(len(corpus)))

    subset = get_sample(corpus)
    transformed_path = join('.', 'data', 'transformed')
    if not exists(transformed_path):
        makedirs(transformed_path)

    for i in range(3):
        s = i * 1000
        e = s + 1000
        save_file(subset[s:e], join(transformed_path, '{}.csv'.format(i)))
