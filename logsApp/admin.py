from django.contrib import admin
from .models import RegistredCars,EmployesInfo,InUseCars,LogsC
models_list = [LogsC,RegistredCars,EmployesInfo,InUseCars]


class LogsCAdmin(admin.ModelAdmin):
    list_display = ('Logs_employee_ins__ceoName', 'taken_date', 'return_time','Logs_car_ins__carNumber')
    search_fields = ('taken_date','taken_time', 'return_time','Logs_car_ins__carNumber','Logs_employee_ins__ceoNumber')
    list_filter = ('taken_date','taken_time','Logs_car_ins__carNumber')

class RegCarsAdmin(admin.ModelAdmin):
    list_display = ('cownerName','carNumber','vType','section','cownerEmpNumber','carIsInparking')
    search_fields = ('vType','id')
    list_filter = ('vType',)

class InuseCarsAdmin(admin.ModelAdmin):
    list_display = ('employee__ceoName','car__carNumber',)
    search_fields = ('employee__ceoNumber','employee__ceoName')
    list_filter = ('start_date', )

admin.site.register(LogsC, LogsCAdmin)
admin.site.register(RegistredCars, RegCarsAdmin)
admin.site.register(EmployesInfo)
admin.site.register(InUseCars, InuseCarsAdmin)