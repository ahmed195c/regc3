from django.contrib import admin
from .models import RegistredCars, EmployesInfo, InUseCars, LogsC, AccidentsRecord, FinesAccidentsImage, LicenseFile, FinesRecord

class LogsCAdmin(admin.ModelAdmin):
    list_display = ('id','Logs_employee_ins', 'taken_date','taken_time','return_date', 'return_time','Logs_car_ins')
    search_fields = ('taken_date', 'return_time')
    list_filter = ('taken_date',)
    # readonly_fields = ('Logs_car_ins','Logs_employee_ins')

class RegCarsAdmin(admin.ModelAdmin):
    list_display = ('carNumber','vType','section','cownerName','cownerEmpNumber')
    search_fields = ('vType','id',"carNumber")
    list_filter = ()

class EmpInfoAdmin(admin.ModelAdmin):
    list_display = ('ceoName','ceoNumber','phoneNumber','position','section','email')
    search_fields = ('ceoName','ceoNumber','phoneNumber','position','section','email')
    list_filter = ('position','section')
admin.site.register(FinesRecord)
admin.site.register(LicenseFile)
admin.site.register(LogsC, LogsCAdmin)
admin.site.register(RegistredCars, RegCarsAdmin)
admin.site.register(EmployesInfo, EmpInfoAdmin)
admin.site.register(InUseCars)
admin.site.register(AccidentsRecord)
admin.site.register(FinesAccidentsImage)