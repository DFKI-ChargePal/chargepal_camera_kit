from __future__ import annotations

# global
import logging
import cv2 as cv

# local
from camera_kit.camera.camera_base import CameraBase

# typing
from typing import Any


LOGGER = logging.getLogger(__name__)


class CameraBuildIn(CameraBase):

    _type_id = "build_in"
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CameraBuildIn:
        if not isinstance(cls._instance, cls):
            cls._instance = super(CameraBuildIn, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: str, frame_size: tuple[int, int] = (1280, 720), launch: bool = True) -> None:
        if self.alive:
            super().destroy()
            self.name = name
            self.size = frame_size
        else:
            # Initialize super class
            super().__init__(name, frame_size)
            # OpenCV camera capture
            self.cap: cv.VideoCapture | None = None
            if launch:
                self.start()

    def start(self) -> None:
        # Create OpenCV video capture and start video stream
        self.cap = cv.VideoCapture(0)
        self.alive = True
        self.thread.start()

    def update(self) -> None:
        assert self.cap
        while self.alive:
            self.alive, raw_frame = self.cap.read()
            if self.alive:
                self.color_frame = cv.resize(raw_frame, self.size, interpolation=cv.INTER_CUBIC)

    def destroy(self) -> None:
        if self.alive:
            self.alive = False
            if self.cap is not None:
                self.cap.release()
        super().destroy()
