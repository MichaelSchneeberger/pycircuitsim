from pycircuitsim.impl.nodeimpl import NodeImpl
from pycircuitsim.node import Node


def create_node(name: str) -> Node:
    return NodeImpl(name=name)
