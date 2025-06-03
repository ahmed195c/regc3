from logsApp.models import MaintanceLogs, InGarageCars, RegistredCars, EmployesInfo, InUseCars, LogsC, AccidentsRecord, FinesAccidentsImage, LicenseFile, FinesRecord, GivenCarsToOtherAdminstrations
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl.styles import Font, Alignment, PatternFill
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from .newempData import newemp
from .empinfo import empInfo
from .cars import carsList
import pandas as pd
import shutil
import pytz
import os
import re

# REST Framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import LogsCSerializer


def seedemp(request):
    for i in newemp:
        emp, created = EmployesInfo.objects.update_or_create(
            ceoNumber=i["empId"],
            defaults={
                'ceoName': i["empName"],
                'phoneNumber': i["tel"],
                'jobTtile': i["jobTitle"],
                'department': i["department"],
                'unit': i["unit"],
                'nationality': i["nationality"]
            }
        )

    for q in carsList:
        car, created = RegistredCars.objects.update_or_create(
            carNumber=q["vnumber"],
            defaults={
                'vType': q["vType"],
                'carYear': q['Myear'],
                'cownerEmpNumber': q['empid'],
                'cownerName': q['empName'],
            }
        )

    return HttpResponse("done")


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
    all_in_use_cars = InUseCars.objects.all().order_by('-id')
    dubai_tz = pytz.timezone('Asia/Dubai')
    current_time = timezone.now().astimezone(dubai_tz)
    if request.method == "POST":
        ceo_number = request.POST.get("ceoNumber").strip()
        car_number = request.POST.get("carNumber").strip()
        car_number = car_number.replace("/", "-")
       # تاكد اذا كان الرقم الاداري مستعمل 
        try:
            its_in_use = LogsC.objects.get(Logs_employee_ins__ceoNumber=ceo_number, carIsInUse=True)
            return render(request, "logsApp/registerCar.html", {
                "itsinuse": its_in_use,
                "l": all_in_use_cars,
                "ceoNumber": "",
                "carNumber": car_number,
            })
        except LogsC.DoesNotExist:
            pass
        # تاكد اذا كانت المركبه قيد الاستخدام 
        try:
            car_is_in_use = LogsC.objects.get(Logs_car_ins__carNumber=car_number, carIsInUse=True)
            return render(request, "logsApp/registerCar.html", {
                "carIsInUse": car_is_in_use,
                "l": all_in_use_cars,
                "ceoNumber": ceo_number,
                "carNumber": "",
            })
        except LogsC.DoesNotExist:
            pass
        # تاكد اذا كانت المركبه معطاه لاداره اخرى
        try:
            car_given_to_other_admin = GivenCarsToOtherAdminstrations.objects.get(car__carNumber=car_number, carIsInUse=True)
            message = "المركبه معطاه لاداره اخرى"
            return render(request, "logsApp/registerCar.html", {
                "message": message,
                "carGivenToOtherAdmin": car_given_to_other_admin,
                "l": all_in_use_cars,
                "ceoNumber": ceo_number,
                "carNumber": "",
            })
        except GivenCarsToOtherAdminstrations.DoesNotExist:
            pass
        # تاكد اذا كان الرقم الاداري صحيح وليس لديه مركبه
        try:
            emp_exists = EmployesInfo.objects.get(ceoNumber=ceo_number, EmpHaveCar=False)
        except EmployesInfo.DoesNotExist:
            emp_does_not_exist = "الرقم الاداري المدخل غير صحيح"
            return render(request, "logsApp/registerCar.html", {
                "empDoseNotEXISTS": emp_does_not_exist,
                "l": all_in_use_cars,
                "ceoNumber": "",
                "carNumber": car_number,
            })
        #تاكد اذا كان رقم المركبه صحيح وفي الباركنج
        try:
            car_exists = RegistredCars.objects.get(carNumber=car_number, carIsInparking=True)
        except RegistredCars.DoesNotExist:
            car_dne = "رقم المركبة المدخل غير صحيح"
            return render(request, "logsApp/registerCar.html", {
                "carDNE": car_dne,
                "l": all_in_use_cars,
                "ceoNumber": ceo_number,
                "carNumber": "",
            })
        current_time = timezone.now().astimezone(dubai_tz)
        # حفظ بينات المستلم في قائمة مركبات قيد الاستخدام 
        InUseCars.objects.create(car=car_exists, employee=emp_exists ,create_date=current_time.date(), create_time=current_time.time())
        #حفظ البيانات في سجل الاستلام و التسجيل 
        LogsC.objects.create(Logs_employee_ins=emp_exists, Logs_car_ins=car_exists, taken_date=current_time.date(), taken_time=current_time.time())

        emp_exists.EmpHaveCar = True
        emp_exists.save()
        car_exists.carIsInparking = False
        car_exists.save()

        success_message = "تم التسجيل بنجاح"
        return redirect("/add/")


    
        return render(request, "logsApp/registerCar.html", {
            "sucssuMessge": success_message,
            "l": all_in_use_cars
        })

    return render(request, "logsApp/registerCar.html", {"l": all_in_use_cars})

