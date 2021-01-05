from typing import Optional

import numpy as np

from pycircuitsim.impl.lticircuitimpl import LTICircuitImpl
from pycircuitsim.impl.currentsourceimpl import CurrentSourceImpl
from pycircuitsim.init.createlticircuit import create_lti_circuit
from pycircuitsim.mixins.currentstatemixin import CurrentStateMixin
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin


def create_ind(
        val: float,
        i_meas: MeasurableMixin = None,
        u_meas: MeasurableMixin = None,
        i0: Optional[float] = None,
) -> LTICircuitMixin:
    """
    AB = [0, 1/L]
    """

    mat_states = ((0, 1/val), )

    measurables = tuple()
    mat_outputs = tuple()

    if u_meas:
        measurables += ((u_meas, len(measurables) - 1), )
        mat_outputs += ((0, 1), )

    if i_meas:
        measurables += ((i_meas, len(measurables) - 1), )
        mat_outputs += ((1, 0), )

    if i0 is None:
        x0 = (0,)

    else:
        x0 = (i0,)

    return create_lti_circuit(
        type=CurrentStateMixin(),
        mat=mat_states + mat_outputs,
        n_states=1,
        n_outputs=len(mat_outputs),
        n_inputs=1,
        n_add=0,
        x0=x0,
        measurables=measurables,
    )

