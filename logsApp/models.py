from django.db import models
import os
import shutil
from django.db.models.signals import post_delete
from django.dispatch import receiver

def fines_accident_file_upload_to(instance, filename):
    car_number = instance.accidents_record.car.carNumber if instance.accidents_record.car else 'unknown'
    return f'fines_accidents/{car_number}_{instance.accidents_record.id}/{filename}'

def fines_accident_pdf_upload_to(instance, filename):
    car_number = instance.car.carNumber if instance.car else 'unknown'
    return f'fines_accidents/{car_number}_{instance.id}/{filename}'

def paid_fine_image_upload_to(instance, filename):
    return f'paid_fines/{instance.id}_{instance.car.carNumber}/{filename}'

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


class AccidentsRecord(models.Model):
    car = models.ForeignKey(RegistredCars, related_name="accidents", on_delete=models.CASCADE, null=True)
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
    accidents_record = models.ForeignKey(AccidentsRecord, related_name='images', on_delete=models.CASCADE,default=None)
    image = models.ImageField(upload_to=fines_accident_file_upload_to)
    def __str__(self):
        return str(f" {self.accidents_record.pk} " )

class LicenseFile(models.Model):
    accidents_record = models.ForeignKey(AccidentsRecord, related_name='license_files', on_delete=models.CASCADE,default=None)
    file = models.FileField(upload_to=fines_accident_file_upload_to)
    def __str__(self):
        return str(f" {self.accidents_record.pk} " )

class FinesRecord(models.Model):
    car = models.ForeignKey(RegistredCars, on_delete=models.CASCADE, null=True)
    employe = models.ForeignKey(EmployesInfo, blank=True,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    paidDate = models.DateField(null=True, blank=True)
    paid_fine_image = models.FileField(upload_to=paid_fine_image_upload_to, null=True, blank=True, max_length=500)

    def delete(self, *args, **kwargs):
        if self.paid_fine_image:
            directory = os.path.dirname(self.paid_fine_image.path)
            if os.path.exists(directory):
                shutil.rmtree(directory)
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(f" {self.pk} ")

@receiver(post_delete, sender=FinesAccidentsImage)
def delete_fines_accidents_image_files(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
        directory = os.path.dirname(instance.image.path)
        if os.path.exists(directory):
            shutil.rmtree(directory)

@receiver(post_delete, sender=LicenseFile)
def delete_license_file_files(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
        directory = os.path.dirname(instance.file.path)
        if os.path.exists(directory):
            shutil.rmtree(directory)

@receiver(post_delete, sender=AccidentsRecord)
def delete_accidents_record_files(sender, instance, **kwargs):
    if instance.report_pdf_file:
        if os.path.isfile(instance.report_pdf_file.path):
            os.remove(instance.report_pdf_file.path)
        directory = os.path.dirname(instance.report_pdf_file.path)
        if os.path.exists(directory):
            shutil.rmtree(directory)
    if instance.car_paperwork_file:
        if os.path.isfile(instance.car_paperwork_file.path):
            os.remove(instance.car_paperwork_file.path)
        directory = os.path.dirname(instance.car_paperwork_file.path)
        if os.path.exists(directory):
            shutil.rmtree(directory)

