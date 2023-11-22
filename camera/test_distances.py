#!/usr/bin/env python3
import cv2
import imutils
import numpy

CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"

def check():
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    flux = cv2.VideoCapture(CAMERA_PATH)
    _, img = flux.read()
    (corners, ids, rejected) = detector.detectMarkers(img)
    if ids != None :
        print(corners)
print("begins check")
while True :
    check()
