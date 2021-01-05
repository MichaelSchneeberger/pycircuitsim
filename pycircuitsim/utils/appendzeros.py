import numpy as np


def append_zeros(a, n_zeros: int = None, axis: int = None):
    if n_zeros is None:
        n_zeros = 1

    if axis is None:
        axis = 1

    if axis == 1:
        return np.concatenate((a, np.zeros((a.shape[0], n_zeros))), axis=1)

    else:
        return np.concatenate((a, np.zeros((n_zeros, a.shape[1]))))
