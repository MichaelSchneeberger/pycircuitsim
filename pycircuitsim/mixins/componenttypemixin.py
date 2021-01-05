from abc import ABC, abstractmethod


class ComponentTypeMixin(ABC):
    @property
    @abstractmethod
    def n_add(self) -> int:
        ...

    @property
    @abstractmethod
    def is_curr_input(self) -> bool:
        ...
