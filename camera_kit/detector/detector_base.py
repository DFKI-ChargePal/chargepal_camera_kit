from __future__ import annotations

# global
import abc
import yaml
import logging
import numpy as np
from pathlib import Path

# local
from camera_kit.view.drawing import Drawing
from camera_kit.camera.camera_base import CameraBase

# typing
from typing import Any
from numpy import typing as npt


LOGGER = logging.getLogger(__name__)


class DetectorBase(metaclass=abc.ABCMeta):

    def __init__(self, config_file: Path | str):
        """ Initialize base class and load configuration

        Args:
            config_file: Path to configuration file
        """
        config_fp = Path(config_file)
        if not config_fp.exists():
            raise FileNotFoundError(f"Can't find configuration file under: {config_fp}")
        self.config_fp = config_fp
        # load configuration
        with self.config_fp.open("r") as filestream:
            try:
                self.config: dict[str, Any] = yaml.safe_load(filestream)
            except yaml.YAMLError as e:
                LOGGER.error(f"Error while reading {self.config_fp.name} configuration. {e}")
        self._camera: CameraBase | None = None  # Camera reference

    @property
    def camera(self) -> CameraBase:
        if self._camera is None:
            raise RuntimeError(f"There is no registered camera object yet.")
        else:
            return self._camera

    def register_camera(self, camera: CameraBase) -> None:
        """ Add camera to detector object

        Args:
            camera: Camera instance
        """
        self._camera = camera
        if not self._camera.is_calibrated:
            self._camera.load_coefficients()

    def find_pose(self, object_name: str, render: bool = False) -> tuple[bool, npt.NDArray[np.float_]]:
        """ Method to find object pose estimate

        Args:
            object_name: Unique name of the searched object type
            render:    If results should be shown on display or not

        Returns:
            (True if pose was found; Pose as numpy array. Containing the rotation and translation vector)
            Note: Rotation vector is expressed with Rodrigues formula following OpenCV style
        """
        img = self.camera.get_color_frame()
        _ret, _pose = self._find_pose(object_name)
        if render:
            if _ret:
                r_vec, t_vec = _pose[0], _pose[1]
                img = Drawing.frame_axes(self.camera, img, r_vec, t_vec, frame_length=0.01)
            self.camera.render(img)
        return _ret, _pose

    @abc.abstractmethod
    def _find_pose(self, object_name: str) -> tuple[bool, npt.NDArray[np.float_]]:
        """ Abstract class method to get the object pose estimate

        Args:
            object_name: Unique name of the searched object type

        Returns:
            (True if pose was found; Pose as numpy array. Containing the rotation and translation vector)
            Note: Rotation vector is expressed with Rodrigues formula following OpenCV style
        """
        raise NotImplementedError("Must be implemented in subclass")
