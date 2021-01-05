from dataclass_abc import dataclass_abc

from numpy.core._multiarray_umath import ndarray
from scipy.signal import StateSpace


@dataclass_abc
class ResConvModel1SimArg:
    u1: float
    x0: ndarray
    t_sim: float
    n_sample: int

    ss_nom: StateSpace
    ss_sat: StateSpace
    im_sat: float
