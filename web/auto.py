import motor
from consignes import *
Motor = motor.MotorDriver()
import time as t
import numpy as np
from rotation_distance import *



last_rotation = t.time()
CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
flux = cv2.VideoCapture(CAMERA_PATH)

def index_of_aruco(ids, i):
    for index in range(ids.size):
        if ids[index][0] == i:
            return index
    return False



def search_balise(i, last_x):
    
    last_rotation = t.time()

    while True:
        corners, ids = check(flux)
        if type(ids) == np.ndarray and i in ids.flatten():
            return True
        else:
            if t.time() - last_rotation < 0.1: #regarde pendant 0.2 secondes
                    Motor.MotorStop(0)
                    Motor.MotorStop(1)

            else: #tourne pendant 0.2 secondes
                if last_x<WIDTH/2:
                    Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
                else:
                    Motor.Move(vertical_speed=0, horizontal_speed=h_s)

                t.sleep(0.05)
                last_rotation = t.time()
def charge():
    lastTimeSeenTarget = t.time()
    while True:
        corners, ids = check(flux)

        if (type(ids) == np.ndarray and i in ids.flatten()) or  t.time() - lastTimeSeenTarget < 0.1: #ça fait plus d'un dixième de seconde qu'on ne voit plus la balise, on s'arrête
            Motor.Move(vertical_speed=v_s, horizontal_speed=0)
        else:
            Motor.Stop()

def ajuste(i):
    while True:
        corners, ids = check(flux)
        if type(ids) == np.ndarray and i in ids.flatten():
            x, y = get_middle(corners)
            if x < WIDTH*0.4:
                pass
            


            

def search(i):
    h_s = 30
    v_s = 50
    lastTimeSeenTarget = t.time()
    last_rotation = t.time()
    last_x = 0
    while True:
        corners, ids = check(flux)
        if type(ids) == np.ndarray and i in ids.flatten():
            index = list(ids.flatten()).index(i)
            
            
            corners = (corners[index],)
                       
            

            d = get_distance(corners)
            x, y = get_middle(corners)
            last_x = x
            lastTimeSeenTarget = t.time()
            last_rotation = t.time()

            print("cible repéré à :", d, "m")
            if d>0.24:
                Motor.Move(vertical_speed=v_s, horizontal_speed=0)
            else:
                Motor.MotorStop(0)
                Motor.MotorStop(1)
                print("robot arrivé")
                break
                # if x <= WIDTH*0.3:
                #     Motor.Move(vertical_speed=0, horizontal_speed=-h_s)

                # if x >= WIDTH*0.7:
                #     Motor.Move(vertical_speed=0, horizontal_speed=h_s)
        
                # else:
                
                    
        elif t.time()-lastTimeSeenTarget > 0.3: #attend d'avoir perdu la cible pendant au moins 0.5 secondes

            if t.time() - last_rotation < 0.4: #regarde pendant 0.4 secondes
                    Motor.MotorStop(0)
                    Motor.MotorStop(1)

            else: #tourne pendant 0.2 secondes
                if last_x<WIDTH/2:
                    Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
                else:
                    Motor.Move(vertical_speed=0, horizontal_speed=h_s)

                t.sleep(0.5)
                Motor.MotorStop(0)
                Motor.MotorStop(1)
                last_rotation = t.time()

if __name__ == "__main__":
    search(10)

#tourne(120)
#deplacement(1)
#search(4)
#tourne(120)
#deplacement(1)
#search(9)



