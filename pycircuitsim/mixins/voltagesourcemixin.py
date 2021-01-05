from abc import ABC

from pycircuitsim.mixins.voltageinjectionmixin import VoltageInjectionMixin


class VoltageSourceMixin(VoltageInjectionMixin, ABC):
    pass