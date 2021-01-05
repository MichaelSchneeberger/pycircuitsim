import unittest

import numpy as np

from pycircuitsim.init.createcap import create_cap
from pycircuitsim.init.createind import create_ind
from pycircuitsim.init.createmeas import create_meas
from pycircuitsim.init.createres import create_res
from pycircuitsim.init.createvoltagesource import create_voltage_source
from pycircuitsim.utils.series import series


class TestSeries(unittest.TestCase):
    def test_resres(self):
        r1 = create_res(val=2)
        r2 = create_res(val=3)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((5.0, -1.0),), r2.mat)

    def test_resres_with_umeas(self):
        meas1 = create_meas(name='meas1')

        r1 = create_res(val=2, u_meas=meas1)
        r2 = create_res(val=3)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((2, 0), (5.0, -1.0),), r2.mat)

    def test_resres_with_umeas2(self):
        meas1 = create_meas(name='meas1')

        r1 = create_res(val=2)
        r2 = create_res(val=3, u_meas=meas1)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((3, 0), (5.0, -1.0),), r2.mat)

    def test_resres_with_umeas3(self):
        meas1 = create_meas(name='meas1')
        meas2 = create_meas(name='meas2')

        r1 = create_res(val=2, u_meas=meas1)
        r2 = create_res(val=3, u_meas=meas2)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((2, 0), (3, 0), (5.0, -1.0),), r2.mat)

    def test_resres_with_imeas(self):
        meas1 = create_meas(name='meas1')

        r1 = create_res(val=2, i_meas=meas1)
        r2 = create_res(val=3)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((1, 0), (5.0, -1.0),), r2.mat)

    def test_resres_with_imeas2(self):
        meas1 = create_meas(name='meas1')

        r1 = create_res(val=2)
        r2 = create_res(val=3, i_meas=meas1)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((1, 0), (5.0, -1.0),), r2.mat)

    def test_resres_with_imeas3(self):
        meas1 = create_meas(name='meas1')
        meas2 = create_meas(name='meas2')

        r1 = create_res(val=2, i_meas=meas1)
        r2 = create_res(val=3, i_meas=meas2)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((1, 0), (1, 0), (5.0, -1.0),), r2.mat)

    def test_resres_with_umeas_imeas(self):
        meas1 = create_meas(name='meas1')
        meas2 = create_meas(name='meas2')

        r1 = create_res(val=2, i_meas=meas1)
        r2 = create_res(val=3, u_meas=meas2)
        r2 = series(r1, r2)

        np.testing.assert_almost_equal(((1, 0), (3, 0), (5.0, -1.0),), r2.mat)

    # res cap
    # -------

    def test_rescap(self):
        r1 = create_res(val=2)
        c2 = create_cap(val=0.1)
        z1 = series(r1, c2)

        np.testing.assert_almost_equal(((0, 10, 0), (1, 2, -1)), z1.mat)

    # res ind
    # -------

    def test_resind(self):
        r1 = create_res(val=2)
        c2 = create_ind(val=0.1)
        z1 = series(r1, c2)

        np.testing.assert_almost_equal(((-2/0.1, 1/0.1),), z1.mat)

    # voltage_source ind
    # -------

    def test_voltsrcind(self):
        c1 = create_voltage_source()
        c2 = create_ind(val=0.1)
        b1 = series(c1, c2)

        np.testing.assert_almost_equal(((0, -10, 10),), b1.mat)
        self.assertEqual(1, b1.n_states)
        self.assertEqual(2, b1.n_inputs)

    def test_voltsrcind_imeas(self):
        meas1 = create_meas(name='meas1')

        c1 = create_voltage_source()
        c2 = create_ind(val=0.1, i_meas=meas1)
        b1 = series(c1, c2)

        np.testing.assert_almost_equal(((0, -10, 10), (1, 0, 0)), b1.mat)

    def test_voltsrcindres_imeas(self):
        meas1 = create_meas(name='meas1')

        c1 = create_voltage_source()
        c2 = create_ind(val=0.1, i_meas=meas1)
        c3 = create_res(val=1)
        b1 = series(series(c1, c2), c3)

        np.testing.assert_almost_equal(((-1/0.1, -10, 10), (1, 0, 0)), b1.mat)

