from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from string import Template
from tablib import Dataset
from django.conf import settings
from attendance.models import Attendance, Task, Employee_Attendance_History, Attendance_Interface
from attendance.forms import (FormAttendance, Tasks_inline_formset, FormTasks, ConfirmImportForm,
                              FormEmployeeAttendanceHistory)
from attendance.resources import AttendanceResource
from attendance.tmp_storage import TempFolderStorage
from attendance.utils import is_day_a_weekend, is_day_a_holiday, is_day_a_leave, is_day_a_service
from employee.models import Employee
from leave.models import Leave
from service.models import Bussiness_Travel
from company.models import Working_Days_Policy
import pytz
from zk import ZK, const
from zk.exception import ZKErrorConnection, ZKErrorResponse, ZKNetworkError
import datetime as mydatetime
import calendar
from attendance.resources import *

# from dateutil.parser import parse


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


def connect_download_from_machine(company):
    conn = None
    zk = ZK('192.168.1.220', port=4370, timeout=5)
    device_users = []
    try:
        conn = zk.connect()
        # Get all users (will return list of User object)
        users = conn.get_users()
        for x in users:
            device_users.append(x)
        # Get attendances (will return list of Attendance object)
        attendances_list = conn.get_attendance()
        if Attendance_Interface.objects.all().exists():
            Attendance_Interface.objects.all().delete()
        for att in attendances_list:
            att_int = Attendance_Interface(

                company=company,
                user_name=[x.name for x in device_users if x.user_id == att.user_id][0],
                user_id=att.user_id,

                date=pytz.utc.localize(att.timestamp),
                punch=att.punch,
            )
            att_int.save()
    except Exception as e:
        print("Process terminate : {}".format(e))
    return "Device Connected Successfully"


def disconnect_device():
    zk = ZK('192.168.1.220', port=4370, timeout=5)
    try:
        print('Disconnecting to device ...')
        zk.disconnect()
    except ZKErrorConnection as e:
        return "instance are not connected."
    return "Disconnected"


def populate_attendance_table(date):
    atts = Attendance_Interface.objects.filter(date__date=date)
    if len(atts) == 0:
        print("Attendance Interface table doesn't have data for date selected")
    else:
        data = {}
        for att in atts:
            try:
                Employee.objects.get(emp_number=att.user_id)
            except Employee.DoesNotExist:
                continue
            # initialize the dictionary that hold attendance check in and check out
            data[att.user_id] = ({} if data.get(att.user_id, None) is None else data[att.user_id])
            if att.punch == '0':
                data[att.user_id]['check_in'] = att.date.time()
            elif att.punch == '1':
                data[att.user_id]["check_out"] = att.date.time()
        for key, value in data.items():
            emp = Employee.objects.get(emp_number=key)
            try:
                attendance = Attendance.objects.filter(date=date).get(employee=emp)
                attendance.check_in = value.get("check_in", None)
                attendance.check_out = value.get("check_out", None)
            except Attendance.DoesNotExist:
                attendance = Attendance(
                    employee=emp,
                    date=date,
                    check_in=value.get("check_in", None),
                    check_out=value.get("check_out", None),
                )
            attendance.save()
        # This part to get all employees who are absent this day
        att_employees = Attendance.objects.filter(date=date).values_list("employee", flat=True)
        employees = Employee.objects.all().values_list("id", flat=True)
        for employee in employees:
            if employee not in att_employees:
                employee = Employee.objects.get(id=employee)
                attendance = Attendance(
                    employee=employee,
                    date=date,
                )
                attendance.save()


@login_required(login_url='home:user-login')
def get_unsigned_and_absence_days(request):
    att_context = {}
    if request.method == "POST":
        month = request.POST.get('month', None)
        unsigned = Attendance.objects.filter(employee__enterprise=request.user.company, date__month=month, status="N")
        absence = Attendance.objects.filter(employee__enterprise=request.user.company, date__month=month, status="A")
        att_context = {
            'unsigned': unsigned,
            'absence': absence,
            'month': month,
        }
    return render(request, 'list_attendance_with_deductions.html', att_context)


