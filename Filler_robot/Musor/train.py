import cv2
import numpy as np
from picamera2 import Picamera2

class Camera:
    def __init__(self):
        self.picam = Picamera2()
        config = self.picam.create_still_configuration(main={"size": (2592, 1944)})
        self.picam.configure(config)

    def start_stream(self):
        self.picam.start()

    def stop_stream(self):
        self.picam.stop()


    def read_frame(self):
        return self.picam.capture_array()

camera = Camera()
camera.start_stream()

while True:
    frame = camera.read_frame()
       
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([110, 150, 50])
    upper_blue = np.array([130, 255, 120])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            cv2.drawContours(frame, [contour], 0, (0, 0, 255), 3)  # ������ ����� ������ �������

    cv2.imshow('Video Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop_stream()
cv2.destroyAllWindows()
