import os
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from leave.check_manager import Check_Manager
from leave.check_balance import Check_Balance
from employee.models import JobRoll, Employee
from leave.models import LeaveMaster, Leave, Employee_Leave_balance
from leave.forms import FormLeave, FormLeaveMaster, Leave_Balance_Form
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template import loader
import datetime
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from custom_user.models import User
from django.http import JsonResponse


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
    employee = Employee.objects.get(user=instance_name.user)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    reviewed_by = employee_job.manager
    from_date = instance_name.startdate
    to_date = instance_name.enddate
    resume = instance_name.resume_date
    reason = instance_name.reason
    html_message = loader.render_to_string(
        html_template,
        {
            'leave_id': instance_name.id,
            'result': result,
            'requestor': employee,
            'user_name': instance_name.user,
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


@login_required(login_url='home:user-login')
def add_leave(request):
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    employee_leave_balance = Employee_Leave_balance.objects.get(
        employee=employee)

    total_balance = employee_leave_balance.total_balance
    absence_days = employee_leave_balance.absence
    # print(have_leave_balance(request.user))
    if request.method == "POST":
        leave_form = FormLeave(data=request.POST, form_type=None)
        if eligible_user_leave(request.user):
            if leave_form.is_valid():
                if valid_leave(request.user, leave_form.cleaned_data['startdate'], leave_form.cleaned_data['enddate']):
                    leave = leave_form.save(commit=False)
                    leave.user = request.user
                    required_employee = Employee.objects.get(user=request.user)
                    # check_validate_balance=Employee_Leave_balance.check_balance(
                    # required_employee, leave_form.data['startdate'], leave_form.data['enddate'])
                    # if check_validate_balance:
                    leave.save()
                    team_leader_email = []
                    check_manager = Check_Manager.check_manger(
                        required_employee)
                    for manager in check_manager:
                        team_leader_email.append(manager.user.email)

                        # if employee_job.manager:
                        #     NotificationHelper(
                        #         employee, employee_job.manager, leave).send_notification()
                    requestor_email = employee.email

                    # print(team_leader_email)
                    html_message = message_composer(request, html_template='leave_mail.html', instance_name=leave,
                                                    result=None)
                    email_sender('Applying for a leave', 'Applying for a leave', requestor_email,
                                 team_leader_email, html_message)

                    messages.add_message(request, messages.SUCCESS,
                                         'Leave Request was created successfully')
                    return redirect('leave:list_leave')
                else:
                    leave_form.add_error(
                        None, "Requested leave intersects with another leave")
            else:
                print(leave_form.errors)
        else:
            leave_form.add_error(
                None, "You are not eligible for leave request")
    else:  # http request
        leave_form = FormLeave(form_type=None)
    return render(request, 'add_leave.html',
                  {'leave_form': leave_form, 'total_balance': total_balance, 'absence_days': absence_days})


def eligible_user_leave(user):
    now_date = datetime.date(datetime.now())
    leaves = Leave.objects.filter(user=user, status='Approved')
    for leave in leaves:
        if leave.enddate >= now_date >= leave.startdate:
            return False
        else:
            continue
    return True


def have_leave_balance(user):
    required_user = Employee.objects.get(user=user.id)
    employee_leave_balance = Employee_Leave_balance.objects.get(
        employee=required_user)
    total_balance = employee_leave_balance.total_balance
    if not total_balance > 0:
        return False
    return True


def valid_leave(user, req_startdate, req_enddate):
    leaves = Leave.objects.filter(user=user, status='Approved').order_by('-id')
    for leave in leaves[0:3]:
        if leave.enddate >= req_startdate >= leave.startdate or \
                req_enddate >= leave.startdate >= req_startdate:
            return False
    return True


# #############################################################################

@login_required(login_url='home:user-login')
def list_leave(request):
    is_manager = False
    try:
        employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
        employee_job = JobRoll.objects.get(
            end_date__isnull=True, emp_id=employee)
        if employee_job.manager == None:  # check if the loged in user is a manager
            list_leaves = Leave.objects.all_pending_leaves()
            is_manager = True
        else:
            list_leaves = Leave.objects.filter(user=request.user)
            is_manager = False
    except JobRoll.DoesNotExist:
        list_leaves = []
    except Employee.DoesNotExist:
        list_leaves = []

    return render(request, 'list_leave.html', {'leaves': list_leaves, 'is_manager': is_manager})


@login_required(login_url='home:user-login')
def delete_leave_view(request, id):
    instance = get_object_or_404(Leave, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Leave was deleted successfully')
    return redirect('leave:list_leave')


@login_required(login_url='home:user-login')
def edit_leave(request, id):
    instance = get_object_or_404(Leave, id=id)
    employee = Employee.objects.get(user=instance.user,  emp_end_date__isnull=True)
    home = False  # a variable indicating whether the request is from homepage or other link
    if request.method == "POST":
        leave_form = FormLeave(
            data=request.POST, form_type='respond', instance=instance)
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
        home = True  # only person who will approve could see the leave after its creation,and this is only avalaible
        # from homepage
    return render(request, 'edit-leave.html',
                  context={'leave_form': leave_form, 'leave_id': id, 'employee': employee, 'home': home, })


@login_required(login_url='home:user-login')
def leave_approve(request, leave_id, redirect_to):
    """
     :params:
         redirect_to : a string representing the redirection link name ex:'home:homepage'
     """
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    instance = get_object_or_404(Leave, id=leave_id)
    instance.status = 'Approved'
    instance.is_approved = True
    instance.approval = employee
    instance.save(update_fields=['status', 'is_approved'])
    startdate = instance.startdate
    enddate = instance.enddate
    dates = (enddate - startdate)
    tottal_days = dates.days + 1
    user = instance.user

    required_employee = Employee.objects.get(user=user,emp_end_date__isnull=True)
    required_user = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    employee_leave_balance = Employee_Leave_balance.objects.get(
        employee=required_user)
    leave_form = FormLeave(data=request.POST, form_type=None)
    #print(leave_form.data['startdate'])
    check_validate_balance=Check_Balance.check_balance(
                    required_employee, startdate, enddate,leave_id)
    approved_by_email = Employee.objects.get(user=request.user, emp_end_date__isnull=True).email
    employee_email = Employee.objects.get(user=request.user, emp_end_date__isnull=True).email
    html_message = message_composer(request, html_template='reviewed_leave_mail.html', instance_name=instance,
                                    result='approved')
    email_sender('Submitted leave reviewed', 'Submitted leave reviewed', approved_by_email, employee_email,
                 html_message)
    return redirect(redirect_to)


@login_required(login_url='home:user-login')
def leave_unapprove(request, leave_id, redirect_to):
    """
    :params:
        redirect_to : a string representing the redirection link name ex:'home:homepage'
    """
    instance = get_object_or_404(Leave, id=leave_id)
    instance.status = 'Rejected'
    instance.is_approved = False
    instance.save(update_fields=['status', 'is_approved'])
    approved_by_email = Employee.objects.get(user=request.user, emp_end_date__isnull=True).email
    employee_email = Employee.objects.get(user=request.user, emp_end_date__isnull=True).email
    html_message = message_composer(request, html_template='reviewed_leave_mail.html', instance_name=instance,
                                    result='rejected')
    email_sender('Submitted leave reviewed', 'Submitted leave reviewed', approved_by_email, employee_email,
                 html_message)
    return redirect(redirect_to)


# #############################################################################
@login_required(login_url='home:user-login')
def list_leave_master(request):
    leave_master_list = LeaveMaster.objects.filter(
        enterprise=request.user.company)
    return render(request, 'list_leave_master.html', {'leave_master_list': leave_master_list})


@login_required(login_url='home:user-login')
def add_leave_master(request):
    leaves = LeaveMaster.objects.all()
    if request.method == "POST":
        leave_form = FormLeaveMaster(data=request.POST)
        if leave_form.is_valid():
            leave_obj = leave_form.save(commit=False)
            leave_obj.enterprise = request.user.company
            leave_obj.created_by = request.user
            leave_obj.save()
            messages.add_message(request, messages.SUCCESS,
                                 _('Leave master was created successfully'))
            if 'save_and_exit' in request.POST:
                return redirect('leave:list-leave-master')
            else:
                return redirect('leave:add_leave_master')
        else:
            print(leave_form.errors)
    else:  # http request
        leave_form = FormLeaveMaster()
    return render(request, 'create_leave_master.html', {'leave_form': leave_form, 'leaves': leaves})


@login_required(login_url='home:user-login')
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
    return render(request, 'create_leave_master.html', {'leave_form': leave_form})


@login_required(login_url='home:user-login')
def del_leave_master(request, id):
    instance = get_object_or_404(LeaveMaster, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Leave Type was deleted successfully')
    return redirect('leave:add_leave_master')


class Elmplyees_Leave_Balance(ListView):
    model = Employee_Leave_balance
    context_object_name = 'employee_leave_balance_list'
    template_name = 'leave_balance_list.html'


@login_required(login_url='home:user-login')
def create_employee_leave_balance(request):
    leave_balance_form = Leave_Balance_Form(request.user)
    if request.method == 'POST':
        leave_balance_form = Leave_Balance_Form(request.user, request.POST)
        if leave_balance_form.is_valid():
            balance_obj = leave_balance_form.save(commit=False)
            balance_obj.created_by = request.user
            balance_obj.absence = 0
            balance_obj.save()
            messages.success(request, _('Balance Saved Successfully'))
            return redirect('leave:leave-balance')
        else:
            messages.error(request, leave_balance_form.errors)
    leave_balance_context = {
        'leave_balance_form': leave_balance_form,
    }
    return render(request, 'leave_balance_create.html', leave_balance_context)


@login_required(login_url='home:user-login')
def view_employee_leaves_list(request, employee_id):
    employee = Employee.objects.get(id=employee_id, emp_end_date__isnull=True)
    list_leaves = Leave.objects.filter(user=employee.user)
    leave_balance_context = {
        'list_leaves': list_leaves,
        'employee': employee,
    }
    return render(request, 'list_leave_by_employee.html', leave_balance_context)


@login_required(login_url='home:user-login')
def edit_employee_leaves_balance(request, leave_balance_id):
    """
    edit employee leaves balance
    """
    employee_leave_balance_instance = Employee_Leave_balance.objects.get(id=leave_balance_id)
    if request.method == 'POST':
        print(request.POST)
        leave_balance_form = Leave_Balance_Form(request.user, request.POST,
                                                instance=employee_leave_balance_instance)
        if leave_balance_form.is_valid():
            balance_edited_obj = leave_balance_form.save(commit=False)
            balance_edited_obj.last_update_by = request.user
            balance_edited_obj.save()
            messages.success(request, _('Balance Updated Successfully'))
            return redirect('leave:leave-balance')
        else:
            print('error: ', leave_balance_form.errors)
            messages.error(request, leave_balance_form.errors)

    else:
        leave_balance_form = Leave_Balance_Form(user_v=request.user, instance=employee_leave_balance_instance)

    leave_balance_context = {
        'leave_balance_form': leave_balance_form,
    }
    return render(request, 'leave_balance_create.html', leave_balance_context)


@login_required(login_url='home:user-login')
def delete_leave_balance(request, leave_balance_id):
    """
    delete leave balance record
    """
    employee_leave_balance_instance = Employee_Leave_balance.objects.get(id=leave_balance_id)
    employee_leave_balance_instance.delete()
    messages.add_message(request, messages.SUCCESS,
                         _('Leave Balance was deleted successfully'))
    return redirect('leave:leave-balance')


def get_leave_type(request):
    """
    get leave value to be returned through ajax request
    """
    leave_type_id = request.META.get('QUERY_STRING')[request.META.get('QUERY_STRING').index('=')+1:] # +1 to exclude =
    leave_value = LeaveMaster.objects.get(id=leave_type_id).leave_value
    print(leave_value)
    return JsonResponse({'leave_value':leave_value})
