import numpy as np
from scipy.stats import ortho_group
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import umap

#get N random points on a sphere
def get_sphere(N, r, dim):
    u = np.random.normal(0, 1, (N, dim))
    norm = np.linalg.norm(u, axis = 1)
    return r * u/norm[:, None]


def get_mobius(N, r, R):
    # Generate random angles and radii
    angles = np.random.uniform(0, 2*np.pi, size=N)
    rs = np.random.uniform(r, R, size=N)
    
    # Calculate x, y, z coordinates of points on a circle
    x = (R + rs*np.cos(angles/2.0)) * np.cos(angles)
    y = (R + rs*np.cos(angles/2.0)) * np.sin(angles)
    z = rs*np.sin(angles/2.0)
    
    # Shift the x and y coordinates to connect the ends
    x = x + z*np.cos(angles/2.0)
    y = y + z*np.sin(angles/2.0)
    
    return np.vstack([x, y, z]).T


def sphere_experiment(N, r, dim):
    #initialize params
    orth = ortho_group.rvs(100)
    orth3 = orth[0:3, :] #3 dimensional subframe

    sphere = get_sphere(N, r, dim)

    #rotate into 100 dimesnional space
    X = np.matmul(sphere, orth3)

    #UMAP algorithm
    model = umap.UMAP(
        n_neighbors = 50,
        min_dist = 0.1,
        n_components = 3,
        metric = 'euclidean'
    )
    u = model.fit_transform(X)

    fig_umap = plt.figure()
    ax_umap = fig_umap.add_subplot(111, projection = '3d')

    c = np.zeros_like(sphere)
    c[:, 0] = ((sphere[:,0]+r)/(2*r))
    c[:, 1] = ((sphere[:,1]+r)/(2*r))
    c[:, 2] = ((sphere[:,2]+r)/(2*r))

    for i in range(N):
        color = matplotlib.colors.to_hex(c[i,:])
        ax_umap.scatter3D(u[i,0], u[i,1], u[i, 2], c = color)

    plt.show()
    return


def mobius_experiment(N, r, R):
    #initialize params
    orth = ortho_group.rvs(100)
    orth3 = orth[0:3, :] #3 dimensional subframe


    mobius = get_mobius(N, r, R)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(mobius[:,0], mobius[:,1], mobius[:,2], '.', markersize=1)
    plt.show()

    #rotate into 100 dimesnional space
    X = np.matmul(mobius, orth3)

    #UMAP algorithm
    model = umap.UMAP(
        n_neighbors = 50,
        min_dist = 0.1,
        n_components = 3,
        metric = 'euclidean'
    )
    u = model.fit_transform(X)

    fig_umap = plt.figure()
    ax_umap = fig_umap.add_subplot(111, projection = '3d')

    c = np.zeros_like(mobius)
    c[:, 0] = (np.abs((mobius[:,0]+ r + R)/(2*(r+R))))
    c[:, 1] = (np.abs((mobius[:,1]+ r + R)/(2*(r+R))))
    c[:, 2] = (np.abs((mobius[:,2]+ r + R)/(2*(r+R))))

    for i in range(N):
        color = matplotlib.colors.to_hex(c[i,:])
        ax_umap.scatter3D(u[i,0], u[i,1], u[i, 2], c = color)

    plt.show()
    return


sphere_experiment(1000, 5, 3)

#mobius_experiment(1000, 1, 2)
