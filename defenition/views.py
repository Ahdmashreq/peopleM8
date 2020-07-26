from django.shortcuts import render, get_object_or_404, reverse, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.management import call_command
from defenition.forms import LookupTypeForm, LookupDetinlineFormSet, InsuranceRuleForm, TaxRuleForm, TaxSectionFormSet
from defenition.models import LookupType, LookupDet, TaxRule, InsuranceRule, TaxSection
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language


###############################################################################
def copy_insurance_rule(request):
    insurance_obj = InsuranceRule(
                         enterprise_name = request.user.company,
                         name = 'قانون التأمينات المصري',
                         basic_deduction_percentage = 14,
                         variable_deduction_percentage = 11,
                         maximum_insurable_basic_salary = 1250,
                         maximum_insurable_variable_salary = 1650,
                         start_date =  date.today(),
                         created_by =  request.user,
                         creation_date =  date.today(),
                         last_update_date = date.today()
    )
    insurance_obj.save()
    return redirect('defenition:insurance-list')

def copy_tax_rule(request):
    tax_obj = TaxRule(
                     enterprise = request.user.company,
                     name = "قانون الضرائب المصري",
                     personal_exemption = 7200.0,
                     round_down_to_nearest_10 = True,
                     start_date =  date.today(),
                     created_by =  request.user,
                     creation_date =  date.today(),
                     last_update_date = date.today()
    )
    tax_obj.save()
    tax_rule_id = TaxRule.objects.get(enterprise = request.user.company)
    first_section  = TaxSection(
                     name = "الشريحة الاولي",
                     tax_rule_id = tax_rule_id,
                     salary_from = 0,
                     salary_to = 7200,
                     tax_percentage =0,
                     tax_discount_percentage = 0,
                     section_execution_sequence = 1,
                     start_date =  date.today(),
                     created_by =  request.user,
                     creation_date =  date.today(),
                     last_update_date = date.today()
    )
    second_section = TaxSection(
                     name = "الشريحة الثانية",
                     tax_rule_id = tax_rule_id,
                     salary_from = 7201,
                     salary_to = 30000,
                     tax_percentage = 10,
                     tax_discount_percentage = 80,
                     section_execution_sequence = 2,
                     start_date =  date.today(),
                     created_by =  request.user,
                     creation_date =  date.today(),
                     last_update_date = date.today()
    )
    thired_section = TaxSection(
                     name = "الشريحة الثالثة",
                     tax_rule_id = tax_rule_id,
                     salary_from = 30001,
                     salary_to = 45000,
                     tax_percentage = 15,
                     tax_discount_percentage = 40,
                     section_execution_sequence = 3,
                     start_date =  date.today(),
                     created_by =  request.user,
                     creation_date =  date.today(),
                     last_update_date = date.today()
    )
    forth_section  = TaxSection(
                     name = "الشريحة الرابعة",
                     tax_rule_id = tax_rule_id,
                     salary_from = 45001,
                     salary_to = 200000,
                     tax_percentage = 20,
                     tax_discount_percentage = 5,
                     section_execution_sequence = 4,
                     start_date =  date.today(),
                     created_by =  request.user,
                     creation_date =  date.today(),
                     last_update_date = date.today()
    )
    fifth_section  = TaxSection(
                     name = "الشريحة الخامسة",
                     tax_rule_id = tax_rule_id,
                     salary_from = 200001,
                     salary_to = 10000000,
                     tax_percentage =22.5,
                     tax_discount_percentage = 0,
                     section_execution_sequence = 5,
                     start_date =  date.today(),
                     created_by =  request.user,
                     creation_date =  date.today(),
                     last_update_date = date.today()
    )


    TaxSection.objects.bulk_create([first_section, second_section, thired_section, forth_section, fifth_section ])
    return redirect('defenition:tax-list')
###############################################################################

@login_required(login_url='/login')
def listLookupView(request):
    lookup_list = LookupType.objects.all(user=request.user)
    lookupContext = {
                     'page_title':_("Lookup list"),
                     'lookup_list': lookup_list}
    return render(request, 'lookups-list.html', lookupContext)


