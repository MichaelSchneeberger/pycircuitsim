from typing import Dict

from dataclass_abc import dataclass_abc

from pycircuitsim.mixins.columnselectormixin import ColumnSelectorMixin
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin


@dataclass_abc
class ComponentCollectionImpl(ColumnSelectorMixin):
    n_cols: int
    index_mapping: Dict[LTICircuitMixin, int]