# global
import logging
import argparse
import camera_kit as ck

# typing
from argparse import Namespace


def use_factory_function(opt: Namespace) -> None:
    # Set camera up
    ll = logging.DEBUG if opt.debug else logging.INFO
    cam = ck.camera_factory.create(opt.camera_name, logger_level=ll)
    # Loop camera stream
    while not ck.user.stop():
        frame = cam.get_color_frame()
        frame = ck.Drawing.add_text(frame, f"hello {opt.camera_name}", (50, 50))
        cam.render(frame)
    # Bring it to end
    cam.end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calibration demo")
    parser.add_argument('--camera_name', type=str, default="build_in")
    parser.add_argument('--debug', action='store_true', help='Set logging level to debug')
    args = parser.parse_args()
    use_factory_function(args)
