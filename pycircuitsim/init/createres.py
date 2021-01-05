import numpy as np

from pycircuitsim.impl.lticircuitimpl import LTICircuitImpl
from pycircuitsim.impl.resistivetypeimpl import ResistiveTypeImpl
from pycircuitsim.init.createlticircuit import create_lti_circuit
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin
from pycircuitsim.mixins.resistivetypemixin import ResistiveTypeMixin


def create_res(
        val: float,
        u_meas: MeasurableMixin = None,
        i_meas: MeasurableMixin = None,
) -> LTICircuitMixin:
    mat_add = ((val, -1), )

    measurables = tuple()
    mat_outputs = tuple()

    if u_meas:
        measurables += ((u_meas, len(measurables) - 1), )
        mat_outputs += ((0, 1),)

    if i_meas:
        measurables += ((i_meas, len(measurables) - 1), )
        mat_outputs += ((1, 0), )

    return create_lti_circuit(
        type=ResistiveTypeMixin(),
        mat=mat_outputs + mat_add,
        n_states=0,
        n_outputs=len(mat_outputs),
        n_inputs=1,
        n_add=1,
        x0=tuple(),
        measurables=measurables,
    )
