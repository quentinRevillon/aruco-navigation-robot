"""Arena geometry: heading change needed to go from one beacon to the next.

The arena is a circle of radius 2.5 m with beacons on its border. A beacon at
position p (integer in [-3, 3], 0 facing the start) sits at polar angle
pi/2 - p * pi/4 from the arena centre.

Usage:
    from robot.geometry import turn_angle
    turn_angle(0, 1, 0.3, 0.0)   # 45.0: turn 45 degrees to the right
"""
from math import acos, cos, degrees, pi, sin

import numpy as np

ARENA_RADIUS_M = 2.5
TARGET_OFFSET_M = 0.2  # aim at a point this far in front of the next beacon


def beacon_angle(position):
    """Polar angle (radians) of the beacon at a given arena position."""
    return pi / 2 - position * pi / 4


def turn_angle(current, target, distance, angle):
    """Heading change, in degrees, to aim at the point in front of the next beacon.

    Args:
        current: arena position of the beacon the robot stands in front of.
        target: arena position of the next beacon.
        distance: robot-to-current-beacon distance, in metres.
        angle: angle between robot axis and current beacon normal, in radians
            (robot.detection.marker_angle).

    Returns:
        float, positive to turn right, negative to turn left.
    """
    b_current, b_target = beacon_angle(current), beacon_angle(target)
    robot_to_current = np.array([distance * cos(angle + b_current), distance * sin(angle + b_current)])
    centre_to_current = ARENA_RADIUS_M * np.array([cos(b_current), sin(b_current)])
    centre_to_aim = (ARENA_RADIUS_M - TARGET_OFFSET_M) * np.array([cos(b_target), sin(b_target)])
    robot_to_aim = robot_to_current - centre_to_current + centre_to_aim

    cosine = robot_to_current @ robot_to_aim / (distance * np.linalg.norm(robot_to_aim))
    theta = degrees(acos(cosine))
    cross = robot_to_current[0] * robot_to_aim[1] - robot_to_current[1] * robot_to_aim[0]
    return theta if cross <= 0 else -theta
