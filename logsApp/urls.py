from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "logsApp"
urlpatterns = [
    path('', views.index, name='index'),
    path('add/',views.registerCar,name="add"),
    path("logs/",views.logsfunc,name='logslink'),
    path("ret/",views.returncar, name="ret"),
    path('export/excel/', views.export_to_excel, name='export_to_excel'),
]