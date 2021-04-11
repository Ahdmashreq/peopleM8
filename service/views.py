from django.shortcuts import render, redirect
from django.http import HttpResponse
from employee.models import Employee, JobRoll
from service.models import Bussiness_Travel, Purchase_Request
from service.forms import FormAllowance, PurchaseRequestForm, Purchase_Item_formset
from django.db.models import Q
from company.models import Department
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout  # for later
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.core.mail import send_mail
from django.template import loader
from datetime import date, datetime


@login_required(login_url='/user_login/')
def services_list(request):
    request_employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    bussiness_travel_list = Bussiness_Travel.objects.filter(emp=request_employee).order_by('-creation_date')
    servicesContext = {
        'services': bussiness_travel_list,
    }
    return render(request, 'list_bussiness_travel.html', servicesContext)


@login_required(login_url='/user_login/')
def services_edit(request, id):
    instance = get_object_or_404(Bussiness_Travel, id=id)
    service_form = FormAllowance(instance=instance)
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    home = False
    if request.method == "POST":
        service_form = FormAllowance(data=request.POST, instance=instance)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.created_by = request.user
            service.last_update_by = request.user
            service.save()
            messages.add_message(request, messages.SUCCESS, 'Service was updated successfully')
            return redirect('service:services_list')
        else:
            print(service_form.errors)
    else:  # http request
        service_form = FormAllowance(instance=instance)
        context = {'service_form': service_form}
        home = True
    return render(request, 'edit_allowance.html',
                  context={'service_form': service_form, 'service_id': id, 'employee': employee, 'home': home})


@login_required(login_url='/user_login/')
def services_update(request, id):
    instance = get_object_or_404(Bussiness_Travel, id=id)
    service_form = FormAllowance(instance=instance)
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    if request.method == "POST":
        service_form = FormAllowance(data=request.POST, instance=instance)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.created_by = request.user
            service.last_update_by = request.user
            service.save()
            messages.add_message(request, messages.SUCCESS, 'Service was updated successfully')
            return redirect('service:services_list')
        else:
            print(service_form.errors)
    else:  # http request
        service_form = FormAllowance(instance=instance)
        context = {'service_form': service_form}
    return render(request, 'add_allowance.html', {'service_form': service_form, 'service_id': id, 'employee': employee})


@login_required(login_url='/user_login/')
def services_delete(request, id):
    instance = get_object_or_404(Bussiness_Travel, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS, 'Service was deleted successfully')
    return redirect('service:services_list')


@login_required(login_url='/user_login/')
def services_create(request):
    flag = False
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    if request.method == "POST":
        service_form = FormAllowance(data=request.POST)
        if service_form.is_valid():
            service_obj = service_form.save(commit=False)
            service_obj.emp = employee
            service_obj.manager = employee_job.manager
            service_obj.position = employee_job.position
            service_obj.department = employee_job.position.department
            service_obj.created_by = request.user
            service_obj.last_update_by = request.user
            service_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Service was created successfully')

            # NotificationHelper(employee, employee_job.manager, service_obj).send_notification()

            return redirect('service:services_list')
        else:
            service_form.errors
    else:  # http request
        service_form = FormAllowance()
    return render(request, 'add_allowance.html', {'service_form': service_form, 'flag': flag})


def send_allowance_notification(request):
    manager = get_object_or_404(Employee, user=request.user.is_authenticated)
    if manager is not None:  # check is signed in user is manager
        pending = Bussiness_Travel.objects.filter(status='pending').order_by('creation_date')
        for request in pending:
            emp = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
        return


@login_required(login_url='home:user-login')
def service_approve(request, service_id,redirect_to):
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    instance = get_object_or_404(Bussiness_Travel, id=service_id)
    instance.status = 'Approved'
    instance.approval = employee
    instance.is_approved = True
    instance.save(update_fields=['status'])
    return redirect(redirect_to)


@login_required(login_url='home:user-login')
def service_unapprove(request, service_id,redirect_to):
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    instance = get_object_or_404(Bussiness_Travel, id=service_id)
    instance.status = 'Rejected'
    instance.is_approved = False
    instance.approval = employee
    instance.save(update_fields=['status'])
    return redirect(redirect_to)


