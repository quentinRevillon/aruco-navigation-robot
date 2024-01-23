import websockets
import asyncio
import json
import time


MASTERROBOT = {"robots" : {11 : None, 12 : None, 13 : None, 14: None, 15 : None}, "balises" : None}

ORDRE_ROBOTS = [15, 14, 13, 12, 11]
I_ROBOT = 0 # indexe du robot dans la liste précédente


async def handler(websocket):
    global N_ROBOT # Le robot qui a le droit d'avancer

    id = int(await websocket.recv())

    if id == 15:
        balises_m = await websocket.recv()
        MASTERROBOT["balises"] = json.loads(balises_m)
    else:
        while MASTERROBOT["balises"] == None: 
            time.sleep(1)
        MASTERROBOT_m = json.dumps(MASTERROBOT)
        await websocket.send(MASTERROBOT_m)

    while True:
        robot_to_master_m = await websocket.recv()
        robot_to_master = await websocket.loads(robot_to_master_m)
        MASTERROBOT["robots"][id]["etape"] = request["etape"]

        if ORDRE_ROBOTS[N_ROBOT] == id:
            if robot_to_master["etape"] == 8:
                # le robot est arrivé
                I_ROBOT += 1
                if I_ROBOT == 5:
                    await websocket.close()
                    return

            MASTERROBOT["robots"][id]["go"] = True

        else:
            MASTERROBOT["robots"][id]["go"] = False
        
        MASTERROBOT_m = json.dumps(MASTERROBOT)
        await websocket.send(MASTERROBOT_m)


    
    return None


start_server = websockets.serve(handler, "localhost", 9000, ping_timeout = 600)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
