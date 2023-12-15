import motor
from consignes import *
Motor = motor.MotorDriver()
import time as t

h_s = 3
v_s = 30
dt = 0.05




def avance_et_corrige(x, y, d):
    print("coordonées :", x, y)
    if x <= (200 - 200 * d *0.01):
        Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)
        print("tourne vers la gauche")
    if x >= (400 + 200*d*0.01):
        Motor.Move(vertical_speed=0, horizontal_speed=h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)
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
            #print(x, y)
            #continue
            print("cible repéré à :", d, "m")
            if d<=25:

                Motor.MotorStop(0)
                Motor.MotorStop(1)
                t.sleep(2)
                break
            else:
                
                avance_et_corrige(x, y, d)
        else:
            
            #continue
            Motor.Move(0, h_s) 
            t.sleep(dt)
            Motor.Move(vertical_speed=0, horizontal_speed=0)
            t.sleep(dt)

search(1, h_s)
Motor.Move(-v_s, 0)
t.sleep(5)
search(0, -h_s)

