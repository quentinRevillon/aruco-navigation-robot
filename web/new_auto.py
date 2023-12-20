import motor
from consignes import *
Motor = motor.MotorDriver()
import time as t

h_s = 30
v_s = 30
dt = 0.05

last_rotation = t.time()
CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
flux = cv2.VideoCapture(CAMERA_PATH)
lastTimeSeenTarget = t.time()
last_rotation = t.time()
def search(i):
    last_x = 0
    while True:
        corners, ids = check(flux)
        if ids:
            print(ids[0][0])
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
                
                    
        elif t.time()-lastTimeSeenTarget > 0.1: #attend d'avoir perdu la cible pendant au moins 0.5 secondes

            if t.time() - last_rotation < 0.2: #regarde pendant 0.2 secondes
                    Motor.MotorStop(0)
                    Motor.MotorStop(1)

            elif 0.2 < t.time() - last_rotation < 0.4: #tourne pendant 0.2 secondes
                if last_x<WIDTH/2:
                    Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
                else:
                    Motor.Move(vertical_speed=0, horizontal_speed=h_s)

                last_rotation = t.time()

search(64)


