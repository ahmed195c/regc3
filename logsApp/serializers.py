from rest_framework import serializers
from .models import LogsC, EmployesInfo, RegistredCars

class EmployesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployesInfo
        fields = ['id', 'ceoNumber', 'ceoName', 'phoneNumber', 'jobTtile', 'department', 'unit', 'nationality']

class RegistredCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistredCars
        fields = ['id', 'carNumber', 'vType', 'carYear', 'cownerName', 'section']

class LogsCSerializer(serializers.ModelSerializer):
    employee = EmployesInfoSerializer(source='Logs_employee_ins', read_only=True)
    car = RegistredCarsSerializer(source='Logs_car_ins', read_only=True)
    
    class Meta:
        model = LogsC
        fields = [
            'id', 
            'employee', 
            'car', 
            'carIsInUse', 
            'created_at', 
            'taken_date', 
            'taken_time', 
            'ended_at', 
            'return_date', 
            'return_time', 
            'carNote'
        ]
