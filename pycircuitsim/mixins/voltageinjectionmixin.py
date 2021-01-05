from abc import ABC

from pycircuitsim.mixins.lticircuittypemixin import LTICircuitTypeMixin


class VoltageInjectionMixin(LTICircuitTypeMixin, ABC):
    def in_series(self, other: 'LTICircuitTypeMixin'):
        return other

    def in_parallel(self, other: 'LTICircuitTypeMixin'):
        return self
