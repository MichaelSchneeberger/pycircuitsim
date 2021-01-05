from abc import ABC

from pycircuitsim.mixins.currentinjectionmixin import CurrentInjectionMixin
from pycircuitsim.mixins.lticircuittypemixin import LTICircuitTypeMixin
from pycircuitsim.mixins.voltageinjectionmixin import VoltageInjectionMixin


class ResistiveTypeMixin(LTICircuitTypeMixin):
    def in_series(self, other: 'LTICircuitTypeMixin'):
        if isinstance(other, CurrentInjectionMixin):
            return other
        else:
            return self

    def in_parallel(self, other: 'LTICircuitTypeMixin'):
        if isinstance(other, VoltageInjectionMixin):
            return other
        else:
            return self