@login_required(login_url='/login')
def createLookupView(request):
    lookup_master_form = LookupTypeForm()
    lookup_det_form = LookupDetinlineFormSet()
    if request.method == 'POST':
        lookup_master_form = LookupTypeForm(request.POST)
        lookup_det_form = LookupDetinlineFormSet(request.POST)
        if lookup_master_form.is_valid() and lookup_det_form.is_valid():
            master_obj = lookup_master_form.save(commit=False)
            master_obj.enterprise = request.user.company
            master_obj.created_by = request.user
            master_obj.save()
            lookup_det_form = LookupDetinlineFormSet(
                request.POST, instance=master_obj)
            if lookup_det_form.is_valid():
                lookup_det_obj = lookup_det_form.save(commit=False)
                for obj in lookup_det_obj:
                    obj.created_by = request.user
                    obj.last_update_by = request.user
                    obj.save()
            return redirect('defenition:list-lookups')
        else:
            messages.error(request, lookup_master_form.errors)
            messages.error(request, lookup_det_form.errors.value() )
    lookupContext = {
        "page_title": _("Create new lookup"),
        'lookup_master_form': lookup_master_form,
        'lookup_det_form': lookup_det_form
    }
    return render(request, 'lookup-create.html', lookupContext)


@login_required(login_url='/login')
def updateLookupView(request, pk):
    required_lookupType = LookupType.objects.get_lookup(user=request.user, lookup_id=pk)
    lookup_master_form = LookupTypeForm(instance=required_lookupType)
    lookup_det_form = LookupDetinlineFormSet(instance=required_lookupType)
    if request.method == 'POST':
        lookup_master_form = LookupTypeForm(
            request.POST, instance=required_lookupType)
        lookup_det_form = LookupDetinlineFormSet(
            request.POST, instance=required_lookupType)
        if lookup_master_form.is_valid() and lookup_det_form.is_valid():
            lookup_master_form.save()
            lookup_det_obj = lookup_det_form.save(commit=False)
            for obj in lookup_det_obj:
                obj.last_update_by = request.user
                obj.save()
            return redirect('defenition:list-lookups')
        else:
            messages.error(request, lookup_master_form.errors)
            messages.error(request, lookup_det_form.errors)
    lookupContext = {
        "page_title": _("Update lookup"),
        'lookup_master_form': lookup_master_form,
        'lookup_det_form': lookup_det_form
    }
    return render(request, 'lookup-create.html', lookupContext)


@login_required(login_url='/login')
def deleteLookupView(request, pk):
    required_lookupType = LookupType.objects.get_lookup(user=request.user, lookup_id=pk)
    try:
        lookup_type_form = LookupTypeForm(instance=required_lookupType)
        lookup_type_obj = lookup_type_form.save(commit=False)
        lookup_type_obj.end_date = date.today()
        lookup_det_form = LookupDetinlineFormSet(instance=required_lookupType)
        lookup_det_obj = lookup_det_form.save(commit=False)
        for x in lookup_det_obj:
            x.end_date = date.today()
            x.save(update_fields=['end_date'])
        lookup_type_obj.save(update_fields=['end_date'])
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{} تم حذف'.format(required_lookupType)
        else:
            success_msg = '{} was deleted successfully'.format(required_lookupType)
        # success_msg = '{} was deleted successfully'.format(required_lookupType)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف'.format(required_lookupType)
        else:
            error_msg = '{} was deleted successfully'.format(required_lookupType)
        # error_msg = '{} cannot be deleted '.format(required_lookupType)
        messages.error(request, error_msg)
        raise e
    return redirect('defenition:list-lookups')

################################################################################
@login_required(login_url='/login')
def create_insurance_rules(request):
    insurance_form = InsuranceRuleForm()
    if request.method == "POST":
        insurance_form = InsuranceRuleForm(request.POST)
        if insurance_form.is_valid():
            insurance_rule = insurance_form.save(commit=False)
            insurance_rule.created_by = request.user
            insurance_rule.last_update_by = request.user
            insurance_rule.save()
            user_lang=to_locale(get_language())
            if user_lang=='ar':
                success_msg ='تم انشاء {} '.format(
                    insurance_rule.name)
            else:
                success_msg = 'Rule {} created successfully'.format(
                    insurance_rule.name)
            messages.success(request, success_msg)
            return redirect('defenition:insurance-list')
        else:  # Form was not valid
            # Spitting the errors coming from the form
            [messages.error(request, error[0])
             for error in form.errors.values()]
    context = {
        'page_title': _('Create Insurance Rule'),
        'insurance_form': insurance_form
    }
    return render(request, 'insurance_rules_create.html', context=context)


