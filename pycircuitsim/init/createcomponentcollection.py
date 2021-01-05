from pycircuitsim.impl.componentcollectionimpl import ComponentCollectionImpl


def create_component_collection(components):
    def gen_index():
        idx = 0
        for comp in components:
            yield comp, idx
            idx += 2 * comp.n_states + comp.n_inputs + comp.n_outputs + comp.n_add

    index_mapping = dict(gen_index())
    last_comp = components[-1]
    return ComponentCollectionImpl(
        n_cols=index_mapping[
                   last_comp] + 2 * last_comp.n_states + last_comp.n_inputs + last_comp.n_outputs + last_comp.n_add,
        index_mapping=index_mapping,
    )