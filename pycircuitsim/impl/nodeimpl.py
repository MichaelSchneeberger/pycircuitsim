from dataclass_abc import dataclass_abc

from pycircuitsim.node import Node


@dataclass_abc(frozen=True)
class NodeImpl(Node):
    name: str