def returnCar(request):
    if request.method == "POST":
        ceo_number = remove_non_numeric(request.POST.get("ceonumber")).strip()
        emp_note = request.POST.get("empnote")
        all_in_use_cars = InUseCars.objects.select_related('car', 'employee').all().order_by('-id')
        dubai_tz = pytz.timezone('Asia/Dubai')

        try:
            emp_instance = EmployesInfo.objects.get(ceoNumber=ceo_number)
        except EmployesInfo.DoesNotExist:
            ret_err_msg = "الرقم الاداري المدخل لاعادة مركبه غير صحيح"
            return render(request, "logsApp/registerCar.html",{
                "retErrm": ret_err_msg,
                "l": all_in_use_cars,
                "ceonumber": "",
                "empnote": "emp_note",
                "form_open": True
            })

        try:
            in_use_car_instance = InUseCars.objects.select_related('car', 'employee').get(employee=emp_instance)
        except InUseCars.DoesNotExist:
            ret_car_err = "لاتوجد مركبه مرتبطه بل رقم الاداري المدخل"
            return render(request, "logsApp/registerCar.html", {
                "retCarErr": ret_car_err,
                "l": all_in_use_cars,
                "ceonumber": "",
                "empnote": "emp_note",
                "form_open": True})

        ret_success_msg = "تم اعاده المركبه بنجاح"
        registered_car_instance = RegistredCars.objects.get(carNumber=in_use_car_instance.car.carNumber)
        log_instance = LogsC.objects.select_related('Logs_employee_ins', 'Logs_car_ins').get(Logs_employee_ins=emp_instance, carIsInUse=True)
        current_time = timezone.now().astimezone(dubai_tz)
        log_instance.ended_at = current_time
        log_instance.return_date = current_time.date()
        log_instance.return_time = current_time.time()
        log_instance.carIsInUse = False
        log_instance.carNote = emp_note

        registered_car_instance.carIsInparking = True
        emp_instance.EmpHaveCar = False

        emp_instance.save()
        log_instance.save()
        registered_car_instance.save()
        in_use_car_instance.delete()

        return render(request, "logsApp/registerCar.html", {"retSucssM": ret_success_msg,"l": all_in_use_cars})

    return render(request, "logsApp/registerCar.html", {"l": InUseCars.objects.select_related('car', 'employee').all().order_by('-id')})

def logsfunc(request):
    years = range(2020, 2040)
    if request.method == "POST" or request.method == "GET":
        car_number = request.GET.get('carNumper')
        ceo_number = request.GET.get('ceoN')
        date_filter = request.GET.get('date')
        month_filter = request.GET.get('month')
        year_filter = request.GET.get('year')
        year_only_filter = request.GET.get('yearOnly')
        date_type = request.GET.get('dateType')
        show_all = request.GET.get('showAll')

        filters = Q()

        if date_type == "day" and date_filter:
            filters &= Q(taken_date=date_filter)
        elif date_type == "month" and month_filter and year_filter:
            month_start = datetime(year=int(year_filter), month=int(month_filter), day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            filters &= Q(taken_date__range=(month_start, month_end))
        elif date_type == "year" and year_only_filter:
            year_start = datetime(year=int(year_only_filter), month=1, day=1)
            year_end = datetime(year=int(year_only_filter), month=12, day=31, hour=23, minute=59, second=59)
            filters &= Q(taken_date__range=(year_start, year_end))

        if ceo_number:
            filters &= Q(Logs_employee_ins__ceoNumber=ceo_number.strip())

        if car_number:
            filters &= Q(Logs_car_ins__carNumber=car_number.strip())

        if show_all:
            logs = LogsC.objects.all().order_by('-id')
        else:
            logs = LogsC.objects.filter(filters).order_by('-id')


        paginator = Paginator(logs, 50)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "logsApp/logs.html", {'page_obj': page_obj, 'years': years})

    current_date = datetime.now().date()
    today_logs = LogsC.objects.filter(Q(taken_date=current_date) | Q(taken_date__isnull=True)).order_by('-id')
    
    paginator = Paginator(today_logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "logsApp/logs.html", {'page_obj': page_obj, 'years': years})

def is_pdf(file_field):
    return file_field.url.endswith(".pdf")

def AccidentsRecords(request):
    fines = AccidentsRecord.objects.all()
    if request.method == "POST":
        car_number = request.POST.get('carNumber')
        emp_number = request.POST.get('empNumber')
        text = request.POST.get('text')
        report_pdf_file = request.FILES.get('reportPdfFile')
        car_paperwork_file = request.FILES.get('carPaperworkFile')
        license_files = request.FILES.getlist('licenseFiles')
        images = request.FILES.getlist('images')

        try:
            car_instance = RegistredCars.objects.get(carNumber=car_number)
        except RegistredCars.DoesNotExist:
            car_instance = None
            
        emp_instance = None
        if emp_number:
            try:
                emp_instance = EmployesInfo.objects.get(ceoNumber=emp_number)
            except EmployesInfo.DoesNotExist:
                emp_err_message = "الرقم الاداري غير صحيح"
                return render(request, "logsApp/accidentsPage.html", {
                    'form_open': True,
                    'fines': fines,
                    'emp_err_message': emp_err_message,
                    'images': images,
                    'carNumber': car_number,
                    'empNumber': emp_number,
                    'text': text,
                    'reportPdfFile': report_pdf_file,
                    'carPaperworkFile': car_paperwork_file,
                    'licenseFiles': license_files
                })

        accidents_record = AccidentsRecord.objects.create(
            car=car_instance,
            text=text)

        if report_pdf_file:
            accidents_record.report_pdf_file = report_pdf_file
        if car_paperwork_file:
            accidents_record.car_paperwork_file = car_paperwork_file

        if emp_instance:
            accidents_record.employees.add(emp_instance)

        for image in images:
            FinesAccidentsImage.objects.create(accidents_record=accidents_record, image=image)

        for license_file in license_files:
            LicenseFile.objects.create(accidents_record=accidents_record, file=license_file)

        accidents_record.save()

    return render(request, "logsApp/accidentsPage.html", {'fines': fines, 'form_open': False})

