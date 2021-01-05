from abc import ABC, abstractmethod
from typing import List

from pycircuitsim.mixins.measurablemixin import MeasurableMixin


class SimResultMixin(ABC):
    @abstractmethod
    def __getitem__(self, key: MeasurableMixin) -> List[float]:
        ...
