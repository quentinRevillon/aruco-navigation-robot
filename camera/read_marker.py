import cv2
import imutils

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
camera_path = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
flux = cv2.VideoCapture(camera_path)
while True:
    _, img = flux.read()
    (corners, ids, rejected) = detector.detectMarkers(img)
    print((ids))
    KEY = cv2.waitKey(1)
    if KEY == ord("q"):
        break
    if len(corners) > 0:
		# flatten the ArUco IDs list
        ids = ids.flatten()
		# loop over the detected ArUCo corners
        print(zip(corners, ids))

        for (markerCorner, markerID) in zip(corners, ids):
            print((markerCorner, markerID))
