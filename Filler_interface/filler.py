import datetime

# Получить текущее время
now = datetime.datetime.now()
print("Текущее время: ", now.strftime("%H:%M:%S"))


class Filler:
    def __init__(self) -> None:
        self.param1 = True
        self.param111 = 1

        self.param2 = True
        self.param222 = 0

        self.param3 = 500
        self.param3_def = 500

        self.param4 = 600
        self.param4_def = 600

        self.param5 = 50
        self.param5_def = 50

        self.param6 = 50
        self.param6_def = 60

        self.param11 = 2
        self.param11_def = 2

        self.param21 = 0
        self.param21_def = False

        self.param31 = 1
        self.param31_def = 1

        self.param41 = 0
        self.param41_def = False

        now = datetime.datetime.now()
        self.static_time = now.strftime("%H:%M")
        def_datetime =  datetime.datetime(2023, 3, 15, 0, 0)
        self.static_time_def = def_datetime.strftime("%H:%M")

        self.static_ml = 60
        self.static_ml_def = 0

        now2 = now + datetime.timedelta(hours=2, minutes=30)
        self.static_time_all = '0д ' + now2.strftime("%H:%M")
        self.static_time_all_def =  '0д ' + def_datetime.strftime("%H:%M")

        self.static_ml_all = 600
        self.static_ml_all_def = 0


filler = Filler()