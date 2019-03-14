"""
This module provides some helper functions\
to fetch data from an dsebaseapp instance to create word embeddings
run something like:
from enrich.spacy_utils.vecs import stream_docs_to_file, create_word_vecs
domain = "http://127.0.0.1:8080"
app_name = "akademie"
filename = stream_docs_to_file(domain, app_name, verbose=False)
create_word_vecs(filename)
"""

from gensim.models import Word2Vec
from gensim.utils import simple_preprocess


def read_input(input_file):
    """ yields preprocessed lines read from a file (document per line)
        :input_file: Name of the file to process
        :return: yields processed lines of file
    """

    with open(input_file, encoding="utf-8") as f:
        for line in f:
            yield simple_preprocess(line)


def create_word_vecs(input_file, size=300, window=5, min_count=2, workers=4):
    """ creates word embeddings
        :input_file: Name of the file to process
        :size: The number of dimensions of the embedding
        :window: The maximum distance between a target word and words around the target word.
        :min_count: The minimum count of words to consider when training the models
        :workers: The number of threads to use while training.
    """
    documents = read_input(input_file)
    model = Word2Vec(
        [x for x in documents],
        size=size, window=window, min_count=min_count, workers=workers
    )
    model_file_name = "{}.word2vec.model".format(input_file)
    model.wv.save_word2vec_format(model_file_name)
    return model_file_name
