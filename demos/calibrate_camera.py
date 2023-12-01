# global
import logging
import argparse
import camera_kit as ck

# typing
from argparse import Namespace


def calibrate(opt: Namespace) -> None:

    ll = logging.DEBUG if opt.debug else logging.INFO
    with ck.camera_manager(name='build_in_calib', logger_level=ll) as camera:
        # Record some images
        ck.CameraCalibration().record_images(camera)
        # Run calibration
        chessboard = ck.ChessboardDescription((11, 17), 16)
        cc = ck.CameraCalibration().find_coeffs(camera, chessboard, display=True)
        camera.save_coefficients(cc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calibration demo")
    parser.add_argument('--debug', action='store_true', help='Set logging level to debug')
    args = parser.parse_args()
    calibrate(args)
