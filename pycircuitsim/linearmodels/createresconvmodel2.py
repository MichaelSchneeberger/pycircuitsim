import numpy as np
from scipy.signal import StateSpace


def create_res_conv_model_2(Lr1, Cr1, Lr2, Cr2, Lm, C2):
    """
    resonant converter without resistive parts
    """

    # [i1 ucr1 i2 ucr2 im, uc2]
    A = np.array([
        [0, -1 / Lr1, 0, 0, 0, 0],
        [1 / Cr1, 0, 0, 0, 0, 0],
        [0, 0, 0, -1 / Lr2, 0, -1 / Lr2],
        [0, 0, 1 / Cr2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1 / C2],
    ])

    # [u1 u2 u3]
    B = np.array([
        [1 / Lr1, 0, 0],
        [0, 0, 0],
        [0, 1 / Lr2, 0],
        [0, 0, 1/Lm],
        [0, 0, 0],
    ])

    # [si1, sucr1, si2, sucr2, sim, suc1, i1 uc1 i2 uc2 im u1 u2 um]
    phi_lower = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],              # voltage loop 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],              # voltage loop 2
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1/Lm],          # current node 1
    ])

    phi = np.concatenate((
        np.concatenate((
            -np.eye(5),
            A,
            B,
        ), axis=1),
        np.concatenate((
            np.zeros((5, 5)),
            np.eye(5),
            np.zeros((5, 3)),
        ), axis=1),
        phi_lower,
    ))

    phi_inv = np.linalg.inv(phi)

    A = phi_inv[:5, 5:10]
    B = phi_inv[:5, 10:12]
    C = np.eye(5)

    ss = StateSpace(
        A, B, C
    )

    A = phi_inv[12, 5:12]

    return ss, A