def export_to_excel(request):
    dubai_tz = pytz.timezone('Asia/Dubai')
    
    # Initialize base queryset
    data = LogsC.objects.select_related('Logs_employee_ins', 'Logs_car_ins').all()
    
    # Get filter parameters
    car_number = request.GET.get('carNumper')
    ceo_number = request.GET.get('ceoN')
    date_filter = request.GET.get('date')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')
    year_only_filter = request.GET.get('yearOnly')
    date_type = request.GET.get('dateType')
    show_all = request.GET.get('showAll')

    # Apply filters
    if not show_all:
        filters = Q()
        
        # Date type filters
        if date_type == "day" and date_filter:
            filters &= Q(taken_date=date_filter)
        elif date_type == "month" and month_filter and year_filter:
            month_start = datetime(year=int(year_filter), month=int(month_filter), day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            filters &= Q(taken_date__range=(month_start, month_end))
        elif date_type == "year" and year_only_filter:
            year_start = datetime(year=int(year_only_filter), month=1, day=1)
            year_end = datetime(year=int(year_only_filter), month=12, day=31, hour=23, minute=59, second=59)
            filters &= Q(taken_date__range=(year_start, year_end))

        # Car number and CEO number filters
        if ceo_number:
            filters &= Q(Logs_employee_ins__ceoNumber=ceo_number.strip())
        if car_number:
            filters &= Q(Logs_car_ins__carNumber=car_number.strip())

        # Apply all filters
        data = data.filter(filters)


    # Order the data
    data = data.order_by('-id')

    # Prepare data for Excel
    export_data = []
    for log in data:
        taken_time_dubai = log.taken_time.replace(tzinfo=dubai_tz) if log.taken_time else None
        return_time_dubai = log.return_time.replace(tzinfo=dubai_tz) if log.return_time else None

        export_data.append({
            'ID': log.id,
            'رقم السياره': log.Logs_car_ins.carNumber,
            'الاسم': log.Logs_employee_ins.ceoName,
            'الرقم الاداري': log.Logs_employee_ins.ceoNumber,
            'تاريخ الاستلام': log.taken_date,
            'وقت الاستلام': taken_time_dubai.strftime('%I:%M %p') if taken_time_dubai else None,
            'تاريخ التسليم': log.return_date,
            'وقت التسليم': return_time_dubai.strftime('%I:%M %p') if return_time_dubai else None,
            'ملاحظه على المركبه': log.carNote,
            'قسم الموظف': log.Logs_employee_ins.department
        })

    df = pd.DataFrame(export_data)

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="logs_data.xlsx"'

    # Create Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Logs Data')

        worksheet = writer.sheets['Logs Data']
        worksheet.sheet_view.rightToLeft = True

        header_font = Font(size=16, bold=True, color='000000')
        header_fill = PatternFill(start_color='B7E1A1', end_color='B7E1A1', fill_type='solid')
        cell_font = Font(size=16)
        center_alignment = Alignment(horizontal='center')

        # Style header row
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_alignment

        # Style data rows
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
            for cell in row:
                cell.font = cell_font
                cell.alignment = center_alignment

        # Adjust column widths
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
    finon = None
    allFines = FinesRecord.objects.all()
    if request.method == "POST":
        fine_date = request.POST.get('finedate')
        fine_time = request.POST.get('finetime')
        fine_car_number = request.POST.get('finecar')
        fine_amount = request.POST.get('fineamount')
        dubai_tz = pytz.timezone('Asia/Dubai')
        combined_fine_datetime = dubai_tz.localize(timezone.datetime.strptime(f"{fine_date} {fine_time}", '%Y-%m-%d %H:%M'))
        
        try:
            car_ins = RegistredCars.objects.get(carNumber=fine_car_number)
        except RegistredCars.DoesNotExist:
            car_err_message = "رقم المركبه المدخل غير صحيح"
            return render(request, "logsApp/finespage.html", {
                'form_open': True,
                'allFines': allFines,
                'car_err_message': car_err_message,
                'fine_date': fine_date,
                'fine_time': fine_time,
                'fine_car_number': fine_car_number,
                'fine_amount': fine_amount
            })
            
        try:
            finon = LogsC.objects.get(Logs_car_ins=car_ins,
                                      created_at__lte=combined_fine_datetime,
                                      ended_at__gte=combined_fine_datetime
                                      )
            FinesRecord.objects.create(
                car=car_ins,
                employe=finon.Logs_employee_ins,
                created_at=combined_fine_datetime,
                fine_date=fine_date,
                fine_time=fine_time,
                fine_amount=fine_amount
            )
            return redirect('logsApp:finespage')
        except LogsC.DoesNotExist:
            pass

        try:
            finon = LogsC.objects.get(Logs_car_ins=car_ins,
                                      created_at__lte=combined_fine_datetime,
                                      ended_at__isnull=True
                                      )
            FinesRecord.objects.create(
                car=car_ins,
                employe=finon.Logs_employee_ins,
                created_at=combined_fine_datetime,
                fine_date=fine_date,
                fine_time=fine_time,
                fine_amount=fine_amount
            )
        except LogsC.DoesNotExist:
            print(f"Car with number {fine_car_number} does not exist.")
        # check if the fine is on a give  car to other adminstration 
        try:
            finon = GivenCarsToOtherAdminstrations.objects.get(car=car_ins,
                                      created_at__lte=combined_fine_datetime,
                                      ended_at__gte=combined_fine_datetime
                                      )
            
            FinesRecord.objects.create(
                car=car_ins,
                unRegistredEmpCeoNumber=finon.empNumber,
                unRegistredEmpName=finon.empName,
                created_at=combined_fine_datetime,
                fine_date=fine_date,
                fine_time=fine_time,
                fine_amount=fine_amount
            )
            return redirect('logsApp:finespage')
        except GivenCarsToOtherAdminstrations.DoesNotExist:
            pass

        try:
            finon = GivenCarsToOtherAdminstrations.objects.get(car=car_ins,
                                      created_at__lte=combined_fine_datetime,
                                      ended_at__isnull=True
                                      )
            
            FinesRecord.objects.create(
                car=car_ins,
                unRegistredEmpCeoNumber=finon.empNumber,
                unRegistredEmpName=finon.empName,
                created_at=combined_fine_datetime,
                fine_date=fine_date,
                fine_time=fine_time,
                fine_amount=fine_amount
            )
            return redirect('logsApp:finespage')
        except GivenCarsToOtherAdminstrations.DoesNotExist:
            pass

        return render(request, "logsApp/finespage.html", {'finon': finon})
    return render(request, "logsApp/finespage.html", {'allFines': allFines, 'finon': finon})

def fineDetails(request, fine_id):
    fine = get_object_or_404(FinesRecord, id=fine_id)
    fine_files = []
    fine_images = []
    if fine.paid_fine_image:
        if is_pdf(fine.paid_fine_image):
            fine_files.append(fine.paid_fine_image)
        else:
            fine_images.append(fine.paid_fine_image)
    if request.method == "POST":
        paid_fine_image = request.FILES.get('paidFineImage')
        if paid_fine_image:
            fine.paid_fine_image = paid_fine_image
            fine.paidDate = timezone.now().date()
            fine.save()
            fine = get_object_or_404(FinesRecord, id=fine_id)
            fine_files = []
            fine_images = []
            if fine.paid_fine_image:
                if is_pdf(fine.paid_fine_image):
                    fine_files.append(fine.paid_fine_image)
                else:
                    fine_images.append(fine.paid_fine_image)
    return render(request, 'logsApp/fineDetails.html', {'fine': fine, 'fine_files': fine_files, 'fine_images': fine_images})

def carddetails(request, fine_id):
    accident = get_object_or_404(AccidentsRecord, id=fine_id)
    employees = EmployesInfo.objects.all()
    cars = RegistredCars.objects.all()
    if request.method == "POST":
        report_pdf_file = request.FILES.get('reportPdfFile')
        car_paperwork_file = request.FILES.get('carPaperworkFile')
        license_files = request.FILES.getlist('licenseFiles')
        images = request.FILES.getlist('images')
        emp_number = request.POST.get('empNumber')
        car_number = request.POST.get('carNumber')

        if report_pdf_file:
            accident.report_pdf_file = report_pdf_file
        if car_paperwork_file:
            accident.car_paperwork_file = car_paperwork_file

        for image in images:
            FinesAccidentsImage.objects.create(accidents_record=accident, image=image)

        for license_file in license_files:
            LicenseFile.objects.create(accidents_record=accident, file=license_file)

        if emp_number:
            try:
                emp_instance = EmployesInfo.objects.get(ceoNumber=emp_number)
                accident.employees.clear()
                accident.employees.add(emp_instance)
            except EmployesInfo.DoesNotExist:
                pass

        if car_number:
            try:
                car_instance = RegistredCars.objects.get(carNumber=car_number)
                accident.car = car_instance
            except RegistredCars.DoesNotExist:
                pass

        accident.save()

    license_files = []
    license_images = []
    for license_file in accident.license_files.all():
        if is_pdf(license_file.file):
            license_files.append(license_file)
        else:
            license_images.append(license_file)
    return render(request, 'logsApp/accidentDetails.html', {
        'accident': accident,
        'license_files': license_files,
        'license_images': license_images,
        'employees': employees,
        'cars': cars
    })

def markasfixed(request, fine_id):
    fine = get_object_or_404(AccidentsRecord, id=fine_id)
    fine.fixin_date = timezone.now()
    fine.save()
    return redirect('logsApp:carddetails', fine_id=fine_id)

# حذف صورة الدفع او الملف اذا كانت مورفقه
# def deleteFineImage(request, fine_id):
#     fine = get_object_or_404(FinesRecord, id=fine_id)
#     if fine.paid_fine_image:
#         # Get the directory path
#         directory = os.path.dirname(fine.paid_fine_image.path)
#         # Delete the entire directory
#         shutil.rmtree(directory)
#         # Clear the fields in the database
#         fine.paid_fine_image = None
#         fine.paidDate = None
#         fine.save()
#     return redirect('logsApp:fineDetails', fine_id=fine_id)



def gCTOA(request):
    cgtoa = GivenCarsToOtherAdminstrations.objects.all()
    if request.method == "POST":
        dubai_tz = pytz.timezone('Asia/Dubai')
        current_time = timezone.now().astimezone(dubai_tz)
        carNumberq = request.POST.get("carNumber")
        other_adminstration = request.POST.get("other_adminstration")
        emp_number = request.POST.get("emp_number")
        emp_name = request.POST.get("emp_name")
        telephone = request.POST.get("telephone")
        note = request.POST.get("note")
        #تاكد اذا كانت المركبه قيد الاستخدام من قبل ادارتنا 
        try:
            ourAdmin = LogsC.objects.get(Logs_car_ins__carNumber=carNumberq, carIsInUse=True)
            error_message = "المركبه قيد الاستخدام"
            return render(request, "logsApp/gctoa.html", {
                "ourAdmin": ourAdmin,
                "cgtoa": cgtoa,
                "error_message": error_message,
                "carNumber": carNumberq,
                "other_adminstration": other_adminstration,
                "emp_number": emp_number,
                "emp_name": emp_name,
                "telephone": telephone
            })
        except LogsC.DoesNotExist:
            pass
        
        #تاكد اذا كانت المركبه مسجله من قبل ادارة ارخى
        try:
            otheradmin = GivenCarsToOtherAdminstrations.objects.get(car__carNumber=carNumberq, carIsInUse=True)
            error_message = "المركبه معطاه لاداره اخرى"
            return render(request, "logsApp/gctoa.html", {
                "otheradmin": otheradmin,
                "cgtoa": cgtoa,
                "error_message": error_message,
                "carNumber": carNumberq,
                "other_adminstration": other_adminstration,
                "emp_number": emp_number,
                "emp_name": emp_name,
                "telephone": telephone
            })
        except GivenCarsToOtherAdminstrations.DoesNotExist:
            pass

        try:
            car_instance = RegistredCars.objects.get(carNumber=carNumberq, carIsInparking=True)
            GivenCarsToOtherAdminstrations.objects.create(
                car=car_instance,
                otherAdminstration=other_adminstration,
                empNumber=emp_number,
                empName=emp_name,
                telephone=telephone,
                taken_date=current_time.date(),
                taken_time=current_time.time(),
                note=note,
                carIsInUse=True
            )
            car_instance.carIsInparking = False
            car_instance.save()
            cgtoa = GivenCarsToOtherAdminstrations.objects.all()
            success_message = "تم حفظ البيانات بنجاح"
            return render(request, "logsApp/gctoa.html", {"cgtoa": cgtoa, "success_message": success_message})
        except RegistredCars.DoesNotExist:
            error_message = "رقم السيارة غير صحيح او المركبه قيد الاستخدام"
            print("رقم السيارة غير صحيح او المركبه قيد الاستخدام")
            return render(request, "logsApp/gctoa.html", {
                "cgtoa": cgtoa,
                "error_message": error_message,
                "carNumber": carNumberq,
                "other_adminstration": other_adminstration,
                "emp_number": emp_number,
                "emp_name": emp_name,
                "telephone": telephone,
                "note":note
            })

    return render(request, "logsApp/gctoa.html", {"cgtoa": cgtoa})

def return_car(request, car_id):
    car_instance = get_object_or_404(GivenCarsToOtherAdminstrations, id=car_id)
    dubai_tz = pytz.timezone('Asia/Dubai')
    current_time = timezone.now().astimezone(dubai_tz)
    carNumberq = car_instance.car.carNumber
    print(carNumberq)
    car_instance_original = RegistredCars.objects.get(carNumber=carNumberq, carIsInparking=False)
    car_instance_original.carIsInparking = True
    car_instance.ended_at = current_time
    car_instance.return_date = current_time.date()
    car_instance.retern_time = current_time.time()
    car_instance.carIsInUse = False
    car_instance.save()
    car_instance_original.save()
    
    success_message = "تم تسجيل عودة المركبة بنجاح"
    cgtoa = GivenCarsToOtherAdminstrations.objects.all()
    return render(request, "logsApp/gctoa.html", {"cgtoa": cgtoa, "success_message": success_message})



def maintaincePage(request):
    AllInGarageCars = InGarageCars.objects.all().order_by('-id')
    return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {
                            "AllInGarageCars":AllInGarageCars,
                        } )


