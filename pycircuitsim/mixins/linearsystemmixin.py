import itertools
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple

import numpy as np

from pycircuitsim.init.createcomponentcollection import create_component_collection
from pycircuitsim.utils.createloopequation import create_loop_equation
from pycircuitsim.utils.createnodeequation import create_node_equation
from pycircuitsim.mixins.branchmixin import BranchMixin
from pycircuitsim.node import Node
from pycircuitsim.utils.extend import diagonalize


class LinearSystemMixin(ABC):
    @property
    @abstractmethod
    def branches(self) -> List[BranchMixin]:
        ...

    def get_matrix(self):
        @dataclass
        class NodeOrder:
            index: Dict[Node, int]

            def __getitem__(self, node: Node) -> int:
                if node not in self.index:
                    self.index[node] = len(self.index) - 1

                return self.index[node]

        node_order = NodeOrder(index={})

        def gen_sorted_branches():
            for branch in self.branches:
                if node_order[branch.node1] < node_order[branch.node2]:
                    yield branch
                else:
                    yield branch.swap()

        sorted_branches = list(gen_sorted_branches())

        node_branches_dict = defaultdict(list)
        for branch in sorted_branches:
            node_branches_dict[branch.node1].append(branch)

        sorted_nodes = sorted(set(line.node1 for line in sorted_branches), key=lambda node: node_order[node])

        repr_lines: Dict[Node, Tuple[Node, List[BranchMixin]]] = {
            sorted_nodes[0]: (sorted_nodes[0], []),
        }

        def gen_loops_for_each_node():
            for start_node in sorted_nodes:

                # collect all end nodes
                end_node_dict = defaultdict(list)
                for line in node_branches_dict[start_node]:
                    end_node_dict[line.node2].append(line)

                def pairwise(iterable):
                    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
                    a, b = itertools.tee(iterable)
                    next(b, None)
                    return zip(a, b)

                def gen_loops_from_local_connections():
                    for node2, lines in dict(end_node_dict).items():
                        yield from (([l], [r]) for l, r in pairwise(lines))

                local_loops = gen_loops_from_local_connections()

                root_node, path_to_start = repr_lines[start_node]

                def gen_loops_from_open_connections():
                    for end_node, lines in dict(end_node_dict).items():
                        # pick an arbitrary line that is used to form
                        # - a loop in this iteration
                        # - zero or more loops in later iterations
                        line = lines[0]

                        if end_node in repr_lines and root_node == repr_lines[end_node][0]:
                            _, path_to_end = repr_lines[end_node]

                            yield path_to_start + [line], path_to_end

                        else:
                            repr_lines[end_node] = (root_node, path_to_start + [line])

                non_local_loops = gen_loops_from_open_connections()

                yield from itertools.chain(local_loops, non_local_loops)

        loops = list(gen_loops_for_each_node())

        comp_coll = create_component_collection([branch.comp for branch in self.branches])

        def to_sign(inverse: bool):
            return int(inverse) * 2 - 1

        def gen_loop_equations():
            for left, right in loops:
                comp = [branch.comp for branch in left + right]
                comp_sign = [to_sign(not branch.inverse) for branch in left] + [to_sign(branch.inverse) for branch in right]
                yield create_loop_equation(comp_coll, comp, comp_sign)

        loop_equations = list(gen_loop_equations())

        nodes_dict = defaultdict(list)
        for branch in self.branches:
            nodes_dict[branch.node1].append((branch, to_sign(not branch.inverse)))
            nodes_dict[branch.node2].append((branch, to_sign(branch.inverse)))

        def gen_node_equations():
            for node, branches in list(nodes_dict.items())[:-1]:
                comp = [branch.comp for branch, _ in branches]
                comp_sign = [sign for _, sign in branches]
                yield create_node_equation(comp_coll, comp, comp_sign)

        node_equations = list(gen_node_equations())

        component_equations = self.branches[0].comp.get_full_mat()
        for branch in self.branches[1:]:
            component_equations = diagonalize(component_equations, branch.comp.get_full_mat())

        equations = np.concatenate((
            component_equations,
            *loop_equations,
            *node_equations,
        ))

        # print(equations)

        inverted = np.linalg.inv(equations)

        # print(inverted)

        input_index = comp_coll.get_all_input_index()

        state_index = comp_coll.get_all_d_state_index()
        output_index = comp_coll.get_all_output_index()

        # print(state_index)
        # print(input_index)

        mat_ab = inverted[state_index, :][:, input_index]
        mat_cd = inverted[output_index, :][:, input_index]

        def gen_initial_state():
            for branch in self.branches:
                comp = branch.comp
                yield from comp.x0

        x0 = tuple(gen_initial_state())

        # print(mat_ab)
        # print(mat_cd)
        # print(x0)

        # for node, sorted_branches in nodes_dict.items():
        #     print(f'{node.name}: {len(sorted_branches)}')

        return mat_ab, mat_cd
