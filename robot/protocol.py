"""WebSocket client of the race master server (see master_server.py).

All robots of the race connect to one master. Each robot reports its current
step and beacon; the master answers with the shared state and tells which
robot may move ("go"). JSON keys ("id", "balise", "etape", "robots", "go",
"balises") are part of the protocol shared by all teams and stay in French.

Usage:
    import asyncio
    from robot import protocol

    async def main():
        ws = await protocol.open_connection(13)
        beacons = await protocol.get_beacon_positions(ws)   # {"4": 1, "6": -1, ...}
        while not await protocol.can_go(ws, step=0, marker=0):
            await asyncio.sleep(0.5)

    asyncio.run(main())
"""
import json

import websockets

MASTER_ADDRESS = "ws://robotpi-15.enst.fr:9000"
ROBOT_ID = -1  # set by open_connection


async def open_connection(robot_id):
    """Connect to the master and register with a robot id (e.g. 13 for robotpi-13)."""
    global ROBOT_ID
    ROBOT_ID = robot_id
    websocket = await websockets.connect(MASTER_ADDRESS)
    await websocket.send(str(robot_id))
    return websocket


async def send_signal(websocket, step, marker=None):
    """Report the current race step and the beacon the robot is at."""
    await websocket.send(json.dumps({"id": ROBOT_ID, "balise": marker, "etape": step}))


async def receive_state(websocket):
    """Wait for the next master state message and decode it."""
    return json.loads(await websocket.recv())


async def can_go(websocket, step, marker):
    """Report the current step and return True if the master allows this robot to move."""
    await send_signal(websocket, step, marker)
    state = await receive_state(websocket)
    return state["robots"][str(ROBOT_ID)]["go"]


async def get_beacon_positions(websocket):
    """Return the beacon id -> arena position map announced by the master (call first)."""
    await send_signal(websocket, 0)
    state = await receive_state(websocket)
    return state["balises"]
