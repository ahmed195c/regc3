# from .empinfo import empInfo
# from .cars import carsList


# def seedemp(request):

#     for i in carsList:
#         try:
#             RegistredCars.objects.get(carNumber=i["vnumber"])
#             pass
#         except RegistredCars.DoesNotExist:
#             RegistredCars.objects.create(carYear=i["Myear"],
#                                                 cownerEmpNumber=i["empid"],
#                                                 cownerName=i["empName"],
#                                                 cownerPhone=i["tel"],
#                                                 section=i["section"],
#                                                 carNumber=i["vnumber"],
#                                                 vType=i["vType"],
#                                                 )
            
#     for i in empInfo:
#         try:
#             EmployesInfo.objects.get(ceoNumber=i["empId"])
#             pass
#         except EmployesInfo.DoesNotExist:
#             EmployesInfo.objects.create(ceoName=i["empName"],
#                                             ceoNumber=i["empId"],
#                                             phoneNumber=i["tel"],
#                                             position=i["job"],
#                                             section=i["Sections"],
#                                             )
    
#     return HttpResponse("done")