from django.db import models
import os

def fines_accident_file_upload_to(instance, filename):
    car_number = instance.fines_accident.car.carNumber if instance.fines_accident.car else 'unknown'
    return f'fines_accidents/{car_number}_{instance.fines_accident.id}/{filename}'

def fines_accident_pdf_upload_to(instance, filename):
    car_number = instance.car.carNumber if instance.car else 'unknown'
    return f'fines_accidents/{car_number}_{instance.id}/{filename}'

class RegistredCars(models.Model):
    carYear = models.IntegerField(null=True)
    cownerEmpNumber = models.IntegerField(null=True)
    cownerName= models.TextField(null=True)
    cownerPhone = models.TextField(null=True)
    section = models.TextField(null=True)
    carNumber = models.TextField(default='0')
    vType = models.TextField(max_length=100,null=True)
    carIsInparking = models.BooleanField(default=True)
    def __str__(self):
        return str(f" رقم المركبه: {self.carNumber}")    


class EmployesInfo(models.Model):
    EmpHaveCar = models.BooleanField(default=False)
    ceoNumber = models.CharField(default='0', max_length=100, unique=True)
    ceoName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100, default='0000000000')
    position = models.CharField(max_length=100,default="الوظيفه")
    section = models.CharField(max_length=100,default="القسم")
    email = models.EmailField(default='example@example.com')
    def __str__(self):
        return str(f"  الرقم الاداري: {self.ceoNumber}  :الاسم {self.ceoName} ")


class InUseCars(models.Model):
    car = models.ForeignKey(RegistredCars, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployesInfo, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    logsc_ley = models.ForeignKey('LogsC', on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(f"مستخدم المركبه : {self.employee.ceoName} |||  رقم المركبه : {self.car.carNumber}")


class LogsC(models.Model):
    Logs_employee_ins = models.ForeignKey(EmployesInfo, on_delete=models.CASCADE)
    Logs_car_ins = models.ForeignKey(RegistredCars, on_delete=models.CASCADE)
    carIsInUse = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    carNote = models.TextField(null=True, blank=True)
    taken_date = models.DateField(null=True, blank=True)
    taken_time = models.TimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['Logs_employee_ins', 'carIsInUse']),
            models.Index(fields=['Logs_car_ins', 'carIsInUse']),
            models.Index(fields=['created_at']),
            models.Index(fields=['ended_at']),
        ]

    def __str__(self):
        return str(f" name: {self.Logs_car_ins.carNumber}  ceo nam: {self.Logs_employee_ins.ceoName} carIsINuSE: {self.carIsInUse}")


class FinesAccidents(models.Model):
    car = models.ForeignKey(RegistredCars, on_delete=models.CASCADE, null=True)
    employees = models.ManyToManyField(EmployesInfo, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    report_date = models.DateField(null=True, blank=True)
    fixin_date = models.DateField(null=True, blank=True)
    report_pdf_file = models.FileField(upload_to=fines_accident_pdf_upload_to, null=True, blank=True, max_length=500)
    car_paperwork_file = models.FileField(upload_to=fines_accident_pdf_upload_to, null=True, blank=True, max_length=500)
    def __str__(self):
        return str(f" {self.pk} " )

class FinesAccidentsImage(models.Model):
    fines_accident = models.ForeignKey(FinesAccidents, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=fines_accident_file_upload_to)
    def __str__(self):
        return str(f" {self.fines_accident.pk} " )

class LicenseFile(models.Model):
    fines_accident = models.ForeignKey(FinesAccidents, related_name='license_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=fines_accident_file_upload_to)
    def __str__(self):
        return str(f" {self.fines_accident.pk} " )

class FinesRecord (models.Model):
    car = models.ForeignKey(RegistredCars, on_delete=models.CASCADE, null=True)
    employe = models.ForeignKey(EmployesInfo, blank=True,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    paidDate = models.DateField(null=True, blank=True)