@login_required(login_url='/login')
def list_insurance_rules(request):
    insurance_form = InsuranceRule.objects.all(user=request.user)
    egy_rule_flag = False
    print(InsuranceRule.objects.filter(enterprise_name = request.user.company))
    if InsuranceRule.objects.filter(enterprise_name = request.user.company):
        egy_rule_flag = True
    else:
        egy_rule_flag = False
    print(egy_rule_flag)
    insuranceContext = {
        'page_title': _('Insurance Rules'),
        'insurance_form': insurance_form,
        'egy_rule_flag':egy_rule_flag,
    }
    return render(request, 'insurance_rules_list.html', insuranceContext)

@login_required(login_url='/login')
def update_insurance_rule(request, pk):
    try:
        insurance_rule = InsuranceRule.objects.get_insuracne(user=request.user, insuracne_id=pk)
        if request.method == 'POST':
            insurance_form = InsuranceRuleForm(
                request.POST, instance=insurance_rule)
            if insurance_form.is_valid():
                obj = insurance_form.save(commit=False)
                obj.created_by = request.user
                obj.last_update_by = request.user
                obj.save()
                success_msg = 'تم تعديل "{}" بنجاح'.format(insurance_rule.name)
                insurance_rule = insurance_form.save()
                user_lang=to_locale(get_language())
                if user_lang=='ar':
                    success_msg = 'تم تعديل "{}" بنجاح'.format(insurance_rule.name)
                else:
                    success_msg = 'Record is Updated"{}" '.format(insurance_rule.name)
                # success_msg = 'تم تعديل "{}" بنجاح'.format(insurance_rule.name)
                messages.success(request, success_msg)
            else:  # Form was not valid
                # Spitting the errors coming from the form
                [messages.error(request, error[0])
                 for error in form.errors.values()]
        else:  # request method is GET
            insurance_form = InsuranceRuleForm(instance=insurance_rule)
            modal_close_url = 'payroll:insurance_rules_list'
            context = {'page_title': _('Update Rule'),
                       'insurance_form': insurance_form}
            return render(request, 'insurance_rules_create.html', context=context)
    except:
        error_msg = 'Object cannot be found!!'
        messages.error(request, error_msg)
    return redirect('defenition:insurance-list')


@login_required(login_url='/login')
def delete_insurance_rule(request, pk):
    insurance_rule =  InsuranceRule.objects.get_insuracne(user=request.user, insuracne_id=pk)
    try:
        insurance_form = InsuranceRuleForm(instance=insurance_rule)
        insurance_obj = insurance_form.save(commit=False)
        insurance_obj.end_date = date.today()
        insurance_obj.save(update_fields=['end_date'])
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{} تم حذف'.format(insurance_rule)
        else:
            success_msg = '{} was deleted successfully'.format(insurance_rule)
        # success_msg = '{} was deleted successfully'.format(insurance_rule)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف '.format(insurance_rule)
        else:
            error_msg = '{} cannot be deleted '.format(insurance_rule)
        # error_msg = '{} cannot be deleted '.format(insurance_rule)
        messages.error(request, error_msg)
        raise e
    return redirect('defenition:insurance-list')

################################################################################
#     what if we want to run django command from html we use the next
################################################################################
def runningManagementCommand(request):
    command = 'python manage.py cities_light'  # compile the cities_light library
    call_command('cities_light')
    # call_command('migrate')
    return render(request, 'insurance_rules_create.html', context=None)
################################################################################
#                               Tax section
################################################################################

@login_required(login_url='/login')
def create_tax_rules(request):
    form = TaxRuleForm()
    formset = TaxSectionFormSet()
    if request.method == "POST":
        form = TaxRuleForm(request.POST)
        formset = TaxSectionFormSet(request.POST)
        formset.can_delete = False
        if form.is_valid():
            tax_rule = form.save(commit=False)
            formset = TaxSectionFormSet(request.POST, instance=tax_rule)
            # formset.can_delete = False
            if formset.is_valid():
                tax_rule.save()
                formset.save()
                user_lang=to_locale(get_language())
                if user_lang=='ar':
                    success_msg = 'تم اضافة "{}" بنجاح'.format(tax_rule.name)
                else:
                    success_msg ='Record Created successfully "{}" '.format(tax_rule.name)
                # success_msg = 'تم اضافة "{}" بنجاح'.format(tax_rule.name)
                messages.success(request, success_msg)
                return redirect('defenition:tax-list')
            else:  # formset was not valid
                for error_dict in formset.errors:
                    [messages.error(request, error[0])
                     for error in error_dict.values()]
        else:  # Form was not valid
            [messages.error(request, error[0])
             for error in form.errors.values()]

    context = {'form': form,
               'formset': formset,
               'page_title': _('New Tax Rule'),
               'formset_title': 'Tax sections'}
    return render(request, 'tax_rules_create.html', context=context)


