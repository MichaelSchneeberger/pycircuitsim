from abc import ABC, abstractmethod
from typing import Dict, Tuple

from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.mixins.currentinjectionmixin import CurrentInjectionMixin
from pycircuitsim.mixins.voltagesourcemixin import VoltageSourceMixin


class ColumnSelectorMixin(ABC):
    """
    helper class to find column in matrix representing multiple components
    """

    @property
    @abstractmethod
    def n_cols(self) -> int:
        ...

    @property
    @abstractmethod
    def index_mapping(self) -> Dict[LTICircuitMixin, int]:
        ...

    def get_current_idx(self, comp: LTICircuitMixin) -> int:
        return self.index_mapping[comp] + comp.get_current_index()

    def get_d_current_idx(self, comp: LTICircuitMixin) -> int:
        # assert isinstance(comp.type, CurrentSourceMixin)

        return self.index_mapping[comp] + 2 * comp.n_states + comp.n_inputs - 1

    def get_voltage_idx(self, comp: LTICircuitMixin) -> int:
        return self.index_mapping[comp] + comp.get_voltage_index()

    def get_d_voltage_idx(self, comp: LTICircuitMixin) -> int:
        # assert isinstance(comp.type, VoltageSourceMixin)

        return self.index_mapping[comp] + 2 * comp.n_states + comp.n_inputs - 1

    def get_d_state_index(self, comp: LTICircuitMixin) -> Tuple[int]:
        return tuple(self.index_mapping[comp] + comp.n_states + comp.n_inputs + comp.n_add + idx for idx in range(comp.n_states))

    def get_output_index(self, comp: LTICircuitMixin) -> Tuple[int]:
        return tuple(
            self.index_mapping[comp] + comp.n_states + comp.n_inputs + comp.n_add + comp.n_states + idx for idx in range(comp.n_outputs))

    def get_all_d_state_index(self):
        def gen_state_index():
            for comp in self.index_mapping.keys():
                yield from self.get_d_state_index(comp)
        return tuple(gen_state_index())

    def get_all_output_index(self):
        def gen_output_index():
            for comp in self.index_mapping.keys():
                yield from self.get_output_index(comp)
        return tuple(gen_output_index())

    def get_all_input_index(self):
        def gen_input_index():
            curr_pos = 0
            for comp in self.index_mapping.keys():
                yield from tuple(curr_pos + comp.n_states + comp.n_outputs + idx for idx in range(comp.n_states))
                curr_pos += comp.n_rows

            curr_pos = 0
            for comp in self.index_mapping.keys():
                yield from tuple(curr_pos + comp.n_states + comp.n_outputs + comp.n_states + idx for idx in range(comp.n_inputs - 1))
                curr_pos += comp.n_rows

        return tuple(gen_input_index())