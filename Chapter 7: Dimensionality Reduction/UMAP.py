import umap
import numpy as np
from scipy.stats import ortho_group
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D



#paramaterize a sphere
def get_sphere(N, r, dim):
    u = np.random.normal(0, 1, (N, dim))
    norm = np.linalg.norm(u, axis = 1)
    return r * u/norm[:, None]

#initialize params
orth = ortho_group.rvs(100)
orth3 = orth[0:3, :] #3 dimensional subframe
N = 1000 #points

sphere = get_sphere(N, 5, 3)

#rotate into 100 dimesnional space
X = np.matmul(sphere, orth3)

#UMAP algorithm
model = umap.UMAP(
    n_neighbours = 50,
    min_dist = 0.1,
    n_compnents = 3,
    metric = 'euclidean'
)
u = model.fit_transform(X)

fig_umap = plt.figure()
ax_umap = fig_umap.add_subplot(111, prjection = '3d')

c = np.zeros_like(sphere)
c[:, 0] = ((sphere[:,0]))
c[:, 1] = ((sphere[:,1]))
c[:, 2] = ((sphere[:,2]))

for i in range(N):
    color = matplotlib.colors.to_hex(c[i,:])
    ax_umap.scatter3D(u[i,0], u[i,1], u[i, 2], c = color)

plt.show()