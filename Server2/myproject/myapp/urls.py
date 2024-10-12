# myapp/urls.py

from django.urls import path
from .views import settings1_view, index, innotech, get_data, settings2_view, reset_to_default, control, set_control

urlpatterns = [
    path('', index, name='index'),
    path('innotech/', innotech, name='innotech'),
    path('settings1/', settings1_view, name='settings1'),
    path('get_data/', get_data, name='get_data'),
    path('settings2/', settings2_view, name='settings2'),
    path('reset_to_default/', reset_to_default, name='reset_to_default'),
    path('control/', control, name='control'),
    path('set_control/', set_control, name='set_control'),
]
