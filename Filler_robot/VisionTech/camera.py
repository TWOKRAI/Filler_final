import cv2
import numpy as np
import math
from picamera2 import Picamera2
import logging
import os

#from Lib.Decorators.wrapper import _timing
from Filler_robot.VisionTech.perspective import Perspective


class Camera:
    def __init__(self):
        self.connect_0 = None

        self.print_on = True

        logging.debug("Initializing camera...")
        try:
            self.picam = Picamera2()
            logging.debug("Camera initialized successfully.")
        except RuntimeError as e:
            logging.error(f"Failed to initialize camera: {e}")
            raise

        #config = self.picam.create_still_configuration(main={"size": (2592, 1944)})
        config = self.picam.create_still_configuration(main={"size": (1640, 1232)})
        self.picam.configure(config)

        path = os.path.join('/home/innotech/Project/Filler/Filler_robot/VisionTech/calibration', 'camera_params.yml')
        self.cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
        # self.cv_file = cv2.FileStorage('Filler_robot/VisionTech/calibration/camera_params.yml', cv2.FILE_STORAGE_READ)
        self.camera_matrix = self.cv_file.getNode('K').mat()
        self.distortion_coeffs = self.cv_file.getNode('D').mat()
        self.cv_file.release()

        self.calibration_on = True
        
        #print(self.camera_matrix, self.distortion_coeffs)
        
        self.picam.start()
        
        self.img = []
        
        self.img_width = 640
        self.img_height = 640
        
        self.width_out = 640
        self.height_out = 640

        image = np.zeros((self.width_out, self.height_out, 3), dtype=np.uint8)
        
        self.point_pixel = [(113, 508), (212, 302), (522, 508), (423, 302)]
        self.point_real = [(-12, 12.5), (-12, 33.5), (12, 12.5), (12, 33.5)]
        
        self.perspective = Perspective(image, self.point_pixel, self.point_real)


    def running(self):
        self.read_cam()
    
    
    def stop(self):    
        self.picam.close()
        self.picam.stop()

    
    def calibraion(self, image):
        image = cv2.undistort(image , self.camera_matrix, self.distortion_coeffs)
        #image = cv2.fisheye.undistortImage(image, self.camera_matrix, self.distortion_coeffs)
        #image = image[:, 124:2468,:3]

        return image
    

    def read_cam(self) -> np.ndarray:
        img_read = self.picam.capture_array()
        
        #img_calibration = self.calibraion(img_read)
        img_calibration = img_read

        
        self.img_width, self.img_height = img_calibration.shape[1], img_calibration.shape[0]
        
        center = (self.img_width // 2, self.img_height // 2)

        angle = 0.0
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle, scale)

        image_warp = cv2.warpAffine(img_calibration, M, (self.img_width, self.img_height)) 

        #image_cropp = image_warp[100:1800, 480:2180,:3]
        image_cropp = image_warp[:, 200:1440]
        img_resize = cv2.resize(image_cropp, (self.width_out, self.height_out), interpolation = cv2.INTER_AREA)
        img_border = self.add_border(img_resize, 100)
        
        self.image_out = cv2.cvtColor(img_border, cv2.COLOR_RGB2BGR)
        self.image_copy = self.image_out.copy()

        self.img_width, self.img_height = self.image_out.shape[1], self.image_out.shape[0]

        # print('Camera read')
        # print(type(image_out), self.img_width, self.img_height)

        # cv2.imwrite('test2.png', self.image_out)
        
        return self.image_out
    

    def add_border(self, image, border_width):
        # Проверяем, что изображение имеет размер 640x640
        if image.shape[:2] != (640, 640):
            raise ValueError("Изображение должно быть размером 640x640 пикселей")

        # Проверяем, что ширина рамки не превышает половины размера изображения
        if border_width * 2 >= 640:
            raise ValueError("Ширина рамки слишком велика для изображения размером 640x640 пикселей")

        # Создаем новое изображение с черным фоном
        new_image = np.zeros((640, 640, 3), dtype=np.uint8)

        # Вычисляем размеры масштабированного изображения
        scaled_size = 640 - 2 * border_width

        # Масштабируем исходное изображение до размера scaled_size x scaled_size
        scaled_image = cv2.resize(image, (scaled_size, scaled_size))

        # Вставляем масштабированное изображение в центр нового изображения
        new_image[border_width:border_width + scaled_size, border_width:border_width + scaled_size] = scaled_image

        return new_image
