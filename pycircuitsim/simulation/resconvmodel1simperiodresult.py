from dataclass_abc import dataclass_abc

from numpy.core._multiarray_umath import ndarray
from scipy.signal import StateSpace


@dataclass_abc
class ResConvModel1SimPeriodResult:
    y: ndarray
    x0: ndarray
    is_db_high: bool
    is_sat: bool
