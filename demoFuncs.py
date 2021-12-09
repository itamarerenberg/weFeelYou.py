import cv2


def takePicture():
    cam = cv2.VideoCapture(0)
    ret, image = cam.read()
    cam.release()
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def take_n_picture(n):
    cam = cv2.VideoCapture(0)
    images = []
    for i in range(n):
        ret, image = cam.read()
        images += [cv2.cvtColor(image, cv2.COLOR_RGB2BGR)]
    cam.release()
    return images