import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration(main={"size": (2592, 1944)})
picam.configure(config)

picam.start_preview(Preview.QTGL)

for i in range(10):
    picam.start()
    input('££££')
    picam.capture_file(f"calibration/photo/{i}.jpg")

picam.close()
