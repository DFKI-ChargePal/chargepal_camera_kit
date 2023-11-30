from __future__ import annotations
# global
import logging
import cv2 as cv
import numpy as np

# local
from camera_kit.view.user_event import EventObserver

# typing
from numpy import typing as npt

LOGGER = logging.getLogger(__name__)


class Display:

    def __init__(self, name: str) -> None:
        self.name = name
        self.window = cv.namedWindow(self.name, cv.WINDOW_AUTOSIZE)

    def show(self, img: npt.NDArray[np.uint8]) -> None:
        cv.imshow(self.name, img)
        EventObserver.update()

    def destroy(self) -> None:
        cv.destroyWindow(self.name)
        self.window = None
