from typing import Dict

import numpy as np

from pycircuitsim.mixins.componenttypemixin import ComponentTypeMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin


def add_measurables(
        type: ComponentTypeMixin,
        n_states: int,
        n_cols: int,
        mat_add: np.array,
        init_measurables: Dict[MeasurableMixin, int] = None,
        u_meas: MeasurableMixin = None,
        i_meas: MeasurableMixin = None,
):
    if init_measurables is None:
        measurables = {}
    else:
        measurables = init_measurables

    if u_meas:
        measurables[u_meas] = len(measurables) - 1
        mat_u = type.get_u_meas(n_states=n_states, n_cols=n_cols, mat_add=mat_add)
    else:
        mat_u = np.empty((0, n_cols))

    if i_meas:
        measurables[i_meas] = len(measurables) - 1
        mat_i = type.get_i_meas(n_states=n_states, n_cols=n_cols, mat_add=mat_add)
    else:
        mat_i = np.empty((0, n_cols))

    return np.concatenate((mat_u, mat_i)), measurables