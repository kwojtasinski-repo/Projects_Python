from time import time
import numpy as np
import matplotlib.pyplot as plot

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

np.random.seed(42)

digits = load_digits()
data = scale(digits.data)

n_samples, n_features = data.shape
n_digits = len(np.unique(digits.target))
labels = digits.target

sample_size = 300

print("n_digits: %d, \t n_samples %d \t n_features %d" % (n_digits, n_samples, n_features))

print(82 * '_')
print('init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette')

def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          %(name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
              name="k-means++", data=data)

bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
              name="random", data=data)

print(82 * '_')

# #############################################################################
# Wizualizacja wynikow

reduced_data = PCA(n_components=2).fit_transform(data)
kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
kmeans.fit(reduced_data)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Ograniczenia wykreslania wykresu przypisanie kolorw itd
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() +1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() +1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Uzyskaj etykiety dla każdego punktu w siatce. Użyj ostatnio wyszkolonego modelu.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()]) # dodanie pkt x- [1,2,3] y- [4,5,6] to po zastoswaniu funkcji [1,4];[2,5];[3,6] itd

# nanies wyniki na wykres
Z = Z.reshape(xx.shape)
plot.figure(1)
plot.clf()
plot.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plot.cm.Paired,
           aspect='auto', origin='lower')

plot.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# wykresl centroids jako bialy X
centroids = kmeans.cluster_centers_
plot.scatter(centroids[:,0], centroids[:,1],
             marker='x', s=169, linewidths=3,
             color='w', zorder=10)

plot.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross')

plot.xlim(x_min,x_max)
plot.ylim(y_min,y_max)
plot.xticks(())
plot.yticks(())
plot.show()
