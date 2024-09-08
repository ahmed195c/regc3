from django.urls import path
from . import views

app_name = "logsApp"
urlpatterns = [
    path('', views.index, name='index'),
    path('add/',views.registerCar,name="add"),
    path("logs/",views.logsfunc,name="logslink"),
    path("ret/",views.returncar, name="ret"),
]