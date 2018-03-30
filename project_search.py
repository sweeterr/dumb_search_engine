__authors__ = 'Marija Aleksejeva, Daniil Kolomeitsev, Jevgenij Mozajev,' \
              ' Nina Mustafina, Svetlana Pavlova'

# This module creates tf-idf vector representation of the corpus and
# a query, computes cosine similarity between the vector of the query
# and the vectors of the texts in the corpus, and prints file names of
# the 10 most relevant documents.

             
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import numpy as nm
import pandas as pd
from project_lemmatize import lemmatize_text
from project_lemmatize import lemmatize_req


# This function renames 9 files from '1.txt' to '01.txt' to preserve correct
# document order.
def rename_files(path):
    for num in range(10)[1:]:
        pathToFolder = os.path.join(path, '0')
        try:
            os.rename(os.path.join(pathToFolder, str(num) + '.txt'),
                      os.path.join(pathToFolder, '0' + str(num) + '.txt'))
        except:
            continue


# This function reads file, returns text.
def f_read(filename):
    f = open(filename, 'r', encoding = 'utf-8-sig')
    text = f.read()
    f.close()
    return text

    
# This function returns a list of all texts in a given directory and
# its subdirectories.
def return_texts(path):
    texts = []
    for i in os.walk(path):
        for filename in i[2]:
            text = f_read(os.path.join(i[0], filename)).strip().split('\n')
            text = ' '.join(text[1:])
            texts.append(text)
    return texts
    

# This function takes a list of texts and a list of stopwords, makes
# a matrix of tf-idfs of texts (rows = documents, columns = tokens),
# and returns a tf-idfVectorizer class object.
def return_tfidf_docs(texts, swords):     
    ##создает объект векторайзера       
    tfidf_vectorizer = TfidfVectorizer(stop_words=swords)
    ##создает матрицу-векторное пространство текстов корпуса
    docs_matrix = tfidf_vectorizer.fit_transform(texts)    
    return tfidf_vectorizer, docs_matrix

    
# This function converts query to a tf-idf query matrix.
def return_tfidf_query(query, tfidf_vectorizer):
    ##представляет запрос в виде вектора в том же пространстве
    query_matrix = tfidf_vectorizer.transform(query)
    return query_matrix


# This function measures cosine similarity between query and documents,
# returns indices of 10 most relevant documents.
def return_relevant_indices(docs_matrix, query_matrix):    
    cosim = cosine_similarity(query_matrix, docs_matrix)
    indices = cosim.nonzero()[1]
    values = cosim.take(indices)
    df = pd.DataFrame(data=values, index=indices)
    dfSorted = df.sort(0, ascending=False)
    return dfSorted[0:10].index.tolist()


# This function converts indices of documents into their file names.
def return_filenames(indices):
    filenames = list(map(lambda x: str(x) + '.txt', indices))
    return filenames


# This function prints out file names.
def print_filenames(filenames):
    for i in range(len(filenames)):
        print(str(i + 1)+' - ' + filenames[i])
        for root, dirs, files in os.walk('clean_collection'):
            for file in files:
                if file == filenames[i]:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        print(f.readline())


# This is the main search function. It takes a string containing
# the path to lemmatized document collection, a query string, and
# initializes the search of the documents most relevant to the query,
# and the print out of the file names.
def search(query, path):
    rename_files(path)
    rename_files('clean_collection')
    swords = stopwords.words('russian')
    texts = return_texts(path)
    tfidf_vectorizer, docs_matrix = return_tfidf_docs(texts,
                                                      swords)
    query = [lemmatize_req(query)]
    query_matrix = return_tfidf_query(query, tfidf_vectorizer)
    indices = return_relevant_indices(docs_matrix,
                                       query_matrix)
    filenames = return_filenames(indices)
    print_filenames(filenames)
