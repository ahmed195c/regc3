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

        if ceoNmberInput or carNumperInput:
            try:
                caro = RegistredCars.objects.get(carNumber=carNumperInput,carIsInparking=True)
                employeo = EmployesInfo.objects.get(ceoNumber=ceoNmberInput,EmpHaveCar=False)
                # If a car with this number exists, you can work with 'car'
            except EmployesInfo.DoesNotExist:
               print("emp or car are in use")
            return render(request,"logsApp/registerCar.html",{ "message":"car no ceo numberworng","l":allInUseCars })
        
        
             
        try:
                inusecart = InUseCars.objects.get(car=caro,employee=employeo)
                print("car is in use")
        except InUseCars.DoesNotExist:
                print("")
                employeo.EmpHaveCar = True
                caro.carIsInparking = False
                caro.save()
                employeo.save()
                new = InUseCars(car=caro,employee=employeo)
                new.save()
                newL = LogsC(Logs_car_ins=caro,Logs_employee_ins=employeo)
                newL.save()
        print("Car found")
        return render(request,"logsApp/registerCar.html",{"car":caro, "em":employeo,"l":allInUseCars })
            # Do something with 'car'
    except RegistredCars.DoesNotExist:
            # Handle the case where the car number doesn't exist
        print("Car not found")

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