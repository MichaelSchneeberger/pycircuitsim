from typing import List

import numpy as np

from pycircuitsim.mixins.columnselectormixin import ColumnSelectorMixin
from pycircuitsim.mixins.currentinjectionmixin import CurrentInjectionMixin
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin


def create_node_equation(comp_coll: ColumnSelectorMixin, sel_comp: List[LTICircuitMixin], comp_sign: List[int]):
    node_equation = np.zeros((1, comp_coll.n_cols))

    # special case if all components are current source
    if all(isinstance(comp.type, CurrentInjectionMixin) for comp in sel_comp):
        for comp, sign in zip(sel_comp, comp_sign):
            assert sel_comp[0].x0[0] == comp.x0[0]

            node_equation[0, comp_coll.get_d_current_idx(comp)] = sign

    else:
        for comp, sign in zip(sel_comp, comp_sign):
            node_equation[0, comp_coll.get_current_idx(comp)] = sign

    return node_equation
