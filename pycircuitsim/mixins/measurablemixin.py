from abc import ABC, abstractmethod


class MeasurableMixin(ABC):
    @property
    @abstractmethod
    def name(self):
        ...
