

# tosave new data

# new = RegistredCars.objects.create(carYear=i["Myear"],
#                                         cownerEmpNumber=ceon,
#                                         cownerName=i["empName"],
#                                         cownerPhone=i["tel"],
#                                         section=i["section"],
#                                         carNumber=i["vnumber"],
#                                         vType=i["vType"],
#                                         )



# savin multi emp info 

# def seedCars(request):
#     # print(carsList)
#     for i in empInfo:
        
#         new = EmployesInfo.objects.create(ceoNumber=i["empId"],
#                                     ceoName=i["empName"],
#                                     phoneNumber=i["tel"],
#                                     section=i["Sections"],
#                                     position=i["job"]
#                                     )
#         new.save()
#     return  redirect('logslink')