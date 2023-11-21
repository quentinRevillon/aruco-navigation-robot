import numpy as np
import cv2

# Créez un tableau NumPy pour stocker l'image générée par ArUco
arr = np.zeros((300, 300), dtype=np.uint8)

# Obtenir un dictionnaire ArUco prédéfini
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

# Générer l'image du marqueur et stocker dans "arr"
marker_image = cv2.aruco.generateImageMarker(arucoDict, 0, 300)
arr = marker_image

# Sauvegarder l'image sur le disque
cv2.imwrite("./camera/aruco_1.png", arr)

# Afficher l'image (optionnel)
cv2.imshow("ArUCo Tag", arr)
cv2.waitKey(0)
cv2.destroyAllWindows()




