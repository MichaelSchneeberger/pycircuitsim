from typing import Optional, Dict, Tuple

import numpy as np

from pycircuitsim.impl.lticircuitimpl import LTICircuitImpl
from pycircuitsim.mixins.lticircuittypemixin import LTICircuitTypeMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin


def create_lti_circuit(
        type: LTICircuitTypeMixin,
        mat: Tuple[Tuple[float]],
        measurables: Optional[Dict[MeasurableMixin, int]],
        x0: Tuple[float],
        n_states: int,
        n_inputs: int,
        n_outputs: int,
        n_add: int,
        # is_voltage_source: bool = None,
        # is_current_source: bool = None,
        # is_resistive: bool = None,
        # is_voltage_state: bool = None,
        # is_current_state: bool = None,
):

    # if is_voltage_source is None:
    #     is_voltage_source = False
    #
    # if is_current_source is None:
    #     is_current_source = False
    #
    # if is_resistive is None:
    #     is_resistive = False
    #
    # if is_voltage_state is None:
    #     is_voltage_state = False
    #
    # if is_current_state is None:
    #     is_current_state = False

    if measurables is None:
        measurables = tuple()

    return LTICircuitImpl(
        type=type,
        # is_voltage_source=is_voltage_source,
        # is_current_source=is_current_source,
        # is_resistive=is_resistive,
        # is_voltage_state=is_voltage_state,
        # is_current_state=is_current_state,
        mat=mat,
        measurables=measurables,
        x0=x0,
        n_states=n_states,
        n_inputs=n_inputs,
        n_outputs=n_outputs,
        n_add=n_add,
    )