def maintainceRegisterCar(request):
    
    if request.method == "POST":
        AllInGarageCars = InGarageCars.objects.all().order_by('-id')
        dubai_tz = pytz.timezone('Asia/Dubai')
        current_time = timezone.now().astimezone(dubai_tz)
        emp_number = request.POST.get("empNumber").strip()
        car_number = request.POST.get("carNumber").strip()
        reason = request.POST.get("reason")
        car_number = car_number.replace("/", "-")
        print("formAceepted")
        
        # تاكد اذا كان الرقم الاداري صحيح لاكن ليس من فريق الصيانة 
        try:
            emp_instance = EmployesInfo.objects.get(ceoNumber=emp_number , MaintenanceEmp=False)
            print("الرقم الاداري المدخل ليس من ضمن فريق الصيانة")
            empNotInMaintance = "الرقم الاداري المدخل ليس من ضمن فريق الصيانة"
            return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {"car_number_err":car_number,
                           "empNumberErr":emp_number,
                           "reasonErr":reason,
                           "AllInGarageCars": AllInGarageCars,
                           "error_message": empNotInMaintance})
      
        except EmployesInfo.DoesNotExist:
            pass
            
        # تاكد اذا كان الرقم الاداري صحيح و لفريق الصيانة
        try:
            emp_instance = EmployesInfo.objects.get(ceoNumber=emp_number , MaintenanceEmp=True)
        except EmployesInfo.DoesNotExist:
            error_message = "الرقم الاداري المدخل غير صحيح"
            print("الرقم الاداري المدخل غير صحيح")
            return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {"car_number_err":car_number,
                           "empNumberErr":emp_number,
                           "reasonErr":reason,
                           "AllInGarageCars": AllInGarageCars,
                           "error_message": error_message})
        
        # تاكد اذا كان رقم المركبة المدخل صحيح
        try:
            car_instance = RegistredCars.objects.get(carNumber=car_number)
        except RegistredCars.DoesNotExist:
            print("رقم المركبة المدخل غير صحيح")
            error_message = "رقم المركبة المدخل غير صحيح"
            return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {"AllInGarageCars": AllInGarageCars,
                           "car_number_err":car_number,
                           "empNumberErr":emp_number,
                           "reasonErr":reason,
                           "error_message": error_message})
        
        # تاكد اذا كانت المركبة قيد الاستخدام من قبل ادارتنا
        try:
            car_in_use = LogsC.objects.get(Logs_car_ins__carNumber=car_number, carIsInUse=True)
            print("المركبة قيد الاستخدام من قبل موظف")
            error_message = "المركبة قيد الاستخدام من قبل موظف"
            return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {"AllInGarageCars": AllInGarageCars,
                           "car_number_err":car_number,
                           "empNumberErr":emp_number,
                           "reasonErr":reason,
                           "error_message": error_message,
                           "car_in_use": car_in_use})
        except LogsC.DoesNotExist:
            pass
        
        # تاكد اذا كانت المركبة معطاه لادارة اخرى   
        try:
            car_in_other_admin = GivenCarsToOtherAdminstrations.objects.get(car__carNumber=car_number, carIsInUse=True)
            error_message = "المركبة معطاه لادارة اخرى"
            print("المركبة معطاه لادارة اخرى")
            return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {"AllInGarageCars": AllInGarageCars,
                           "car_number_err":car_number,
                           "empNumberErr":emp_number,
                           "reasonErr":reason,
                           "error_message": error_message,
                           "car_in_other_admin": car_in_other_admin})
        except GivenCarsToOtherAdminstrations.DoesNotExist:
            pass
            
        # تاكد اذا كانت المركبة موجودة في الجراج بالفعل
        try:
            car_in_garage = InGarageCars.objects.get(car__carNumber=car_number)
            print("المركبة موجودة بالفعل في الجراج")
            maintenance_log = MaintanceLogs.objects.filter(
                car__carNumber=car_number, 
                car_is_in_garage=True
            ).latest('maintance_emp_send_to_garage_date')
            
            error_message = "المركبة موجودة بالفعل في الجراج"
            return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {
                           "AllInGarageCars": AllInGarageCars,
                           "car_number_err":car_number,
                           "empNumberErr":emp_number,
                           "reasonErr":reason,
                           "error_message": error_message,
                           "maintenance_log": maintenance_log})
        except (InGarageCars.DoesNotExist, MaintanceLogs.DoesNotExist):
            pass

        # تاكد اذا كانت المركبة في الباركنج
        if not car_instance.carIsInparking:
            print("المركبة ليست موجودة في الباركنج")
            error_message = "المركبة ليست موجودة في الباركنج"
            return render(request,"logsApp/maintenanceEmployeesForms.html",
                          {
                           "AllInGarageCars": AllInGarageCars,
                           "car_number_err":car_number,
                           "empNumberErr":emp_number,
                           "reasonErr":reason,
                           "error_message": error_message})

        #تسجيل مركبه باسم سائق الصيانه من الباركن الى الجراج 
        maintenance_log = MaintanceLogs.objects.create(
            car=car_instance,
            maintance_emp_send_to_garage=emp_instance,
            maintance_emp_send_to_garage_time=current_time.time(),
            maintance_emp_send_to_garage_date=current_time.date(),
            maintance_emp_send_to_garage_reason=reason,
        )

        # Create InGarageCars record
        InGarageCars.objects.create(
            car=car_instance,
            maintance_emp_send_to_garage=emp_instance,
            maintance_emp_send_to_garage_time=current_time.time(),
            maintance_emp_send_to_garage_date=current_time.date(),
            maintance_emp_send_to_garage_reason=reason
        )
        
        # Update car status 
        car_instance.carIsInparking = False
        car_instance.save()

        AllInGarageCars = InGarageCars.objects.all().order_by('-id')
        return render(request,"logsApp/maintenanceEmployeesForms.html",
                      {
                        "AllInGarageCars": AllInGarageCars,
                        "success_message": "تم تسجيل المركبة في الصيانة بنجاح"
                      })
                      
    AllInGarageCars = InGarageCars.objects.all().order_by('-id')
    return render(request,"logsApp/maintenanceEmployeesForms.html",
                  {
                    "AllInGarageCars": AllInGarageCars,
                  })


