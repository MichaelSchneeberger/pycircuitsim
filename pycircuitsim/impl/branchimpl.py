from dataclasses import dataclass, replace

from dataclass_abc import dataclass_abc

from pycircuitsim.branch import Branch
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.node import Node


@dataclass_abc
class BranchImpl(Branch):
    node1: Node
    node2: Node
    comp: LTICircuitMixin
    inverse: bool

    def copy(self, *args, **kwargs) -> 'BranchMixin':
        return replace(self, *args, **kwargs)
