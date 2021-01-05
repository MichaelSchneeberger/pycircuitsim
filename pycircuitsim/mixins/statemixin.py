from abc import ABC, abstractmethod
from typing import Tuple, Optional

from pycircuitsim.mixins.simresultmixin import SimResultMixin


class StateMixin(ABC):
    @abstractmethod
    def update(self, result: SimResultMixin) -> Optional[Tuple[float, 'StateMixin']]:
        """
        the state changes if some condition on the simulation result is fulfilled.
        In this case, `update` method returns the time as a float and the new state.
        Otherwise, `update` method returns None.
        """

        ...