def returnCarFromGarage(request):
    if request.method == "POST":
        dubai_tz = pytz.timezone('Asia/Dubai')
        current_time = timezone.now().astimezone(dubai_tz)
        
        emp_number = request.POST.get("empNumber").strip()
        car_number = request.POST.get("carNumber").strip()
        reason = request.POST.get("reason")
        car_number = car_number.replace("/", "-")
        
        # Get all cars in garage for rendering the template
        AllInGarageCars = InGarageCars.objects.all().order_by('-id')
        
        # Validate employee
        try:
            emp_instance = EmployesInfo.objects.get(ceoNumber=emp_number, MaintenanceEmp=True)
        except EmployesInfo.DoesNotExist:
            return render(request, "logsApp/maintenanceEmployeesForms.html",
                        {
                            "AllInGarageCars": AllInGarageCars,
                            "Rcar_number_err": car_number,
                            "RempNumberErr": emp_number,
                            "RreasonErr": reason,
                            "error_message": "الرقم الاداري المدخل غير صحيح أو ليس من فريق الصيانة"
                        })
        
        # Validate car
        try:
            car_instance = RegistredCars.objects.get(carNumber=car_number)
        except RegistredCars.DoesNotExist:
            return render(request, "logsApp/maintenanceEmployeesForms.html",
                        {
                            "AllInGarageCars": AllInGarageCars,
                            "Rcar_number_err": car_number,
                            "RempNumberErr": emp_number,
                            "RreasonErr": reason,
                            "error_message": "رقم المركبة المدخل غير صحيح"
                        })
        
        # Check if the car is actually in the garage
        try:
            in_garage_car = InGarageCars.objects.get(car=car_instance)
        except InGarageCars.DoesNotExist:
            return render(request, "logsApp/maintenanceEmployeesForms.html",
                        {
                            "AllInGarageCars": AllInGarageCars,
                            "Rcar_number_err": car_number,
                            "RempNumberErr": emp_number,
                            "RreasonErr": reason,
                            "error_message": "المركبة ليست موجودة في الجراج"
                        })
                        
        # Get the maintenance log record
        try:
            maintenance_log = MaintanceLogs.objects.filter(
                car=car_instance,
                car_is_in_garage=True
            ).latest('maintance_emp_send_to_garage_date')
            
            # Calculate arrival times
            arrival_time_from_garage = current_time - timedelta(hours=1, minutes=30)
            
            # Get the original date and time from the model
            date = maintenance_log.maintance_emp_send_to_garage_date
            time = maintenance_log.maintance_emp_send_to_garage_time
            
            # Combine date and time into datetime, then add 1h30m for garage arrival time
            combined_datetime = datetime.combine(date, time)
            new_datetime = combined_datetime + timedelta(hours=1, minutes=30)
            
            # Update the maintenance log with all the required information
            maintenance_log.maintance_emp_send_to_garage_arriving_time_date = new_datetime
            maintenance_log.maintance_emp_return_from_garage_arriving_time_date = arrival_time_from_garage
            maintenance_log.maintance_emp_return_from_garage = emp_instance
            maintenance_log.maintance_emp_return_from_garage_time = current_time.time()
            maintenance_log.maintance_emp_return_from_garage_date = current_time.date()
            maintenance_log.maintance_emp_return_from_garage_reason = reason
            maintenance_log.car_is_in_garage = False
            maintenance_log.save()
            
            # Remove car from InGarageCars
            in_garage_car.delete()
            
            # Update car status to indicate it's back in parking
            car_instance.carIsInparking = True
            car_instance.save()
            
            # Get updated list of cars in garage
            AllInGarageCars = InGarageCars.objects.all().order_by('-id')
            return render(request, "logsApp/maintenanceEmployeesForms.html",
                        {
                            "AllInGarageCars": AllInGarageCars,
                            "success_message": "تم إرجاع المركبة من الصيانة بنجاح"
                        })
                        
        except MaintanceLogs.DoesNotExist:
            return render(request, "logsApp/maintenanceEmployeesForms.html",
                        {
                            "AllInGarageCars": AllInGarageCars,
                            "Rcar_number_err": car_number,
                            "RempNumberErr": emp_number,
                            "RreasonErr": reason,
                            "error_message": "لا يوجد سجل صيانة لهذه المركبة"
                        })
    
    # For GET requests, just render the template with the list of cars in garage
    AllInGarageCars = InGarageCars.objects.all().order_by('-id')
    return render(request, "logsApp/maintenanceEmployeesForms.html",
                {
                    "AllInGarageCars": AllInGarageCars,
                })

