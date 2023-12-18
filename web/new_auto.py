import motor
from consignes import *
Motor = motor.MotorDriver()
import time as t

h_s = 30
v_s = 30
dt = 0.05
last_x = 0
last_t = t.time()



def corrige(x, y, d):
    print("coordonées :", x, y)
    if x <= WIDTH*0.4:
        Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
        
        print("tourne vers la gauche")
    if x >= WIDTH*0.8:
        Motor.Move(vertical_speed=0, horizontal_speed=h_s)

        print("tourne vers la droite")
    else:
        Motor.Move(vertical_speed=v_s, horizontal_speed=0)
        print("s'approche")

def search(i, h_s):
    
    while True:
        id, corners = check()
        if id and id%2==1:
            d = get_distance(corners)
            x, y = get_middle(corners)
            last_x = x
            #print(x, y)
            #continue
            print("cible repéré à :", d, "m")
            if d<=25:

                Motor.MotorStop(0)
                Motor.MotorStop(1)
                t.sleep(2)
                break
            else:
                if x <= WIDTH*0.3:
                    Motor.Move(vertical_speed=0, horizontal_speed=-h_s)

                if x >= WIDTH*0.7:
                    Motor.Move(vertical_speed=0, horizontal_speed=h_s)
        
                else:
                    Motor.Move(vertical_speed=v_s, horizontal_speed=0)
        elif t.time()-last_t > 0.5:
            Motor.MotorStop(0)
            Motor.MotorStop(1)
            #continue
            if last_x<WIDTH/2:
                Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
            else:
                Motor.Move(vertical_speed=0, horizontal_speed=h_s)

search(1, h_s)
Motor.Move(-v_s, 0)
t.sleep(5)
search(0, -h_s)

