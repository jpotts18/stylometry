from __future__ import division

import nltk
from nltk import sent_tokenize, word_tokenize, Text
from nltk.probability import FreqDist

class Stylo(object):

    def term_per_thousand(self, term, fdist):
        """
        
        term       X
        -----  = ------
          N       1000
        
        """
        return (fdist[term] * 1000) / fdist.N()

    def mean_sentence_len(self, doc):
        sentences = sent_tokenize(doc)
        sentence_chars = [ len(sent) for sent in sentences]
        return sum(sentence_chars) / float(len(sentence_chars))

    def mean_word_len(self, doc):
        words = set(word_tokenize(doc))
        word_chars = [ len(word) for word in words]
        return sum(word_chars) /  float(len(word_chars))

    def type_token_ratio(self, text):
        return (len(set(text)) / len(text)) * 100

    def mean_document_len(self, doc):
        sentences = sent_tokenize(doc)
        sentence_chars = [ len(sent) for sent in sentences]
        return sum(sentence_chars)


# raw = open("gen1.txt", "r").read()
# raw = open("stylometry.txt", "r").read()
raw = open("theprince.txt", "r").read()

stylo = Stylo()

tokens = word_tokenize(raw)
text = Text(tokens)
fdist = FreqDist(text)

print ""
print ">>> Phraseology Analysis <<<"
print ""
print "Lexical diversity        :", stylo.type_token_ratio(text)
print "Mean Word Length         :", stylo.mean_word_len(raw)
print "Mean Sentence Length     :", stylo.mean_sentence_len(raw)
print "STDEV Sentence Length    : Not Supported"
print "Mean paragraph Length    : Not Supported"
print "Document Length          :", stylo.mean_document_len(raw)
print ""
print ">>> Punctuation Analysis (per 1000 tokens) <<<"
print ""
print 'Commas                   :', stylo.term_per_thousand(',', fdist)
print 'Semicolons               :', stylo.term_per_thousand(';', fdist)
print 'Quotations               :', stylo.term_per_thousand('\"', fdist)
print 'Exclamations             :', stylo.term_per_thousand('!', fdist)
print 'Colons                   :', stylo.term_per_thousand(':', fdist)
print 'Hyphens                  :', stylo.term_per_thousand('-', fdist) # m-dash or n-dash?
print 'Double Hyphens           :', stylo.term_per_thousand('--', fdist) # m-dash or n-dash?
print ""
print ">>> Lexical Usage Analysis (per 1000 tokens) <<<"
print ""
print 'and                      :', stylo.term_per_thousand('and', fdist)
print 'but                      :', stylo.term_per_thousand('but', fdist)
print 'however                  :', stylo.term_per_thousand('however', fdist)
print 'if                       :', stylo.term_per_thousand('if', fdist)
print 'that                     :', stylo.term_per_thousand('that', fdist)
print 'more                     :', stylo.term_per_thousand('more', fdist)
print 'must                     :', stylo.term_per_thousand('must', fdist)
print 'might                    :', stylo.term_per_thousand('might', fdist)
print 'this                     :', stylo.term_per_thousand('this', fdist)
print 'very                     :', stylo.term_per_thousand('very', fdist)
