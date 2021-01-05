from abc import ABC

from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin


class LTICircuit(LTICircuitMixin, ABC):
    pass
