import numpy as np

from pycircuitsim.init.createlticircuit import create_lti_circuit
from pycircuitsim.init.createcomponentcollection import create_component_collection
from pycircuitsim.mixins.currentinjectionmixin import CurrentInjectionMixin
from pycircuitsim.mixins.currentstatemixin import CurrentStateMixin
from pycircuitsim.mixins.resistivetypemixin import ResistiveTypeMixin
from pycircuitsim.utils.createnodeequation import create_node_equation
from pycircuitsim.mixins.lticircuitmixin import LTICircuitMixin
from pycircuitsim.mixins.measurablemixin import MeasurableMixin
from pycircuitsim.utils.appendzeros import append_zeros
from pycircuitsim.utils.extend import diagonalize


def series(
        comp1: LTICircuitMixin,
        comp2: LTICircuitMixin,
        u_meas: MeasurableMixin = None,
        i_meas: MeasurableMixin = None,
) -> LTICircuitMixin:

    type = comp1.type.in_series(comp2.type)

    # node equation
    # -------------

    components = [comp1, comp2]
    comp_coll = create_component_collection(components)

    node_equation = create_node_equation(
        comp_coll=comp_coll,
        sel_comp=components,
        comp_sign=[1, -1],
    )

    OUTPUT_VOLTAGE_IDX = -1
    OUTPUT_CURRENT_IDX = -2

    voltage_equation = np.zeros((1, comp_coll.n_cols+2))
    for comp in components:
        # print(comp_coll.get_voltage_idx(comp))
        voltage_equation[0, comp_coll.get_voltage_idx(comp)] = 1
    voltage_equation[0, OUTPUT_VOLTAGE_IDX] = -1

    current_equation = np.zeros((1, comp_coll.n_cols+2))
    current_equation[0, comp_coll.get_current_idx(comp1)] = 1
    current_equation[0, OUTPUT_CURRENT_IDX] = -1

    output_equation = np.zeros((1, comp_coll.n_cols + 2))
    if isinstance(type, CurrentInjectionMixin):
        output_equation[0, OUTPUT_VOLTAGE_IDX] = 1
    else:
        output_equation[0, OUTPUT_CURRENT_IDX] = 1

    equations = np.concatenate((
        append_zeros(
            np.concatenate((
                diagonalize(
                    comp1.get_full_mat(),
                    comp2.get_full_mat(),
                ),
                node_equation,
            )),
            n_zeros=2,
        ),
        voltage_equation,
        current_equation,
        output_equation,
    ))

    # print(equations)

    if all(isinstance(comp.type, CurrentStateMixin) for comp in components):
        # input_index = tuple(range(comp1.n_states - 1)) + tuple(2 * comp1.n_states + comp1.n_outputs + comp1.n_add + idx for idx in range(comp2.n_states)) + (-1,)
        x0 = comp1.x0[:-1] + comp2.x0

    else:
        x0 = comp1.x0 + comp2.x0

    inverted = np.linalg.inv(equations)

    input_index = comp_coll.get_all_input_index() + (-1,)

    # states_index = comp_coll.get_d_state_index(comp1) + comp_coll.get_d_state_index(comp2)
    states_index = comp_coll.get_all_d_state_index()
    mat_states = inverted[np.ix_(states_index, input_index)]

    # output_index = comp_coll.get_output_index(comp1) + comp_coll.get_output_index(comp2)
    output_index = comp_coll.get_all_output_index()
    mat_outputs = inverted[np.ix_(output_index, input_index)]

    measurables = comp1.measurables + tuple((k, v + comp_coll.index_mapping[comp2]) for k, v in comp2.measurables)

    if u_meas:
        measurables += (u_meas, len(measurables))

        u_equation = np.zeros((1, comp_coll.n_cols + 2))
        u_equation[0, OUTPUT_VOLTAGE_IDX] = 1

        mat_outputs = np.concatenate((
            mat_outputs,
            u_equation,
        ))

    if i_meas:
        measurables += (i_meas, len(measurables))

        i_equation = np.zeros((1, comp_coll.n_cols + 2))
        i_equation[0, OUTPUT_CURRENT_IDX] = 1

        mat_outputs = np.concatenate((
            mat_outputs,
            i_equation,
        ))

    # print(inverted)
    # print(input_index)
    # print(states_index)
    # print(output_index)

    if isinstance(type, ResistiveTypeMixin):
        mat_add = np.expand_dims(inverted[-1, input_index], axis=0)
        mat = np.concatenate((
            mat_states,
            mat_outputs,
            mat_add,
        ))
        mat = np.concatenate((
            mat,
            np.zeros((mat.shape[0], 1))
        ), axis=1)
        mat[-1, -1] = -1
        n_add = 1
    else:
        mat = np.concatenate((
            mat_states,
            mat_outputs,
        ))
        n_add = 0

    comp = create_lti_circuit(
        type=type,
        mat=tuple(map(tuple, mat)),
        n_states=mat_states.shape[0],
        n_outputs=mat_outputs.shape[0],
        n_add=n_add,
        n_inputs=comp1.n_inputs + comp2.n_inputs - 1,
        x0=x0,
        measurables=measurables,
    )

    return comp
