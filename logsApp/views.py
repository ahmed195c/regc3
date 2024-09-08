from django.shortcuts import render
from django import forms
from logsApp.models import  RegistredCars , EmployesInfo,InUseCars
# Create your views here.


def index(request):
    return render(request, "logsApp/layout.html")


def registerCar(request):
    allInUseCars = InUseCars.objects.all()
    if request.method == "POST":
        ceoN = request.POST["ceoNumber"]
        carnumberreq = request.POST.get("carNumber")  # Use .get() to avoid KeyError if carNumber is not in POST
        allregscars = RegistredCars.objects.all()
        print(allInUseCars)
        if carnumberreq:
            try:
                caro = RegistredCars.objects.get(carNumber=carnumberreq)
                employeo = EmployesInfo.objects.get(ceoNumber=ceoN)
                # If a car with this number exists, you can work with 'car'
                if carnumberreq:
                    try:
                        inusecart = InUseCars.objects.get(car=caro)
                        print("car is in use")
                    except InUseCars.DoesNotExist:
                        print("")
                        new = InUseCars(car=caro,employee=employeo)
                        new.save()
                
                print("Car found")
                return render(request,"logsApp/registerCar.html",{"car":caro, "em":employeo,"l":allInUseCars })
                # Do something with 'car'
            except RegistredCars.DoesNotExist:
                # Handle the case where the car number doesn't exist
                print("Car not found")

        return render(request, "logsApp/registerCar.html",{"all":allregscars,"l":allInUseCars})
    
    return render(request, "logsApp/registerCar.html",{"l":allInUseCars})


def logsfunc(request):
    return render(request, "logsApp/logs.html")