import random
import unittest2 as unittest
import os
from extract import *
from classify import *

class TestStyloDecisionTree(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #self.corpus = StyloCorpus.from_glob_pattern([os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Shakespeare/*.txt'),os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Poe/*.txt')])
        self.corpus = StyloCorpus.from_paths_by_author(
            {'Shakespeare':[os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Shakespeare/As You Like it.txt'),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Shakespeare/The Tempest.txt'),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Shakespeare/King Richard III.txt')],
            'Poe':[os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Poe/The Raven.txt'),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Poe/The Fall of the House of Usher.txt'),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/Poe/The Masque of the Red Death.txt')]})
        self.dtree = StyloDecisionTree(self.corpus)

    def test_corpus_len(self):
        self.assertTrue(6 == len(self.dtree.data_frame))

    def test_incorrect_corpus_type_throws_exception(self):
        with self.assertRaises(ValueError):
            dtree = StyloDecisionTree(2)

    def test_wrong_train_val_count_throws_exception(self):
        with self.assertRaises(ValueError):
            dtree = StyloDecisionTree(self.corpus,num_train=10)
        with self.assertRaises(ValueError):
            dtree = StyloDecisionTree(self.corpus,num_train=2,num_val=2)

    def test_fit(self):
        self.dtree.fit()

if __name__ == '__main__':
    unittest.main()