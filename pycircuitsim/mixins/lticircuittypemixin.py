from abc import ABC, abstractmethod


class LTICircuitTypeMixin(ABC):
    @abstractmethod
    def in_series(self, other: 'LTICircuitTypeMixin'):
        ...

    @abstractmethod
    def in_parallel(self, other: 'LTICircuitTypeMixin'):
        ...
