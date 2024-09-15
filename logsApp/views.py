from django.shortcuts import render
from django import forms
from django.utils import timezone
from logsApp.models import  RegistredCars , EmployesInfo,InUseCars,LogsC
import re
# Create your views here.
def remove_non_numeric(s):
    # Use regular expression to replace all non-numeric characters with an empty string
    return re.sub(r'\D', '', s)

def index(request):
    return render(request, "logsApp/layout.html")



def registerCar(request):
    allnUseCars = InUseCars.objects.all()
    if request.method == "POST":
        ceoNInput = int(remove_non_numeric(request.POST["ceoNumber"]))
        carNInput = int(remove_non_numeric(request.POST.get("carNumber")))
        
        # check if emp exists and dose not have a car
        try:
            #if emp dosenot have a car and exists skip the except
            empExists = EmployesInfo.objects.get(ceoNumber=ceoNInput,EmpHaveCar=False)
        except EmployesInfo.DoesNotExist:
            # if emp dosent exists or do have a car return a message to not him about that
            empDoseNotEXISTS = "الرقم الاداري غير صحصح او مستخدم"
            return render(request, "logsApp/registerCar.html",{"empDoseNotEXISTS":empDoseNotEXISTS,"l":allnUseCars})
        
        try:
            carExists = RegistredCars.objects.get(carNumber=carNInput,carIsInparking=True)
        except RegistredCars.DoesNotExist:
            carDNE = "رقم السياره المدخل خاطء او السياره قيد الاستخدام"
            return render(request, "logsApp/registerCar.html",{"carDNE":carDNE,"l":allnUseCars})
        
        InUseCars.objects.create(car=carExists, employee=empExists)
        LogsC.objects.create(Logs_employee_ins=empExists, Logs_car_ins=carExists)

        empExists.EmpHaveCar = True
        empExists.save()

        carExists.carIsInparking = False
        carExists.save()
        return render(request, "logsApp/registerCar.html",{"l":allnUseCars})    
        
    return render(request, "logsApp/registerCar.html",{"l":allnUseCars})


def returncar(request):
    if request.method == "POST":
        ceonumberq = int(request.POST.get("ceonumber"))
        empnote = request.POST.get("empnote")
        allInUseCars = InUseCars.objects.all()

        try:
           empinstance = EmployesInfo.objects.get(ceoNumber=ceonumberq)
        except EmployesInfo.DoesNotExist:
             f = True
             return render(request,"logsApp/registerCar.html", {"f":f,"l":allInUseCars})
        try:
          inusecatinstance = InUseCars.objects.get(employee=empinstance)
        except InUseCars.DoesNotExist:
            g = True
            return render(request,"logsApp/registerCar.html", {"g":g,"l":allInUseCars})
        registerCarinst = RegistredCars.objects.get(carNumber=inusecatinstance.car.carNumber)
        print(inusecatinstance)
        print(inusecatinstance.employee)
        inusecarinstance = LogsC.objects.get(Logs_employee_ins=empinstance,carIsInUse=True)
        print(inusecarinstance)
        inusecarinstance.ended_at = timezone.now()
        inusecarinstance.carIsInUse = False
        inusecarinstance.carNote = empnote
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