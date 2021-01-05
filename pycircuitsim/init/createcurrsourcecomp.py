# from typing import Dict, Optional
#
# import numpy as np
#
# from simsst.impl.componentimpl import ComponentImpl
# from simsst.mixins.componentmixin import ComponentMixin
# from simsst.mixins.inductivetypemixin import CurrentSourceMixin
# from simsst.mixins.measurablemixin import MeasurableMixin
# from simsst.mixins.capacitivetypemixin import VoltageSourceMixin
#
#
# def create_curr_source_comp(
#         a: np.array,
#         b: np.array,
#         x0: np.array,
#         measurables: Optional[Dict[MeasurableMixin, int]],
# ) -> ComponentMixin:
#
#     return ComponentImpl(
#         a=a,
#         b=b,
#         x0=x0,
#         type=CurrentSourceMixin(),
#         measurables=measurables,
#     )
