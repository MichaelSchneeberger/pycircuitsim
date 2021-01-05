from abc import ABC, abstractmethod

from pycircuitsim.mixins.linearmodelmixin import LinearSystemMixin
from pycircuitsim.mixins.simresultmixin import SimResultMixin
from pycircuitsim.mixins.statemixin import StateMixin


class ModelMixin(ABC):
    @property
    @abstractmethod
    def initial_state(self) -> StateMixin:
        ...

    @property
    @abstractmethod
    def initial_linear_model(self) -> LinearSystemMixin:
        ...

    @abstractmethod
    def get_lin_model(self, state: StateMixin, result: SimResultMixin) -> LinearSystemMixin:
        """
        creates a new linear model from the new state
        """

        ...
