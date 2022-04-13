from os.path import join, realpath, exists
import csv
from utils import utils
from os import makedirs

def save_to_csv(sheet_path, sents, s_tags, d_tags, pair):
    with open(sheet_path, 'a+', encoding='latin', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Sentence #', 'Word',pair[0], pair[1], 'Final'])

    si = 1
    for sent_words, s_tg, d_tg in zip(sents,s_tags, d_tags):
            final_tags = [t1 if t1.strip() == t2.strip() else '?' for t1, t2 in zip(s_tg, d_tg) ]
            # save tsv file
            lines = []
            [lines.append(['Sentence: {}'.format(si), w, t1, t2, tf]) if i == 0 else lines.append(["", w, t1, t2, tf])
                     for i, w, t1, t2, tf in zip(range(len(sent_words)), sent_words, s_tg, d_tg, final_tags)]

            with open(sheet_path, 'a+', encoding='latin', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerows(lines)

            # increment valid sentences only
            si += 1


if __name__ == '__main__':
    pairs = [['Felicitas', 'Sheeba'], ['Nora', 'Leila']]
    data_path = join(realpath('.'), 'data')
    for pair in pairs:
        src = join(data_path, pair[0]+'.csv')
        dest = join(data_path, pair[1]+'.csv')

        # utils.reformat(src)
        # utils.reformat(dest)

        src_sents = utils.get_sentences(src)
        dest_sents = utils.get_sentences(dest)

        src_txt, src_tags = utils.get_text_tags_lists(src_sents)
        dest_txt, dest_tags = utils.get_text_tags_lists(dest_sents)

        assert len(src_txt) == len(dest_txt) == len(src_tags) == len(dest_tags)

        mismatch, match = 0, 0
        for s_txt, d_txt, s_tags, d_tags in zip(src_txt, dest_txt, src_tags, dest_tags):
            if s_tags != d_tags:
                mismatch += 1
            else:
                match += 1

        print(pair)
        print('mismatch: {}'.format(mismatch))
        print('match: {}'.format(match))
        print('\n')

        matches = {}
        i = 0
        for s_txt, d_txt, s_tags, d_tags in zip(src_txt, dest_txt, src_tags, dest_tags):
            if s_tags == d_tags:
                matches[i] = {'sent': s_txt, 'src': s_tags, 'dest': d_tags}
                i += 1

        # save mismatch sheet
        sheet_name = '{}_{}.csv'.format(pair[0], pair[1])
        if not exists(join(realpath('.'), 'results')):
            makedirs(join(realpath('.'), 'results'))
        sheet_path = join(realpath('.'), 'results', sheet_name)

        sents = [vals['sent'] for vals in matches.values()]
        s_tags = [vals['src'] for vals in matches.values()]
        d_tags = [vals['dest'] for vals in matches.values()]

        save_to_csv(sheet_path, sents, s_tags, d_tags, pair)