def maintenanceLogs(request):
    # Initialize years range for the date filters
    years = range(2020, 2040)
    
    # Get filter parameters
    car_number = request.GET.get('carNumber')
    emp_number = request.GET.get('empNumber')
    date_filter = request.GET.get('date')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')
    year_only_filter = request.GET.get('yearOnly')
    date_type = request.GET.get('dateType')
    status_filter = request.GET.get('status')
    show_all = request.GET.get('showAll')
    
    # Initialize base queryset
    queryset = MaintanceLogs.objects.all()
    
    # Apply filters
    if not show_all:
        filters = Q()
        
        # Date filters
        if date_type == "day" and date_filter:
            filters &= Q(maintance_emp_send_to_garage_date=date_filter)
        elif date_type == "month" and month_filter and year_filter:
            month_start = datetime(year=int(year_filter), month=int(month_filter), day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            filters &= Q(maintance_emp_send_to_garage_date__range=(month_start, month_end))
        elif date_type == "year" and year_only_filter:
            year_start = datetime(year=int(year_only_filter), month=1, day=1)
            year_end = datetime(year=int(year_only_filter), month=12, day=31)
            filters &= Q(maintance_emp_send_to_garage_date__range=(year_start, year_end))
            
        # Car number filter
        if car_number:
            filters &= Q(car__carNumber__icontains=car_number.strip())
            
        # Employee number filter
        if emp_number:
            filters &= Q(maintance_emp_send_to_garage__ceoNumber=emp_number.strip())
            
        # Status filter
        if status_filter == "in_garage":
            filters &= Q(car_is_in_garage=True)
        elif status_filter == "returned":
            filters &= Q(car_is_in_garage=False)
            
        # Apply all filters
        queryset = queryset.filter(filters)
    
    # Order logs by most recent first
    all_maintenance_logs = queryset.order_by('-maintance_emp_send_to_garage_date')
    
    # Paginate the results
    paginator = Paginator(all_maintenance_logs, 20)  # Show 20 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "logsApp/maintenanceLogs.html", {
        "all_maintenance_logs": page_obj,
        "years": years,
        "page_obj": page_obj
    })

