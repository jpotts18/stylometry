# Stylometry

**USE AS REFERENCE, NO FUTURE DEVELOPMENT PLANNED**

This was a fun play project that I put together with [@arogers1](https://github.com/arogers1) while learning some NLP. It was a fun exploration in extracting features from text.

## What is Stylometry?

Stylometry is the application of the study of linguistic style, usually to written language, but it has successfully been applied to music and to fine-art paintings as well.

Stylometry is often used to attribute authorship to anonymous or disputed documents. Stylometry has legal, academic, and literary applications, which include determination of the true authorship of some of Shakespeare's works and forensic linguistics.

## Why write a library?

Even after hours of searching through Python libraries, I was unable to find one that seemed to fit my needs.

But soon, I stumbled upon a captivating research paper about applying machine learning techniques to stylometry. In addition, I came across an awesome library that provied the foundation for statistical analysis of raw text data: the Natural Language Tooklit Library, or NLTK. Based on this foundation, I decided to write a simple library that could specifically handle stylometry.

The initial version of the software took only about 3 hours in development but still allowed me to extract a wide variety of features from text data. The library has since been extended into several different facets.

## How to set up the software

1. Mac users must set up some special system dependencies:

```bash
brew install graphviz
```

1. Install necessary packages from requirements.txt:
```bash
pip install -r requirements.txt
```
2. Additionally, install the NLTK `punkt` tokenizer: 
```python
import nltk
nltk.download('punkt')
```

3. If you get this error, ``Couldn't import dot_parser, loading of dot files will not be possible.``, do this:

```bash
pip uninstall pydot
pip uninstall pyparsing
pip install -Iv https://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.7.tar.gz
pip install pydot
```

## How to prepare text data

1. Download some text from Gutenberg Project.
2. Clean up the text files by removing table of contents, licenses, etc.
3. Split the file into 1000 line samples using ``split -l 1000 hamlet.txt -d``. To rename the output files, consider using ``split --numeric-suffixes=1 --additional-suffix=.csv -l 1000 hamlet.txt hamlet_``.
4. After preparation, you may rebuild the original data using this command: ``cat book-0.txt book-1.txt book-2.txt > entire-book.txt``.

Make sure that every author have a similar number of lines and samples to analyze. For example,

| Title | Author | Lines | Samples |
--- | --- | --- | ---
| Pride and Prejudice | Jane Austen | 13024 | 13 |
| Tale of Two Cities | Charles Dickens | 14496 | 14 |
| Romeo & Juliet Hamlet | William Shakespeare | 11077 | 11 |
| The Adventures of Huckleberry Finn | Mark Twain | 11433 | 10 |
| War and Peace - *Only Books 1 & 2* | Leo Tolstoy | 10517 | 11 |

## Demo

Download the repositories

```bash
$ git clone git@github.com:jpotts18/stylometry.git
$ git clone git@github.com:jpotts18/stylometry-data.git

$ ipython
```
Extract stylometry features from one document

```python
from stylometry.extract import *
dickens1 = StyloDocument('stylometry-data/Dickens/tale-two-cities-0.txt')
dickens1.text_output()
```
Extract stylometry features from a set of documents called a corpus

```python
import stylometry

# Single Author Corpus
dickens_corpus = StyloCorpus.from_glob_pattern('stylometry-data/Dickens/*.txt')
dickens_corpus.output_csv('/Users/jpotts18/Desktop/dickens.csv')

# All authors
novel_corpus = StyloCorpus.from_glob_pattern('stylometry-data/*/*.txt')
novel_corpus.output_csv('/Users/jpotts18/Desktop/novels.csv')
```

Decision Tree Classificaiton

```python
from stylometry.classify import *
# splits data into validation and training default 80% train 20% validation
dtree = StyloDecisionTree('/Users/jpotts18/Desktop/novels.csv')
# fit the decision tree to the data
dtree.fit()
# predict the authorship of the validation set
dtree.predict()
# Show the confusion matrix and accuracy of the validation prediction
dtree.confusion_matrix()
# Write the decision tree to an image file
dtree.write_tree('tree.png')
```

Clustering and PCA

```python
from stylometry.cluster import *
# Create a KMeans clusterer and run PCA on the data
kmeans = StyloKMeans('/Users/jpotts18/Desktop/novels.csv')
# Cluster the PCA'd data using K-means
kmeans.fit()
# Shot the plot of explained variance per principle component
kmeans.stylo_pca.plot_explained_variance()
# Show the plot of the PCA'd data with the cluster centroids
kmeans.plot_clusters()
```



