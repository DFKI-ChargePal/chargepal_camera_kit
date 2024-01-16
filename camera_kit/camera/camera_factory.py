from __future__ import annotations
# global
import logging
# local
from camera_kit.camera.camera_base import CameraBase
from camera_kit.utilities.base_logger import set_logging_level

# typing
from typing import Any, Type


class CameraFactory:

    def __init__(self) -> None:
        self.cam_selection: dict[str, Type[CameraBase]] = {}

    def available_cameras(self) -> list[str]:
        return [cam.type_id for cam in self.cam_selection.values()]
        # return [ CameraBuildIn.type_id, CameraRealSense.type_id]

    def register(self, camera: Type[CameraBase]) -> None:
        self.cam_selection[camera.type_id] = camera

    def create(self, name: str, logger_level: int = logging.INFO, **kwargs: Any) -> CameraBase:
        set_logging_level(logger_level)
        for cam_id in self.cam_selection.keys():
            if name.startswith(cam_id):
                return self.cam_selection[cam_id](name, **kwargs)
        raise KeyError(f"Cannot map '{name}' to camera class. "
                       f"Make sure camera name fits to one of the list: {self.available_cameras()}")
