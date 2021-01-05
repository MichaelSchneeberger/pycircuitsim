from dataclass_abc import dataclass_abc

from pycircuitsim.mixins.resistivetypemixin import ResistiveTypeMixin


@dataclass_abc(frozen=True)
class ResistiveTypeImpl(ResistiveTypeMixin):
    pass
