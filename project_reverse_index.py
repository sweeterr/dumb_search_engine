__authors__ = 'Marija Aleksejeva, Daniil Kolomeitsev, Jevgenij Mozajev,' \
              ' Nina Mustafina, Svetlana Pavlova'


# This module builds a reverse index of a collection of documents.
# We do not use this module during the search.


import os
import re


bracket_reg = re.compile('\{|\}')


# This function prints the reverse index dictionary to a txt file.
def print_dict(dictionary, path):
    with open(path, 'w', encoding='utf-8') as f:
        for lemma in sorted(dictionary):
            m = bracket_reg.search(lemma)
            if m:
                continue
            s = lemma + ': '
            for posting in dictionary[lemma]:
                s += posting + ', '
            s += '\n'
            f.write(s)


# This function builds a reverse index of a collection of documents.
def reverse_index(path):
    dictionary = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                file_name = file.replace('.txt', '')
                lemmas = f.readlines()[1:]
                for lemma in lemmas:
                    lemma = lemma.strip('\n')
                    if lemma not in dictionary:
                        postings = []
                        postings.append(file_name)
                        dictionary[lemma] = postings
                    else:
                        postings = dictionary[lemma]
                        if postings[-1] != file_name:
                            postings.append(file_name)
                            dictionary[lemma] = postings
    print_dict(dictionary, 'reverse_index_dict.txt')