from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np

from pycircuitsim.mixins.currentinjectionmixin import CurrentInjectionMixin
from pycircuitsim.mixins.currentsourcemixin import CurrentSourceMixin
from pycircuitsim.mixins.currentstatemixin import CurrentStateMixin
from pycircuitsim.mixins.lticircuittypemixin import LTICircuitTypeMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin
from pycircuitsim.mixins.resistivetypemixin import ResistiveTypeMixin
from pycircuitsim.mixins.voltageinjectionmixin import VoltageInjectionMixin
from pycircuitsim.mixins.voltagesourcemixin import VoltageSourceMixin
from pycircuitsim.mixins.voltagestatemixin import VoltageStateMixin
from pycircuitsim.utils.appendzeros import append_zeros
from pycircuitsim.utils.extend import diagonalize


class LTICircuitMixin(ABC):

    @property
    @abstractmethod
    def type(self) -> LTICircuitTypeMixin:
        ...

    @property
    @abstractmethod
    def mat(self) -> Tuple[Tuple[float, ...], ...]:
        """
        n_states x (n_states + n_inputs) matrix
        """

        ...

    @property
    @abstractmethod
    def measurables(self) -> Tuple[MeasurableMixin, int]:
        ...

    @property
    @abstractmethod
    def x0(self) -> Tuple[float]:
        """
        n_states vector
        """

        ...

    @property
    @abstractmethod
    def n_states(self) -> int:
        ...

    @property
    @abstractmethod
    def n_inputs(self) -> int:
        ...

    @property
    @abstractmethod
    def n_outputs(self) -> int:
        ...

    @property
    @abstractmethod
    def n_add(self) -> int:
        ...

    @property
    def n_cols(self) -> int:
        return self.n_states + self.n_inputs + self.n_add

    @property
    def n_rows(self) -> int:
        return self.n_states + self.n_outputs + self.n_add + self.n_states + self.n_inputs - 1

    def get_full_mat(self) -> np.array:
        if self.n_states + self.n_outputs == 0:
            if len(self.mat) == 0:
                to_zero_equations = np.empty((0, self.n_inputs))
            else:
                to_zero_equations = np.array(self.mat)

        else:
             # include state derivatives
            to_zero_equations = np.concatenate((
                np.array(self.mat),
                append_zeros(
                    # diagonalize(-np.eye(self.n_states), np.eye(self.n_outputs)),
                    -np.eye(self.n_states + self.n_outputs),
                    n_zeros=self.n_add,
                    axis=0,
                )
            ), axis=1)

        if self.n_states + self.n_inputs - 1 == 0:
            return to_zero_equations

        state_input_equations = np.concatenate((
            np.eye(self.n_states + self.n_inputs - 1),
            np.zeros((self.n_states + self.n_inputs - 1, 1 + self.n_add + self.n_states + self.n_outputs))
        ), axis=1)

        return np.concatenate((
            to_zero_equations,
            state_input_equations,
        ))

    def get_current_index(self):
        if isinstance(self.type, CurrentSourceMixin):
            return self.n_states + self.n_inputs - 2

        elif isinstance(self.type, CurrentStateMixin):
            return self.n_states - 1

        else:
            return self.n_states + self.n_inputs - 1

    def get_voltage_index(self):
        if isinstance(self.type, VoltageSourceMixin):
            return self.n_states + self.n_inputs - 2

        elif isinstance(self.type, VoltageStateMixin):
            return self.n_states - 1

        elif isinstance(self.type, CurrentInjectionMixin):
            return self.n_states + self.n_inputs - 1

        elif isinstance(self.type, ResistiveTypeMixin):
            return self.n_states + self.n_inputs + self.n_add - 1

        else:
            raise Exception(f'illegal case "{self.type}"')

    # @property
    # @abstractmethod
    # def mat_states(self) -> np.array:
    #     """
    #     n_states x (n_states + n_inputs) matrix
    #     """
    #
    #     ...
    #
    # @property
    # @abstractmethod
    # def mat_outputs(self) -> np.array:
    #     """
    #     n_outputs x (n_states + n_inputs) matrix
    #     """
    #
    #     ...
    #
    # @property
    # @abstractmethod
    # def mat_add(self) -> np.array:
    #     """
    #     n_add x (n_states + n_inputs) matrix
    #     """
    #
    #     ...
