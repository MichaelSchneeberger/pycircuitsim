from typing import Optional

import numpy as np

from pycircuitsim.impl.capacitivetypeimpl import CapacitiveTypeImpl
from pycircuitsim.impl.lticircuitimpl import LTICircuitImpl
from pycircuitsim.impl.inductivetypeimpl import CurrentSourceImpl
from pycircuitsim.impl.resistivetypeimpl import ResistiveTypeImpl
from pycircuitsim.init.createcurrsourcecomp import create_curr_source_comp
from pycircuitsim.init.createres import create_res
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.mixins.inductivetypemixin import CurrentSourceMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin
from pycircuitsim.mixins.resistivetypemixin import ResistiveTypeMixin
from pycircuitsim.mixins.capacitivetypemixin import VoltageSourceMixin
from pycircuitsim.utils.appendzeros import append_zeros
from pycircuitsim.utils.extend import diagonalize
from pycircuitsim.utils.prependzeros import prepend_zeros


def parallel(
        comp1: LTICircuitMixin,
        comp2: LTICircuitMixin,
        u_meas: MeasurableMixin = None,
        i_meas: MeasurableMixin = None,
) -> LTICircuitMixin:

    def inner_series(
            comp1: LTICircuitMixin,
            comp2: LTICircuitMixin,
    ) -> Optional[LTICircuitMixin]:

        nx1 = comp1.n_states + comp1.n_inputs
        nx2 = comp2.n_states + comp2.n_inputs
        nx3 = 2
        nx4 = comp1.n_states + comp1.n_outputs + comp2.n_states + comp2.n_outputs
        nx123 = nx1 + nx2 + nx3
        n1234 = nx123 + nx4

        n_states = comp1.n_states + comp2.n_states
        n_inputs = comp1.n_inputs + comp2.n_inputs
        ny = n_states + n_inputs - 1

        a1 = np.concatenate((
            append_zeros(
                diagonalize(
                    np.concatenate((comp1.mat_states, comp1.mat_outputs)),
                    np.concatenate((comp2.mat_states, comp2.mat_outputs)),
                ),
                n_zeros=nx3,
            ),
            -np.eye(nx4),
        ), axis=1)

        if isinstance(comp1.type, CurrentSourceMixin) and isinstance(comp2.type, ResistiveTypeMixin):
            type = ResistiveTypeImpl()

        elif isinstance(comp1.type, CurrentSourceMixin) and isinstance(comp2.type, VoltageSourceMixin):
            type = CapacitiveTypeImpl()

        elif isinstance(comp1.type, CurrentSourceMixin) and isinstance(comp2.type, CurrentSourceMixin):
            type = CurrentSourceImpl()

        elif isinstance(comp1.type, VoltageSourceMixin) and isinstance(comp2.type, ResistiveTypeMixin):
            type = CapacitiveTypeImpl()

        elif isinstance(comp1.type, VoltageSourceMixin) and isinstance(comp2.type, VoltageSourceMixin):
            type = CapacitiveTypeImpl()

        elif isinstance(comp1.type, ResistiveTypeMixin) and isinstance(comp2.type, ResistiveTypeMixin):
            type = ResistiveTypeImpl()

        else:
            return None

        u_idx = -1 - int(type.is_curr_input)
        i_idx = -1 - int(not type.is_curr_input)

        ce = append_zeros(
            np.concatenate((
                comp1.i_meas,
                comp2.i_meas,
            ), axis=1),
            n_zeros=2,
        )
        ce[0, i_idx] = -1

        ve1 = append_zeros(
            np.concatenate((
                comp1.u_meas,
            ), axis=1),
            n_zeros=nx2 + 2,
        )
        ve1[0, u_idx] = -1

        ve2 = append_zeros(
            prepend_zeros(
                np.concatenate((
                    comp2.u_meas,
                ), axis=1),
                n_zeros=nx1,
            ),
            n_zeros=2,
        )
        ve2[0, u_idx] = -1

        a2 = append_zeros(
            np.concatenate((ce, ve1, ve2)),
            n_zeros=nx4,
        )

        if nx1 == 0:
            a_states = np.zeros((0, nx123))
        else:
            a_states = append_zeros(
                diagonalize(
                    append_zeros(
                        np.eye(comp1.n_states),
                        n_zeros=comp1.n_inputs,
                    ),
                    np.eye(comp2.n_states),
                ),
                n_zeros=comp2.n_inputs + nx3,
            )

        a_inputs = diagonalize(
            diagonalize(
                append_zeros(
                    prepend_zeros(
                        np.eye(comp1.n_inputs - 1),
                        n_zeros=comp1.n_states,
                    ),
                    n_zeros=1,
                ),
                append_zeros(
                    prepend_zeros(
                        np.eye(comp2.n_inputs - 1),
                        n_zeros=comp2.n_states,
                    ),
                    n_zeros=1,
                ),
            ),
            prepend_zeros(
                np.eye(1),
                n_zeros=1,
            ),
        )

        a3 = np.concatenate((
            a_states,
            a_inputs,
        ))

        a3_full = np.concatenate((
            a3,
            np.zeros((a3.shape[0], nx4))
        ), axis=1)

        a123 = np.concatenate((
            a1, a2, a3_full,
        ))

        a_inv = np.linalg.inv(a123)[:,-ny:]

        if type.n_add == 0:
            mat_add = np.empty((0, ny))
        else:
            mat_add = a_inv[nx123-2:nx123-1, :]

        meas2_offset = comp1.n_states + comp1.n_outputs

        measurables = {
            **comp1.measurables,
            **{k: v + meas2_offset for k, v in comp2.measurables.items()}
        }

        if u_meas:
            measurables[u_meas] = len(measurables)
            mat_u = type.get_u_meas(n_states=n_states, n_cols=ny, mat_add=mat_add)
        else:
            mat_u = np.empty((0, ny))

        if i_meas:
            measurables[i_meas] = len(measurables)
            mat_i = type.get_i_meas(n_states=n_states, n_cols=ny, mat_add=mat_add)
        else:
            mat_i = np.empty((0, ny))

        a_temp = a_inv[-nx4:, :]

        # print(a_temp)

        mat_stat1 = a_temp[:comp1.n_states, :]
        a_temp = a_temp[comp1.n_states:, :]
        mat_out1 = a_temp[:comp1.n_outputs, :]
        a_temp = a_temp[comp1.n_outputs:, :]
        mat_stat2 = a_temp[:comp2.n_states, :]
        a_temp = a_temp[comp2.n_states:, :]
        mat_out2 = a_temp[:comp2.n_outputs, :]

        mat_states = np.concatenate((mat_stat1, mat_stat2))
        mat_outputs = np.concatenate((mat_out1, mat_out2, mat_u, mat_i))

        comp = LTICircuitImpl(
            mat_states=mat_states,
            mat_outputs=mat_outputs,
            mat_add=mat_add,
            x0=comp1.x0 + comp2.x0,
            type=type,
            measurables=measurables,
        )

        return comp

    comp = inner_series(comp1, comp2)

    if comp is None:
        comp = inner_series(comp2, comp1)

    if comp is None:
        raise Exception()

    return comp

