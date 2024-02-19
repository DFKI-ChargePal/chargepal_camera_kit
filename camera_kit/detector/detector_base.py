from __future__ import annotations

# global
import abc
import yaml
import logging
import spatialmath as sm
from pathlib import Path

# local
from camera_kit.view.drawing import Drawing
from camera_kit.camera.camera_base import CameraBase

# typing
from typing import Any
from camera_kit.core import PosOrinType


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
                self.config_dict: dict[str, Any] = yaml.safe_load(filestream)
            except Exception as e:
                raise RuntimeError(f"Error while reading {self.config_fp.name} configuration. {e}")

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

    def find_pose(self, render: bool = False) -> tuple[bool, sm.SE3]:
        """ Method to find object pose estimate

        Args:
            render:    If results should be shown on display or not

        Returns:
            (True if pose was found; Pose as SE(3) transformation matrix)
        """
        img = self.camera.get_color_frame()
        found, se3_mat = self._find_pose()
        if render:
            if found:
                img = Drawing.frame_axes(self.camera, img, se3_mat, frame_length=0.01)
            self.camera.render(img)
        return found, se3_mat

    @abc.abstractmethod
    def _find_pose(self) -> tuple[bool, sm.SE3]:
        """ Abstract class method to get the object pose estimate

        Returns:
            (True if pose was found; Pose as SE(3) transformation matrix)
        """
        raise NotImplementedError("Must be implemented in subclass")
