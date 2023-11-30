from __future__ import annotations
# global
import cv2 as cv
import numpy as np

# local
from camera_kit.camera.camera_base import CameraBase

# typing
from numpy import typing as npt


class Drawing:

    """ Helper class to edit color images """
    # Drawing properties
    edge_thickness = 1
    center_point_thickness = 2
    edge_color = (0, 255, 0)  # bright green
    text_color = (0, 255, 0)  # bright green
    center_point_color = (0, 0, 255)  # bright red
    frame_axes_length = 0.05  # in [m]
    frame_axes_thickness = 2  # in [px]

    @staticmethod
    def tetragon(img: npt.NDArray[np.uint8], corners: npt.NDArray[np.float64]) -> npt.NDArray[np.uint8]:
        """ Draw edges of a tetragon

        Args:
            img:     The image where to draw the edges
            corners: The four corner points in pixel coordinates

        Returns:
            The updated image
        """
        # get corner points as integer tuples
        top_left, top_right, bottom_right, bottom_left = corners
        top_right = int(top_right[0]), int(top_right[1])
        bottom_right = int(bottom_right[0]), int(bottom_right[1])
        bottom_left = int(bottom_left[0]), int(bottom_left[1])
        top_left = int(top_left[0]), int(top_left[1])
        # Draw tetragon
        cv.line(img, top_left, top_right, Drawing.edge_color, Drawing.edge_thickness)
        cv.line(img, bottom_left, top_left, Drawing.edge_color, Drawing.edge_thickness)
        cv.line(img, top_right, bottom_right, Drawing.edge_color, Drawing.edge_thickness)
        cv.line(img, bottom_right, bottom_left, Drawing.edge_color, Drawing.edge_thickness)
        return img

    @staticmethod
    def add_text(img: npt.NDArray[np.uint8], txt: str, pos: tuple[int, int]) -> npt.NDArray[np.uint8]:
        """ Draw text at given position

        Args:
            img: The image where to draw the text
            txt: The text
            pos: The start position of the text

        Returns:
            The updated image
        """
        cv.putText(img, txt, (pos[0], pos[1] + 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, Drawing.text_color, 1)
        return img

    @staticmethod
    def aruco_marker(img: npt.NDArray[np.uint8],
                     marker_corners: npt.NDArray[np.float64],
                     marker_id: int,
                     draw_corners: bool = True,
                     draw_center: bool = True,
                     draw_id: bool = True) -> npt.NDArray[np.uint8]:
        """ Draw marker edges, center point and id on the image.

        Args:
            img:            The image where to draw the marker
            marker_corners: The corner points of the markers [px]
            marker_id:      The marker id
            draw_corners:   Whether to draw the border or not
            draw_center:    Whether to draw the center point or not
            draw_id:        Whether to draw the id or not

        Returns:
            The updated image
        """
        top_left, top_right, bottom_right, bottom_left = marker_corners
        # Get corner points
        top_right = int(top_right[0]), int(top_right[1])
        bottom_right = int(bottom_right[0]), int(bottom_right[1])
        bottom_left = int(bottom_left[0]), int(bottom_left[1])
        top_left = int(top_left[0]), int(top_left[1])
        if draw_corners:
            # Draw rectangle
            cv.line(img, top_left, top_right, Drawing.edge_color, Drawing.edge_thickness)
            cv.line(img, bottom_left, top_left, Drawing.edge_color, Drawing.edge_thickness)
            cv.line(img, top_right, bottom_right, Drawing.edge_color, Drawing.edge_thickness)
            cv.line(img, bottom_right, bottom_left, Drawing.edge_color, Drawing.edge_thickness)
        if draw_center:
            # Draw center point
            cX = int((top_left[0] + bottom_right[0]) / 2.0)
            cY = int((top_left[1] + bottom_right[1]) / 2.0)
            cv.circle(img, (cX, cY), Drawing.center_point_thickness, Drawing.center_point_color, -1)
        if draw_id:
            # Draw marker id
            cv.putText(img, str(marker_id), (top_left[0], top_left[1] - 10),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, Drawing.text_color, 1)
        return img

    @staticmethod
    def single_aruco_marker_corners(img: npt.NDArray[np.uint8],
                                    corners: npt.NDArray[np.float64],
                                    m_id: int) -> npt.NDArray[np.uint8]:
        """ Draw marker edges on the image.

        Args:
            img:     The image where to draw the edges
            corners: The marker corners. Shape should be 4, 2
            m_id:    Marker id

        Returns:
            The manipulated image
        """
        top_left, top_right, bottom_right, bottom_left = corners
        # Get corner points
        top_right = int(top_right[0]), int(top_right[1])
        bottom_right = int(bottom_right[0]), int(bottom_right[1])
        bottom_left = int(bottom_left[0]), int(bottom_left[1])
        top_left = int(top_left[0]), int(top_left[1])
        # Draw rectangle
        cv.line(img, top_left, top_right, Drawing.edge_color, Drawing.edge_thickness)
        cv.line(img, bottom_left, top_left, Drawing.edge_color, Drawing.edge_thickness)
        cv.line(img, top_right, bottom_right, Drawing.edge_color, Drawing.edge_thickness)
        cv.line(img, bottom_right, bottom_left, Drawing.edge_color, Drawing.edge_thickness)
        # Draw center point
        cX = int((top_left[0] + bottom_right[0]) / 2.0)
        cY = int((top_left[1] + bottom_right[1]) / 2.0)
        cv.circle(img, (cX, cY), Drawing.center_point_thickness, Drawing.center_point_color, -1)
        # Draw marker id
        cv.putText(img, str(m_id), (top_left[0], top_left[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, Drawing.text_color, 1)
        return img

    @staticmethod
    def frame_axes(cam: CameraBase,
                   img: npt.NDArray[np.uint8],
                   rot_vector: npt.NDArray[np.float64],
                   trans_vector: npt.NDArray[np.float64],
                   frame_length: float,
                   ) -> npt.NDArray[np.uint8]:
        """ Draw coordinate axes on the image.

        Args:
            cam:          The camera object
            img:          The source image where to draw the axes
            rot_vector:   Rotation vector of the pose in camera frame
            trans_vector: Translation vector of the pose in camera frame
            frame_length: Length of the axes [m]

        Returns:
            The manipulated image
        """
        cv.drawFrameAxes(img,
                         cam.cc.intrinsic,
                         cam.cc.distortion,
                         rot_vector, trans_vector,
                         length=frame_length,
                         thickness=Drawing.frame_axes_thickness)
        return img

    @staticmethod
    def draw_pose(img: npt.NDArray[np.uint8],
                  corner: tuple[int, ...],
                  img_pts: npt.NDArray[np.float32]
                  ) -> npt.NDArray[np.uint8]:
        img = cv.line(img, corner, tuple(img_pts[0].ravel().astype(int)), (0, 255, 0), Drawing.frame_axes_thickness)
        img = cv.line(img, corner, tuple(img_pts[1].ravel().astype(int)), (0, 0, 255), Drawing.frame_axes_thickness)
        img = cv.line(img, corner, tuple(img_pts[2].ravel().astype(int)), (255, 0, 0), Drawing.frame_axes_thickness)
        return img
