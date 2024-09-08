from django.contrib import admin
from .models import RegistredCars,EmployesInfo,InUseCars

# Register your models here.
admin.site.register(InUseCars)
admin.site.register(RegistredCars)
admin.site.register(EmployesInfo)