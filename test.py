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

    def test_csv_header(self):
        self.assertEqual(StyloDocument.csv_header(),'Author,Title,LexicalDiversity,MeanWordLen,MeanSentenceLen,StdevSentenceLen,MeanParagraphLen,DocumentLen,Commas,Semicolons,Quotes,Exclamations,Colons,Dashes,Mdashes,Ands,Buts,Howevers,Ifs,Thats,Mores,Musts,Mights,This,Verys')

if __name__ == '__main__':
    unittest.main()