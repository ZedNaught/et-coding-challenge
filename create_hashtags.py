#!/usr/bin/env python

"""
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
"""

import argparse
import functools
import json
import os
import reprlib
import sys

import text_utils


__author__ = "Alexander Reyes"
__email__ = "alex.reyes.inbox@gmail.com"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Counts word frequency across input documents and remembers the documents and sentences in which the words occurred. Results are output as JSON.")
    parser.add_argument('input_dir',
                        help="directory containing input txt files")
    parser.add_argument('output_filename',
                        help="name of output JSON file")
    parser.add_argument('-d', '--disable-default-stop-words', action='store_true',
                        help="by default, a list of \"stop words\" is used to exclude common words from the output; use this flag to include them")
    parser.add_argument('-s', '--stop-words-file',
                        help="name of file containing comma-separated stop words to be used (in addition to default stop words, if enabled)")
    args = parser.parse_args(argv)

    # process args and perform related setup
    documents = get_document_dicts(args.input_dir)
    stop_words = []
    if not args.disable_default_stop_words:
        stop_words += list(text_utils.get_default_stop_words())
    if args.stop_words_file:
        with open(args.stop_words_file, 'r', encoding='utf8') as f:
            stop_words += [word.strip() for word in f.read().split(',')]

    hc = HashtagCreator(documents, stop_words=stop_words)
    hc.create_hashtags()
    hc.output_results_to_file(args.output_filename)


def get_document_dicts(input_dir):
    input_dir_entries = [entry for entry in os.scandir(input_dir) if entry.name.endswith('.txt')]

    def _get_document_text(filepath):
        with open(filepath, 'r', encoding='utf8') as f:
            return f.read()

    documents = [{
        'name': dir_entry.name,
        'get_text': functools.partial(_get_document_text, dir_entry.path),
    } for dir_entry in input_dir_entries]

    return documents


class HashtagResult:
    """
    Stores and manages "hashtag" information for a specific word, i.e. the
    number of occurrences and the documents and sentences in which it occurs.
    """
    def __repr__(self):
        return 'HashtagResult("{word}")'.format(word=self.word)

    def __str__(self):
        return '{word}: {count} occurrences, {num_docs} documents, {num_sentences} sentences'.format(
            word=self.word,
            count=self.count,
            num_docs=len(self.documents),
            num_sentences=len(self.sentences))

    def __init__(self, word):
        self._word = word
        self._documents = []
        self._sentences = []
        self._count = 0

    @property
    def count(self):
        return self._count

    @property
    def word(self):
        return self._word

    @property
    def documents(self):
        return list(self._documents)

    @property
    def sentences(self):
        return list(self._sentences)

    def _update_documents(self, document_name):
        if document_name not in self._documents:
            self._documents.append(document_name)

    def _update_sentences(self, sentence):
        """
        We don't repeatedly list the same sentence (e.g. if a word occurs
        multiple times in a sentence) but do allow sentences to be repeated
        later.

        Depending on exact output requirements, this could be
        adjusted prevent duplicate sentences altogether.
        """
        if not self._sentences or self._sentences[-1] != sentence:
            self._sentences.append(sentence)

    def add_occurrence(self, document_name, sentence):
        """
        Register a new occurrence of this result's word in the given
        document and sentence.
        """
        self._count += 1
        self._update_documents(document_name)
        self._update_sentences(sentence)

    def as_serializable_dict(self):
        return {
            'Word': self.word,
            'Count': self.count,
            'Documents': self.documents,
            'Sentences containing the word': self.sentences
        }


class HashtagCreator:
    """
    Creates HashtagResults from specified input files and provides a method
    for outputting the results to file.
    """
    def __repr__(self):
        return '<HashtagCreator({input_filepaths}, stop_words={stop_words})>'.format(
            input_filepaths=reprlib.repr([document['name'] for document in self._documents]),
            stop_words=reprlib.repr([self._stop_words]))

    def __init__(self, documents, stop_words=None):
        self._documents = documents
        self._results = {}
        self._stop_words = set(stop_words) if stop_words is not None else set()

    def _get_hashtag_result(self, word):
        if word not in self._results:
            self._results[word] = HashtagResult(word)
        return self._results[word]

    def _get_sorted_results(self):
        # sort first by word count, then by dictionary order of words
        return sorted(self._results.values(), key=lambda result: (-result.count, result.word))

    def create_hashtags(self):
        for document in self._documents:
            self.process_document_hashtags(document)

    def process_document_hashtags(self, document):
        sentences = text_utils.split_into_sentences(document['get_text']())
        for sentence in sentences:
            raw_words = text_utils.split_into_words(sentence)
            normalized_words = map(text_utils.normalize_word, raw_words)
            filtered_normalized_words = filter(
                lambda word: word and word not in self._stop_words,
                normalized_words)
            for word in filtered_normalized_words:
                hashtag_result = self._get_hashtag_result(word)
                hashtag_result.add_occurrence(document['name'], sentence)

    def get_results_table(self):
        return [
            result.as_serializable_dict() for result in self._get_sorted_results()
        ]

    def output_results_to_file(self, filename):
        results_table = self.get_results_table()
        output_dict = {
            'stop_words': sorted(self._stop_words),
            'results': results_table,
        }
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(output_dict, f, indent=2)


if __name__ == '__main__':
    main(sys.argv[1:])