######################################################################################################

@login_required(login_url='/user_login/')
def purchase_request_list(request):
    request_employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    purchase_request_list = Purchase_Request.objects.filter(ordered_by=request_employee).order_by('-creation_date')
    servicesContext = {
        'purchase_request_list': purchase_request_list
    }
    return render(request, 'list_purchase_request.html', servicesContext)


def getOrderSec(n):
    if n < 1:
        return str(1).zfill(5)
    else:
        return str(n + 1).zfill(5)


@login_required(login_url='home:user-login')
def purchase_request_create(request):
    purchase_form = PurchaseRequestForm()
    purchase_form.fields['department'].queryset = Department.objects.filter(
        enterprise=request.user.company).filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    purchase_items_form = Purchase_Item_formset()
    rows_num = Purchase_Request.objects.all().count()
    request_employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=request_employee)
    if request.method == 'POST':
        purchase_form = PurchaseRequestForm(request.POST)
        purchase_items_form = Purchase_Item_formset(request.POST)
        if purchase_form.is_valid() and purchase_items_form.is_valid():
            purchase_obj = purchase_form.save(commit=False)
            purchase_obj.order_number = str(date.today()) + "-" + getOrderSec(rows_num)
            purchase_obj.ordered_by = request_employee
            purchase_obj.created_by = request.user
            purchase_obj.last_update_by = request.user
            purchase_obj.save()
            purchase_items_form = Purchase_Item_formset(request.POST, instance=purchase_obj)
            if purchase_items_form.is_valid():
                purchase_items = purchase_items_form.save(commit=False)
                for item in purchase_items:
                    item.created_by = request.user
                    item.last_update_by = request.user
                    item.save()
            # NotificationHelper(request_employee,employee_job.manager,purchase_obj).send_notification()
            messages.success(request, 'Purchase Request was created successfully')
            return redirect('service:purchase-request-list')
        else:
            messages.error(request, 'Purchase Request was not created')

    purchaseContext = {
        'purchase_form': purchase_form,
        'purchase_items_form': purchase_items_form,

    }
    return render(request, 'create-purchase-order.html', purchaseContext)


@login_required(login_url='home:user-login')
def purchase_request_update(request, id):
    required_request = Purchase_Request.objects.get(pk=id)
    purchase_form = PurchaseRequestForm(instance=required_request)
    purchase_items_form = Purchase_Item_formset(instance=required_request)
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    if request.method == 'POST':
        purchase_form = PurchaseRequestForm(request.POST)
        purchase_items_form = Purchase_Item_formset(request.POST)
        if purchase_form.is_valid() and purchase_items_form.is_valid():
            purchase_obj = purchase_form.save(commit=False)
            purchase_obj.save()
            purchase_items_form = Purchase_Item_formset(request.POST, instance=purchase_obj)
            if purchase_items_form.is_valid():
                purchase_items = purchase_items_form.save(commit=False)
                for item in purchase_items:
                    item.save()
            messages.success(request, 'Purchase Request was updated successfully')
        else:
            messages.error(request, 'Purchase Request was not updated')
    purchaseContext = {
        'purchase_form': purchase_form,
        'purchase_items_form': purchase_items_form,
        'order_id': id
    }
    return render(request, 'edit_purchase_request.html', purchaseContext)


@login_required(login_url='home:user-login')
def purchase_request_approve(request, order_id):
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    instance = Purchase_Request.objects.get(pk=order_id)
    instance.status = 'Approved'
    instance.approval = employee
    # instance.is_approved = True
    instance.save(update_fields=['status'])
    return redirect('home:homepage')


@login_required(login_url='home:user-login')
def purchase_request_unapprove(request, order_id):
    employee = Employee.objects.get(user=request.user, emp_end_date__isnull=True)
    instance = Purchase_Request.objects.get(pk=order_id)
    instance.status = 'Rejected'
    instance.approval = employee
    # instance.is_approved = False
    instance.save(update_fields=['status'])
    return redirect('home:homepage')
