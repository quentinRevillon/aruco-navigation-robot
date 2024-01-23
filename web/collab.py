import motor
import time as t
Motor = motor.MotorDriver()

from fonctions_communes import *
from acquisition_donnees import *
from auto import *

import cv2

CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

h_s = 30 #vitesse virages
v_s = 30 #vitesse avance
dt = 0.05
v = 0.2 #en m/s
    
def deplacement(dist):
    Motor.Move(vertical_speed=v_s, horizontal_speed=0)
    t.sleep(dist/v)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    return


def tourne(alpha):
    N = int(alpha/4.7)
    for i in range(N):
        Motor.Move(vertical_speed=0, horizontal_speed=h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)
    return

def parcours(L):
    '''L = liste de marqueurs à visiter'''
    deplacement(3) #Avance de 3 m = vers le centre
    L = [0] + L
    if search_balise(L[0]) :
        for k in range(len(L)-1):
            i,j = L[k],L[k+1]
            cap = cv2.VideoCapture(CAMERA_PATH)
            Data = acquisition_donnees(cap) #[corners,ids,d,ecart_centre,ecart_centre_norme,angle]
            alpha = angle_ij(i,j,Data[2],Data[6])
            tourne(alpha)
            search(dico[j])
            break

dico = {"-3": 6, "-2" : 3, "-1" : 5, "0" : 10, "1" : 0, "2" : 2, "3" : 4}
L = [-2,1,-1]
parcours(L)
