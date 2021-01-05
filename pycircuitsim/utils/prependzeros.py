import numpy as np


def prepend_zeros(a, n_zeros: int = None, axis: int = None):
    if n_zeros is None:
        n_zeros = 1

    if axis is None:
        axis = 1

    if axis == 1:
        return np.concatenate((np.zeros((a.shape[0], n_zeros)), a), axis=1)

    else:
        return np.concatenate((np.zeros((n_zeros, a.shape[1])), a))
