from dataclass_abc import dataclass_abc

from pycircuitsim.mixins.currentinjectionmixin import CurrentInjectionMixin


@dataclass_abc(frozen=True)
class CurrentSourceImpl(CurrentInjectionMixin):
    pass
