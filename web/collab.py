import motor
import time as t
Motor = motor.MotorDriver()

from fonctions_communes import *
from acquisition_donnees import *
from auto import *
from protocol import *

import cv2

CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

h_s = 30 #vitesse virages
v_s = 30 #vitesse avance
dt = 0.05
v = 0.2 #en m/s
    
async def run():
    # ETAPES POUR TOUTES LES VOITURES (sauf la première):*
    #   - Ouvrir la connexion
    ws = await pr.open_connection(14)
    balises = await pr.get_ordre_balise(ws)
    position = [balises[b] for b in ordre]

    #   - Attendre le go
    print("On attend de pouvoir partir")
    while not await pr.can_go(ws, 0, 0):
        time.sleep(0.2)

    #   - Aller au milieu
    print("On avance au milieu")
    deplacement(2.5)

    #   - Chercher notre balise grace a l'information donnée
    if position[ordre[0]] < 0:
        tourne(-45*position[0])
    else:
        tourne(45*position[0])
    print("On s'oriente vers la première balise")

    #       - Si problème de balise non trouvée chercher normalement

    #   - Aller à la balise

    await pr.send_signal(ws, 1, L[0])
    deplacement(1)
    print("On part vers la première balise")
    search(ordre[0])
    #   - Envoyer un signal quand on est arrivé
    await pr.send_signal(ws, 2, L[0])
    #   - Calculer l'angle avec un decalage pour arriver en face
    angle = angle_ij(position[0], position[1], 0.3, 0)
    # On peut prendre en compte le fait qu'on connait l'angle d'arrivé donc ne
    # pas se placer a 0.3m (y a la fontion sur le git)
    if angle < 0:
        sens_rota = -1
    else:
        sens_rota = 1
    print("On s'oriente vers la deuxième balise")
    tourne(sens_rota*abs(angle))

    #   - Attendre le go
    while not await pr.can_go(ws, 2, ordre[0]):
        print("On attend de pouvoir partir")
        time.sleep(0.2)

    #   - Aller à la balise
    await pr.send_signal(ws, 3, ordre[0])
    print("On part vers la deuxième balise")
    deplacement(1)
    search(ordre[1])

    #   - Envoyer un signal quand on est arrivé
    await pr.send_signal(ws, 4, ordre[1])

    #   - Calculer l'angle avec un decalage pour arriver en face
    angle = angle_ij(position[1], position[2], 0.3, 0)
    if angle < 0:
        sens_rota = -1
    else:
        sens_rota = 1
    print("On s'oriente vers la troisième balise")
    tourne(sens_rota*abs(angle))

    #   - Attendre le go
    while not await pr.can_go(ws, 4, ordre[1]):
        print("On attend de pouvoir partir")
        time.sleep(0.2)

    #   - Aller à la balise
    await pr.send_signal(ws, 5, ordre[1])
    print("On part vers la troisième balise")
    deplacement(1)
    search(ordre[2])

    #   - Envoyer un signal quand on est arrivé
    await pr.send_signal(ws, 6, ordre[2])

    #   - S'orienter vers l'arrivée
    angle = fc.angle_ij(position[0], position[1], 0.3, 0)
    if angle < 0:
        sens_rota = -1
    else:
        sens_rota = 1
    print("On s'oriente vers l'arrivé*")
    tourne(sens_rota*abs(angle))

    #   - Attendre le go
    while not await pr.can_go(ws, 6, ordre[2]):
        print("On attend de pouvoir partir")
        time.sleep(0.2)

    #   - Aller à l'arrivé
    await pr.send_signal(ws, 7, ordre[1])
    print("On part vers l'arrivé")
    # tools.move_to_balise(9)

    #   - Envoyer un signal quand on est arrivé
    await pr.send_signal(ws, 8, 9)
    print("On est arrivé à la fin.")

    #   - Se décaler pour laisser les autres voitures passer
    deplacement(1)

    # POUR TOUTES LES VOITURES ENVOYER DES SIGNAUX DE VIES

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
 
ordre = [2,6,10]
position = {6: '-3', 3: '-2', 5: '-1', 10: '0', 0: '1', 2: '2', 4: '3'}L = [-2,1,-1]
run()