# if n_states == 0:
#     a = a123
# else:
#     n_states_outputs = n_states + comp1.n_outputs + comp2.n_outputs
#
#     a = np.concatenate((
#         a123,
#         np.concatenate((
#             np.eye(n_states_outputs),
#             np.zeros((n_col - n_states_outputs, n_states_outputs)),
#         )),
#     ), axis=1)

# n1 = comp1.a.shape[0]
# m1 = comp1.b.shape[1]
#
# A = np.concatenate((
#     comp1.a[:, :-1],
#     comp1.a[:, -1:] - comp2.b[0] * comp1.b[-1:],
# ), axis=1)
#
# b = comp1.b
# measurables = comp1.measurables
# x0 = comp1.x0
#
# return create_curr_source_comp(
#     a=A,
#     b=b,
#     x0=x0,
#     measurables=measurables,
# )

# n1 = comp1.a.shape[0]
# n2 = comp2.a.shape[0]
# m1 = comp1.b.shape[1]
# m2 = comp2.b.shape[1]
#
# ntot = n1 + n2
# mtot = m1 + m2 - 1
#
# np.concatenate((
#     np.concatenate((    # dx
#         -np.eye(ntot),
#         np.concatenate((
#             np.concatenate((
#                 comp1.a,
#                 np.zeros((n1, n2 - 1)),
#                 comp1.b[:, -1:]
#             ), axis=1),
#             np.concatenate((np.zeros((n2, n1)), comp2.a), axis=1),
#         )),
#         np.concatenate((
#             np.concatenate((comp1.b[:, :-1], np.zeros((n1, m2 - 1))), axis=1),
#             np.concatenate((np.zeros((n2, m1 - 1)), comp2.b[:, :-1],), axis=1),
#         )),
#         np.zeros((ntot, 2)),
#     ), axis=1),
#     np.concatenate((    # x
#         np.zeros((ntot, ntot)),
#         np.eye(ntot),
#         np.zeros((ntot, mtot + 1)),
#     ), axis=1),
#     np.concatenate((    # u
#         np.zeros((mtot, 2*ntot)),
#         np.eye(mtot),
#         np.zeros((mtot, 1)),
#     ), axis=1),
#     np.concatenate((  # u_cs
#         np.zeros((1, ntot - 1)),
#         np.array([[1]]),
#         np.zeros((1, ntot + mtot - 1)),
#         np.array([[-1, 1]]),
#     ), axis=1),
# ))


# n1 = comp1.a.shape[0]
# n2 = comp2.a.shape[0]
# m1 = comp1.b.shape[1]
# m2 = comp2.b.shape[1]
#
# assert n1 == comp1.a.shape[1]
# assert n2 == comp2.a.shape[1]
# assert n1 == comp1.b.shape[0]
# assert n2 == comp2.b.shape[0]
#
# A = np.concatenate((
#     np.concatenate((
#         comp1.a,
#         np.concatenate((
#             np.zeros((n1, n2 - 1)),
#             comp1.b[:, -1:],
#         ), axis=1),
#     ), axis=1),
#     np.concatenate((
#         np.concatenate((
#             np.zeros((n2, n1 - 1)),
#             -comp2.b[:, -1:],
#         ), axis=1),
#         comp2.a,
#     ), axis=1),
# ))
#
# b = np.concatenate((
#     np.concatenate((
#         comp1.b[:, :-1],
#         np.zeros((n1, m2)),
#     ), axis=1),
#     np.concatenate((
#         np.zeros((n2, m1 - 1)),
#         comp2.b,
#     ), axis=1),
# ))
#
# x0 = np.concatenate((
#     comp1.x0,
#     comp2.x0,
# ), axis=0)
#
# measurables = {**comp1.measurables, **{k: v + n1 for k, v in comp2.measurables.items()}}
#
# return create_curr_source_comp(
#     a=A,
#     b=b,
#     x0=x0,
#     measurables=measurables,
# )