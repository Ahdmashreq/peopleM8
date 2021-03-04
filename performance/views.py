from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db import IntegrityError
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q
from company.models import *


# Create your views here.
@login_required(login_url='home:user-login')
def createPerformance(request):
    performance_form = PerformanceForm()
    if request.method == 'POST':
        performance_form = PerformanceForm(request.POST)
        if performance_form.is_valid():
            performance_form.save()
            print("created")
            return redirect('home:homepage')
            
        else:
            print(performance_form.errors) 
            return redirect('home:homepage')
                        
    else:
        myContext = {
        "page_title": _("create performance"),
        "performance_form": performance_form,
    }
    return render(request, 'create-performance.html', myContext)


   