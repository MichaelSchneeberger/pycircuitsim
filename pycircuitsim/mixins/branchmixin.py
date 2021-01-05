from abc import ABC, abstractmethod

from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.node import Node


class BranchMixin(ABC):
    """
    a branch consists of two nodes and the component between the nodes
    """

    @property
    @abstractmethod
    def node1(self) -> Node:
        ...

    @property
    @abstractmethod
    def node2(self) -> Node:
        ...

    @property
    @abstractmethod
    def comp(self) -> LTICircuitMixin:
        ...

    @property
    @abstractmethod
    def inverse(self) -> bool:
        ...

    @abstractmethod
    def copy(self, *args, **kwargs) -> 'BranchMixin':
        ...

    def swap(self) -> 'BranchMixin':
        return self.copy(
            node1=self.node2,
            node2=self.node1,
            comp=self.comp,
            inverse=not self.inverse,
        )
