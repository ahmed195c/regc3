from django.shortcuts import render
from django.utils import timezone
from logsApp.models import  RegistredCars , EmployesInfo,InUseCars,LogsC
import re
from django.http import HttpResponse
from openpyxl.styles import Font, Alignment, PatternFill
import pytz
from datetime import datetime
from django.db.models import Q
from django.db import IntegrityError

from django.http import HttpResponse
import pandas as pd
def remove_non_numeric(s):
    
    return re.sub(r'\D', '', s)

def removechars(c):
    characters_to_remove = "!@#$%^&*()_+|?}{:><`1234567890"

    for char in characters_to_remove:
        c = c.replace(char, "")
    
    return c
def index(request):
    return render(request, "logsApp/layout.html")

def registerCar(request):
    allnUseCars = InUseCars.objects.all().order_by('-id')
    if request.method == "POST":
        ceoNInput = request.POST["ceoNumber"]
        carNInput = request.POST.get("carNumber")

        try:
            itsinuse = LogsC.objects.get(Logs_employee_ins__ceoNumber=ceoNInput,carIsInUse=True)
            return render(request, "logsApp/registerCar.html",{"itsinuse":itsinuse,"l":allnUseCars})
        except LogsC.DoesNotExist:
            pass
        
        try:
            carIsInUse = LogsC.objects.get(Logs_car_ins__carNumber=carNInput,carIsInUse=True)
            return render(request, "logsApp/registerCar.html",{"carIsInUse":carIsInUse,"l":allnUseCars})        
        except LogsC.DoesNotExist:
            pass

        try:
            empExists = EmployesInfo.objects.get(ceoNumber=ceoNInput,EmpHaveCar=False)
        except EmployesInfo.DoesNotExist:
            empDoseNotEXISTS = " الرقم الاداري غير صحصح "
            return render(request, "logsApp/registerCar.html",{"empDoseNotEXISTS":empDoseNotEXISTS,"l":allnUseCars})
        try:
            carExists = RegistredCars.objects.get(carNumber=carNInput,carIsInparking=True)
        except RegistredCars.DoesNotExist:
            carDNE = "رقم المركبة غير صحيح أو تم استخدامه"
            return render(request, "logsApp/registerCar.html",{"carDNE":carDNE,"l":allnUseCars})
        
        InUseCars.objects.create(car=carExists, employee=empExists)
        LogsC.objects.create(Logs_employee_ins=empExists, Logs_car_ins=carExists)

        empExists.EmpHaveCar = True
        empExists.save()
        carExists.carIsInparking = False
        carExists.save()
        sucssuMessge = "تم التسجيل بنجاح"
        return render(request, "logsApp/registerCar.html",{"sucssuMessge":sucssuMessge,"l":allnUseCars})
    
    return render(request, "logsApp/registerCar.html",{"l":allnUseCars})


def returnCar(request):
    if request.method == "POST":
        ceonumberq = remove_non_numeric(request.POST.get("ceonumber")).strip()
        empnote = request.POST.get("empnote")
        carCondq = request.POST.get("carCd")
        allInUseCars = InUseCars.objects.all().order_by('-id')
        dubai_tz = pytz.timezone('Asia/Dubai')
        try:
           empinstance = EmployesInfo.objects.get(ceoNumber=ceonumberq)
        except EmployesInfo.DoesNotExist:
             retErrm = " الرقم الاداري غير صحيح "
             return render(request,"logsApp/registerCar.html", {"retErrm":retErrm,"l":allInUseCars})
        try:
          inusecatinstance = InUseCars.objects.get(employee=empinstance)
        except InUseCars.DoesNotExist:
            retCarErr = "لاتوجد مركبه مرتبطه بل رقم الاداري "
            return render(request,"logsApp/registerCar.html", {"retCarErr":retCarErr,"l":allInUseCars})
        retSucssM = "تم اعاده المركبه بنجاح "
        registerCarinst = RegistredCars.objects.get(carNumber=inusecatinstance.car.carNumber)
        inusecarinstance = LogsC.objects.get(Logs_employee_ins=empinstance,carIsInUse=True)
        inusecarinstance.ended_at = timezone.now().astimezone(dubai_tz)
        inusecarinstance.return_date = timezone.now().astimezone(dubai_tz).date()
        inusecarinstance.return_time = timezone.now().astimezone(dubai_tz).time()
        inusecarinstance.carCondition = carCondq
        inusecarinstance.carIsInUse = False
        inusecarinstance.carNote = empnote
        registerCarinst.carIsInparking = True
        empinstance.EmpHaveCar = False
        empinstance.save()
        inusecarinstance.save()
        registerCarinst.save()
        inusecatinstance.delete()
        return render(request, "logsApp/registerCar.html",{"retSucssM":retSucssM,"l":allInUseCars})



