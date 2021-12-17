import nltk
from nltk.corpus import stopwords
import string
import numpy as np

nltk.download("stopwords")


def cosine_distance(x, y):
    # Check length of x and y
    if len(x) != len(y):
        return None

    # Compute the dot product between x and y
    dot_product = np.dot(x, y)

    # Compute the L2 norms (magnitudes) of x and y
    magnitude_x = np.sqrt(np.sum(x ** 2))
    magnitude_y = np.sqrt(np.sum(y ** 2))

    # Compute the cosine similar_recognition
    cosine_similarity = dot_product / (magnitude_x * magnitude_y)
    return cosine_similarity


def vectorize(tokens, filtered_vocab=None):
    vector = []
    for w in filtered_vocab:
        vector.append(tokens.count(w))
    return vector


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def processing(string_1, string_2):
    # convert them to lower case
    string_1 = string_1.translate(str.maketrans('', '', string.punctuation)).lower()
    string_2 = string_2.translate(str.maketrans('', '', string.punctuation)).lower()

    # create a vocabulary list
    vocab = unique(string_1.split() + string_2.split())

    # filter the vocabulary list
    filtered_vocab = []
    for w in vocab:
        if w not in stopwords.words("russian"):
            filtered_vocab.append(w)

    # convert sentences into vectords
    vector_1 = np.asarray(vectorize(string_1, filtered_vocab=filtered_vocab))
    vector_2 = np.asarray(vectorize(string_2, filtered_vocab=filtered_vocab))

    cosine_similarity = cosine_distance(vector_1, vector_2)
    return round(float(cosine_similarity), 2)
