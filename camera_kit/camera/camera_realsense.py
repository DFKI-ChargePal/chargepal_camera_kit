from __future__ import annotations

# global
import logging
import cv2 as cv
import numpy as np
import pyrealsense2 as rs

# local
from camera_kit.camera.camera_base import CameraBase

# typing
from numpy import typing as npt


LOGGER = logging.getLogger(__name__)


class CameraRealSense(CameraBase):

    type_id = "realsense"
    _rs_cfg: rs.config | None = None
    _rs_pipeline: rs.pipeline | None = None

    def __init__(self, name: str, frame_size: tuple[int, int] = (1280, 720), launch: bool = True) -> None:
        super().__init__(name, frame_size, launch)

    def start(self) -> None:
        self._on_start()
        if not self.alive:
            # Configure depth and color streams
            self._rs_pipeline = rs.pipeline()
            self._rs_cfg = rs.config()
            # Get device product line for setting a supporting resolution
            pipeline_wrapper = rs.pipeline_wrapper(self._rs_pipeline)
            pipeline_profile = self._rs_cfg.resolve(pipeline_wrapper)
            device = pipeline_profile.get_device()
            device_product_line = str(device.get_info(rs.camera_info.product_line))
            LOGGER.debug(f"\nHello RealSense camera {device_product_line}")
            # Search for rgb sensor
            found_rgb = False
            for s in device.sensors:
                if s.get_info(rs.camera_info.name) == 'RGB Camera':
                    found_rgb = True
                    break
            if not found_rgb:
                LOGGER.error("The demo requires Depth camera with Color sensor")
                exit(0)
            # Get depth sensor scale
            depth_sensor = device.first_depth_sensor()
            depth_scale = depth_sensor.get_depth_scale()
            LOGGER.debug(f"Depth Scale is: {depth_scale}")
            # Configure streams
            self._rs_cfg.enable_stream(rs.stream.depth, self._frame_size[0], self._frame_size[1], rs.format.z16, 30)
            self._rs_cfg.enable_stream(rs.stream.color, self._frame_size[0], self._frame_size[1], rs.format.bgr8, 30)
            # Start streaming
            self._rs_pipeline.start(self._rs_cfg)
            # Start thread
            self.alive = True
            assert self._thread
            self._thread.start()

    def update(self) -> None:
        assert self._rs_cfg
        assert self._rs_pipeline
        align_to = rs.stream.color
        align = rs.align(align_to)
        while self.alive:
            # Wait for a coherent pair of frames: depth and color
            frames = self._rs_pipeline.wait_for_frames()
            # Align the depth frame to the color frame
            aligned_frames = align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                continue
            else:
                # Convert images to numpy arrays
                self.color_frame = np.asanyarray(color_frame.get_data(), dtype=np.uint8)
                pixel_distance_in_meters = aligned_depth_frame.get_distance(2 * 35, 2 * 117)
                # print(pixel_distance_in_meters)
                depth_image = np.asanyarray(aligned_depth_frame.get_data(), dtype=np.uint16)
                # print((self.depth_scale * depth_image[2*224, 2*207]))
                # self.depth_frame = depth_image
                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                self.depth_frame = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.03), cv.COLORMAP_TURBO)

    def get_depth_frame(self) -> npt.NDArray[np.uint8]:
        return self.depth_frame

    def end(self) -> None:
        self._on_end()
        if self._rs_pipeline is not None:
            self._rs_pipeline.stop()
            self._rs_cfg = None
            self._rs_pipeline = None
