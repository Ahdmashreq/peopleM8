from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from string import Template
from tablib import Dataset
from django.utils.encoding import force_str
from django.conf import settings
from attendance.models import Attendance, Task, Employee_Attendance_History
from attendance.forms import FormAttendance, Tasks_inline_formset, FormTasks, ConfirmImportForm, \
    FormEmployeeAttendanceHistory
from attendance.resources import AttendanceResource
from attendance.tmp_storage import TempFolderStorage
from employee.models import Employee
from company.models import Working_Hours_Policy, YearlyHoliday
from leave.models import Leave
from service.models import Bussiness_Travel
from datetime import date, timedelta
import datetime
import calendar


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


@login_required(login_url='/login')
def list_attendance(request):
    employee = Employee.objects.get(user=request.user)
    attendance_list = Attendance.objects.filter(employee=employee)
    work_time = []
    att_form = FormAttendance(form_type='check_in')
    employee = Employee.objects.get(user=request.user)
    # opened_attendance = False
    # for att in attendance_list:
    #     if att.check_out is None:
    #         opened_attendance = True
    # if request.method == "POST":
    #     if not opened_attendance:
    #         # att_form = FormAttendance(request.POST, form_type='check_in')
    #         # if att_form.is_valid():
    #         #     att_obj = att_form.save(commit=False)
    #         #     att_obj.employee = employee
    #         #     att_obj.created_by = request.user
    #         #     att_obj.last_update_by = request.user
    #         #     my_time = datetime.now().time()
    #         #     att_obj.check_in = my_time.strftime("%H:%M:%S")
    #         #     messages.success(request, 'You are now checked in')
    #         #     att_obj.save()
    #         #     return redirect('attendance:user-list-attendance')
    #         #     messages.success(request, 'Please fill your daily tasks')
    #         # else:
    #         #     messages.error(request, att_form.errors)
    #     else:
    #         messages.error(request, _("You still have attendance opened. Please check out first"))
    att_context = {
        'attendances': attendance_list,
        'work_time': work_time,
        'att_form': att_form
    }
    return render(request, 'attendance.html', att_context)


@login_required(login_url='/login')
def check_in_time(request):
    company_policy = Working_Hours_Policy.objects.get(enterprise=request.user.company)
    current_employee = Employee.objects.get(user=request.user)
    attendance_list = Attendance.objects.filter(employee=current_employee)

    current_date = datetime.now().date()
    current_time = datetime.now().time()
    difference = datetime.combine(datetime.now(), current_time) - datetime.combine(datetime.now(),
                                                                                   company_policy.hrs_start_from)

    opened_attendance = False
    for att in attendance_list:
        if att.check_out is None:
            opened_attendance = True
    if not opened_attendance:
        att_obj = Attendance(
            employee=current_employee,
            date=current_date,
            check_in=current_time,
            delay_hrs=strfdelta(difference, "%H:%M:%S"),
            day_of_week=current_date.weekday(),
            created_by=request.user,
        )
        att_obj.save()
    else:
        print("You still have attendance opened. Please check out first")
        messages.error(request, _("You still have attendance opened. Please check out first"))
    return redirect('attendance:user-list-attendance')


@login_required(login_url='/login')
def check_out_time(request):
    employee = Employee.objects.get(user=request.user)
    attendance_obj = Attendance.objects.get(employee=employee, check_out__isnull=True)
    user_tasks = Task.objects.filter(attendance=attendance_obj)

    if user_tasks:
        att_form = FormAttendance(form_type='check_out', instance=attendance_obj)
        if request.method == "POST":
            required_check_in = attendance_obj.check_in
            current_time = datetime.datetime.now().time()
            # attendance_obj.check_out = current_time.strftime("%H:%M:%S")
            attendance_obj.check_out = current_time
            attendance_obj.last_update_by = request.user
            attendance_obj.save()
            messages.success(request, 'You are now checked out')
            return redirect('attendance:user-list-attendance')

        att_context = {
            'att_form': att_form,
            'check_in_time': attendance_obj.check_in,
            'check_out_time': datetime.datetime.now().time(),
        }
        return render(request, 'check_out.html', att_context)
    else:
        return redirect('attendance:create_task')


@login_required(login_url='/login')
def list_tasks_view(request, attendance_slug):
    attendance_obj = get_object_or_404(Attendance, id=attendance_slug)
    list_tasks = Task.objects.filter(attendance=attendance_obj)
    task_context = {
        'list_tasks': list_tasks,
        'attendance': attendance_obj
    }
    return render(request, 'list_tasks.html', task_context)


@login_required(login_url='/login')
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
    else:
        tasks_inline_formset = Tasks_inline_formset(queryset=Task.objects.none())
    task_context = {
        'tasks': tasks_inline_formset,
        'list_tasks': list_tasks
    }
    return render(request, 'create_task.html', task_context)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def list_all_attendance(request):
    attendance_list = Attendance.objects.filter(created_by__company=request.user.company).order_by('-date')
    att_context = {
        'attendances': attendance_list,
        'page_title': 'Employees Attendance',

    }
    return render(request, 'list_attendance.html', att_context)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def fill_employee_attendance_days_employee_view(request, month_v, year_v):
    employees_list = Employee.objects.filter(enterprise=request.user.company)
    # Employee_Attendance_History.objects.bulk_create([ Employee_Attendance_History(employee=q, month=month_v, year=year_v,created_by=request.user) for q in employees_list ])
    fill_employee_attendance_days_attendance_view(request, month_v, year_v)
    return True


