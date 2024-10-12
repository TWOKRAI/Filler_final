from django.utils.translation import activate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings 
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Filler
from .models import Robot
from .models import Control


def index(request):
    if request.method == 'POST':
        # Получаем первый объект Filler или создаем новый, если его нет
        filler = Filler.objects.first()
        if not filler:
            filler = Filler()

        filler.info = 0
        filler.info2 = 1

        # Получаем данные из POST-запроса
        drink1 = request.POST.get('drink1', 0)
        drink2 = request.POST.get('drink2', 0)
        status = request.POST.get('status', 'false')

        # Преобразуем drink1 и drink2 в целые числа, если они не пустые
        drink1 = int(drink1) if drink1 else 0
        drink2 = int(drink2) if drink2 else 0

        # Ограничиваем значения от 0 до 500
        drink1 = max(0, min(500, drink1))
        drink2 = max(0, min(500, drink2))

        # Преобразуем status в булево значение
        status = status.lower() == 'true'

        print(f"Received data - drink1: {drink1}, drink2: {drink2}, status: {status} {filler.status}")

        # Проверяем и обновляем значения, если они изменились
        if filler.drink1 != drink1:
            print(f"Drink1 changed from {filler.drink1} to {drink1}")
            filler.drink1 = drink1

        if filler.drink2 != drink2:
            print(f"Drink2 changed from {filler.drink2} to {drink2}")
            filler.drink2 = drink2

        if filler.status != status:
            print(f"Status changed from {filler.status} to {status}")
            filler.status = status

        # Сохраняем изменения
        filler.save()

        return JsonResponse({
            'status': filler.status,
            'info': filler.info,
            'info2': filler.info2,
            'drink1': filler.drink1,
            'drink2': filler.drink2
        })

    # Получаем первый объект Filler или создаем новый, если его нет
    filler = Filler.objects.first()
    if not filler:
        filler = Filler()
        filler.save()

    return render(request, 'index.html', {'filler': filler})


def get_data(request):
    filler = Filler.objects.first()
    if not filler:
        filler = Filler()
        filler.save()

    return JsonResponse({
        'drink1': filler.drink1,
        'drink2': filler.drink2,
        'status': filler.status,
        'info': filler.info,
        'info2': filler.info2,
        'info3': filler.info3,
    })


def innotech(request):
    return render(request, 'innotech.html')


def settings1_view(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        print('language', language)
        if language:
            activate(language)
            request.session['django_language'] = language

            response = redirect('index')
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response

        # return redirect('index')

    return render(request, 'settings1.html')


def settings2_view(request):
    if request.method == 'POST':
        robot = Robot.objects.first()
        if not robot:
            robot = Robot()

        speed = request.POST.get('speed', 0)
        waiting = request.POST.get('waiting', 0)
        lasermode = request.POST.get('lasermode', 0)
        autovalue = request.POST.get('autovalue', None)
        presence_cup = request.POST.get('presence_cup', None)

        speed = int(speed) if speed else 0
        waiting = int(waiting) if waiting else 0

        speed = max(0, min(100, speed))
        waiting = max(0, min(500, waiting))

        autovalue = autovalue is not None
        presence_cup = presence_cup is not None

        if robot.speed != speed:
            robot.speed = speed

        if robot.time_wait != waiting:
            robot.time_wait = waiting

        if robot.laser_mode != lasermode:
            robot.laser_mode = lasermode

        if robot.autovalue != autovalue:
            robot.autovalue = autovalue

        if robot.presence_cup != presence_cup:
            robot.presence_cup = presence_cup

        robot.save()

        return redirect('settings2')

    robot = Robot.objects.first()
    if not robot:
        robot = Robot()
        robot.save()

    return render(request, 'settings2.html', {'robot': robot})


def reset_to_default(request): 
    filler = Filler.objects.first()
    robot = Robot.objects.first()
    control = Control.objects.first()

    filler.reset_to_default()
    robot.reset_to_default()
    control.reset_to_default()

    return redirect('settings2')


def control(request):
    return render(request, 'control.html')


@csrf_exempt
def set_control(request):
    if request.method == 'POST':
        # Получаем первый объект Control или создаем новый, если его нет
        control = Control.objects.first()
        if not control:
            control = Control()

        # Получаем данные из POST-запроса
        data = json.loads(request.body)

        calibration = data.get('calibration', False)
        panel = data.get('panel', False)
        motor = data.get('motor', False)

        # Проверяем и обновляем значения, если они изменились
        if control.calibration != calibration:
            control.calibration = calibration

        if control.panel != panel:
            control.panel = panel

        if control.motor != motor:
            control.motor = motor

        # Сохраняем изменения
        control.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)