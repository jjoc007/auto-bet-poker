import cv2
import uuid
import numpy as np
from PIL import Image
from io import BytesIO


def capture_screenshot(driver):
    image_id = uuid.uuid4()
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(screenshot))
    screenshot_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"pantallas/{image_id}.png", screenshot_image)

    height, width, _ = screenshot_image.shape
    if width > 1920 and height > 956:
        new_size = (1920, 956)
        resized_img = cv2.resize(screenshot_image, new_size)
    else:
        resized_img = screenshot_image

    resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    resized_img = cv2.normalize(resized_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    x = 500
    y = 410
    wr = 800
    hr = 200
    table = resized_img[y:y + hr, x:x + wr]
    return {
        'id': image_id,
        'table': table,
    }

# Procesa la imagen con OpenCV para reconocer cartas y elementos del tablero
# Este paso requerirá un trabajo adicional, como entrenar un modelo de aprendizaje profundo o
# utilizar técnicas de visión por computadora clásicas (umbralización, contornos, etc.)
