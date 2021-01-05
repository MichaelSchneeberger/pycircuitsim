from pycircuitsim.branch import Branch
from pycircuitsim.impl.branchimpl import BranchImpl
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.node import Node


def create_branch(
        node1: Node,
        node2: Node,
        comp: LTICircuitMixin,
) -> Branch:
    return BranchImpl(
        node1=node1,
        node2=node2,
        comp=comp,
        inverse=False,
    )
