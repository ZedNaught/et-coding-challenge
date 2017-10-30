Written using Python 3.6 on OS X.

# setup (in project root with virtualenv active)
```bash
pip install -r requirements.txt
mkdir nltk_data
export NLTK_DATA=${PWD}/nltk_data
python setup_nltk.py
```

# running the script
usage: create_hashtags.py [-h] [-d] [-s STOP_WORDS_FILE]
                          input_dir output_filename

Counts word frequency across input documents and remembers the documents and
sentences in which the words occurred. Results are output as JSON.

positional arguments:
  input_dir             directory containing input txt files
  output_filename       name of output JSON file

optional arguments:
  -h, --help            show this help message and exit
  -d, --disable-default-stop-words
                        by default, a list of "stop words" is used to exclude
                        common words from the output; use this flag to include
                        them
  -s STOP_WORDS_FILE, --stop-words-file STOP_WORDS_FILE
                        name of file containing comma-separated stop words to
                        be used (in addition to default stop words, if
                        enabled)
