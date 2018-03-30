__authors__ = 'Marija Aleksejeva, Daniil Kolomeitsev, Jevgenij Mozajev,' \
              ' Nina Mustafina, Svetlana Pavlova'


# This module creates a collection of links and respective page files
# from source link using breadth-first algorithm with adjustable depth.
# Then it cleans up the page files, lemmatizes the words, and initializes
# query search using tf-idf and cosine similarity measures.


import time
import os
import nltk
from project_cleaning import clean_text
from project_crawler import crawler
from project_lemmatize import lemmatize_text
from project_reverse_index import reverse_index
from project_search import search


if __name__ == '__main__':
    root_path = ['http://www.afisha.ru/']
    depth = 3
    #links = crawler(root_path, depth)
    #links_to_file(links, 'links.txt')
    #clean_text('collection_pages', 'clean_collection')
    #lemmatize_text(os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                            'clean_collection'))
    #reverse_index('clean_collection_lemmatized')
    #nltk.download()
    while True:
        query = input('your query: ')
        search(query, 'clean_collection_lemmatized')
        cont = input('new query? y/n ')
        if cont == 'n':
            break