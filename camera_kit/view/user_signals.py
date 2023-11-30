from camera_kit.view.user_event import EventObserver


def ok() -> bool:
    return EventObserver.state == EventObserver.Type.OK


def stop() -> bool:
    return EventObserver.state == EventObserver.Type.QUIT


def save() -> bool:
    return EventObserver.state == EventObserver.Type.SAVE


def error() -> bool:
    return EventObserver.state == EventObserver.Type.ERROR


def pause() -> bool:
    return EventObserver.state == EventObserver.Type.PAUSE


def resume() -> bool:
    return EventObserver.state == EventObserver.Type.RESUME
