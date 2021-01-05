import numpy as np
from scipy.signal import lsim

from pycircuitsim.simulation.resconvmodel1simperiodarg import ResConvModel1SimPeriodArg
from pycircuitsim.simulation.resconvmodel1simperiodresult import ResConvModel1SimPeriodResult


def sim_res_conv_model_1_period(
        arg: ResConvModel1SimPeriodArg,
) -> ResConvModel1SimPeriodResult:
    sign_val = 1.0 if arg.is_db_high else -1.0

    u = np.concatenate((
        arg.u,
        sign_val * np.ones((arg.u.shape[0], 1)),
    ), axis=1)

    if arg.is_sat:
        ss = arg.ss_sat
    else:
        ss = arg.ss_nom

    _, y, x = lsim(ss, u, arg.t, X0=arg.x0)

    if len(y.shape) == 1:
        y = y[np.newaxis, ...]
        x = x[np.newaxis, ...]

    i2 = y[:, 2]
    im = y[:, 4]

    db_high_index = next((idx for idx, e in enumerate(i2) if arg.is_db_high == (0 < e)), None)
    sat_index = next((idx for idx, e in enumerate(im) if (not arg.is_sat) == (arg.im_sat < abs(e))), None)

    if db_high_index is not None and sat_index is not None:
        if db_high_index < sat_index:
            index = db_high_index
        else:
            index = sat_index

    elif db_high_index is not None:
        index = db_high_index

    else:
        index = sat_index

    if db_high_index is not None and index == db_high_index:
        is_db_high = not arg.is_db_high
    else:
        is_db_high = arg.is_db_high

    if sat_index is not None and index == sat_index:
        is_sat = not arg.is_sat
    else:
        is_sat = arg.is_sat

    if index is not None:
        x0 = x[index, :]
        y = y[:index, :]
    else:
        x0 = x[-1, :]

    return ResConvModel1SimPeriodResult(
        y=y,
        x0=x0,
        is_db_high=is_db_high,
        is_sat=is_sat,
    )
