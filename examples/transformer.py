from pycircuitsim.impl.linearsystemimpl import LinearSystemImpl
from pycircuitsim.init.createbranch import create_branch
from pycircuitsim.init.createind import create_ind
from pycircuitsim.init.createmeas import create_meas
from pycircuitsim.init.createnode import create_node
from pycircuitsim.init.createres import create_res
from pycircuitsim.init.createvoltagesource import create_voltage_source
from pycircuitsim.utils.series import series

meas1 = create_meas(name='meas1')
meas2 = create_meas(name='meas2')

l1 = create_ind(val=0.1, i_meas=meas1)
l2 = create_ind(val=0.2)
l3 = create_ind(val=0.05, u_meas=meas2)
r1 = create_res(val=2)
r2 = create_res(val=3)
s1 = create_voltage_source()
s2 = create_voltage_source()

n1 = create_node('n1')
n2 = create_node('n2')
n3 = create_node('n3')

branches = []
branches += [
    create_branch(
        node1=n1,
        node2=n2,
        comp=series(series(s1, l1), r1),
    ),
    create_branch(
        node1=n1,
        node2=n2,
        comp=l2,
    ),
    create_branch(
        node1=n1,
        node2=n2,
        comp=series(series(s2, l3), r2),
    ),
]

lin_system = LinearSystemImpl(branches=branches)

sys_ab, sys_cd = lin_system.get_matrix()

print(sys_ab)
print(sys_cd)
