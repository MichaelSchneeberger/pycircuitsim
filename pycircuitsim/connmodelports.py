from pycircuitsim.mixins.modelconnstatemixin import ModelConnStateMixin
from pycircuitsim.mixins.modelportmixin import ModelPortMixin


def conn_model_ports(
        port1: ModelPortMixin,
        port2: ModelPortMixin,
):
    def from_state(state: ModelConnStateMixin):
        return state.add_port_conn(port1=port1, port2=port2)

    return from_state