@login_required(login_url='home:user-login')
def list_machine_logs(request):
    machine_status = "Disconnected"
    attendance_list = Attendance.objects.filter().order_by('-date')
    if request.method == 'POST':
        if 'connect' in request.POST:
            connect_download_from_machine(request.user.company)
            populate_attendance_table(datetime.now().date())
            attendance_list = Attendance.objects.filter().order_by('-date')
            machine_status = "Device Connected Successfully"
        else:
            machine_status = disconnect_device()
    att_context = {
        'attendances': attendance_list,
        'machine_status': machine_status,
    }
    return render(request, 'list-machine-log.html', att_context)


@login_required(login_url='home:user-login')
def list_attendance(request):
    employee = Employee.objects.get(user=request.user)
    attendance_list = Attendance.objects.filter(employee=employee)
    work_time = []
    att_form = FormAttendance(form_type='check_in')
    employee = Employee.objects.get(user=request.user)
    att_context = {
        'attendances': attendance_list,
        'work_time': work_time,
        'att_form': att_form
    }
    return render(request, 'attendance.html', att_context)


@login_required(login_url='home:user-login')
def check_in_time(request):
    company_policy = Working_Days_Policy.objects.get(enterprise=request.user.company)
    current_employee = Employee.objects.get(user=request.user)
    attendance_list = Attendance.objects.filter(employee=current_employee)

    current_date = datetime.now().date()
    current_time = datetime.now().time()

    opened_attendance = False
    for att in attendance_list:
        if att.check_out is None:
            opened_attendance = True
    if not opened_attendance:
        att_obj = Attendance(
            employee=current_employee,
            date=current_date,
            check_in=current_time,
            day_of_week=current_date.weekday(),
            created_by=request.user,
        )
        att_obj.save()
    else:
        print("You still have attendance opened. Please check out first")
        messages.error(request, _("You still have attendance opened. Please check out first"))
    return redirect('attendance:user-list-attendance')


@login_required(login_url='home:user-login')
def check_out_time(request):
    employee = Employee.objects.get(user=request.user)
    attendance_obj = Attendance.objects.get(employee=employee, check_out__isnull=True)
    user_tasks = Task.objects.filter(attendance=attendance_obj)

    if user_tasks:
        att_form = FormAttendance(form_type='check_out', instance=attendance_obj)
        if request.method == "POST":
            required_check_in = attendance_obj.check_in
            current_time = datetime.now().time()
            # attendance_obj.check_out = current_time.strftime("%H:%M:%S")
            attendance_obj.check_out = current_time
            attendance_obj.last_update_by = request.user
            attendance_obj.save()
            messages.success(request, 'You are now checked out')
            return redirect('attendance:user-list-attendance')

        att_context = {
            'att_form': att_form,
            'check_in_time': attendance_obj.check_in,
            'check_out_time': datetime.now().time(),
        }
        return render(request, 'check_out.html', att_context)
    else:
        return redirect('attendance:create_task')


@login_required(login_url='home:user-login')
def list_tasks_view(request, attendance_slug):
    attendance_obj = get_object_or_404(Attendance, id=attendance_slug)
    list_tasks = Task.objects.filter(attendance=attendance_obj)
    task_context = {
        'list_tasks': list_tasks,
        'attendance': attendance_obj
    }
    return render(request, 'list_tasks.html', task_context)


@login_required(login_url='home:user-login')
def create_task(request):
    employee = Employee.objects.get(user=request.user)
    user_last_attendance = Attendance.objects.filter(employee=employee, check_out__isnull=True).latest('id')
    list_tasks = Task.objects.filter(attendance=user_last_attendance)
    if request.method == "POST":
        tasks_inline_formset = Tasks_inline_formset(data=request.POST)
        if tasks_inline_formset.is_valid():
            tasks_objs = tasks_inline_formset.save(commit=False)
            for x in tasks_objs:
                x.attendance = user_last_attendance
                x.user = request.user
                x.save()
            messages.success(request, 'Saved Successfully.')
            return redirect('attendance:user-list-attendance')
    else:
        tasks_inline_formset = Tasks_inline_formset(queryset=Task.objects.none())
    task_context = {
        'tasks': tasks_inline_formset,
        'list_tasks': list_tasks
    }
    return render(request, 'create_task.html', task_context)


