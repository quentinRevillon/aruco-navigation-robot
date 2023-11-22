#!/usr/bin/env python3
import cv2
import imutils
import numpy

CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"

def check(First = None):
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    flux = cv2.VideoCapture(CAMERA_PATH)
    _, img = flux.read()
    if First == 1 :
    	cv2.imwrite("test.jpg", img)
    (corners, ids, rejected) = detector.detectMarkers(img)
    if ids != None :
        corner = corners[0][0]
        c1,c2,c3,c4 =corner[0],corner[1],corner[2],corner[3]
        print(dist(c1,c2),dist(c2,c3),dist(c3,c4),dist(c4,c1))

print("begins check")
check(1)
while True :
    check()
