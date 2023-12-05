from __future__ import annotations

# global
import logging
import cv2 as cv
import numpy as np
from numpy import typing as npt

# local
from camera_kit.camera.camera_base import CameraBase


LOGGER = logging.getLogger(__name__)


class CameraBuildIn(CameraBase):

    type_id = "build_in"
    # OpenCV camera capture
    _cap: cv.VideoCapture | None = None

    def __init__(self, name: str, frame_size: tuple[int, int] = (1280, 720), launch: bool = True) -> None:
        super().__init__(name, frame_size, launch)

    def get_depth_frame(self) -> npt.NDArray[np.uint8]:
        raise NotImplementedError(f"Build in camera didn't provide depth information!")

    def start(self) -> None:
        self._on_start()
        if not self.alive:
            # Create OpenCV video capture and start video stream
            self._cap = cv.VideoCapture(0)
            self.alive = True
            assert self._thread
            self._thread.start()

    def update(self) -> None:
        assert self._cap
        while self.alive:
            self.alive, raw_frame = self._cap.read()
            if self.alive:
                self.color_frame = cv.resize(raw_frame, self._frame_size, interpolation=cv.INTER_CUBIC)

    def end(self) -> None:
        self._on_end()
        if self._cap is not None:
            self._cap.release()
