import os
import string

import nltk
# ensure NLTK data path is specified
assert 'NLTK_DATA' in os.environ, "You must specify environment variable NLTK_DATA (see README.txt)"


def normalize_word(word):
    return (
        word.replace('“', '"')
            .replace('”', '"')
            .replace("‘", "'")
            .replace("’", "'")
            .strip(string.punctuation + string.whitespace)
            .lower()
    )


def split_into_sentences(text):
    return nltk.sent_tokenize(text)


def split_into_words(text):
    return text.split(' ')


def get_default_stop_words():
    from nltk.corpus import stopwords
    return stopwords.words('english')
