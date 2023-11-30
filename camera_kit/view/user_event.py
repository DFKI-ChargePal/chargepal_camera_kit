# global
import cv2 as cv
from enum import IntEnum, auto


class EventObserver:

    class Type(IntEnum):
        OK = auto()
        QUIT = auto()
        SAVE = auto()
        PAUSE = auto()
        CONTINUE = auto()
        ERROR = auto()

    state = Type.OK

    @staticmethod
    def update() -> None:
        new_event = cv.waitKey(1)
        if new_event in [ord('q'), ord('Q'), 27]:  # 27 == ESC
            EventObserver.state = EventObserver.Type.QUIT
        elif new_event in [ord('s'), ord('S')]:
            EventObserver.state = EventObserver.Type.SAVE
        elif new_event in [ord('p'), ord('P')]:
            EventObserver.state = EventObserver.Type.PAUSE
        elif new_event in [ord('c'), ord('C'), 32]:  # 32 == SPACE
            EventObserver.state = EventObserver.Type.CONTINUE
        else:
            EventObserver.state = EventObserver.Type.OK

    @staticmethod
    def wait_for_user() -> None:
        cv.waitKey(0)
