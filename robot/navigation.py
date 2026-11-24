"""Visual servoing towards one ArUco beacon.

The robot drives straight while the beacon is visible and stops 0.26 m in
front of it. When the beacon is lost, it rotates in short bursts towards the
side where it was last seen, pausing between bursts to let detection catch up.

Usage (on the Raspberry Pi):
    python -m robot.navigation 10      # drive to beacon 10

    from robot.navigation import go_to_marker
    corners = go_to_marker(motors, capture, 10)
"""
import sys
import time

from robot.camera import FRAME_WIDTH, open_camera, read_frame
from robot.detection import detect_markers, marker_center, marker_corners, marker_distance
from robot.motors import MotorDriver

STOP_DISTANCE_M = 0.26
APPROACH_SPEED = 40  # duty cycle, percent
SEARCH_SPEED = 30  # duty cycle, percent
LOST_DELAY_S = 0.3  # keep going this long after losing the beacon before searching
LOOK_DURATION_S = 0.4  # pause between two search bursts
FIRST_BURST_S = 0.2  # rotation burst before the beacon has ever been seen
NEXT_BURST_S = 0.05  # shorter bursts once it has been seen: it is close to the field of view


def rotate_burst(motors, direction, duration):
    """Spin on the spot for a short duration (direction +1 = right, -1 = left), then stop."""
    motors.move(forward=0, turn=SEARCH_SPEED * direction)
    time.sleep(duration)
    motors.stop()


def go_to_marker(motors, capture, marker_id):
    """Drive to a beacon and stop in front of it.

    Args:
        motors: robot.motors.MotorDriver.
        capture: opened camera (robot.camera.open_camera).
        marker_id: ArUco id of the beacon.

    Returns:
        (4, 2) image corners of the beacon seen from the stop position.
    """
    burst = FIRST_BURST_S
    last_x = 0
    last_seen = last_burst = time.time()
    while True:
        corners, ids = detect_markers(read_frame(capture))
        if marker_id in ids:
            target = marker_corners(corners, ids, marker_id)
            distance = marker_distance(target)
            print(f"beacon {marker_id} at {distance:.2f} m")
            if distance <= STOP_DISTANCE_M:
                motors.stop()
                return target
            motors.move(forward=APPROACH_SPEED, turn=0)
            last_x = marker_center(target)[0]
            last_seen = last_burst = time.time()
            burst = NEXT_BURST_S
        elif time.time() - last_seen > LOST_DELAY_S:
            if time.time() - last_burst < LOOK_DURATION_S:
                motors.stop()
            else:
                rotate_burst(motors, -1 if last_x < FRAME_WIDTH / 2 else 1, burst)
                last_burst = time.time()


if __name__ == "__main__":
    go_to_marker(MotorDriver(), open_camera(), int(sys.argv[1]))
