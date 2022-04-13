import csv


def get_sentences(dataset_path):

    # global var that will be returned
    sentences = []
    # tmp var for sentence's lines
    sent_lines = []

    with open(dataset_path, 'r', encoding='latin' ) as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            # print(row)

            if i < 2:
                continue

            if not row:
                # parse sentence lines
                sent = [(item[1],item[2]) for item in sent_lines]
                sentences += [sent]

                # empty the tmp var for the next line
                sent_lines = []
            else:
                sent_lines += [row]
    # should be a list of list of tuples
    return sentences


def get_text_tags_lists(sentences):
  texts = []
  tags = []
  for sent in sentences: #list of tuples
    sent_texts = []
    sent_tags = []
    for tuple1 in sent:
      sent_texts.append(tuple1[0])
      sent_tags.append(tuple1[1])

    texts.append(sent_texts)
    tags.append(sent_tags)
  return texts, tags


# add extra line before each sentence start to enable parsing using get_sentences and get_text_tags_lists
def reformat(dataset_path):
    # lines = []
    with open(dataset_path, 'r' , encoding='latin') as file:
        lines = file.readlines()
        # print(lines)

    newLines = []
    for line in lines:
        if 'Sentence: ' in line:
            newLines += ['\n']
        newLines += [line]

    with open(dataset_path, 'w' , encoding='latin') as file:
        file.write(''.join(newLines))


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def is_missing_tags(tags):
    if 'B-Thing' in tags or 'I-Thing' in tags:
        return True
    return False

valid_tags = ['Environment', 'Location', 'Matter', 'Phenomena', 'Quality', 'Organism']

def has_annotation(tags):
    for t in tags:
        t = t.replace('B-', '')
        t = t.replace('I-', '')
        if t in valid_tags:
            return True
    return False