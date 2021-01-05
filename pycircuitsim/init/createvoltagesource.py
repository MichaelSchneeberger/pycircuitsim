from typing import Optional

import numpy as np

from pycircuitsim.impl.lticircuitimpl import LTICircuitImpl
from pycircuitsim.impl.currentsourceimpl import CurrentSourceImpl
from pycircuitsim.init.createlticircuit import create_lti_circuit
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin
from pycircuitsim.mixins.voltagesourcemixin import VoltageSourceMixin


def create_voltage_source() -> LTICircuitMixin:
    """
    AB = [0, 1/L]
    """

    return create_lti_circuit(
        type=VoltageSourceMixin(),
        mat=tuple(),
        n_states=0,
        n_outputs=0,
        n_inputs=2,
        n_add=0,
        x0=tuple(),
        measurables=None,
        # is_voltage_state=True,
    )

