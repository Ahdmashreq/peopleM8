import os
from django.shortcuts import render, redirect
from leave.models import LeaveMaster, Leave
from employee.models import JobRoll, Employee
from employee.notification_helper import NotificationHelper
from leave.forms import FormLeave, FormLeaveMaster
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template import loader
import datetime
from datetime import datetime



def email_sender(subject, message, from_email, recipient_list, html_message):
    try:
        send_mail(subject=subject,
                  message=message,
                  from_email=from_email,
                  recipient_list=[recipient_list],
                  fail_silently=False,
                  html_message=html_message)
    except Exception as e:
        print(e)


def message_composer(request, html_template, instance_name, result):
    reviewed_by = Employee.objects.get(user=request.user)
    employee = Employee.objects.get(user=instance.user)
    from_date = instance.startdate
    to_date = instance.enddate
    resume = instance.resume_date
    reason = instance.reason
    html_message = loader.render_to_string(
        html_template,
        {
            'leave_id': instance.id,
            'result': result,
            'reviewer': reviewed_by,
            'requestor':employee,
            'user_name': instance.user,
            'team_leader': reviewed_by,
            'subject': 'Mashreq Arabia approval Form',
            'date_from': from_date,
            'date_to': to_date,
            'date_back': resume,
            'comments': reason,
            'no_of_days': (to_date - from_date).days + 1
        }
    )
    return html_message


@login_required(login_url='/login')
def add_leave(request):
    employee = Employee.objects.get(user=request.user)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    if request.method == "POST":
        leave_form = FormLeave(data=request.POST, form_type=None)
        if eligible_user_leave(request.user):
            if leave_form.is_valid():
                if valid_leave(request.user, leave_form.cleaned_data['startdate'], leave_form.cleaned_data['enddate']):

                    leave = leave_form.save(commit=False)
                    leave.user = request.user
                    leave.save()

                    if employee_job.manager:
                        NotificationHelper(employee, employee_job.manager, leave).send_notification()
                    requestor_email = employee.email
                    team_leader_email = employee_job.manager.email
                    html_message = message_composer(request, html_template='leave_mail.html', instance_name=leave, result=None)


                    email_sender('Applying for a leave', 'Applying for a leave', requestor_email,
                                 team_leader_email, html_message)

                    messages.add_message(request, messages.SUCCESS,
                                         'Leave Request was created successfully')
                    return redirect('leave:list_leave')
                else:
                    leave_form.add_error(None, "Requested leave intersects with another leave")
            else:
                print(leave_form.errors)
        else:
            leave_form.add_error(None, "You are not eligible for leave request")
    else:  # http request
        leave_form = FormLeave(form_type=None)
    return render(request, 'add_leave.html', {'leave_form': leave_form})


def eligible_user_leave(user):
    now_date = datetime.date(datetime.now())
    leaves = Leave.objects.filter(user=user, status='Approved')
    for leave in leaves:
        if leave.enddate >= now_date >= leave.startdate:
            return False
        else:
            continue
    return True


def valid_leave(user, req_startdate, req_enddate):
    leaves = Leave.objects.filter(user=user, status='Approved').order_by('-id')
    for leave in leaves[0:3]:
        if leave.enddate >= req_startdate >= leave.startdate or \
                req_enddate >= leave.startdate >= req_startdate:
            return False
    return True


@login_required(login_url='/login')
def list_leave(request):
    employee = Employee.objects.get(user=request.user)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    is_manager = False
    if employee_job.manager == None:  # check if the loged in user is a manager
        list_leaves = Leave.objects.all_pending_leaves()
        is_manager = True
    else:
        list_leaves = Leave.objects.filter(user=request.user)
        is_manager = False
    return render(request, 'list_leave.html', {'leaves': list_leaves, 'is_manager': is_manager})


@login_required(login_url='/login')
def delete_leave_view(request, id):
    instance = get_object_or_404(Leave, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Leave was deleted successfully')
    return redirect('leave:list_leave')


@login_required(login_url='/login')
def edit_leave(request, id):
    instance = get_object_or_404(Leave, id=id)
    employee = Employee.objects.get(user=instance.user)
    if request.method == "POST":
        leave_form = FormLeave(data=request.POST, form_type='respond', instance=instance)
        if leave_form.is_valid():
            leave = leave_form.save(commit=False)
            leave.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Leave request was created successfully')
            return redirect('leave:list_leave')
        else:
            print(leave_form.errors)
    else:  # http request
        leave_form = FormLeave(form_type='respond', instance=instance)
    return render(request, 'edit-leave.html', {'leave_form': leave_form, 'leave_id': id, 'employee': employee})


@login_required(login_url='/login')
def leave_approve(request, leave_id):
    instance = get_object_or_404(Leave, id=leave_id)
    instance.status = 'Approved'
    instance.is_approved = True
    instance.save(update_fields=['status', 'is_approved'])
    approved_by_email = Employee.objects.get(user=request.user).email
    employee_email = Employee.objects.get(user=instance.user).email
    html_message = message_composer(request, html_template='reviewed_leave_mail.html', instance_name=instance, result='approved')
    email_sender('Submitted leave reviewed', 'Submitted leave reviewed', approved_by_email, employee_email,
                 html_message)
    return redirect('leave:list_leave')


@login_required(login_url='/login')
def leave_unapprove(request, leave_id):
    instance = get_object_or_404(Leave, id=leave_id)
    instance.status = 'Rejected'
    instance.is_approved = False
    instance.save(update_fields=['status', 'is_approved'])
    approved_by_email = Employee.objects.get(user=request.user).email
    employee_email = Employee.objects.get(user=instance.user).email
    html_message = message_composer(request, html_template='reviewed_leave_mail.html', instance_name=instance, result='rejected')
    email_sender('Submitted leave reviewed', 'Submitted leave reviewed', approved_by_email, employee_email,
                 html_message)
    return redirect('leave:list_leave')


# #############################################################################
@login_required(login_url='/login')
def add_leave_master(request):
    leaves = LeaveMaster.objects.all()
    if request.method == "POST":
        leave_form = FormLeaveMaster(data=request.POST)
        if leave_form.is_valid():
            leave = leave_form.save(commit=False)
            leave.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Leave master was created successfully')
            return redirect('leave:add_leave_master')
        else:
            print(leave_form.errors)
    else:  # http request
        leave_form = FormLeaveMaster()
    return render(request, 'add_leave_master.html', {'leave_form': leave_form, 'leaves': leaves})


@login_required(login_url='/login')
def edit_leave_master(request, id):
    instance = get_object_or_404(LeaveMaster, id=id)
    if request.method == "POST":
        leave_form = FormLeaveMaster(data=request.POST, instance=instance)
        if leave_form.is_valid():
            leave = leave_form.save(commit=False)
            leave.save()
            # sendmail(leave)
            messages.add_message(request, messages.SUCCESS,
                                 'Leave Type was edited successfully')
            return redirect('leave:add_leave_master')
        else:
            print(leave_form.errors)
    else:  # http request
        leave_form = FormLeaveMaster(instance=instance)
    return render(request, 'edit_leave_master.html', {'leave_form': leave_form})


@login_required(login_url='/login')
def del_leave_master(request, id):
    instance = get_object_or_404(LeaveMaster, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Leave Type was deleted successfully')
    return redirect('leave:add_leave_master')
