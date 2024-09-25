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



<div>
            <div class="msg-cont">
              {% if {{carDNE}} %}
              <div
                id="error-message"
                style="
                  background-color: #f8d7da;
                  color: #721c24;
                  padding: 10px;
                  border: 1px solid #f5c6cb;
                  border-radius: 5px;
                  margin-bottom: 20px;
                "
              ></div>

              <script>
                // Function to fade out the message
                setTimeout(function () {
                  var message = document.getElementById("error-message");
                  if (message) {
                    message.style.transition = "opacity 1s ease-out";
                    message.style.opacity = 0;
                    setTimeout(function () {
                      message.style.display = "none";
                    }, 1000);
                  }
                }, 5000);
              </script>
              {% endif %}
            </div>
          </div>