from typing import Dict, Optional, Tuple

import numpy as np
from dataclass_abc import dataclass_abc

from pycircuitsim.lticircuit import LTICircuit
from pycircuitsim.mixins.componenttypemixin import ComponentTypeMixin
from pycircuitsim.mixins.lticircuittypemixin import LTICircuitTypeMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin


@dataclass_abc(frozen=True)
class LTICircuitImpl(LTICircuit):
    type: LTICircuitTypeMixin
    mat: Tuple[Tuple[float]]
    measurables: Optional[Dict[MeasurableMixin, int]]
    x0: Tuple[float]
    n_states: int
    n_inputs: int
    n_outputs: int
    n_add: int
