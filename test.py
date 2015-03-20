import random
import unittest
import os
from extract import StyloDocument

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test/oliver_twist_fixture.txt')
        self.doc = StyloDocument(path)

    def test_is_stylo_doc(self):
        self.assertIsInstance(self.doc, StyloDocument)
    
    def test_initial_member_paragraphs(self):
        self.assertEqual(len(self.doc.paragraphs), 187)

    def test_initial_member_sentence_word_length(self):        
        self.assertEqual(sum(self.doc.paragraph_word_length), 8690)
    
    def test_initial_member_sentences(self):
        self.assertEqual(len(self.doc.sentences), 426)

    def test_initial_member_tokens(self):
        self.assertEqual(len(self.doc.tokens),10471)

    def test_initial_member_sentence_chars(self):        
        self.assertEqual(sum(self.doc.sentence_chars), 49230)

    def test_initial_member_sentence_word_length(self):        
        self.assertEqual(sum(self.doc.sentence_word_length, 49230))

    def test_mean_sentence_len(self):
        self.assertAlmostEqual(self.doc.mean_sentence_len(), 20.401408450704224)
        self.assertAlmostEqual(self.doc.mean_word_len(), 6.563677130044843)
        self.assertAlmostEqual(self.doc.type_token_ratio(), 21.296915289848155)




    # def test_shuffle(self):
    #     self.document.
    #     # make sure the shuffled sequence does not lose any elements
    #     random.shuffle(self.seq)
    #     self.seq.sort()
    #     self.assertEqual(self.seq, range(10))

    #     # should raise an exception for an immutable sequence
    #     self.assertRaises(TypeError, random.shuffle, (1,2,3))

    # def test_choice(self):
    #     element = random.choice(self.seq)
    #     self.assertTrue(element in self.seq)

    # def test_sample(self):
    #     with self.assertRaises(ValueError):
    #         random.sample(self.seq, 20)
    #     for element in random.sample(self.seq, 5):
    #         self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()