from __future__ import annotations

# global
import os
import time
import shutil
import logging

import cv2 as cv
import numpy as np
from tqdm import tqdm
from pathlib import Path

# local
from camera_kit.camera import CameraCoefficient
import camera_kit.view.user_signals as user_signal
from camera_kit.camera.camera_base import CameraBase


LOGGER = logging.getLogger(__name__)


class ChessboardDescription:

    def __init__(self, chessboard_size: tuple[int, int], chessboard_size_mm: int, reduce: bool = True):
        """ Description class of a chessboard

        Args:
            chessboard_size:    Number of chessboard rows and columns
            chessboard_size_mm: Size in [mm] of one chessboard square
            reduce:             By default chessboard size will be reduced by one since outer fields are not usable
                                for chessboard detection
        """
        self.n_rows = chessboard_size[0] - 1 if reduce else chessboard_size[0]
        self.n_cols = chessboard_size[1] - 1 if reduce else chessboard_size[1]
        assert self.n_cols > 1
        assert self.n_rows > 1
        self.board_size = (self.n_rows, self.n_cols)
        self.field_size_m = chessboard_size_mm / 1000
        self.field_size_mm = chessboard_size_mm


class CameraCalibration:
    """ Calibration class to find intrinsic and extrinsic values of a camera object """
    _find_chessboard_flags = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE
    _find_corner_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    @staticmethod
    def record_images(camera: CameraBase, dir_path: str = "") -> None:
        """ Function to recording camera calibration images

        Args:
            camera:   Camera object
            dir_path: Optional a path to the directory where the images should be stored.

        """
        # Create target directory
        target_dir = Path(dir_path) if dir_path else camera.cam_info_dir.joinpath('calibration', 'imgs')
        shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True)

        if not camera.alive:
            camera.start()

        file_count = 1
        LOGGER.info(f"Type 'S' to store a new recording. Type 'Q' or 'ESC' to finish recording.")
        while True:
            img = camera.get_color_frame()
            camera.render(img)
            if user_signal.save():
                file_name = f"calib_img_{file_count:02}.png"
                file_path = target_dir.joinpath(file_name)
                cv.imwrite(os.fspath(file_path), img)
                LOGGER.info(f"Record new image with id {file_count:02}")
                LOGGER.debug(f"Image recording path: {file_path}")
                file_count += 1
            elif user_signal.stop():
                LOGGER.info("The recording process is terminated by the user.")
                LOGGER.info(f"Recordings can be found under '{target_dir}'")
                break

    @staticmethod
    def find_coeffs(camera: CameraBase, board: ChessboardDescription, dir_path: str = "", display: bool = False
                    ) -> CameraCoefficient:
        """ Method to find intrinsic and distortion camera parameters

        Args:
            camera:   The camera object
            board:    A Chessboard object
            dir_path: Optional a path to the directory where the calibration images are stored.
            display:  Option to show calibration results

        Returns:
            The camera coefficients
        """
        # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((board.n_rows * board.n_cols, 3), np.float32)
        objp[:, :2] = np.mgrid[0:board.n_rows, 0:board.n_cols].T.reshape(-1, 2)
        objp = objp * board.field_size_mm

        # Arrays to store object points and image points from all the images.
        obj_points = []  # 3d point in real world space
        img_points = []  # 2d points in image plane.

        # Get the directory path to the calibration images
        dp = Path(dir_path) if dir_path else camera.cam_info_dir.joinpath('calibration', 'imgs')
        if not dp.exists():
            raise NotADirectoryError(f"Folder with path {dp} not found.")

        # Read calibration images and find chessboard corners
        img_paths = list(dp.glob("*.png"))
        n_imgs = len(img_paths)
        if n_imgs > 0:
            LOGGER.info(f"Using {n_imgs} images to find camera coefficients.")
            usable_imgs = 0
            for i in tqdm(range(n_imgs), ascii=True, ncols=99):
                # Read images from storage
                img = cv.imread(os.fspath(img_paths[i]))
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Find chessboard corners
                ret, corners = cv.findChessboardCorners(gray, board.board_size, CameraCalibration._find_chessboard_flags)
                if ret:
                    obj_points.append(objp)
                    corners = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), CameraCalibration._find_corner_criteria)
                    img_points.append(corners)
                    usable_imgs += 1
                    if display:
                        # Draw and display the corners
                        cv.drawChessboardCorners(img, board.board_size, corners, ret)
                        camera.render(img)
                        time.sleep(0.5)
            LOGGER.info(f"Found corners for {usable_imgs}/{n_imgs} images ")
            if usable_imgs > 0:
                # ########################### #
                # ####### CALIBRATION ####### #
                # ########################### #
                rep_err, camera_mtx, dist_coeffs, r_vecs, t_vecs = cv.calibrateCamera(
                    obj_points, img_points, camera._frame_size, None, None
                )

                LOGGER.debug('\nCalibration result:')
                LOGGER.debug('\nRe-projection error:\n%s', rep_err)
                LOGGER.debug('\nCamera intrinsic coefficients:\n%s', camera_mtx)
                LOGGER.debug('\nDistortion coefficients:\n%s', dist_coeffs.tolist())
                LOGGER.debug('\nRotation vectors:')
                for r_v in [v.tolist() for v in r_vecs]:
                    LOGGER.debug(r_v)
                LOGGER.debug('\nTranslation vectors:')
                for t_v in [v.tolist() for v in t_vecs]:
                    LOGGER.debug(t_v)

                # Store camera coefficients
                cc = CameraCoefficient(camera_mtx, dist_coeffs)
                LOGGER.info(f"Calibration successfully")
            else:
                cc = CameraCoefficient()
                LOGGER.warning(f"Could not find chessboard corners in the records. Calibration not successfully")
        else:
            LOGGER.warning(f"Not enough image records to run calibration")
            cc = CameraCoefficient()

        return cc
