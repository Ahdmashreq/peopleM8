import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from leave.models import LeaveMaster, Leave
from notification.models import Notification
from employee.models import JobRoll, Employee
from employee.notification_helper import NotificationHelper
from leave.forms import FormLeave, FormLeaveMaster
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout  # for later
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.core.mail import send_mail
from django.template import loader
import datetime
from datetime import datetime
from django.forms.forms import NON_FIELD_ERRORS
from custom_user.models import User


@login_required(login_url='/login')
def add_leave(request):
    employee = Employee.objects.get(user=request.user)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    if request.method == "POST":
        leave_form = FormLeave(data=request.POST)
        if eligible_user_leave(request.user):
            if leave_form.is_valid():

                leave = leave_form.save(commit=False)
                leave.user = request.user
                leave.save()

                if employee_job.manager:
                    NotificationHelper(employee, employee_job.manager, leave).send_notification()
                requestor = employee
                requestor_email = employee.email
                # leave_type = leave.leavetype
                from_date = leave.startdate
                to_date = leave.enddate
                resume = leave.resume_date
                reason = leave.reason
                team_leader = employee_job.manager
                team_leader_email = employee_job.manager.email

                html_message = loader.render_to_string(
                    'leave_mail.html',
                    {
                        'leave_id': leave.id,
                        'requestor': requestor,
                        'user_name': request.user,
                        'team_leader': employee_job.manager,
                        'subject': 'Mashreq Arabia Leave Form',
                        'date_from': from_date,
                        'date_to': to_date,
                        'date_back': resume,
                        'comments': reason,
                        'no_of_days': (to_date - from_date).days + 1
                    }
                )
                try:
                    send_mail(subject='Applying for a leave',
                              message='Applying for a leave',
                              from_email=requestor_email,
                              recipient_list=[team_leader_email],
                              fail_silently=False,
                              html_message=html_message)
                except Exception as e:
                    print(e)

                messages.add_message(request, messages.SUCCESS,
                                     'Leave Request was created successfully')
                return redirect('leave:list_leave')

            else:
                print(leave_form.errors)
        else:
            leave_form.add_error(None, "You are not eligible for leave request")
    else:  # http request
        leave_form = FormLeave()
    return render(request, 'add_leave.html', {'leave_form': leave_form})


def eligible_user_leave(user):
    now_date = datetime.date(datetime.now())
    leaves = Leave.objects.filter(user=user, status='Approved')
    for leave in leaves:
        if leave.resume_date > now_date >= leave.startdate:
            return False
        else:
            continue
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
def del_leave(request, id):
    instance = get_object_or_404(Leave, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Leave was deleted successfully')
    return redirect('leave:list_leave')


@login_required(login_url='/login')
def edit_leave(request, id):
    instance = get_object_or_404(Leave, id=id)
    leave_form = FormLeave(instance=instance)
    employee = Employee.objects.get(user=instance.user)
    if request.method == "POST":
        leave_form = FormLeave(data=request.POST, instance=instance)
        if leave_form.is_valid():
            leave = leave_form.save(commit=False)
            leave.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Leave request was created successfully')
            return redirect('leave:list_leave')
        else:
            print(leave_form.errors)
    else:  # http request
        leave_form = FormLeave(instance=instance)
    return render(request, 'edit-leave.html', {'leave_form': leave_form, 'leave_id': id, 'employee': employee})


@login_required(login_url='/login')
def leave_approve(request, leave_id):
    instance = get_object_or_404(Leave, id=leave_id)
    instance.status = 'Approved'
    instance.is_approved = True
    instance.save(update_fields=['status', 'is_approved'])
    return redirect('leave:list_leave')


@login_required(login_url='/login')
def leave_unapprove(request, leave_id):
    instance = get_object_or_404(Leave, id=leave_id)
    instance.status = 'Rejected'
    instance.is_approved = False
    instance.save(update_fields=['status', 'is_approved'])
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