@login_required(login_url='/login')
def list_tax_rules(request):
    form = TaxRule.objects.all(user=request.user)
    formset = TaxSection.objects.all().exclude((Q(end_date__gte=date.today())|Q(end_date__isnull=True)))
    egy_rule_flag = False
    if TaxRule.objects.filter(enterprise = request.user.company).exclude((Q(end_date__gte=date.today())|Q(end_date__isnull=True))):
        egy_rule_flag = True
    else:
        egy_rule_flag = False
    taxContext = {
                  'page_title':_( 'Tax Rules'),
                  'form': form,
                  'formset': formset,
                  'egy_rule_flag':egy_rule_flag
                  }
    return render(request, 'tax_rules_list.html', taxContext)


@login_required(login_url='/login')
def delete_tax_rule(request, pk):
    required_tax_rule =  TaxRule.objects.get_tax(user=request.user, tax_id=pk)
    try:
        tax_form = TaxRuleForm(instance=required_tax_rule)
        tax_obj = tax_form.save(commit=False)
        tax_obj.end_date = date.today()
        tax_section_form = TaxSectionFormSet(instance=required_tax_rule)
        tax_section_obj = tax_section_form.save(commit=False)
        for x in tax_section_obj:
            x.end_date = date.today()
            x.save(update_fields=['end_date'])
        tax_obj.save(update_fields=['end_date'])
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            success_msg = '{}تم حذف '.format(required_tax_rule)
        else:
            success_msg = '{} was deleted successfully'.format(required_tax_rule)
        # success_msg = '{} was deleted successfully'.format(required_tax_rule)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang=to_locale(get_language())
        if user_lang=='ar':
            error_msg = '{} لم يتم حذف'.format(required_tax_rule)
        else:
            error_msg = '{} Can not be delete'.format(required_tax_rule)
        # error_msg = '{} cannot be deleted '.format(required_tax_rule)
        messages.error(request, error_msg)
        raise e
    return redirect('payroll:tax-list')


@login_required(login_url='/login')
def update_tax_rule(request, pk):
    tax_rule_obj = TaxRule.objects.get_tax(user=request.user, tax_id=pk)
    form = TaxRuleForm(instance=tax_rule_obj)
    formset = TaxSectionFormSet(instance=tax_rule_obj)
    if request.method == "POST":
        form = TaxRuleForm(request.POST, instance=tax_rule_obj)
        formset = TaxSectionFormSet(request.POST, instance=tax_rule_obj)
        formset.can_delete = False
        if form.is_valid():
            tax_rule = form.save(commit=False)
            formset = TaxSectionFormSet(request.POST, instance=tax_rule)
            formset.can_delete = False
            if formset.is_valid():
                tax_rule.save()
                formset.save()
                user_lang=to_locale(get_language())
                if user_lang=='ar':
                    uccess_msg = 'تم اضافة "{}" بنجاح'.format(tax_rule.name)
                else:
                    success_msg = 'Record Created Sucessfully"{}" '.format(tax_rule.name)
                # success_msg = 'تم اضافة "{}" بنجاح'.format(tax_rule.name)
                messages.success(request, success_msg)
                # Emptying the form and formset before rerendering them back
                form = TaxRuleForm()
                formset = TaxSectionFormSet()
                formset.can_delete = False
            else:  # formset was not valid
                for error_dict in formset.errors:
                    [messages.error(request, error[0])
                     for error in error_dict.values()]
        else:  # Form was not valid
            # Spitting the errors coming from the form
            [messages.error(request, error[0])
             for error in form.errors.values()]

    context = {'form': form,
               'formset': formset,
               'page_title': _('New Tax Rule'),
               'formset_title': _('Tax sections')}
    return render(request, 'tax_rules_create.html', context=context)
