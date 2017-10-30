Written using Python 3.6 on OS X.

## Setup (in project root with virtualenv active)
```bash
pip install -r requirements.txt
mkdir nltk_data
export NLTK_DATA=${PWD}/nltk_data
python setup_nltk.py
```

## Running the script
```
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
```

## Notes and considerations
**Stop words**

I elected to enable filtering of "stop words" by default, since the output seemed much less useful with them included. To disable this default filtering, the "-d" flag can be used.

**Splitting text**

Handling all the potential cases of ways sentences can be separated seemed like a sufficiently nontrivial but rote problem to warrant the use of a well-tested solution, hence the inclusion of NLTK. For splitting sentences into words, the simplest solution of splitting on spaces (and stripping whitespace+punctuation) works well enough.

**text_utils.py**

The details of text-processing used in this program were extracted to text_utils.py to allow for easy swapping in case of changes to tokenization, normalization, or stop word specifications.

## Attribution
Default stop words courtesy of https://www.textfixer.com/tutorials/common-english-words.php
