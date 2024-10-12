
from django.db import models


class Filler(models.Model):
    DEFAULT_FILLER = 0
    DEFAULT_DRINK1 = 0
    DEFAULT_DRINK2 = False
    DEFAULT_STATUS = False
    DEFAULT_INFO = 0
    DEFAULT_INFO2 = 0
    DEFAULT_INFO3 = 0

    drink1 = models.IntegerField(default=DEFAULT_DRINK1)
    drink2 = models.IntegerField(default=DEFAULT_DRINK2)
    status = models.BooleanField(default=DEFAULT_STATUS)
    info = models.IntegerField(default=DEFAULT_INFO)
    info2 = models.IntegerField(default=DEFAULT_INFO2)
    info3 = models.IntegerField(default=DEFAULT_INFO3)


    def save(self, *args, **kwargs):
        if self.drink1 == '':
            self.drink1 = 0
        if self.drink2 == '':
            self.drink2 = 0

        self.drink1 = int(self.drink1)
        self.drink2 = int(self.drink2)

        super().save(*args, **kwargs)


    def reset_to_default(self): 
        self.drink1 = self.DEFAULT_DRINK1
        self.drink2 = self.DEFAULT_DRINK2
        self.status = self.DEFAULT_STATUS
        self.info = self.DEFAULT_INFO
        self.info2 = self.DEFAULT_INFO2
        self.info3 = self.DEFAULT_INFO3
        self.save()


class Robot(models.Model):
    DEFAULT_SPEED = 70
    DEFAULT_TIME_WAIT = 5
    DEFAULT_LASER_MODE = 2
    DEFAULT_AUTOVALUE = True
    DEFAULT_PRESENCE_CUP = True

    speed = models.IntegerField(default=DEFAULT_SPEED)
    time_wait = models.IntegerField(default=DEFAULT_TIME_WAIT)
    laser_mode = models.IntegerField(default=DEFAULT_LASER_MODE)
    autovalue = models.BooleanField(default=DEFAULT_AUTOVALUE)
    presence_cup = models.BooleanField(default=DEFAULT_PRESENCE_CUP)


    def reset_to_default(self): 
        self.speed = self.DEFAULT_SPEED
        self.time_wait = self.DEFAULT_TIME_WAIT
        self.laser_mode = self.DEFAULT_LASER_MODE
        self.autovalue = self.DEFAULT_AUTOVALUE
        self.presence_cup = self.DEFAULT_PRESENCE_CUP
        self.save()


class Control(models.Model):
    DEFAULT_CALIBRATION = False
    DEFAULT_PANEL = False
    DEFAULT_MOTOR = False

    calibration = models.BooleanField(default=DEFAULT_CALIBRATION)
    panel = models.BooleanField(default=DEFAULT_PANEL)
    motor = models.BooleanField(default=DEFAULT_MOTOR)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    

    def reset_to_default(self):
        self.calibration = self.DEFAULT_CALIBRATION
        self.panel = self.DEFAULT_PANEL
        self.motor = self.DEFAULT_MOTOR


    def __str__(self):
        return f"Control(calibration={self.calibration}, panel={self.panel}, motor={self.motor})"