def logsfunc(request):
    carnF = request.GET.get('carNumper')
    ceoN = request.GET.get('ceoN')
    dateF = request.GET.get('date')
    showAllq = request.GET.get('showAll')

    print(carnF)
    
    filters = {}
        
    if dateF:
        filters['taken_date'] = dateF

    if ceoN:
        filters['Logs_employee_ins__ceoNumber'] = ceoN.strip()

    if carnF:
        filters['Logs_car_ins__carNumber'] = carnF.strip()

    searchByCarNm = LogsC.objects.filter(**filters).order_by('-id')
    
    if showAllq:
        alllogsq = LogsC.objects.all().order_by('-id')
        return render(request,"logsApp/logs.html",{'alllogs':alllogsq})
    current_date = datetime.now().date()
    print(current_date)
    alllogs = LogsC.objects.filter(Q(taken_date=current_date) | Q(taken_date__isnull=True)).order_by('-id')
    logs = LogsC.objects.all()
    return render(request, "logsApp/logs.html", {'alllogs': searchByCarNm})



def export_to_excel(request):
    dubai_tz = pytz.timezone('Asia/Dubai')
    
    data = LogsC.objects.select_related('Logs_employee_ins', 'Logs_car_ins').all().order_by('-id')

    export_data = []
    for log in data:
        created_at_dubai = log.created_at.astimezone(dubai_tz)
        taken_time_dubai = (log.taken_time.replace(tzinfo=dubai_tz) if log.taken_time else None)
        ended_at_dubai = log.ended_at.astimezone(dubai_tz) if log.ended_at else None
        return_time_dubai = (log.return_time.replace(tzinfo=dubai_tz) if log.return_time else None)

        export_data.append({
            'ID': log.id,
            'رقم السياره': log.Logs_car_ins.carNumber,
            'الاسم': log.Logs_employee_ins.ceoName,
            'الرقم الاداري': log.Logs_employee_ins.ceoNumber,
            'تاريخ ووقت الاستلام': created_at_dubai.strftime('%Y-%m-%d %I:%M %p'),
            'تاريخ الاستلام': log.taken_date,
            'وقت الاستلام': taken_time_dubai.strftime('%I:%M %p') if taken_time_dubai else None,
            'تاريخ و وقت التسليم': ended_at_dubai.strftime('%Y-%m-%d %I:%M %p') if ended_at_dubai else None,
            'تاريخ التسليم': log.return_date,
            'وقت التسليم': return_time_dubai.strftime('%I:%M %p') if return_time_dubai else None,
            'ملاحظه على المركبه': log.carNote,
            'قسم الموظف': log.Logs_employee_ins.section
        })

    
    df = pd.DataFrame(export_data)

    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="logs_data.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Logs Data')

        workbook = writer.book
        worksheet = writer.sheets['Logs Data']

       
        worksheet.sheet_view.rightToLeft = True

       
        header_font = Font(size=16, bold=True, color='000000')
        header_fill = PatternFill(start_color='B7E1A1', end_color='B7E1A1', fill_type='solid')
        cell_font = Font(size=16)
        center_alignment = Alignment(horizontal='center')

       
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_alignment

       
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
            for cell in row:
                cell.font = cell_font
                cell.alignment = center_alignment

       
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 4)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    return response



def addNewEmp(request):
    if request.method == "POST":
        empNameq = request.POST.get('empName')
        empNumber = request.POST.get('empNumber')
        sa = removechars(empNameq)
        print(sa)
        try:
            EmployesInfo.objects.create(ceoName=sa,ceoNumber=empNumber)
            dd = " working"
        except IntegrityError:
            dd = "الرقم الاداري موجود من قبل"
        return render(request, "logsApp/addNewEmp.html", {'dd': dd})
    return render(request,"logsApp/addNewEmp.html")





def fineC(request):
    if request.method == "POST":
        fine_date = request.POST.get('finedate')
        fine_time = request.POST.get('finetime')
        fine_car_number = request.POST.get('finecar')
        print(f"Fine date is: {fine_date}")
        print(f"Fine time is: {fine_time}")
        dubai_tz = pytz.timezone('Asia/Dubai')
        combined_fine_datetime = dubai_tz.localize(timezone.datetime.strptime(f"{fine_date} {fine_time}", '%Y-%m-%d %H:%M'))
        print(combined_fine_datetime.time())
        try:
            car_ins = RegistredCars.objects.get(carNumber=fine_car_number)

            finon = LogsC.objects.get(Logs_car_ins=car_ins,
                                      created_at__lte = combined_fine_datetime,
                                      ended_at__gte = combined_fine_datetime
                                      )
            print(finon)
            return render(request, "logsApp/finespage.html",{"finon":finon})
        except RegistredCars.DoesNotExist:
            print(f"Car with number {fine_car_number} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    return render(request,"logsApp/finespage.html",)