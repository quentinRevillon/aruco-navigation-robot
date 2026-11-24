"""ArUco beacon detection and pose measurements from one camera frame.

Usage:
    from robot.detection import detect_markers, marker_corners, marker_distance
    corners, ids = detect_markers(frame)
    if 4 in ids:
        c = marker_corners(corners, ids, 4)
        print(marker_distance(c), marker_center(c), marker_angle(c))

Live demo on a laptop webcam (prints the distance to the first visible marker,
press q in the video window to quit):
    python -m robot.detection
"""
import math

import cv2
import numpy as np

from robot.camera import CAMERA_MATRIX, DIST_COEFFS, open_camera, read_frame

MARKER_SIZE_M = 0.028  # marker side used for distance estimation, in metres
DETECTOR = cv2.aruco.ArucoDetector(
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000), cv2.aruco.DetectorParameters()
)


def detect_markers(frame):
    """Detect all 6x6 ArUco markers in a frame.

    Args:
        frame: BGR image.

    Returns:
        corners: tuple of (1, 4, 2) float arrays, one per marker.
        ids: 1D int array of marker ids (empty if none).
    """
    corners, ids, _ = DETECTOR.detectMarkers(frame)
    ids = np.empty(0, dtype=int) if ids is None else ids.flatten()
    return corners, ids


def marker_corners(corners, ids, marker_id):
    """Return the 4 image corners of one marker; crash if it is not visible.

    Args:
        corners, ids: output of detect_markers.
        marker_id: id of the wanted marker.

    Returns:
        (4, 2) float array, clockwise from the top-left corner.
    """
    return corners[list(ids).index(marker_id)][0]


def marker_distance(corners):
    """Distance from the camera to a marker, in metres, from its estimated pose.

    Args:
        corners: (4, 2) image corners of the marker.

    Returns:
        float, norm of the marker translation vector.
    """
    half = MARKER_SIZE_M / 2
    object_points = np.array([[-half, half, 0], [half, half, 0], [half, -half, 0], [-half, -half, 0]], np.float32)
    _, _, tvec = cv2.solvePnP(
        object_points, corners.astype(np.float32), CAMERA_MATRIX, DIST_COEFFS, flags=cv2.SOLVEPNP_IPPE_SQUARE
    )
    return float(np.linalg.norm(tvec))


def marker_center(corners):
    """Image coordinates (x, y) of the marker centre, in pixels."""
    return (corners[0] + corners[2]) / 2


def marker_angle(corners):
    """Angle between the camera axis and the marker normal, in radians.

    A marker seen from the side looks narrower than tall: the angle is
    acos(top edge / left edge). Negative when the robot stands on the left of
    the marker. Used as input of robot.geometry.turn_angle.

    Args:
        corners: (4, 2) image corners of the marker.

    Returns:
        float in [-pi/2, pi/2].
    """
    width = np.linalg.norm(corners[1] - corners[0])
    left_height = np.linalg.norm(corners[3] - corners[0])
    right_height = np.linalg.norm(corners[2] - corners[1])
    if width > left_height:
        return 0.0
    angle = math.acos(width / left_height)
    return -angle if left_height > right_height else angle


def print_live_distance(capture):
    """Show the camera stream and print the distance to the first visible marker until q is pressed."""
    while cv2.waitKey(1) & 0xFF != ord("q"):
        frame = read_frame(capture)
        corners, ids = detect_markers(frame)
        cv2.imshow("camera", frame)
        if len(ids):
            print(f"marker {ids[0]}: {marker_distance(corners[0][0]):.3f} m")


if __name__ == "__main__":
    print_live_distance(open_camera(0))
