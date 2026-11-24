"""Estimate the camera intrinsics from photos of a printed chessboard.

The board has 9x6 inner corners and 25 mm squares. Copy the resulting matrix
and distortion coefficients into robot/camera.py.

Usage:
    python calibration/calibrate_camera.py data/calibration_images
    python calibration/calibrate_camera.py data/calibration_images --square-size 0.025
"""
import argparse
from pathlib import Path

import cv2
import numpy as np

BOARD_SIZE = (9, 6)  # inner corners per row and column
SUBPIX_CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def load_gray(path):
    """Read an image as grayscale (works with non-ASCII paths on Windows)."""
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def board_points(square_size):
    """3D coordinates (metres) of the chessboard inner corners, in the board plane z = 0."""
    points = np.zeros((BOARD_SIZE[0] * BOARD_SIZE[1], 3), np.float32)
    points[:, :2] = np.mgrid[0 : BOARD_SIZE[0], 0 : BOARD_SIZE[1]].T.reshape(-1, 2) * square_size
    return points


def find_corners(gray):
    """Return (found, corners refined to sub-pixel accuracy) for one grayscale image."""
    found, corners = cv2.findChessboardCorners(gray, BOARD_SIZE, None)
    if found:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), SUBPIX_CRITERIA)
    return found, corners


def calibrate(image_paths, square_size):
    """Calibrate on every image where the full board is found.

    Args:
        image_paths: list of image files.
        square_size: chessboard square side, in metres.

    Returns:
        rms reprojection error (pixels), camera matrix (3, 3), distortion coefficients (1, 5),
        number of images used.
    """
    object_points, image_points = [], []
    for path in image_paths:
        gray = load_gray(path)
        found, corners = find_corners(gray)
        if found:
            object_points.append(board_points(square_size))
            image_points.append(corners)
    rms, matrix, dist, _, _ = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)
    return rms, matrix, dist, len(image_points)


def parse_args():
    """Parse the image folder and the square size."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("images", type=Path, help="folder of chessboard photos (.jpg, .jpeg, .png)")
    parser.add_argument("--square-size", type=float, default=0.025, help="square side, in metres")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    paths = sorted(p for p in args.images.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    rms, matrix, dist, used = calibrate(paths, args.square_size)
    print(f"board found in {used}/{len(paths)} images, RMS reprojection error {rms:.3f} px")
    print("camera matrix:\n", matrix)
    print("distortion coefficients:\n", dist)
