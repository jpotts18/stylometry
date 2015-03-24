from __future__ import division
import pytz
import glob

import nltk
from nltk import sent_tokenize, word_tokenize, Text
from nltk.probability import FreqDist
import numpy as np

DEFAULT_AUTHOR = "Unknown"

class StyloDocument(object):

    def __init__(self, file_name, author=DEFAULT_AUTHOR):
        self.doc = open(file_name, "r").read().decode(encoding='utf-8', errors='ignore')
        self.author = author
        self.file_name = file_name
        self.tokens = word_tokenize(self.doc)
        self.text = Text(self.tokens)
        self.fdist = FreqDist(self.text)
        self.sentences = sent_tokenize(self.doc)
        self.sentence_chars = [ len(sent) for sent in self.sentences]
        self.sentence_word_length = [ len(sent.split()) for sent in self.sentences]
        self.paragraphs = [p for p in self.doc.split("\n\n") if len(p) > 0 and not p.isspace()]
        self.paragraph_word_length = [len(p.split()) for p in self.paragraphs]

    @classmethod
    def csv_header(cls):
        return (
            'Author,Title,LexicalDiversity,MeanWordLen,MeanSentenceLen,StdevSentenceLen,MeanParagraphLen,DocumentLen,'
            'Commas,Semicolons,Quotes,Exclamations,Colons,Dashes,Mdashes,'
            'Ands,Buts,Howevers,Ifs,Thats,Mores,Musts,Mights,This,Verys'
        )

    def term_per_thousand(self, term):
        """
        term       X
        -----  = ------
          N       1000
        """
        return (self.fdist[term] * 1000) / self.fdist.N()

    def mean_sentence_len(self):
        return np.mean(self.sentence_word_length)

    def std_sentence_len(self):
        return np.std(self.sentence_word_length)

    def mean_paragraph_len(self):
        return np.mean(self.paragraph_word_length)
        
    def std_paragraph_len(self):
        return np.std(self.paragraph_word_length)

    def mean_word_len(self):
        words = set(word_tokenize(self.doc))
        word_chars = [ len(word) for word in words]
        return sum(word_chars) /  float(len(word_chars))

    def type_token_ratio(self):
        return (len(set(self.text)) / len(self.text)) * 100

    def document_len(self):
        return sum(self.sentence_chars)

    def csv_output(self):
        return '"%s","%s",%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g' % (
            self.author, 
            self.file_name, 
            self.type_token_ratio(), 
            self.mean_word_len(), 
            self.mean_sentence_len(),
            self.std_sentence_len(),
            self.mean_paragraph_len(), 
            self.document_len(),

            self.term_per_thousand(','),
            self.term_per_thousand(';'),
            self.term_per_thousand('\"'),
            self.term_per_thousand('!'),
            self.term_per_thousand(':'),
            self.term_per_thousand('-'),
            self.term_per_thousand('--'),
            
            self.term_per_thousand('and'),
            self.term_per_thousand('but'),
            self.term_per_thousand('however'),
            self.term_per_thousand('if'),
            self.term_per_thousand('that'),
            self.term_per_thousand('more'),
            self.term_per_thousand('must'),
            self.term_per_thousand('might'),
            self.term_per_thousand('this'),
            self.term_per_thousand('very'),
        )

    def text_output(self):
        return """
            Author: %s
            File: %s
        """ % (
            self.file_name,
            self.author
        )
        print "##############################################"
        print ""
        print "Name: ", self.file_name
        print ""
        print ">>> Phraseology Analysis <<<"
        print ""
        print "Lexical diversity        :", stylo.type_token_ratio()
        print "Mean Word Length         :", stylo.mean_word_len()
        print "Mean Sentence Length     :", stylo.mean_sentence_len()
        print "STDEV Sentence Length    :", stylo.std_sentence_len()
        print "Mean paragraph Length    :", stylo.mean_paragraph_len()
        print "Document Length          :", stylo.document_len()
        print ""
        print ">>> Punctuation Analysis (per 1000 tokens) <<<"
        print ""
        print 'Commas                   :', stylo.term_per_thousand(',')
        print 'Semicolons               :', stylo.term_per_thousand(';')
        print 'Quotations               :', stylo.term_per_thousand('\"')
        print 'Exclamations             :', stylo.term_per_thousand('!')
        print 'Colons                   :', stylo.term_per_thousand(':')
        print 'Hyphens                  :', stylo.term_per_thousand('-') # m-dash or n-dash?
        print 'Double Hyphens           :', stylo.term_per_thousand('--') # m-dash or n-dash?
        print ""
        print ">>> Lexical Usage Analysis (per 1000 tokens) <<<"
        print ""
        print 'and                      :', stylo.term_per_thousand('and')
        print 'but                      :', stylo.term_per_thousand('but')
        print 'however                  :', stylo.term_per_thousand('however')
        print 'if                       :', stylo.term_per_thousand('if')
        print 'that                     :', stylo.term_per_thousand('that')
        print 'more                     :', stylo.term_per_thousand('more')
        print 'must                     :', stylo.term_per_thousand('must')
        print 'might                    :', stylo.term_per_thousand('might')
        print 'this                     :', stylo.term_per_thousand('this')
        print 'very                     :', stylo.term_per_thousand('very')
        print ''



class StyloCorpus(object):
    def __init__(self,documents_by_author):
        self.documents_by_author = documents_by_author

    @classmethod
    def from_path_list(cls, path_list, author=DEFAULT_AUTHOR):
        stylodoc_list = cls.convert_paths_to_stylodocs(path_list)
        documents_by_author = {author:stylodoc_list}
        return cls(documents_by_author)

    @classmethod
    def from_stylodoc_list(cls, stylodoc_list, author=DEFAULT_AUTHOR):
        author = DEFAULT_AUTHOR
        documents_by_author = {author:stylodoc_list}
        return cls(documents_by_author)

    @classmethod
    def from_documents_by_author(cls, documents_by_author):
        return cls(documents_by_author)

    @classmethod
    def from_paths_by_author(cls, paths_by_author):
        documents_by_author = {}
        for author, path_list in paths_by_author.iteritems():
            documents_by_author[author] = cls.convert_paths_to_stylodocs(path_list,author)
        return cls(documents_by_author)

    @classmethod
    def convert_paths_to_stylodocs(cls, path_list, author=DEFAULT_AUTHOR):
        stylodoc_list = []
        for path in path_list:
            sd = StyloDocument(path, author)
            stylodoc_list.append(sd)
        return stylodoc_list

    def output_csv(self, author=None, out_file=None):
        csv_data = StyloDocument.csv_header() + '\n'
        if not author:
            for a in self.documents_by_author.keys():
                for doc in self.documents_by_author[a]:
                    csv_data += doc.csv_output() + '\n'
        else:
            for doc in self.documents_by_author[author]:
                csv_data += doc.csv_output() + '\n'
        if out_file:
            with open(out_file,'w') as f:
                f.write(csv_data)
        return csv_data
            
