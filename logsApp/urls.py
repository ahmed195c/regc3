from django.urls import path
from . import views

app_name = "logsApp"
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.registerCar, name="add"),
    path("logs/", views.logsfunc, name='logslink'),
    path("ret/", views.returnCar, name="ret"),
    path("finec/", views.fineC, name='finec'),
    path('export/excel/', views.export_to_excel, name='export_to_excel'),
    path('addNewEmp/', views.addNewEmp, name="addNewEmp"),
    path("AccidentsRecords/", views.AccidentsRecords, name="AccidentsRecords"),
    path('carddetails/<int:fine_id>/', views.carddetails, name='carddetails'),
    path('markasfixed/<int:fine_id>/', views.markasfixed, name='markasfixed'),
    path('fine/<int:fine_id>/', views.fineDetails, name='fineDetails'),
    path('fine/<int:fine_id>/delete-image/', views.deleteFineImage, name='deleteFineImage'),
    path('fines/', views.fineC, name='finespage'),
]