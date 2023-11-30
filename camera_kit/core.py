
# global
from contextlib import contextmanager
# local
from camera_kit.camera.camera_base import CameraBase
from camera_kit.camera.camera_factory import CameraFactory
# typing
from typing import Iterator


@contextmanager
def camera_manager(name: str) -> Iterator[CameraBase]:
    cam = CameraFactory().create(name)
    try:
        yield cam
    finally:
        cam.destroy()


def create(name: str) -> CameraBase:
    return CameraFactory().create(name)