#!/usr/bin/env python3

from consignes import *

dico = {1:"gauche",2:"droite"}
print("Begins automatic")

while True :
    id = check()
    if id != None :
        for i in dico.keys():
            if i == id :
                print(dico[i])
                #or do what you have to do with motors
