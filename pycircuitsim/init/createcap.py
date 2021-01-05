from typing import Optional

import numpy as np

from pycircuitsim.impl.lticircuitimpl import LTICircuitImpl
from pycircuitsim.impl.voltagesourceimpl import VoltageSourceImpl
from pycircuitsim.init.createlticircuit import create_lti_circuit
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin
from pycircuitsim.mixins.voltagestatemixin import VoltageStateMixin


def create_cap(
        val: float,
        u_meas: Optional[MeasurableMixin] = None,
        i_meas: Optional[MeasurableMixin] = None,
        u0: Optional[float] = None,
) -> LTICircuitMixin:
    """
    AB = [0, 1/C]
    """

    mat_states = ((0.0, 1.0/val), )

    measurables = tuple()
    mat_outputs = tuple()

    if u_meas:
        measurables += ((u_meas, len(measurables) - 1), )
        mat_outputs += ((1, 0), )

    if i_meas:
        measurables += ((i_meas, len(measurables) - 1), )
        mat_outputs += ((0, 1), )

    if u0 is None:
        x0 = (0,)

    else:
        x0 = (u0,)

    return create_lti_circuit(
        type=VoltageStateMixin(),
        mat=mat_states + mat_outputs,
        n_states=1,
        n_outputs=len(mat_outputs),
        n_inputs=1,
        n_add=0,
        x0=x0,
        measurables=measurables,
    )
