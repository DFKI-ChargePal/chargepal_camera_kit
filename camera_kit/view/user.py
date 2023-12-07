from camera_kit.view.user_event import EventObserver

# typing
from typing import Callable


def event(func: Callable[[], bool]) -> Callable[[], bool]:
    def on_event() -> bool:
        is_event = func()
        if is_event:
            EventObserver.state = EventObserver.Type.OK
        return is_event
    return on_event


@event
def ok() -> bool:
    return EventObserver.state == EventObserver.Type.OK


@event
def stop() -> bool:
    return EventObserver.state == EventObserver.Type.QUIT


@event
def save() -> bool:
    return EventObserver.state == EventObserver.Type.SAVE


@event
def error() -> bool:
    return EventObserver.state == EventObserver.Type.ERROR


@event
def pause() -> bool:
    return EventObserver.state == EventObserver.Type.PAUSE


@event
def resume() -> bool:
    return EventObserver.state == EventObserver.Type.RESUME


def wait_for_command() -> None:
    EventObserver.wait_for_user()
