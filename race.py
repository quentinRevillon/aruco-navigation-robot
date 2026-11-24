"""Run the PROJ103 race on the robot: visit three beacons in order, then the finish.

The master server (master_server.py) announces the arena position of every
beacon and lets one robot move at a time. Our robot drives to the arena centre,
faces its first beacon, then for each beacon: drives to it with visual
servoing, measures its viewing angle, turns towards the next beacon and waits
for the master's "go".

Usage (on the Raspberry Pi, master server running):
    python race.py --robot-id 13 --route 4 6 2
"""
import argparse
import asyncio

from robot import protocol
from robot.camera import open_camera
from robot.detection import marker_angle
from robot.geometry import turn_angle
from robot.motion import move_forward, turn
from robot.motors import MotorDriver
from robot.navigation import go_to_marker

FINISH_MARKER = 9
FINISH_POSITION = -3
CENTRE_DISTANCE_M = 2.5  # start line to arena centre
APPROACH_DISTANCE_M = 1.0  # blind drive before visual servoing towards a beacon
STANDOFF_M = 0.3  # distance to the beacon used to compute the next heading
POLL_S = 0.5


async def wait_for_go(websocket, step, marker):
    """Poll the master until this robot is allowed to move."""
    while not await protocol.can_go(websocket, step, marker):
        print("waiting for go")
        await asyncio.sleep(POLL_S)


def face_next_beacon(motors, corners, current, target):
    """Turn from the current beacon towards the point in front of the next one."""
    turn(motors, turn_angle(current, target, STANDOFF_M, marker_angle(corners)))


async def run_race(robot_id, route):
    """Run the whole race for one robot.

    Args:
        robot_id: id registered with the master (13 for robotpi-13).
        route: ArUco ids of the beacons to visit, in order.
    """
    motors, capture = MotorDriver(), open_camera()
    websocket = await protocol.open_connection(robot_id)
    beacons = await protocol.get_beacon_positions(websocket)
    positions = [beacons[str(marker)] for marker in route] + [FINISH_POSITION]

    await wait_for_go(websocket, 0, 0)
    move_forward(motors, CENTRE_DISTANCE_M)
    turn(motors, 45 * positions[0])

    previous = route[0]
    for k, marker in enumerate(route):
        await protocol.send_signal(websocket, 2 * k + 1, previous)
        move_forward(motors, APPROACH_DISTANCE_M)
        corners = go_to_marker(motors, capture, marker)
        await protocol.send_signal(websocket, 2 * k + 2, marker)
        face_next_beacon(motors, corners, positions[k], positions[k + 1])
        await wait_for_go(websocket, 2 * k + 2, marker)
        previous = marker

    final_step = 2 * len(route) + 1
    await protocol.send_signal(websocket, final_step, previous)
    move_forward(motors, 2 * APPROACH_DISTANCE_M)
    go_to_marker(motors, capture, FINISH_MARKER)
    await protocol.send_signal(websocket, final_step + 1, FINISH_MARKER)
    move_forward(motors, APPROACH_DISTANCE_M)  # clear the finish for the next robot


def parse_args():
    """Parse the robot id and the beacon route from the command line."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--robot-id", type=int, default=13, help="id registered with the master server")
    parser.add_argument("--route", type=int, nargs=3, default=[4, 6, 2], help="ArUco ids of the 3 beacons, in order")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_race(args.robot_id, args.route))
