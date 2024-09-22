from django.shortcuts import render 
from django.utils import timezone
from logsApp.models import  RegistredCars , EmployesInfo,InUseCars,LogsC
import re

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
import pytz

# Get the Asia/Dubai timezone
dubai_tz = pytz.timezone('Asia/Dubai')

from django.http import HttpResponse
import pandas as pd
# Create your views here.
def remove_non_numeric(s):
    # Use regular expression to replace all non-numeric characters with an empty string
    return re.sub(r'\D', '', s)

def index(request):
    return render(request, "logsApp/layout.html")



def registerCar(request):
    allnUseCars = InUseCars.objects.all()
    if request.method == "POST":
        ceoNInput = request.POST["ceoNumber"]
        carNInput = request.POST.get("carNumber")
        print(ceoNInput)
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
        ceonumberq = remove_non_numeric(request.POST.get("ceonumber")).strip()
        empnote = request.POST.get("empnote")
        carCondq = request.POST.get("carCd")
        print(carCondq)
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
        return render(request, "logsApp/registerCar.html",{"l":allInUseCars})



def logsfunc(request):
    alllogs = LogsC.objects.all()
    logs = LogsC.objects.all()
    for log in logs:
        print(log.created_at, log.taken_date, log.ended_at)
    return render(request, "logsApp/logs.html",{"alllogs":alllogs})


def export_to_excel(request):
    # Define the Dubai timezone
    dubai_tz = pytz.timezone('Asia/Dubai')

    # Fetch data from the model with related fields
    data = LogsC.objects.select_related('Logs_employee_ins', 'Logs_car_ins').all()

    export_data = []
    for log in data:
        created_at_dubai = log.created_at.astimezone(dubai_tz)
        taken_date_dubai = log.taken_date
        taken_time_dubai = (log.taken_time.replace(tzinfo=dubai_tz) if log.taken_time else None)
        ended_at_dubai = log.ended_at.astimezone(dubai_tz) if log.ended_at else None
        return_date_dubai = log.return_date
        return_time_dubai = (log.return_time.replace(tzinfo=dubai_tz) if log.return_time else None)

        export_data.append({
            'ID': log.id,
            'رقم السياره': log.Logs_car_ins.carNumber,
            'الاسم': log.Logs_employee_ins.ceoName,
            'الرقم الاداري': log.Logs_employee_ins.ceoNumber,
            'تاريخ ووقت الاستلام': created_at_dubai.strftime('%Y-%m-%d %I:%M %p'),
            'تاريخ الاستلام': taken_date_dubai,
            'وقت الاستلام': taken_time_dubai.strftime('%I:%M %p') if taken_time_dubai else None,
            'تاريخ و وقت التسليم': ended_at_dubai.strftime('%Y-%m-%d %I:%M %p') if ended_at_dubai else None,
            'تاريخ التسليم': return_date_dubai,
            'وقت التسليم': return_time_dubai.strftime('%I:%M %p') if return_time_dubai else None,
            'ملاحظه على المركبه': log.carNote,
            'قسم الموظف':log.Logs_employee_ins.section
        })

    # Create a DataFrame from the export data
    df = pd.DataFrame(export_data)

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="logs_data.xlsx"'

    # Use Pandas to write to a temporary Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Logs Data')

        # Get the workbook and the active worksheet
        workbook = writer.book
        worksheet = writer.sheets['Logs Data']

        # Define styles
        header_font = Font(size=16, bold=True, color='000000')  # Black header font
        header_fill = PatternFill(start_color='B7E1A1', end_color='B7E1A1', fill_type='solid')  # Olive green accent 3 lighter 40%
        cell_font = Font(size=16)  # Font for all cells
        center_alignment = Alignment(horizontal='center')

        # Style the header row
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_alignment

        # Apply font style to all cells and keep original width adjustment
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
            for cell in row:
                cell.font = cell_font
                cell.alignment = center_alignment  # Center align all cells

        # Set column widths based on content
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter  # Get the column name
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 4)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    return response



def fineC(request):
    if request.method == "POST":
        fine_date = request.POST.get('finedate')
        fine_time = request.POST.get('finetime')
        fine_car_number = request.POST.get('finecar')

        print(f"Fine date is: {fine_date}")
        print(f"Fine time is: {fine_time}")

        # Combine date and time into a single datetime object
        dubai_tz = pytz.timezone('Asia/Dubai')
        combined_fine_datetime = dubai_tz.localize(timezone.datetime.strptime(f"{fine_date} {fine_time}", '%Y-%m-%d %H:%M'))
        print(combined_fine_datetime.time())
        try:
            car_ins = RegistredCars.objects.get(carNumber=fine_car_number)

            # Query logs based on combined datetime
            finon = LogsC.objects.get(
                taken_date__gte=combined_fine_datetime.date(),
                return_date__lte=combined_fine_datetime.date(),
                taken_time__gte=combined_fine_datetime.time(),
                return_time__lte=combined_fine_datetime.time(),
                Logs_car_ins=car_ins
            )
            print(finon)
            # Handle the result of the finon query as needed
        except RegistredCars.DoesNotExist:
            print(f"Car with number {fine_car_number} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    return render(request,"logsApp/finespage.html",)