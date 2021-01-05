from typing import List

from dataclass_abc import dataclass_abc

from pycircuitsim.mixins.branchmixin import BranchMixin
from pycircuitsim.mixins.linearsystemmixin import LinearSystemMixin


@dataclass_abc
class LinearSystemImpl(LinearSystemMixin):
    branches: List[BranchMixin]
