from camera_kit.view.user_event import EventObserver


def ok() -> bool:
    # EventObserver.update()
    ret = EventObserver.state == EventObserver.Type.OK
    EventObserver.state = EventObserver.Type.OK
    return ret


def stop() -> bool:
    # EventObserver.update()
    # return EventObserver.state == EventObserver.Type.QUIT
    ret = EventObserver.state == EventObserver.Type.QUIT
    EventObserver.state = EventObserver.Type.OK
    return ret


def save() -> bool:
    # EventObserver.update()
    # return EventObserver.state == EventObserver.Type.SAVE
    ret = EventObserver.state == EventObserver.Type.SAVE
    EventObserver.state = EventObserver.Type.OK
    return ret


def error() -> bool:
    # EventObserver.update()
    # return EventObserver.state == EventObserver.Type.ERROR
    ret = EventObserver.state == EventObserver.Type.ERROR
    EventObserver.state = EventObserver.Type.OK
    return ret


def pause() -> bool:
    # EventObserver.update()
    # return EventObserver.state == EventObserver.Type.PAUSE
    ret = EventObserver.state == EventObserver.Type.PAUSE
    EventObserver.state = EventObserver.Type.OK
    return ret


def resume() -> bool:
    # EventObserver.update()
    # return EventObserver.state == EventObserver.Type.RESUME
    ret = EventObserver.state == EventObserver.Type.RESUME
    EventObserver.state = EventObserver.Type.OK
    return ret
