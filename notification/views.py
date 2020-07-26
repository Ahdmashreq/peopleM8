from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import FormNotificationLeave
from notification.models import Notification
from employee.models import Employee, JobRoll
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest
from django.utils import translation
from datetime import date
from django.utils import formats
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language

# Create your views here.
@login_required(login_url='/login')
def list_notification(request):
    employee = Employee.objects.get(user=request.user)
    employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=employee)
    is_manager = False
    if employee_job.manager == None:       #check if the loged in user is a manager
        unread_notifications=Notification.objects.filter(status = 'delivered').order_by('-creation_date')
        is_manager = True
    else:
        #here if the employee is NOT a manager, he'll only view notifications sent to him.
        unread_notifications=Notification.objects.filter(status = 'delivered', to_emp=employee).order_by('-creation_date')
        is_manager = False

    return render(request, 'list_notification.html',{'notifications':unread_notifications,})

@login_required(login_url='/login')
def clear_all(request):
    for x in Notification.objects.all():
        x.delete()
    return redirect('notification:list_notification')

@login_required(login_url='/login')
def change_status(request,id):
    notification = Notification.objects.get(id=id)
    notification.status = 'read'
    notification.save()
    return redirect('notification:list_notification')
