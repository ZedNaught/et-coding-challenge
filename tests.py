import unittest

import create_hashtags
import text_utils


class TestCreateHashtags(unittest.TestCase):
    def test_without_stop_words(self):
        stop_words = []
        hc = create_hashtags.HashtagCreator(
            create_hashtags.get_document_dicts('test_docs'),
            stop_words=stop_words)
        hc.create_hashtags()

        results_table = hc.get_results_table()
        self.assertTrue(results_table[0]['Word'] == 'the')
        self.assertGreater(results_table[0]['Count'], 1)

    def test_with_stop_words(self):
        stop_words = text_utils.get_default_stop_words()
        self.assertGreater(len(stop_words), 0)
        self.assertIn('the', stop_words)

        hc = create_hashtags.HashtagCreator(
            create_hashtags.get_document_dicts('test_docs'),
            stop_words=stop_words)
        hc.create_hashtags()

        results_table = hc.get_results_table()
        results_table_words = set(result['Word'] for result in results_table)
        self.assertTrue(all(stop_word not in results_table_words for stop_word in stop_words))


if __name__ == '__main__':
    unittest.main()
