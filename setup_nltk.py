import os

import nltk

assert 'NLTK_DATA' in os.environ, "You must specify environment variable NLTK_DATA (see README.txt)"
print("downloading NLTK packages 'punkt' and 'stopwords'...")
nltk.download('punkt')
nltk.download('stopwords')
