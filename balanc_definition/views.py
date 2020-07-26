from django.shortcuts import render,get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.db.models import Q
from django.views.generic import ListView
from balanc_definition.models import Cost_Level, Cost_Detail
from django.utils.translation import to_locale, get_language
from balanc_definition.forms import CostLevelForm, CostDetailForm, Cost_detail_inline_form
from django.utils.translation import ugettext_lazy as _

def costAccountList(request):
    list_all = Cost_Detail.objects.all().exclude((Q(end_date__gte=date.today())|Q(end_date__isnull=True)))
    listContext = {
                   "page_title":_("cost accounts"),
                   "list_all":list_all
                   }
    return render(request, 'list-cost-accounts.html', listContext)

def costAccountCreate(request):
    cost_level_form = CostLevelForm()
    cost_det_form = Cost_detail_inline_form(queryset= Cost_Detail.objects.none())
    if request.method == 'POST':
        cost_level_form = CostLevelForm(request.POST)
        cost_det_form = Cost_detail_inline_form(request.POST)
        if cost_level_form.is_valid() and cost_det_form.is_valid():
            master_obj = cost_level_form.save(commit=False)
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            cost_det_form = Cost_detail_inline_form(request.POST, instance= master_obj)
            det_obj = cost_det_form.save(commit=False)
            for obj in det_obj:
                obj.created_by = request.user
                obj.last_update_by = request.user
                obj.save()
    costContext = {
                   "page_title":_( "Create Costing Accounts"),
                   "cost_level_form": cost_level_form,
                   "cost_det_form": cost_det_form,
                   }
    return render(request, 'create-cost-accounts.html', costContext)

def costAccountupdate(request, pk):
    cost_level_obj = get_object_or_404(Cost_Level, pk=pk)
    cost_level_form = CostLevelForm(instance = cost_level_obj)
    cost_det_form = Cost_detail_inline_form(instance = cost_level_obj)
    if request.method == 'POST':
        cost_level_form = CostLevelForm(request.POST, instance = cost_level_obj)
        cost_det_form = Cost_detail_inline_form(request.POST, instance = cost_level_obj)
        if cost_level_form.is_valid() and cost_det_form.is_valid():
            cost_level_form.save()
            for det_obj in cost_det_form:
                det_obj.save()
    costContext = {
                   "page_title": _("Update Costing Accounts"),
                   "cost_level_form": cost_level_form,
                   "cost_det_form": cost_det_form,
                   }
    return render(request, 'create-cost-accounts.html', costContext)

def costAccountdelete(request, pk):
    required_cost = get_object_or_404(Cost_Level, pk=pk)
    try:
        cost_form = CostLevelForm(instance = required_cost)
        cost_obj = cost_form.save(commit=False)
        cost_obj.end_date = date.today()
        cost_obj.save(update_fields=['end_date'])
        if user_lang=='ar':
            user_lang=to_locale(get_language())
            success_msg = '{} تم حذف السجل بنجاح'.format(required_cost)
        else:
            success_msg = '{} was deleted successfully'.format(required_cost)

        messages.success(request, success_msg)
    except Exception as e:
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف'.format(required_cost)
        else:
            error_msg = '{} was deleted successfully'.format(required_cost)


        messages.error(request, error_msg)
        raise e
    return redirect('balanc_definition:list-costing')
