import random
import unittest
import os
from extract import StyloDocument

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test/oliver_twist_fixture.txt')
        self.doc = StyloDocument(self.path)

    def test_is_stylo_doc(self):
        self.assertIsInstance(self.doc, StyloDocument)

    def test_doc_has_author(self):
        unknown_doc = StyloDocument(self.path)
        self.assertEqual(unknown_doc.author,"Unknown")

    def test_doc_with_author(self):
        dickens_doc = StyloDocument(self.path, author="Charles Dickens")
        self.assertEqual(dickens_doc.author,"Charles Dickens")        
    
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
        self.assertEqual(sum(self.doc.sentence_word_length), 8691)

    def test_mean_sentence_len(self):
        self.assertAlmostEqual(self.doc.mean_sentence_len(), 20.401408450704224)

    def test_mean_word_len(self):
        self.assertAlmostEqual(self.doc.mean_word_len(), 6.563677130044843)

    def test_type_token_ration(self):
        self.assertAlmostEqual(self.doc.type_token_ratio(), 21.296915289848155)

    def test_csv_output(self):
        out = self.doc.csv_output()
        self.assertTrue("Unknown" in out)
        self.assertTrue("oliver_twist_fixture.txt" in out)
        self.assertTrue("20.4014,19.5202,46.4706" in out)

    def test_csv_header(self):
        out = self.doc.text_output()
        self.assertTrue('Author,Title,LexicalDiversity' in out)
        self.assertTrue('Mights,This,Verys' in out)

if __name__ == '__main__':
    unittest.main()