from dataclass_abc import dataclass_abc

from pycircuitsim.mixins.measurablemixin import MeasurableMixin


@dataclass_abc(frozen=True)
class MeasurableImpl(MeasurableMixin):
    name: str
