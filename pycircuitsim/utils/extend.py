import numpy as np


def diagonalize(a, b):
    n11, n12 = a.shape
    n21, n22 = b.shape

    return np.concatenate((
        np.concatenate((a, np.zeros((n11, n22))), axis=1),
        np.concatenate((np.zeros((n21, n12)), b), axis=1),
    ))
