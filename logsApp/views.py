from django.shortcuts import render
from django import forms
from django.utils import timezone
from logsApp.models import  RegistredCars , EmployesInfo,InUseCars,LogsC

# Create your views here.


def index(request):
    return render(request, "logsApp/layout.html")



def registerCar(request):
    allInUseCars = InUseCars.objects.all()
    if request.method == "POST":
        ceoNmberInput = request.POST["ceoNumber"]
        carNumperInput = request.POST.get("carNumber")
        try:
            print("ceo number 1")
            employeeNumperCheck = EmployesInfo.objects.get(ceoNumber=ceoNmberInput,EmpHaveCar=False)
        except EmployesInfo.DoesNotExist:
            employeeNumperNotFoundErrorMessage = "الرقم الاداري غير صحيح او مستخدم من قبل"
            return render(request,"logsApp/registerCar.html",{"EmpErr":employeeNumperNotFoundErrorMessage,"l":allInUseCars})
        try:
            print("carnumber 1")
            registredCarCheck = RegistredCars.objects.get(carNumber=carNumperInput,carIsInparking=True)
        except RegistredCars.DoesNotExist:
            carNotFoundErrorMessage = " رقم السيارة المدخل غير صحيح او مستخدم"
            return render(request, "logsApp/registerCar.html",{"carErr":carNotFoundErrorMessage,"l":allInUseCars})
        try:
            InUseCarCheck = InUseCars.objects.get(car=registredCarCheck,employee=employeeNumperCheck)
            print("in use car 1")
            
            return render(request, "logsApp/registerCar.html",{"l":allInUseCars})
        except InUseCars.DoesNotExist:
            newInuseCarTemp = InUseCars(car=registredCarCheck,employee=employeeNumperCheck)
            newInuseCarTemp.save()
            newLog = LogsC(Logs_employee_ins=employeeNumperCheck,Logs_car_ins=registredCarCheck)
            newLog.save()
            employeeNumperCheck.EmpHaveCar = True
            employeeNumperCheck.save()
            registredCarCheck.carIsInparking = False
            registredCarCheck.save()
            return render(request, "logsApp/registerCar.html",{"l":allInUseCars})    

    
    return render(request, "logsApp/registerCar.html",{"l":allInUseCars})


def returncar(request):
    if request.method == "POST":
        ceonumberq = request.POST.get("ceonumber")
        allInUseCars = InUseCars.objects.all()
        empinstance = EmployesInfo.objects.get(ceoNumber=ceonumberq)
        inusecatinstance = InUseCars.objects.get(employee=empinstance)
        registerCarinst = RegistredCars.objects.get(carNumber=inusecatinstance.car.carNumber)
        print(inusecatinstance)
        print(inusecatinstance.employee)
        inusecarinstance = LogsC.objects.get(Logs_employee_ins=empinstance,carIsInUse=True)
        print(inusecarinstance)
        inusecarinstance.ended_at = timezone.now()
        inusecarinstance.carIsInUse = False
        registerCarinst.carIsInparking = True
        empinstance.EmpHaveCar = False
        empinstance.save()
        inusecarinstance.save()
        registerCarinst.save()
        inusecatinstance.delete()
        return render(request, "logsApp/registerCar.html", {"l":allInUseCars})



def logsfunc(request):
    alllogs = LogsC.objects.all()
    return render(request, "logsApp/logs.html",{"alllogs":alllogs})