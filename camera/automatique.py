#!/usr/bin/env python3

from consignes import *


while True :
    id,corners = check()
    if id != None :
        print("cible repéré à :",get_distance(corners),"m")
        if id%2 == 0 :
            while True :
                _,corners2 = check()
                d = get_distance(corners2)
                if d<=20 :
                    print("fait demi-tour")
                    break
                else :
                    print("s'approche")
        else :
            while True :
                _,corners2 = check()
                if get_distance(corners2)<=20 :
                    print("s'arrête")
                    break
                else :
                    print("s'approche")
        break