@login_required(login_url='home:user-login')
def edit_task_view(request, slug_text):
    instance = get_object_or_404(Task, id=slug_text)
    if request.method == "POST":
        task_form = FormTasks(data=request.POST, instance=instance)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.save()
            messages.success(request, 'Saved Successfully.')
        else:
            messages.error(request, 'Something went wrong.')
    else:  # http request
        task_form = FormTasks(instance=instance)
    task_context = {
        'task_form': task_form,
        'all_tasks_id': instance.attendance.id,
    }
    return render(request, 'edit_task.html', task_context)


@login_required(login_url='home:user-login')
def edit_inline_tasks(request, attendance_text):
    required_att = Attendance.objects.get(id=attendance_text)
    req_tasks_formset = Tasks_inline_formset(instance=required_att)
    if request.method == 'POST':
        req_tasks_formset = Tasks_inline_formset(request.POST, instance=required_att)
        if req_tasks_formset.is_valid():
            req_tasks_obj = req_tasks_formset.save(commit=False)
            for task in req_tasks_obj:
                task.attendance = required_att
                task.user = request.user
                task.save()
        else:
            req_tasks_formset.errors
    return render(request, 'create_task.html', {'tasks': req_tasks_formset})


@login_required(login_url='home:user-login')
def delete_task(request, slug_text):
    instance = get_object_or_404(Task, id=slug_text)
    instance.delete()
    messages.add_message(request, messages.SUCCESS, 'Task was deleted successfully')
    return redirect('attendance:list-tasks', attendance_slug=instance.attendance.slug)


TMP_STORAGE_CLASS = getattr(settings, 'IMPORT_EXPORT_TMP_STORAGE_CLASS',
                            TempFolderStorage)


def write_to_tmp_storage(import_file):
    tmp_storage = TMP_STORAGE_CLASS()
    data = bytes()
    for chunk in import_file.chunks():
        data += chunk

    tmp_storage.save(data, 'rb')
    return tmp_storage


@login_required(login_url='home:user-login')
def upload_xls_file(request):
    attendance_resource = AttendanceResource()
    context = {}
    if request.method == "POST":
        import_file = request.FILES['import_file']
        dataset = Dataset()
        # unhash the following line in case of csv file
        # imported_data = dataset.load(import_file.read().decode(), format='csv')
        imported_data = dataset.load(import_file.read(), format='xlsx')  # this line in case of excel file

        result = attendance_resource.import_data(imported_data, dry_run=True,
                                                 user=request.user)  # Test the data import
        context['result'] = result
        tmp_storage = write_to_tmp_storage(import_file)
        if not result.has_errors() and not result.has_validation_errors():
            initial = {
                'import_file_name': tmp_storage.name,
                'original_file_name': import_file.name,
            }
            confirm_form = ConfirmImportForm(initial=initial)
            context['confirm_form'] = confirm_form

    context['fields'] = [f.column_name for f in attendance_resource.get_user_visible_fields()]

    return render(request, 'upload-attendance.html', context=context)


