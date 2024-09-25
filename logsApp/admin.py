from django.contrib import admin
from .models import RegistredCars,EmployesInfo,InUseCars,LogsC
models_list = [LogsC,RegistredCars,EmployesInfo,InUseCars]


class LogsCAdmin(admin.ModelAdmin):
    list_display = ('id','Logs_employee_ins', 'taken_date', 'return_time','Logs_car_ins')  # Display these fields in the list view
    search_fields = ('taken_date', 'return_time')
    list_filter = ('taken_date',)  # Add filters for the taken_date field

class RegCarsAdmin(admin.ModelAdmin):
    list_display = ('carNumber','vType','section','cownerName','cownerEmpNumber')  # Display these fields in the list view
    search_fields = ('vType','id')
    list_filter = ('vType',)



admin.site.register(LogsC, LogsCAdmin)
admin.site.register(RegistredCars, RegCarsAdmin)
admin.site.register(EmployesInfo)
admin.site.register(InUseCars)
 
