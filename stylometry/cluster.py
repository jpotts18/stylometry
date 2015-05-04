from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from sklearn.decomposition import PCA, KernelPCA
from stylometry.classify import StyloClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split

class StyloKMeans(StyloClassifier):
	def __init__(self,corpus,num_train=-1,num_val=-1,n_components=2,kernel=None,random_state=None,
		n_clusters=-1,max_iter=300,n_init=10,init='k-means++',precompute_distances=True,tol=1e-4,n_jobs=1):
		self.kernel = kernel
		self.n_components = n_components
		StyloClassifier.__init__(self,corpus,num_train=num_train,num_val=num_val)
		if n_clusters < 0:
			n_clusters = len(set(self.data_frame["Author"]))
		self.stylo_pca = StyloPCA(corpus,n_components=n_components,kernel=kernel)
		self.k_means = KMeans(n_clusters=n_clusters,n_init=n_init,init=init,
			precompute_distances=precompute_distances,tol=tol,n_jobs=n_jobs)
		rs = 42
		self.X = self.data_frame[self.cols].values
		self.y = self.data_frame[self.pred_col].values
		if random_state != None:
			rs = random_state
		self.Xr, self.Xt, self.yr, self.yt = train_test_split(self.X, self.y, train_size=self.num_train, test_size=self.num_val, random_state=rs)

	def fit(self):
		self.k_means.fit(self.stylo_pca.pca_data)

	def predict(self,corpus):
		test_pca = StyloPCA(corpus,n_components=self.n_components,kernel=self.kernel)
		self.ypred = self.k_means.predict(test_pca.pca_data)
		return self.ypred

	def plot_clusters(self):
		self.stylo_pca.create_plot_pca()
		centroids = self.k_means.cluster_centers_
		inert = self.k_means.inertia_
		plt.scatter(centroids[:, 0], centroids[:, 1],
		   marker='x', s=169, linewidths=3,
		   color='red', zorder=8)
		plt.show()

class StyloPCA(StyloClassifier):
	def __init__(self,corpus,n_components=2,kernel=None):
		StyloClassifier.__init__(self,corpus)
		data = self.data_frame[self.cols].values
		self.n_components = n_components
		self.kernel = kernel
		if not kernel:
			self.pca = PCA(n_components=self.n_components)
		else:
			self.pca = KernelPCA(kernel=kernel, gamma=10)
		self.pca_data = self.pca.fit_transform(StandardScaler().fit_transform(data))

	def plot_pca(self, out_file=None):
		self.create_plot_pca()
		plt.show()
		# if out_file:
		# 	plt.savefig(out_file)

	def create_plot_pca(self):
		plt.figure(1)
		plt.clf()
		all_authors = set(self.data_frame["Author"])
		for a in all_authors:
			rows = self.data_frame.loc[self.data_frame["Author"] == a]
			indices = self.data_frame.loc[self.data_frame["Author"] == a].index
			plt.plot(self.pca_data[indices,0],self.pca_data[indices,1], 'o', markersize=7,\
				color=(random.random(),random.random(),random.random()), alpha=0.5, label=rows["Author_Orig"][indices[0]])
		
		plt.xlabel(self.cols[0])
		plt.ylabel(self.cols[1])
		plt.legend()
		plt.title('Transformed stylometry data using PCA')

	def plot_explained_variance(self, out_file=None):
		self.create_plot_explained_variance()
		plt.show()

	def create_plot_explained_variance(self):
		if not self.kernel:
			evr = self.pca.explained_variance_
		else:
			evr = self.pca.lambdas_
		print evr
		fig = plt.figure()
		ax = fig.add_subplot(111)
		tot = sum(evr)
		var_exp = [(i / tot)*100 for i in sorted(evr, reverse=True)]
		cum_var_exp = np.cumsum(var_exp)
		plt.plot(range(1,len(cum_var_exp)+1),cum_var_exp, 'b*-')
		width = .8
		plt.bar(range(1,len(var_exp)+1), var_exp, width=width)
		# ax.set_xticklabels()
		plt.grid(True)
		ax.set_ylim((0,110))
		plt.xlabel('n_components')
		plt.ylabel('Percentage of variance explained')
		plt.title('Variance Explained vs. n_components')