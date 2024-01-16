from __future__ import annotations
# global
import logging
from contextlib import contextmanager

# local
from camera_kit.camera.camera_base import CameraBase
from camera_kit.camera.camera_build_in import CameraBuildIn
from camera_kit.camera.camera_realsense import CameraRealSense
from camera_kit.camera.camera_factory import CameraFactory

# typing
from typing import Any, Iterator, Tuple, Type


PosOrinType = Tuple[Tuple[float, float, float], Tuple[float, float, float, float]]


camera_factory = CameraFactory()
camera_factory.register(CameraBuildIn)
camera_factory.register(CameraRealSense)


@contextmanager
def camera_manager(name: str, logger_level: int = logging.INFO, **kwargs: Any) -> Iterator[CameraBase]:
    cam = camera_factory.create(name, logger_level, **kwargs)
    try:
        yield cam
    finally:
        cam.end()
