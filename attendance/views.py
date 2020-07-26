from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance,Task
from employee.models import Employee
from django.utils import timezone
from attendance.forms import FormAttendance, Tasks_inline_formset, FormTasks
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from string import Template


class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

@login_required(login_url='/login')
def attendance(request):
    employee = Employee.objects.get(user=request.user)
    attendance_list= Attendance.objects.filter(employee=employee)
    work_time=[]
    att_form = FormAttendance(form_type='check_in')
    now = timezone.now()
    employee = Employee.objects.get(user=request.user)
    opened_attendance = False
    for att in attendance_list:
        if att.check_out is None:
            opened_attendance = True
    if request.method == "POST":
        if not opened_attendance:
            att_form = FormAttendance(request.POST, form_type='check_in' )
            if att_form.is_valid() :
                att_obj = att_form.save(commit=False)
                att_obj.employee=employee
                att_obj.created_by=request.user
                att_obj.last_update_by=request.user
                mytime = datetime.now().time()
                mydate = datetime.now().date()
                att_obj.check_in= mytime.strftime("%H:%M:%S")
                messages.success(request,'You are now checked in' )
                att_obj.save()
                return redirect('attendance:list-attendance')
                messages.success(request,'Please fill your daily tasks' )
            else:
                messages.error(request,att_form.errors )
        else:
            messages.error(request,_("You still have attendance opened. Please check out first"))
    return render(request, 'attendance.html',{'attendances':attendance_list,'work_time':work_time,'att_form': att_form})

# @login_required(login_url='/login')
# def check_in_time(request):
#     now = timezone.now()
#     employee = Employee.objects.get(user=request.user)
#     employee_obj = Attendance.objects.get(employee=employee, check_out__isnull = True)
#     if request.method == "POST":
#         att_form = FormAttendance(request.POST, form_type='check_in' )
#         if att_form.is_valid() :
#             att_obj = att_form.save(commit=False)
#             att_obj.employee=employee
#             att_obj.created_by=request.user
#             att_obj.last_update_by=request.user
#             mytime = datetime.now().time()
#             mydate = datetime.now().date()
#             att_obj.check_in= mytime.strftime("%H:%M:%S")
#
#             messages.success(request,'You are now checked in' )
#             att_obj.save()
#             return redirect('attendance:create_task')
#         else:
#             messages.error(request,att_form.errors )
#     return redirect('attendance:create_task')



@login_required(login_url='/login')
def check_out_time(request):
    now = timezone.now()
    employee = Employee.objects.get(user=request.user)
    attendance_obj = Attendance.objects.get(employee=employee, check_out__isnull = True)
    user_tasks = Task.objects.filter(attendance=attendance_obj)
    if user_tasks:
        att_form = FormAttendance(form_type='check_out', instance=attendance_obj)
        if request.method == "POST":
            att_form = FormAttendance(request.POST, form_type='check_out', instance=attendance_obj)
            required_check_in = attendance_obj.check_in
            if att_form.is_valid():
                att_obj = att_form.save(commit=False)
                att_obj.last_update_by=request.user
                att_obj.check_in = required_check_in
                myDate = datetime.now().time()
                att_obj.check_out = myDate.strftime("%H:%M:%S")
                tdelta_worked_time = datetime.combine(datetime.now(), myDate) - datetime.combine(datetime.now(), att_obj.check_in)
                att_obj.work_time = strfdelta(tdelta_worked_time,"%H:%M:%S")
                att_obj.save()
                messages.success(request,'You are now checked out' )
                return redirect('attendance:list-attendance')
            else:
                messages.error(request,att_form.errors )
        return render(request, 'check_out.html', {'att_form': att_form,})
    else:
        return redirect('attendance:create_task')

@login_required(login_url='/login')
def list_tasks(request,id):
    attendance_obj = get_object_or_404(Attendance, id=id)
    list_tasks = Task.objects.filter(attendance = attendance_obj)
    return render(request, 'list_tasks.html',{'list_tasks':list_tasks,'attendance':attendance_obj})

@login_required(login_url='/login')
def delete_task(request,id):
    instance = get_object_or_404(Task, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS,'Task was deleted successfully')
    return redirect('attendance:list_tasks', id=instance.attendance.id)

@login_required(login_url='/login')
def edit_task(request,slug_text):
    instance = get_object_or_404(Task, slug=slug_text)
    task_form = FormTasks(instance=instance)
    if request.method == "POST":
        task_form = FormTasks(data=request.POST, instance=instance)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.save()
            messages.success(request,'Saved Successfully.')
        else:
            print(task_form.errors)
    else:  # http request
        task_form = FormTasks(instance=instance)
    return render(request, 'edit_task.html', {'task_form': task_form,'all_tasks_id': instance.attendance.id,})

@login_required(login_url='/login')
def edit_inline_tasks(request, id):
    required_att = Attendance.objects.get(id = id)
    req_tasks_formset = Tasks_inline_formset(instance=required_att)
    if request.method == 'POST':
        req_tasks_formset = Tasks_inline_formset(request.POST, instance=required_att)
        if req_tasks_formset.is_valid():
            req_tasks_obj = req_tasks_formset.save(commit=False)
            for task in req_tasks_obj:
                task.attendance=required_att
                task.user=request.user
                task.save()
        else:
            req_tasks_formset.errors
    return render(request, 'create_task.html', {'tasks':req_tasks_formset})

@login_required(login_url='/login')
def create_task(request):
    employee = Employee.objects.get(user=request.user)
    attendance = Attendance.objects.filter(employee=employee).latest('id')
    tasks = Task.objects.filter(attendance=attendance)
    if request.method == "POST":
        TasksFormSet = Tasks_inline_formset(data=request.POST)
        if TasksFormSet.is_valid():
            tasks=TasksFormSet.save(commit=False)
            for x in tasks:
                x.attendance=attendance
                x.user=request.user
                x.save()
            # return redirect('attendance:edit_task id=TasksFormSet.id')
            messages.success(request,'Saved Successfully.')
    else:
        TasksFormSet = Tasks_inline_formset(queryset=Task.objects.none())
    return render(request, 'create_task.html', {'tasks':TasksFormSet,'list_tasks':tasks})