@login_required(login_url='home:user-login')
def confirm_xls_upload(request):
    if request.method == "POST":
        confirm_form = ConfirmImportForm(request.POST)
        attendance_resource = AttendanceResource()
        if confirm_form.is_valid():
            tmp_storage = TMP_STORAGE_CLASS(name=confirm_form.cleaned_data['import_file_name'])
            data = tmp_storage.read('rb')
            # Uncomment the following line in case of 'csv' file
            # data = force_str(data, "utf-8")
            dataset = Dataset()
            # Enter format = 'csv' for csv file
            imported_data = dataset.load(data, format='xlsx')

            result = attendance_resource.import_data(imported_data,
                                                     dry_run=False,
                                                     raise_errors=True,
                                                     file_name=confirm_form.cleaned_data['original_file_name'],
                                                     user=request.user, )
            messages.success(request, 'Attendance successfully uploaded')
            tmp_storage.remove()
            return redirect('attendance:emp-attendance')
        else:
            messages.error(request, 'Uploading failed ,please try again')
            return redirect('attendance:upload-attendance')


@login_required(login_url='home:user-login')
def export_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        attendance_resource = AttendanceResource()
        dataset = attendance_resource.export()


        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="attendance_exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="attendance_exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="attendance_exported_data.xls"'
            return response
    export_context = {
    'page_title':'Please select format of file.',
    }
    #context['fields'] = [f.column_name for f in department_resource.get_user_visible_fields()]
    return render(request, 'export.html', export_context )
















@login_required(login_url='home:user-login')
def list_all_attendance(request):
    attendance_list = Attendance.objects.filter(created_by__company=request.user.company).order_by('-date')
    att_context = {
        'attendances': attendance_list,
        'page_title': 'Employees Attendance',

    }
    return render(request, 'list_attendance.html', att_context)


@login_required(login_url='home:user-login')
def list_employee_attendance_history_view(request):
    get_deductions_overtime_and_delay(employee_id=1, month=9, year=2020)
    emp_attendance_form = FormEmployeeAttendanceHistory()
    emp_attendance_list = Employee_Attendance_History.objects.filter(created_by__company=request.user.company).order_by(
        '-month')
    if request.method == 'POST':
        emp_attendance_form = FormEmployeeAttendanceHistory(request.POST)
        if emp_attendance_form.is_valid():
            fill_employee_attendance_days_employee_view(request,
                                                        emp_attendance_form.cleaned_data['month'],
                                                        emp_attendance_form.cleaned_data['year'],
                                                        )
        else:
            messages.error(request, emp_attendance_form.errors)
            # print(emp_attendance_form.errors)
    att_context = {
        'emp_attendance_list': emp_attendance_list,
        'page_title': 'Employees Attendance Days',
        'emp_attendance_form': emp_attendance_form,
    }
    return render(request, 'employee_attendance_history.html', att_context)


@login_required(login_url='home:user-login')
def fill_employee_attendance_days_employee_view(request, month_v, year_v):
    employees_list = Employee.objects.filter(enterprise=request.user.company)
    # Employee_Attendance_History.objects.bulk_create([ Employee_Attendance_History(employee=q, month=month_v, year=year_v,created_by=request.user) for q in employees_list ])
    fill_employee_attendance_days_attendance_view(request, month_v, year_v)
    return True


@login_required(login_url='home:user-login')
def fill_employee_attendance_days_attendance_view(request, month_v, year_v):
    employee_attendance = Attendance.objects.filter(created_by__company=request.user.company).values('employee',
                                                                                                     'date__month',
                                                                                                     'date__year').annotate(
        attendance_count=Count('date'))
    for emp in employee_attendance:
        print(emp)
    return True


@login_required(login_url='home:user-login')
def fill_employee_attendance_days_leaves_view(request, month_v, year_v):
    all_leave_list = Leave.objects.filter(employee__user=request.user).values('employee', 'startdate__month').annotate(
        leave_count=Count('startdate'))
    bussiness_travel_list = Bussiness_Travel.objects.filter(emp=employees_list)
    return True


@login_required(login_url='home:user-login')
def update_attendance(request, id, flag):
    # flag parameter to determine form where the request is issued so "back" button functions correctly
    required_att = Attendance.objects.get(id=id)
    att_form = FormAttendance(form_type=None, instance=required_att)
    if request.method == "POST":
        att_form = FormAttendance(request.POST, form_type=None, instance=required_att)
        if att_form.is_valid():
            att_obj = att_form.save(commit=False)
            att_obj.last_update_by = request.user
            att_obj.save()
            messages.success(request, 'Record is successfully updated')
        else:
            messages.error(request, 'Record is NOT updated')

    name = required_att.employee.emp_name
    context = {
        'attendance_form': att_form,
        'page_title': f"Update {name} attendance",
        'flag': flag
    }
    return render(request, 'create-attendance.html', context)


