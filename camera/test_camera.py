import cv2
WC = cv2.VideoCapture(0)
while True:
    RET, F = WC.read()
    cv2.imshow("Live Feeds", F)
    KEY = cv2.waitKey(1)
    if KEY == ord("q"):
        break
WC.release()
cv2.destroyAllWindows()