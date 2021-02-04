from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from attendance.models import Attendance
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest
from django.utils import translation
from datetime import date
from django.utils import formats
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language
# Create your views here.


def all_reports(request):
    return render(request,'all_reports.html',{})

# report on people who came in late
def late_report(request):
    late=Attendance.objects.filter(check_in__gt='9:00')

    print(late)
    return render(request,'late_report.html',{'late':late})

def all_people_report(request):
    all_people=Attendance.objects.filter(date=date.today())
    no_people=Attendance.objects.filter(date=date.today()).count()
    return render(request,'all_people_report.html',{'all_people':all_people,'no_people':no_people})
