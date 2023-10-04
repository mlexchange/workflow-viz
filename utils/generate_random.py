import numpy as np
from scipy.stats import multivariate_normal as mvn


def generate_zeros(width, height):
    data = np.zeros((height, width))
    return data


def generate_random(width, height):
    np.random.seed(0)
    data = np.random.rand(height, width)

    # Add one gaussian blob
    y, x = np.mgrid[0 : 1 : height * 1j, 0 : 1 : width * 1j]
    pos = np.dstack((x, y))
    v = mvn([0.5, 0.2], [[2.0, 0.3], [0.3, 0.5]])
    data = data + v.pdf(pos) * 2
    return data
