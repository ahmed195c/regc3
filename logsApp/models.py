from django.db import models

# Create your models here.

class RegistredCars(models.Model):
    carYear = models.IntegerField(null=True)
    cownerEmpNumber = models.IntegerField(null=True)
    cownerName= models.TextField(null=True)
    cownerPhone = models.TextField(null=True)
    section = models.TextField(null=True)
    carNumber = models.TextField(default=0)
    vType = models.TextField(max_length=100,null=True)
    carIsInparking = models.BooleanField(default=True)
    def __str__(self):
        return str(f" carIsInparking : {self.carIsInparking } car number: {self.carNumber} car name: {self.vType}")
   
    


class EmployesInfo(models.Model):
    EmpHaveCar = models.BooleanField(default=False)
    ceoNumber = models.IntegerField(default=0)
    ceoName = models.CharField(max_length=100)
    phoneNumber = models.TextField( default='0000000000')
    position = models.TextField()
    section = models.TextField()
    phone = models.TextField()
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
    dateFilter = models.DateField(blank=True, null=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    carIsInUse =  models.BooleanField(default=True)
    carNote = models.CharField(default=None,null=True, max_length=200,blank=True)
    def __str__(self):
        return str(f" name: {self.Logs_car_ins.carNumber}  ceo nam: {self.Logs_employee_ins.ceoName} carIsINuSE: {self.carIsInUse}")