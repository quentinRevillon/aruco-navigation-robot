#code manon
#!/usr/bin/env python3
#
# from consignes import *
#
#
# while True :
#     id,corners = check()
#     if id!=None:
#         d = get_distance(corners)
#         print("cible repéré à :",d,"m")
#         if (d<=20 and id%2 == 0) :
#             print("fait demi-tour")
#         if (d<=20 and id%2 == 1) :
#             print("s'arrête")
#         if (20<=d<=100) :
#             x,y = get_middle(corners)
#             print("coordonées :",x,y)
#             if x<=(WIDTH*0.33) :
#                  print("tourne vers la droite")
#             if x>=(WIDTH*0.66):
#                  print("tourne vers la gauche")
#             else :
#                 print("s'approche")
#         if d >= 100 :
#             print("s'approche")
#     else :
#          print("tourne sur lui-même")



#!/usr/bin/env python3
import motor
from consignes import *
Motor = motor.MotorDriver()
import time as t

flag1 = False
flag2 = False
h_s = 30
v_s = 50
dt = 0.1




def avance_et_corrige(x, y):
    print("coordonées :", x, y)
    if x <= (WIDTH * 0.1):
        Motor.Move(vertical_speed=0, horizontal_speed=h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)
        print("tourne vers la droite")
    if x >= (WIDTH * 0.9):
        Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)
        print("tourne vers la gauche")
    else:
        Motor.Move(vertical_speed=v_s, horizontal_speed=0)
        print("s'approche")


while True:
    id, corners = check()
    if id and id%2==1:
        d = get_distance(corners)
        x, y = get_middle(corners)
        print("cible repéré à :", d, "m")
        if d<=25:
            break
        else:
            avance_et_corrige(x, y)
    else:
        Motor.Move(vertical_speed=0, horizontal_speed=h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)

Motor.Move(-v_s, 0)
t.sleep(5)

while True:
    id, corners = check()
    if id and id%2==2:
        d = get_distance(corners)
        x, y = get_middle(corners)
        print("cible repéré à :", d, "m")
        if d<=25:
            Motor.MotorStop(0)
            Motor.MotorStop(1)
            break
        else:
            avance_et_corrige(x, y)
    else:
        Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)


#
# while True :
#     id,corners = check()
#     if id!=None:
#         d = get_distance(corners)
#         x, y = get_middle(corners)
#         print("cible repéré à :", d, "m")
#         if not(flag1):
#
#             if id%2==0 :
#                 Motor.Move(vertical_speed=0, horizontal_speed=h_s)
#                 continue
#
#             elif d<=20:
#
#                 flag1 = True
#                 Motor.Move(vertical_speed=0, horizontal_speed=0)
#                 t.sleep(1)
#                 # Motor.Move(vertical_speed=-50, horizontal_speed=0)
#
#                 Motor.Move(vertical_speed=-v_s, horizontal_speed=0)
#                 print("fait demi-tour")
#                 continue
#             else:
#                 avance_et_corrige(x, y)
#
#
#         else:
#             if not(flag2):
#                 if id%2 == 1:
#                     if d <= 100:
#                         Motor.Move(vertical_speed=-v_s, horizontal_speed=0)
#                         print("s'éloigne")
#                     else :
#
#                         Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
#                         t.sleep(dt)
#                         Motor.Move(vertical_speed=0, horizontal_speed=0)
#                         t.sleep(dt)
#                 else:
#                     if d<=20:
#                         flag2 = True
#                         Motor.MotorStop(0)
#                         Motor.MotorStop(1)
#                     else:
#                         avance_et_corrige(x, y)
#
#     else:
#         if not(flag1):
#             Motor.Move(vertical_speed=0, horizontal_speed=h_s)
#             t.sleep(dt)
#             Motor.Move(vertical_speed=0, horizontal_speed=0)
#             t.sleep(dt)
#
#
#         else:
#             Motor.Move(vertical_speed=0, horizontal_speed=-h_s)
#             t.sleep(dt)
#             Motor.Move(vertical_speed=0, horizontal_speed=0)
#             t.sleep(dt)
#
