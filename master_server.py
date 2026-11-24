"""Race master: WebSocket server that lets the robots move one after the other.

Robot 15 starts first and uploads the beacon id -> arena position map; the
other robots receive it, then report their step after each move. The master
grants "go" only to the robot whose turn it is, and passes the turn to the next
robot once the current one reports step 8 (finish reached).

Usage:
    python master_server.py               # listens on 0.0.0.0:9000
"""
import asyncio
import json

import websockets

PORT = 9000
ROBOT_ORDER = [15, 14, 13, 12, 11]
FINISH_STEP = 8
STATE = {"robots": {robot: {"etape": 0, "go": False} for robot in ROBOT_ORDER}, "balises": None}
TURN = {"index": 0}  # index in ROBOT_ORDER of the robot allowed to move


async def register(websocket):
    """Read the robot id; the first robot uploads the beacons, the others receive the state."""
    robot_id = int(await websocket.recv())
    if robot_id == ROBOT_ORDER[0]:
        STATE["balises"] = json.loads(await websocket.recv())
        return robot_id
    while STATE["balises"] is None:
        await asyncio.sleep(1)
    await websocket.send(json.dumps(STATE))
    return robot_id


def update_turn(robot_id, step):
    """Record a robot's step, pass the turn when it finishes, and set its "go" flag."""
    STATE["robots"][robot_id]["etape"] = step
    my_turn = ROBOT_ORDER[TURN["index"]] == robot_id
    if my_turn and step == FINISH_STEP:
        TURN["index"] += 1
    STATE["robots"][robot_id]["go"] = my_turn


async def handler(websocket):
    """Serve one robot until all robots have finished."""
    robot_id = await register(websocket)
    async for message in websocket:
        update_turn(robot_id, json.loads(message)["etape"])
        if TURN["index"] == len(ROBOT_ORDER):
            return
        await websocket.send(json.dumps(STATE))


async def main():
    """Serve forever on PORT."""
    async with websockets.serve(handler, "0.0.0.0", PORT, ping_timeout=600):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
