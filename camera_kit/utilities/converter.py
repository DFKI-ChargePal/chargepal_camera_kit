from __future__ import annotations

# global
import numpy as np
from scipy.spatial.transform import Rotation as R

# typing
from numpy import typing as npt
from camera_kit.core import PosOrinType


def pq_to_cv(pq: PosOrinType) -> tuple[npt.NDArray[np.float_], npt.NDArray[np.float_]]:
    """ Convert a position quaternion vector in OpenCV convention

    Args:
        pq: Tuple containing xyz and wxyz vector

    Returns:
        Rotation vector and translation vector as numpy arrays
    """
    t_vec = np.reshape(pq[0], 3)
    r_vec = R.from_quat(pq[1]).as_rotvec()
    return r_vec, t_vec


def cv_to_pq(r_vec: npt.NDArray[np.float_], t_vec: npt.NDArray[np.float_]) -> PosOrinType:
    """ Convert a OpenCV style rotation and transformation vector into a position quaternion representation

    Args:
        r_vec: Rotation vector with axis-angle representation
        t_vec: Translation vector

    Returns:
        Position vector in xyz order and quaternion in wxyz order
    """
    p = tuple(t_vec.tolist())
    q = tuple(R.from_rotvec(r_vec).as_quat().tolist())
    return p, q
