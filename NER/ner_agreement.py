from os.path import join, realpath
from utils import utils
from sklearn.metrics import cohen_kappa_score as agreement
import numpy as np

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

        # flatten lists
        src_flat, dest_flat = [], []
        [src_flat.extend(lst) for lst in src_tags]
        [dest_flat.extend(lst) for lst in dest_tags]

        src_arr = np.array(src_flat)
        dest_arr = np.array(dest_flat)

        print(pair)
        score = agreement(src_arr, dest_arr)
        print(score)
