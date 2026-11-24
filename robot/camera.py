"""Camera access and intrinsic parameters of the robot camera.

Usage:
    from robot.camera import open_camera, read_frame
    capture = open_camera()          # USB camera of the robot
    capture = open_camera(0)         # first webcam of a laptop
    frame = read_frame(capture)

CAMERA_MATRIX and DIST_COEFFS are the output of calibration/calibrate_camera.py
on 1280x720 chessboard photos (16 of 23 photos with a detected board).
"""
import cv2
import numpy as np

CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
FRAME_WIDTH = 640  # pixels, default capture width on the Raspberry Pi

CAMERA_MATRIX = np.array([
    [2.15047552e+03, 0.00000000e+00, 6.17240716e+02],
    [0.00000000e+00, 2.15215949e+03, 4.49841712e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00],
])
DIST_COEFFS = np.array([[1.14570525e-01, -1.65621384e+00, -2.70686270e-03, -1.52625388e-02, 3.58384525e+01]])


def open_camera(path=CAMERA_PATH):
    """Open a video capture on a device path or index.

    Args:
        path: Linux device path or OpenCV camera index.

    Returns:
        cv2.VideoCapture
    """
    return cv2.VideoCapture(path)


def read_frame(capture):
    """Read one BGR frame; fail loudly if the camera returns nothing.

    Args:
        capture: an opened cv2.VideoCapture.

    Returns:
        np.ndarray of shape (H, W, 3).
    """
    ok, frame = capture.read()
    assert ok, "camera returned no frame"
    return frame
