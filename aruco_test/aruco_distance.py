import cv2
from cv2 import aruco
import numpy as np

matrix = np.array([[2.15047552e+03, 0.00000000e+00, 6.17240716e+02],
                   [0.00000000e+00, 2.15215949e+03, 4.49841712e+02],
                   [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distortionCoeffs = np.array([[ 1.14570525e-01, -1.65621384e+00, -2.70686270e-03, -1.52625388e-02,
   3.58384525e+01]])

flux = cv2.VideoCapture(0)
while True:
    _, img = flux.read()
    arucoDict = aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
    arucoParams = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(img)
    cv2.imshow("flux", img)
    if ids:
        # print(corners)
        p = aruco.estimatePoseSingleMarkers(corners[0], 0.028, matrix, distortionCoeffs)
        # print(p)
        print(np.linalg.norm(p[1]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    