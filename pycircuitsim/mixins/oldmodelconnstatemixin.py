from abc import ABC, abstractmethod
from copy import copy
from typing import List, DefaultDict

from pycircuitsim.mixins.modelportmixin import ModelPortMixin


class ModelConnStateMixin(ABC):
    @property
    @abstractmethod
    def conn_ports(self) -> DefaultDict[ModelPortMixin, List[ModelPortMixin]]:
        ...

    @abstractmethod
    def _add_port_conn(
            self,
            conn_ports: DefaultDict[ModelPortMixin, List[ModelPortMixin]],
    ):
        ...

    def add_port_conn(
            self,
            port1: ModelPortMixin,
            port2: ModelPortMixin,
    ):
        conn_ports = copy(self.conn_ports)
        conn_ports[port1].append(port2)
        conn_ports[port2].append(port1)

        return self._add_port_conn(conn_ports=conn_ports)