@login_required(login_url='/login')
def fill_employee_attendance_days_attendance_view(request, month_v, year_v):
    employee_attendance = Attendance.objects.filter(created_by__company=request.user.company).values('employee',
                                                                                                     'date__month',
                                                                                                     'date__year').annotate(
        attendance_count=Count('date'))
    for emp in employee_attendance:
        print(emp)
    return True


@login_required(login_url='/login')
def fill_employee_attendance_days_leaves_view(request, month_v, year_v):
    all_leave_list = Leave.objects.filter(employee__user=request.user).values('employee', 'startdate__month').annotate(
        leave_count=Count('startdate'))
    bussiness_travel_list = Bussiness_Travel.objects.filter(emp=employees_list)
    return True


@login_required(login_url='/login')
def update_attendance(request, att_update_slug):
    required_att = Attendance.objects.get(slug=att_update_slug)
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
        'page_title': f"Update {name} attendance"
    }
    return render(request, 'create-attendance.html', context)


@login_required(login_url='/login')
def delete_attendance(request, att_delete_slug):
    required_att = Attendance.objects.get(slug=att_delete_slug)
    deleted = required_att.delete()
    if deleted:
        messages.success(request, 'Record successfully deleted')

    else:
        messages.error(request, 'Record is NOT deleted')

    return redirect('attendance:emp-attendance')


def get_deductions_overtime_and_delay(employee_id, month, year):
    deduction_days = calculate_deduction_days(month, year, employee_id)
    overtime_hrs = calculate_overtime(employee_id, month, year)
    delay_hrs = calculate_delay_hrs(employee_id, month, year)
    return {"deduction_days": deduction_days, "overtime": overtime_hrs, "delay_hrs": delay_hrs}


def is_day_a_leave(user_id, day):
    leaves = Leave.objects.filter(
        Q(user__id=user_id) and ((Q(startdate__month=day.month) and Q(startdate__year=day.year)) or (
                Q(enddate__month=day.month) and Q(enddate__year=day.year))))
    for leave in leaves:
        if leave['startdate'] <= day <= leave['enddate']:
            return True
    return False


def is_day_a_service(employee_id, day):
    services = Bussiness_Travel.objects.filter(
        Q(emp__id=employee_id) and (
                (Q(estimated_date_of_travel_from__month=day.month) and Q(
                    estimated_date_of_travel_from__year=day.year)) or (
                        Q(estimated_date_of_travel_to__month=day.month) and Q(
                    estimated_date_of_travel_from__year=day.year))))
    for service in services:
        if service['estimated_date_of_travel_from'] <= day <= service['estimated_date_of_travel_to']:
            return True
    return False


def is_day_a_holiday(day):
    month_holidays = YearlyHoliday.objects.filter(
        Q(year=day.year) and (Q(start_date__month=day.month) or
                              Q(end_date__month=day.month))).values('start_date',
                                                                    'end_date')
    for x in month_holidays:
        if x['start_date'] <= day <= x['end_date']:
            return True
    return False


def is_day_a_weekend(day):
    weekends = Working_Hours_Policy.objects.values('week_end_days')
    day_name = calendar.day_name[day.weekday()]
    if day_name.upper() in weekends[0]['week_end_days']:
        return True
    else:
        return False


def calculate_deduction_days(month, year, employee_id):
    # return the number of days to be deducted from a given employee in a given month and year
    # days that are either weekends,holidays ,leaves or services are not deduced
    employee = Employee.objects.get(id=employee_id)
    attendances = Attendance.objects.filter(date__month=month, date__year=year, employee__id=employee_id)
    absence_day_rate = \
        Working_Hours_Policy.objects.filter(enterprise=employee.enterprise).values('absence_days_rate')[0][
            'absence_days_rate']
    absence_days = []
    number_of_days = calendar.monthrange(2020, month)[1]
    days = [datetime.date(year, month, day) for day in range(1, number_of_days + 1)]
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
    overtime_hrs = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for x in attendance:
        if x.check_out:
            try:
                delta = datetime.timedelta(hours=x.normal_overtime_hours.hour, minutes=x.normal_overtime_hours.minute,
                                           seconds=x.normal_overtime_hours.second)
                overtime_hrs += delta
            except Exception as e:
                print(e)
    return overtime_hrs


def calculate_delay_hrs(employee_id, month, year):
    # calculate delay hours for a given employee in a given month and year for all records that have checkout
    # ignoring records with no checkout
    attendance = Attendance.objects.filter(date__month=month, date__year=year, employee__id=employee_id)
    delay_hrs = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for x in attendance:
        if x.check_out:
            try:
                delta = datetime.timedelta(hours=x.delay_hrs.hour, minutes=x.delay_hrs.minute,
                                           seconds=x.delay_hrs.second)
                delay_hrs += delta
            except Exception as e:
                print(e)

    return delay_hrs
