from __future__ import annotations
# global
import abc
import copy
import logging
import cv2 as cv
import numpy as np
from pathlib import Path
from threading import Thread
# local
from camera_kit.view.display import Display
from camera_kit.camera import CameraCoefficient
# typing
from typing import Any
from numpy import typing as npt

LOGGER = logging.getLogger(__name__)


class CameraBase(metaclass=abc.ABCMeta):

    type_id = ""
    alive = False
    _instance = None
    _name = ""
    _frame_size = (0, 0)
    _thread: Thread | None = None
    _display: Display | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CameraBase:
        if not isinstance(cls._instance, cls):
            cls._instance = super(CameraBase, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: str, frame_size: tuple[int, int], launch: bool):
        """ Camera base class

        Args:
            name:       Name of the camera
            frame_size: Image size in pixels
        """
        if self._frame_size != frame_size:
            self.end()
        if self._name != name:
            self.remove_display()

        self._name = name
        self._frame_size = frame_size

        self.cam_info_dir = Path.cwd().joinpath('camera_info', self._name)
        self.coeffs_path = Path(self.cam_info_dir).joinpath('calibration', 'coefficients.toml')

        # Color frame
        self.color_frame = cv.cvtColor(np.zeros((3,) + self._frame_size, dtype=np.uint8).T, cv.COLOR_RGB2BGR)
        self.depth_frame = np.zeros((3,) + self._frame_size, dtype=np.uint8).T
        # Camera coefficients
        self.cc = CameraCoefficient(self._name)
        self.is_calibrated = False
        self.log_calib_msg = True
        if launch:
            self.start()

    @property
    def name(self) -> str:
        return self._name

    @property
    def frame_size(self) -> tuple[int, int]:
        return self._frame_size

    def _on_start(self) -> None:
        # Create thread
        if self._thread is None:
            self._thread = Thread(target=self.update, args=(), daemon=True)

    def _on_end(self) -> None:
        self.alive = False
        self._thread = None
        self.remove_display()

    @property
    def display(self) -> Display:
        if self._display is not None:
            return self._display
        else:
            raise RuntimeError(f"There is no display yet. Please add first via interface.")

    def get_color_frame(self) -> npt.NDArray[np.uint8]:
        if self.log_calib_msg and not self.is_calibrated:
            LOGGER.debug("Camera is not calibrated. Coefficients are default values!")
            self.log_calib_msg = False
        return np.array(self.color_frame, dtype=np.uint8)

    def get_depth_frame(self) -> npt.NDArray[np.uint8]:
        if self.log_calib_msg and not self.is_calibrated:
            LOGGER.debug("Camera is not calibrated. Coefficients are default values!")
            self.log_calib_msg = False
        return np.array(self.depth_frame, dtype=np.uint8)

    def add_display(self, name: str = "") -> None:
        if len(name) <= 0:
            name = self._name
        self._display = Display(name)

    def remove_display(self) -> None:
        if self._display is not None:
            self._display.destroy()
            self._display = None

    def render(self, frame: npt.NDArray[np.uint8] | None = None) -> None:
        if self._display is None:
            self.add_display()
        if frame is None:
            frame = self.get_color_frame()
        self.display.show(frame)

    def load_coefficients(self, file_path: Path | str = "") -> None:
        """ Class method to load camera coefficients

        Args:
            file_path: File path to the intrinsic and distorted parameters

        """
        self.cc.load(file_path)
        self.is_calibrated = True

    def save_coefficients(self, cc: CameraCoefficient, dir_path: Path | str = "") -> None:
        """ Set camera coefficients and save them in the (optionally) given file_path
        as coefficients.toml.

        Args:
            cc:       The camera intrinsic and distortion coefficient object
            dir_path: Optional directory path where the coefficients are saved
        """
        # Update camera coefficients
        self.cc = copy.copy(cc)
        self.is_calibrated = True
        self.cc.save(dir_path)

    @abc.abstractmethod
    def start(self) -> None:
        """ Abstract class method to start video stream

        Returns:
            None
        """
        raise NotImplementedError("Must be implemented in subclass")

    @abc.abstractmethod
    def update(self) -> None:
        """ Abstract class method which will be called by the thread to update the image stream

        Returns:
            None
        """
        raise NotImplementedError("Must be implemented in subclass")

    @abc.abstractmethod
    def end(self) -> None:
        """ Class method to end/destroy the specific camera stream

        Returns:
            None
        """
        raise NotImplementedError("Must be implemented in subclass")
