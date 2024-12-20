from __future__ import annotations

# global
import numpy as np
import spatialmath as sm
from scipy.spatial.transform import Rotation as R

# typing
from typing import cast, Tuple
from numpy import typing as npt
from camera_kit.core import PosOrinType


def pq_to_cv(pq: PosOrinType) -> tuple[npt.NDArray[np.float_], npt.NDArray[np.float_]]:
    """ Convert a position quaternion vector in OpenCV convention

    Args:
        pq: Tuple containing xyz and xyzw vector

    Returns:
        Rotation vector and translation vector as numpy arrays
    """
    t_vec = np.reshape(pq[0], 3)
    r_vec = np.reshape(R.from_quat(pq[1]).as_rotvec(), 3)
    return r_vec, t_vec


def se3_to_cv(mat: sm.SE3) -> tuple[npt.NDArray[np.float_], npt.NDArray[np.float_]]:
    """ Convert a SE3 object into the OpenCV convention

    Args:
        mat: Object in SE(3) matrix representation

    Returns:
        Rotation vector and translation vector as numpy arrays
    """
    t_vec = np.reshape(mat.t, 3)
    r_vec = np.reshape(mat.eulervec(), 3)
    return r_vec, t_vec


def cv_to_pq(r_vec: npt.NDArray[np.float_], t_vec: npt.NDArray[np.float_]) -> PosOrinType:
    """ Convert a OpenCV style rotation and transformation vector into a position quaternion representation

    Args:
        r_vec: Rotation vector with axis-angle representation
        t_vec: Translation vector

    Returns:
        Position vector in xyz order and quaternion in xyzw order
    """
    p = cast(Tuple[float, float, float], tuple(np.reshape(t_vec, 3).tolist()))
    q = cast(Tuple[float, float, float, float], tuple(R.from_rotvec(np.reshape(r_vec, 3)).as_quat().tolist()))
    return p, q


def cv_to_se3(r_vec: npt.NDArray[np.float_], t_vec: npt.NDArray[np.float_]) -> sm.SE3:
    """ Convert a OpenCV style rotation and transformation vector into a SE(3) matrix representation

    Args:
        r_vec: Rotation vector with axis-angle representation
        t_vec: Translation vector

    Returns:
        SE3 object
    """
    t = np.reshape(t_vec, 3)
    rot = sm.SO3.EulerVec(r_vec)
    return sm.SE3.Rt(rot, t)
