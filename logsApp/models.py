from django.db import models


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
        return str(f" رقم المركبه: {self.carNumber}")    


class EmployesInfo(models.Model):
    EmpHaveCar = models.BooleanField(default=False)
    ceoNumber = models.CharField(default=0,max_length=100,unique=True)
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
    Logs_car_ins = models.ForeignKey(RegistredCars, on_delete=models.CASCADE, )
    Logs_employee_ins = models.ForeignKey(EmployesInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    taken_date = models.DateField(auto_now_add=True,null=True)
    taken_time = models.TimeField(auto_now_add=True,null=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    carIsInUse =  models.BooleanField(default=True)
    carNote = models.CharField(default=None,null=True, max_length=200,blank=True)
    def __str__(self):
        return str(f" name: {self.Logs_car_ins.carNumber}  ceo nam: {self.Logs_employee_ins.ceoName} carIsINuSE: {self.carIsInUse}")
    
class FinesAccidents(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/")