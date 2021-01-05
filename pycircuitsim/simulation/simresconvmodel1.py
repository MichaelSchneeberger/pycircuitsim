import math
from typing import Iterable

from numpy.core._multiarray_umath import ndarray

import numpy as np

from pycircuitsim.simulation.resconvmodel1simarg import ResConvModel1SimArg
from pycircuitsim.simulation.resconvmodel1simperiodarg import ResConvModel1SimPeriodArg
from pycircuitsim.simulation.resconvmodel1simperiodresult import ResConvModel1SimPeriodResult
from pycircuitsim.simulation.simresconvmodel1period import sim_res_conv_model_1_period


def sim_res_conv_model_1(arg: ResConvModel1SimArg) -> Iterable[ndarray]:
    t_sample = arg.t_sim / arg.n_sample
    n_half_period = int(0.12 / t_sample)

    is_db_high = True
    is_sat = False
    x0 = arg.x0

    for idx_half_period in range(math.ceil(arg.n_sample / n_half_period)):

        delta_sample = min(arg.n_sample - idx_half_period * n_half_period, n_half_period)

        if idx_half_period % 2 == 0:
            u = arg.u1 * np.ones((delta_sample, 1))
        else:
            u = -arg.u1 * np.ones((delta_sample, 1))

        index = 0

        t = np.array(list(e * t_sample for e in range(delta_sample)))

        while True:

            period_arg = ResConvModel1SimPeriodArg(
                u=u,
                t=t,
                x0=x0,
                is_db_high=is_db_high,
                is_sat=is_sat,
                ss_sat=arg.ss_sat,
                ss_nom=arg.ss_nom,
                im_sat=arg.im_sat,
            )

            result: ResConvModel1SimPeriodResult = sim_res_conv_model_1_period(period_arg)

            x0 = result.x0
            is_db_high = result.is_db_high
            is_sat = result.is_sat

            index += result.y.shape[0]

            yield result.y

            if delta_sample <= index:
                break

            n_to_go = delta_sample - index
            t = np.array(list(e*t_sample for e in range(n_to_go)))
            u = u[-n_to_go:, :]
