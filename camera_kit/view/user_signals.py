from camera_kit.view.user_event import EventObserver


def ok() -> bool:
    ret = EventObserver.state == EventObserver.Type.OK
    if ret:
        EventObserver.state = EventObserver.Type.OK
    return ret


def stop() -> bool:
    ret = EventObserver.state == EventObserver.Type.QUIT
    if ret:
        EventObserver.state = EventObserver.Type.OK
    return ret


def save() -> bool:
    ret = EventObserver.state == EventObserver.Type.SAVE
    if ret:
        EventObserver.state = EventObserver.Type.OK
    return ret


def error() -> bool:
    ret = EventObserver.state == EventObserver.Type.ERROR
    if ret:
        EventObserver.state = EventObserver.Type.OK
    return ret


def pause() -> bool:
    ret = EventObserver.state == EventObserver.Type.PAUSE
    if ret:
        EventObserver.state = EventObserver.Type.OK
    return ret


def resume() -> bool:
    ret = EventObserver.state == EventObserver.Type.RESUME
    if ret:
        EventObserver.state = EventObserver.Type.OK
    return ret
