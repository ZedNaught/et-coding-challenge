import os

import nltk

assert 'NLTK_DATA' in os.environ, "You must specify environment variable NLTK_DATA (see README.txt)"
print("downloading required NLTK package 'punkt'")
nltk.download('punkt')
