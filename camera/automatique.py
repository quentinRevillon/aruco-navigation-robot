#!/usr/bin/env python3

from consignes import *


while True :
    id,corners = check()
    if id!=None:
        d = get_distance(corners)
        print("cible repéré à :",d,"m")
        if d<=20 and id%2 == 0 :
            print("fait demi-tour")
            
        elif d<=20 and id%2 == 1 :
            print("s'arrête")
            
        else :
            print("s'approche")
            
