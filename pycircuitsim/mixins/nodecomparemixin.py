from abc import ABC, abstractmethod

from pycircuitsim.mixins.nodemixin import NodeMixin


class NodeCompareMixin(ABC):
    @abstractmethod
    def compare(self, node1: NodeMixin, node2: NodeMixin) -> bool:
        ...
