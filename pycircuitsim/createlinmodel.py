from typing import List, Generator

from pycircuitsim.mixins.linmodelmixin import LinearModelMixin
from pycircuitsim.mixins.modelmixin import ModelMixin
from pycircuitsim.mixins.nodecomparemixin import NodeCompareMixin
from pycircuitsim.mixins.statemixin import StateMixin


def create_lin_model(
        models: List[ModelMixin],
        states: List[StateMixin],
        node_compare: NodeCompareMixin,
):
    def gen_lin_models() -> Generator[LinearModelMixin, None, None]:
        for model, state in zip(models, states):
            yield model.get_lin_model(state)

    lin_models = list(gen_lin_models())

    branches = [branch for model in lin_models for branch in model.branches]
