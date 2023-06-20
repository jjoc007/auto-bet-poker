from deteccion_fase import *
import pytesseract

import cv2
import numpy as np

templates = load_cards()
img = cv2.imread('pantallas/0e2dd581-66d2-46bb-8187-caba264a744a.png',0)
# Obtiene las dimensiones de la imagen
height, width = img.shape
if width > 1920 and height > 956:
    new_size = (1920, 956)
    resized_img = cv2.resize(img, new_size)
else:
    resized_img = img

resized_img = cv2.normalize(resized_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

x = 600
y = 410
wr = 800
hr = 200
table = resized_img[y:y+hr, x:x+wr]

result = detect_cards(table, templates)
print(result)

cv2.imshow('Matches', table)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
templates = load_cards()

img = cv2.imread('pantallas/turn-1.png', 0)
template = cv2.imread('cards/P_J.png', 0)

# Crear el detector ORB
orb = cv2.ORB_create()


# Detectar las características y calcular los descriptores
kp1, des1 = orb.detectAndCompute(img, None)
kp2, des2 = orb.detectAndCompute(template, None)

des1 = np.float32(des1)
des2 = np.float32(des2)

# Crear un matcher BFMatcher y emparejar los descriptores
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Ordenar los matches por distancia
matches = sorted(matches, key = lambda x:x.distance)

# Dibujar los primeros 10 matches
out_img = cv2.drawMatches(img, kp1, template, kp2, matches[:10], None, flags=2)

cv2.imshow('Matches', out_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

'''
screen = cv2.imread('pantallas/1-river.png', cv2.IMREAD_GRAYSCALE)
cv2.rectangle(screen, (1600, 927), (2500, 1200), (0, 0, 255), 2)

cv2.imshow('Image', screen)
# Esperar a que se presione una tecla para cerrar la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


