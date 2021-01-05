from abc import ABC

from pycircuitsim.mixins.lticircuittypemixin import LTICircuitTypeMixin


class CurrentInjectionMixin(LTICircuitTypeMixin, ABC):
    def in_series(self, other: 'LTICircuitTypeMixin'):
        return self

    def in_parallel(self, other: 'LTICircuitTypeMixin'):
        return other
