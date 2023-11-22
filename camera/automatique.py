#!/usr/bin/env python3

from consignes import *


while True :
    id,corners = check()
    if id!=None:
        d = get_distance(corners)
        print("cible repéré à :",d,"m")
        if (d<=20 and id%2 == 0) :
            print("fait demi-tour")
        if (d<=20 and id%2 == 1) :
            print("s'arrête")
        if (20<=d<=100) :
            x,y = get_middle(corners)
            print("coordonées :",x,y)
            if x<=(WIDTH*0.33) :
                 print("tourne vers la droite")
            if x>=(WIDTH*0.66):
                 print("tourne vers la gauche")
            else :
                print("s'approche")
        if d >= 100 :
            print("s'approche")
    else :
         print("tourne sur lui-même")       
