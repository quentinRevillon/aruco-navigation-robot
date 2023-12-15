import motor
from consignes import *
Motor = motor.MotorDriver()
import time as t

h_s = 30
v_s = 30




def avance_et_corrige(x, y, d):
    print("coordonées :", x, y)
    if x <= WIDTH*0.4:
        Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
 
        print("tourne vers la gauche")
    if x >= WIDTH*0.6:
        Motor.Move(vertical_speed=0, horizontal_speed=h_s)

        print("tourne vers la droite")
    else:
        Motor.Move(vertical_speed=v_s, horizontal_speed=0)
        print("s'approche")

def search(h_s):
    
    while True:
        id, corners = check()
        if id:
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
            

search(h_s)
# Motor.Move(-v_s, 0)
# t.sleep(5)
# search(0, -h_s)