@api_view(['GET', 'OPTIONS'])
def logs_api(request):
    """
    API endpoint that returns the latest 3500 car logs (LogsC) data.
    Optional query parameters:
    - in_use: Filter by carIsInUse (true/false)
    """
    # Handle preflight OPTIONS request for CORS
    if request.method == 'OPTIONS':
        response = Response()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Accept, Accept-Encoding, Authorization, Content-Type, DNT, Origin, User-Agent, X-Requested-With, Cache-Control, Pragma'
        return response
    
    # Get query parameters
    in_use_param = request.query_params.get('in_use', None)
    
    # Base queryset - limit to the latest 3500 records
    queryset = LogsC.objects.all().order_by('-created_at')[:3500]
    
    # Apply filters if provided
    if in_use_param is not None:
        in_use = in_use_param.lower() == 'true'
        queryset = LogsC.objects.filter(carIsInUse=in_use).order_by('-created_at')[:3500]
    
    # Serialize the data
    serializer = LogsCSerializer(queryset, many=True)
    
    # Create response with explicit CORS headers
    response = Response(serializer.data)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response['Cache-Control'] = 'no-cache'
    
    return response

def export_maintenance_to_excel(request):
    dubai_tz = pytz.timezone('Asia/Dubai')
    
    # Initialize base queryset
    data = MaintanceLogs.objects.all()
    
    # Get filter parameters
    car_number = request.GET.get('carNumber')
    emp_number = request.GET.get('empNumber')
    date_filter = request.GET.get('date')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')
    year_only_filter = request.GET.get('yearOnly')
    date_type = request.GET.get('dateType')
    status_filter = request.GET.get('status')
    show_all = request.GET.get('showAll')

    # Apply filters
    if not show_all:
        filters = Q()
        
        # Date type filters
        if date_type == "day" and date_filter:
            filters &= Q(maintance_emp_send_to_garage_date=date_filter)
            filename_suffix = f"day_{date_filter}"
        elif date_type == "month" and month_filter and year_filter:
            month_start = datetime(year=int(year_filter), month=int(month_filter), day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            filters &= Q(maintance_emp_send_to_garage_date__range=(month_start, month_end))
            
            # Get the month name in Arabic
            month_names = {
                '1': 'يناير', '2': 'فبراير', '3': 'مارس', '4': 'أبريل',
                '5': 'مايو', '6': 'يونيو', '7': 'يوليو', '8': 'أغسطس',
                '9': 'سبتمبر', '10': 'أكتوبر', '11': 'نوفمبر', '12': 'ديسمبر'
            }
            month_name = month_names.get(month_filter, month_filter)
            filename_suffix = f"month_{month_name}_{year_filter}"
        elif date_type == "year" and year_only_filter:
            year_start = datetime(year=int(year_only_filter), month=1, day=1)
            year_end = datetime(year=int(year_only_filter), month=12, day=31, hour=23, minute=59, second=59)
            filters &= Q(maintance_emp_send_to_garage_date__range=(year_start, year_end))
            filename_suffix = f"year_{year_only_filter}"
        else:
            filename_suffix = "filtered_maintenance"

        # Car number and Employee number filters
        if car_number:
            filters &= Q(car__carNumber__icontains=car_number.strip())
            if 'filename_suffix' not in locals():
                filename_suffix = f"car_{car_number.strip()}"
                
        if emp_number:
            filters &= Q(maintance_emp_send_to_garage__ceoNumber=emp_number.strip())
            if 'filename_suffix' not in locals():
                filename_suffix = f"emp_{emp_number.strip()}"
        
        # Status filter
        if status_filter == "in_garage":
            filters &= Q(car_is_in_garage=True)
            if 'filename_suffix' not in locals():
                filename_suffix = "in_garage"
        elif status_filter == "returned":
            filters &= Q(car_is_in_garage=False)
            if 'filename_suffix' not in locals():
                filename_suffix = "returned"

        # Apply all filters
        data = data.filter(filters)
    else:
        filename_suffix = "all_maintenance"

    # Order the data
    data = data.order_by('-maintance_emp_send_to_garage_date')

    # Prepare data for Excel - updated to match table fields exactly
    export_data = []
    for log in data:
        send_time = log.maintance_emp_send_to_garage_time.replace(tzinfo=dubai_tz) if log.maintance_emp_send_to_garage_time else None
        return_time = log.maintance_emp_return_from_garage_time.replace(tzinfo=dubai_tz) if log.maintance_emp_return_from_garage_time else None

        export_data.append({
            'رقم المركبة': log.car.carNumber if log.car else "غير متوفر",
            'الرقم الاداري': log.maintance_emp_send_to_garage.ceoNumber if log.maintance_emp_send_to_garage else "غير متوفر",
            'اسم السائق': log.maintance_emp_send_to_garage.ceoName if log.maintance_emp_send_to_garage else "غير متوفر",
            'تاريخ الاستلام': log.maintance_emp_send_to_garage_date,
            'وقت الاستلام': send_time.strftime('%I:%M %p') if send_time else "غير متوفر",
            'سبب الصيانة': log.maintance_emp_send_to_garage_reason or "غير متوفر",
            'الرقم الاداري للمعيد': log.maintance_emp_return_from_garage.ceoNumber if log.maintance_emp_return_from_garage else "--",
            'اسم المعيد': log.maintance_emp_return_from_garage.ceoName if log.maintance_emp_return_from_garage else "--",
            'نتيجة الصيانة': log.maintance_emp_return_from_garage_reason or "--",
            'تاريخ الإرجاع': log.maintance_emp_return_from_garage_date or "--",
            'وقت الإرجاع': return_time.strftime('%I:%M %p') if return_time else "--",
        })
    
    df = pd.DataFrame(export_data)

    # Generate current_time for filename
    current_time = timezone.now().strftime('%Y%m%d%H%M%S')
    
    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"maintenance_logs_{filename_suffix}_{current_time}.xlsx" if 'filename_suffix' in locals() else f"maintenance_logs_{current_time}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create Excel file - SIMPLIFIED VERSION WITHOUT HEADER ROWS
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Maintenance Logs')

        worksheet = writer.sheets['Maintenance Logs']
        worksheet.sheet_view.rightToLeft = True

        # Style the table - starting with header row
        header_font = Font(size=16, bold=True, color='000000')
        header_fill = PatternFill(start_color='B7E1A1', end_color='B7E1A1', fill_type='solid')
        cell_font = Font(size=16)
        center_alignment = Alignment(horizontal='center')

        # Style header row (first row)
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_alignment

        # Style data rows
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
            for cell in row:
                cell.font = cell_font
                cell.alignment = center_alignment

        # Adjust column widths - improved to avoid merged cells issues
        for column in worksheet.columns:
            max_length = 0
            column_letter = None
            
            # Find the first cell with a column_letter (not a merged cell)
            for cell in column:
                if hasattr(cell, 'column_letter'):
                    column_letter = cell.column_letter
                    break
                    
            if column_letter:
                for cell in column:
                    if cell.value:
                        try:
                            cell_length = len(str(cell.value))
                            max_length = max(max_length, cell_length)
                        except:
                            pass
                            
                adjusted_width = (max_length + 4)
                worksheet.column_dimensions[column_letter].width = adjusted_width

    return response