# global
import logging
from contextlib import contextmanager
# local
from camera_kit.utilities.base_logger import set_logging_level
from camera_kit.camera.camera_base import CameraBase
from camera_kit.camera.camera_factory import CameraFactory
# typing
from typing import Any, Iterator


@contextmanager
def camera_manager(name: str, logger_level: int = logging.INFO, **kwargs: Any) -> Iterator[CameraBase]:
    cam = create(name, logger_level, **kwargs)
    try:
        yield cam
    finally:
        cam.end()


def create(name: str, logger_level: int = logging.INFO, **kwargs: Any) -> CameraBase:
    set_logging_level(logger_level)
    return CameraFactory().create(name, **kwargs)
