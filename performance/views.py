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


# gehad : createPerformance
@login_required(login_url='home:user-login')
def createPerformance(request):
    performance_form = PerformanceForm()
    if request.method == 'POST':
        performance_form = PerformanceForm(request.POST)
        if performance_form.is_valid():
            performance_obj = performance_form.save()
            print("created")
            return redirect('performance:rating-create',
                per_id = performance_obj.id)
            
        else:
            print(performance_form.errors) 
            return redirect('home:homepage')
                        
    else:
        myContext = {
        "page_title": _("create performance"),
        "performance_form": performance_form,
    }
    return render(request, 'create-performance.html', myContext)


@login_required(login_url='home:user-login')
def listPerformance(request):
    performances_list = Performance.objects.all()
    context = {
        'page_title': _('User Companies List'),
        'performances_list': performances_list,
    }
    return render(request, 'performance-list.html', context)




@login_required(login_url='home:user-login')
def createPerformanceRating(request,per_id):
    performance_rating_formset = RatingInline(queryset=PerformanceRating.objects.none())
    performance = Performance.objects.get(id=per_id)
    if request.method == 'POST':
        performance_rating_formset = RatingInline(request.POST)
        print(len(performance_rating_formset.forms))
        if performance_rating_formset.is_valid():
            print(len(performance_rating_formset))
            for form in performance_rating_formset:
                obj = form.save(commit=False)
                obj.performance = performance
                obj.save()
                print("created")
            return redirect('home:homepage')
        else:
            print(performance_rating_formset.errors) 
            return redirect('home:homepage')
                        
    else:
        myContext = {
        "page_title": _("create rating"),
        "performance_rating_formset": performance_rating_formset,
    }
    return render(request, 'create-rating.html', myContext)

