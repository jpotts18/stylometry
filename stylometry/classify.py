from __future__ import division
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.decomposition import PCA, KernelPCA
from sklearn.tree import export_graphviz
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from IPython.display import Image
import StringIO, pydot
from extract import StyloCorpus
from pkgutil import get_data
import random
import os


class StyloClassifier(object):
	def __init__(self,corpus,num_train=-1,num_val=-1,pred_col='Author'):
		self.corpus = corpus
		print("Reading corpus data...")
		if isinstance(corpus,str):
			csv_file = corpus
		elif isinstance(corpus,StyloCorpus):
			csv_file = StringIO.StringIO(self.corpus.output_csv())
		else:
			raise ValueError('Must input either corpus or csv_path.')
		self.data_frame = pd.read_csv(csv_file)
		if num_train > len(self.data_frame) or num_val > len(self.data_frame):
			raise ValueError('num_train + num_val must equal the number of documents in your corpus.')
		if num_train == -1 and num_val == -1:
			self.num_train = int(4*len(self.data_frame)/5)
			self.num_val = len(self.data_frame) - self.num_train
		elif num_train == -1 and num_val > -1:
			self.num_val = num_val
			self.num_train = len(self.data_frame) - self.num_val
		elif num_train > -1 and num_val == -1:
			self.num_train = num_train
			self.num_val = len(self.data_frame) - self.num_train
		elif num_train > -1 and num_val > -1:
			self.num_train = num_train
			self.num_val = num_val
		if self.num_train + self.num_val != len(self.data_frame):
			raise ValueError('num_train + num_val must equal the number of documents in your corpus.')
		self.data_frame['Author_Orig'] = self.data_frame['Author']
		self.data_frame['Author'] = pd.factorize(self.data_frame['Author'])[0]
		self.pred_col = pred_col
		self.cols = [c for c in self.data_frame.columns if c not in (self.pred_col,'Title','Author_Orig')]

class StyloDecisionTree(StyloClassifier):
	def __init__(self,corpus,num_train=-1,num_val=-1,pred_col='Author',unknown_author=None,criterion='gini',splitter='best',
		max_depth=None,max_features=None,min_samples_split=2,min_samples_leaf=1,
		max_leaf_nodes=None,random_state=None):
		# Create classifier
		StyloClassifier.__init__(self,corpus,num_train,num_val,pred_col)
		self.classifier = DecisionTreeClassifier(criterion=criterion,splitter=splitter,max_depth=max_depth,
			max_features=max_features,min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf,
			max_leaf_nodes=max_leaf_nodes,random_state=random_state)
		# Create dataset
		self.X = self.data_frame[self.cols].values
		self.y = self.data_frame[self.pred_col].values
		if not unknown_author:
			rs = 42
			if random_state != None:
				rs = random_state
			self.Xr, self.Xt, self.yr, self.yt = train_test_split(self.X, self.y, train_size=self.num_train, test_size=self.num_val, random_state=rs)
		else:
			self.Xt = self.data_frame.loc[self.data_frame["Author_Orig"] == unknown_author][self.cols].values
			self.Xr = self.data_frame.loc[self.data_frame["Author_Orig"] != unknown_author][self.cols].values
			self.yt = self.data_frame.loc[self.data_frame["Author_Orig"] == unknown_author][self.pred_col].values
			self.yr = self.data_frame.loc[self.data_frame["Author_Orig"] != unknown_author][self.pred_col].values

	def fit(self,check_input=True,sample_weight=None):
		self.classifier.fit(self.Xr,self.yr,check_input,sample_weight)

	def predict(self,corpus=None):
		if not corpus:
			self.ypred = self.classifier.predict(self.Xt)
		else:
			if isinstance(corpus,str):
				csv_file = corpus
			elif isinstance(corpus,StyloCorpus):
				csv_file = StringIO.StringIO(self.corpus.output_csv())
			else:
				raise ValueError('Must input either corpus or csv_path.')
			test_frame = pd.read_csv(csv_file)
			test_frame['Author'] = pd.factorize(test_frame['Author'])[0]
			Xt = test_frame[self.cols].values
			self.ypred = self.classifier.predict(Xt)
		return self.ypred
			
	def confusion_matrix(self):
		# return pd.crosstab(self.yt, self.ypred, rownames=['actual'],colnames=['prediction'])
		return (confusion_matrix(self.yt, self.ypred), accuracy_score(self.yt, self.ypred))

	def output_image(self,path):
		dot_data = StringIO.StringIO()
		export_graphviz(self.classifier, feature_names=self.cols, out_file=dot_data)
		graph = pydot.graph_from_dot_data(dot_data.getvalue())
		graph.write_png(path)


