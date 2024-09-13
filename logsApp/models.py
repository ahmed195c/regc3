from django.db import models

# Create your models here.

class RegistredCars(models.Model):
    carNumber = models.IntegerField(default=0)
    carName = models.TextField(max_length=100,null=True)
    carCode = models.IntegerField(default=0)
    carIsInparking = models.BooleanField(default=True)
    def __str__(self):
        return str(f" carIsInparking : {self.carIsInparking } car number: {self.carNumber} car name: {self.carName}")
   
    


class EmployesInfo(models.Model):
    EmpHaveCar = models.BooleanField(default=False)
    ceoNumber = models.IntegerField(default=0)
    ceoName = models.CharField(max_length=100)
    phoneNumber = models.IntegerField( default='0000000000')
    email = models.EmailField(default='example@example.com')
    def __str__(self):
        return str(f" have a car: {self.EmpHaveCar}  name: {self.ceoNumber}   ceo number: {self.ceoName} ")


    
class InUseCars(models.Model):
    car = models.ForeignKey(RegistredCars, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployesInfo, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    logsc_ley = models.ForeignKey('LogsC', on_delete=models.CASCADE,null=True) 

class LogsC(models.Model):
    Logs_car_ins = models.ForeignKey(RegistredCars, on_delete=models.CASCADE)
    Logs_employee_ins = models.ForeignKey(EmployesInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    carIsInUse =  models.BooleanField(default=True)
    def __str__(self):
        return str(f" name: {self.Logs_car_ins.carNumber}  ceo nam: {self.Logs_employee_ins.ceoName} carIsINuSE: {self.carIsInUse}")