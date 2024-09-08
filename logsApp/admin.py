from django.contrib import admin
from .models import RegistredCars,EmployesInfo,InUseCars,LogsC
models_list = [LogsC,RegistredCars,EmployesInfo,InUseCars]
# Register your models here.

for i in models_list:
    admin.site.register(i)    
