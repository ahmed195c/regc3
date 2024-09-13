kok = "smoke"

try:
  print(kok)
except kok.DoesNotExist:
        print("")
        # employeo.EmpHaveCar = True
        # caro.carIsInparking = False
        # caro.save()
        # employeo.save()
        new = InUseCars(car=caro,employee=employeo)
        new.save()
        newL = LogsC(Logs_car_ins=caro,Logs_employee_ins=employeo)
        newL.save()
        print("Car found")
return render(request,"logsApp/registerCar.html",{"car":caro, "em":employeo,"l":allInUseCars })



"اذا ما رجعت السياره للكراج و حصل مخالفه مرور عليها يتحمل من اخذها المسؤوليه"