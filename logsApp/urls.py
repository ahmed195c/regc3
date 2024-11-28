from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "logsApp"
urlpatterns = [
    path('', views.index, name='index'),
    path('add/',views.registerCar,name="add"),
    path("logs/",views.logsfunc,name='logslink'),
    path("ret/",views.returnCar, name="ret"),
    path("finec/",views.fineC,name='finec'),
    path('export/excel/', views.export_to_excel, name='export_to_excel'),
    path('addNewEmp/',views.addNewEmp, name="addNewEmp"),
    path("finesAccidents/", views.finesAccidents, name="finesAccidents")
]
