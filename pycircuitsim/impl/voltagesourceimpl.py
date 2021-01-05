from dataclass_abc import dataclass_abc

from pycircuitsim.mixins.voltagesourcemixin import VoltageSourceMixin


@dataclass_abc(frozen=True)
class VoltageSourceImpl(VoltageSourceMixin):
    pass
