from __future__ import annotations
# local
from camera_kit.camera.camera_base import CameraBase
from camera_kit.camera.camera_build_in import CameraBuildIn
from camera_kit.camera.camera_realsense import CameraRealSense

# typing
from typing import Any


class CameraFactory:

    @staticmethod
    def available_cameras() -> list[str]:
        return [CameraBuildIn._type_id, CameraRealSense._type_id]

    @staticmethod
    def create(name: str, **kwargs: Any) -> CameraBase:
        if name.startswith('realsense'):
            return CameraRealSense(name, **kwargs)
        elif name.startswith('build_in'):
            return CameraBuildIn(name, **kwargs)
        else:
            raise KeyError(f"Cannot map '{name}' to camera class. "
                           f"Make sure camera name fits to one of the list: {CameraFactory.available_cameras()}")