@login_required(login_url='home:user-login')
def delete_attendance(request, att_delete_slug):
    required_att = Attendance.objects.get(slug=att_delete_slug)
    deleted = required_att.delete()
    if deleted:
        messages.success(request, 'Record successfully deleted')

    else:
        messages.error(request, 'Record is NOT deleted')

    return redirect('attendance:emp-attendance')


def calculate_deduction_days(month, year, employee_id):
    # return the number of days to be deducted from a given employee in a given month and year
    # days that are either weekends,holidays ,leaves or services are not deduced
    employee = Employee.objects.get(id=employee_id)
    attendances = Attendance.objects.filter(date__month=month, date__year=year, employee__id=employee_id)
    absence_day_rate = \
        Working_Days_Policy.objects.filter(enterprise=employee.enterprise).values('absence_days_rate')[0][
            'absence_days_rate']
    absence_days = []
    number_of_days = calendar.monthrange(2020, month)[1]
    days = [mydatetime.date(year, month, day) for day in range(1, number_of_days + 1)]
    attendance_list = list()
    for date in attendances:
        attendance_list.append(date.date)
    missing = sorted(set(days) - set(attendance_list))
    for day in missing:
        if is_day_a_weekend(day):
            print("this day is weekend", day)
            pass
        elif is_day_a_holiday(day):
            print("this day is Holiday", day)
            pass
        elif is_day_a_leave(employee.user.id, day):
            print("this day is a leave", day)
            pass
        elif is_day_a_service(employee_id, day):
            print("this day is a service", day)
            pass
        else:
            absence_days.append(day)

    deduction_days = absence_day_rate * len(absence_days)
    return deduction_days


def calculate_overtime(employee_id, month, year):
    # calculate normal overtime hours for a given employee in a given month and year for all records that have checkout
    # ignoring records with no checkout
    attendance = Attendance.objects.filter(date__month=month, date__year=year, employee__id=employee_id)
    overtime_hrs = mydatetime.timedelta(hours=0, minutes=0, seconds=0)
    for x in attendance:
        if x.check_out:
            try:
                # delta = mydatetime.timedelta(hours=x.normal_overtime_hours.hour, minutes=x.normal_overtime_hours.minute,
                #                            seconds=x.normal_overtime_hours.second)
                overtime_hrs += x.normal_overtime_hours
            except Exception as e:
                print(e)
    return overtime_hrs


def calculate_delay_hrs(employee_id, month, year):
    # calculate delay hours for a given employee in a given month and year for all records that have checkout
    # ignoring records with no checkout
    attendance = Attendance.objects.filter(date__month=month, date__year=year, employee__id=employee_id)
    delay_hrs = mydatetime.timedelta(hours=0, minutes=0, seconds=0)
    for x in attendance:
        if x.check_out:
            try:
                # delta = mydatetime.timedelta(hours=x.delay_hrs.hour, minutes=x.delay_hrs.minute,
                #                            seconds=x.delay_hrs.second)
                delay_hrs = delay_hrs + x.delay_hrs
            except Exception as e:
                print(e)

    return delay_hrs


def get_deductions_overtime_and_delay(employee_id, month, year):
    deduction_days = calculate_deduction_days(month, year, employee_id)
    overtime_hrs = calculate_overtime(employee_id, month, year)
    delay_hrs = calculate_delay_hrs(employee_id, month, year)
    print("mY calculated delays are ", delay_hrs)
    print("mY calculated overtime are ", overtime_hrs)
    return {"deduction_days": deduction_days, "overtime_hrs": overtime_hrs, "delay_hrs": delay_hrs}
