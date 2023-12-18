#!/usr/bin/env python3
import cv2
from cv2 import aruco
import imutils
from math import *
import numpy as np

CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
WIDTH, HEIGHT = 640, 480

def check():
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
    arucoParams = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    flux = cv2.VideoCapture(CAMERA_PATH)
    _, img = flux.read()
    alpha = 2.5  # Contrast control (1.0 means no change)
    beta = 40    # Brightness control (0 means no change)
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    (corners, ids, rejected) = detector.detectMarkers(adjusted_img)
    return ids,corners


# def get_distance(corners):
#     corner = corners[0][0]
#     c1,c2,c3,c4 =corner[0],corner[1],corner[2],corner[3]
#     S = dist(c1,c2)+dist(c2,c3)+dist(c3,c4)+dist(c4,c1)
#     M = S/4
#     d = 12376*(M**-1.122)
#     return max(d,0)

def get_distance(corners):

    matrix = np.array([[2.15047552e+03, 0.00000000e+00, 6.17240716e+02],
                    [0.00000000e+00, 2.15215949e+03, 4.49841712e+02],
                    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    distortionCoeffs = np.array([[ 1.14570525e-01, -1.65621384e+00, -2.70686270e-03, -1.52625388e-02,
    3.58384525e+01]])

    p = aruco.estimatePoseSingleMarkers(corners[0], 0.028, matrix, distortionCoeffs)

    return np.linalg.norm(p[1])

def get_middle(corners):
    corner = corners[0][0]
    c1,c2,c3,c4 =corner[0],corner[1],corner[2],corner[3]
    x = (c1[0] + c3[0]) / 2
    y = (c1[1] + c3[1]) / 2
    return x,y

if __name__ == "__main__":
    while True:
        ids, corners = check()
        if ids:
            print(get_distance(corners))
        
