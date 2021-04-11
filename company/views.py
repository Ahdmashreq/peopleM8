from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from custom_user.models import User, UserCompany
from company.forms import (EnterpriseForm, DepartmentInline, DepartmentForm, JobInline,
                           JobForm, GradeInline, GradeForm, PositionInline, PositionForm, WorkingDaysForm,
                           WorkingHoursDeductionForm, Working_Hours_Deduction_Form_Inline,
                           YearlyHolidayInline, YearlyHolidayForm, YearForm, CompanySetupForm)
from company.models import (Enterprise, Department, Job, Grade, Position, YearlyHoliday,
                            Working_Days_Policy, Working_Hours_Deductions_Policy, Year)
from django.utils.translation import ugettext_lazy as _
from cities_light.models import City, Country
from django.core.exceptions import ObjectDoesNotExist
from tablib import Dataset
from .resources_two import *

########################################Enterprise views###################################################################
from defenition.models import TaxRule, Tax_Sections, LookupType, LookupDet
from company.utils import DatabaseLoader



def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def list_user_companies_view(request):
    user_companies = UserCompany.objects.filter(user=request.user)
    userCompanyContext = {
        'page_title': _('User Companies List'),
        'user_companies': user_companies,
    }
    return render(request, 'user-companies-list.html', userCompanyContext)


def deactivate_company(user_v, new_active_company):
    try:
        old_active_company = UserCompany.objects.get(user=user_v, active=True)
        old_active_company.active = False
        old_active_company.save(update_fields=['active'])
        update_user_company = User.objects.get(id=user_v.id)
        new_company = Enterprise.objects.get(id=new_active_company)
        update_user_company.company = new_company
        update_user_company.save(update_fields=['company'])
        return True
    except ObjectDoesNotExist as e:
        return False
        messages.error(request, _('Company Does Not Exist'))


@login_required(login_url='home:user-login')
def mark_as_active_view(request, company_id):
    success_flag = deactivate_company(request.user, company_id)
    required_company = UserCompany.objects.get(company=company_id)
    required_company.active = True
    required_company.last_update_by = request.user
    required_company.save(update_fields=['active', 'last_update_by'])
    if success_flag:
        return redirect('home:homepage')
    else:
        messages.error(request, _('Something went wrong'))
        return redirect('company:user-companies-list')


@login_required(login_url='home:user-login')
def create_user_companies_view(request):
    bgForm = EnterpriseForm()
    current_user_obj = User.objects.get(id=request.user.id)
    if request.method == "POST":
        bgForm = EnterpriseForm(request.POST)
        if bgForm.is_valid():
            bg_obj = bgForm.save(commit=False)
            bg_obj.enterprise_user = request.user
            bg_obj.created_by = request.user
            bg_obj.save()
            current_user_obj.company = bg_obj
            current_user_obj.save(update_fields=['company', ])
            user_company_count = UserCompany.objects.filter(user=request.user).count()
            user_co = UserCompany(
                user=request.user,
                company=bg_obj,
                active=False if user_company_count >= 1 else True,
                created_by=request.user
            )
            user_co.save()
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم الانشاء بنجاح'
            else:
                success_msg = 'Create Successfully'

            messages.success(request, success_msg)

            if 'Save and exit' in request.POST:
                return redirect('company:user-companies-list')
            elif 'Save and add' in request.POST:
                return redirect('company:user-companies-create')

        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, bgForm.errors)]
    userCompanyContext = {
        'page_title': _('Create Enterprise'),
        'bgForm': bgForm,
    }
    return render(request, 'user-companies-create.html', userCompanyContext)


@login_required(login_url='home:user-login')
def companyCreateView(request):
    bgForm = EnterpriseForm()
    current_user_obj = User.objects.get(id=request.user.id)
    if request.method == "POST":
        bgForm = EnterpriseForm(request.POST)
        if bgForm.is_valid():
            bg_obj = bgForm.save(commit=False)
            bg_obj.enterprise_user = request.user
            bg_obj.created_by = request.user
            bg_obj.last_update_by = request.user
            bg_obj.save()
            current_user_obj.company = bg_obj
            current_user_obj.save()
            return redirect('company:list-company-information')

            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم الانشاء بنجاح'
            else:
                success_msg = 'Create Successfully'

            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, bgForm.errors)]
    myContext = {
        'page_title': _('Create Enterprise'),
        'bgForm': bgForm,
    }
    return render(request, 'company-create.html', myContext)


@login_required(login_url='home:user-login')
def listCompanyInformation(request):
    if request.method == 'GET':
        bgList = Enterprise.objects.filter(id=request.user.company.id).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    myContext = {
        'page_title': _('Enterprises'),
        'bgList': bgList,
    }
    return render(request, 'company-list.html', myContext)


@login_required(login_url='home:user-login')
def updateBusinessGroup(request, pk):
    required_enterprice = Enterprise.objects.get(pk=pk)
    bgForm = EnterpriseForm(instance=required_enterprice)
    if request.method == "POST":
        bgForm = EnterpriseForm(request.POST, instance=required_enterprice)
        if bgForm.is_valid():
            bg_obj = bgForm.save(commit=False)
            bg_obj.save()
            return redirect('company:list-company-information')
            # success_msg = 'Business Group Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم التعديلء بنجاح'
            else:
                success_msg = 'Business Group Updated Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, bgForm.errors)]
    myContext = {
        "page_title": _("update Business unit"),
        'bgForm': bgForm,
    }
    return render(request, 'company-create.html', context=myContext)


@login_required(login_url='home:user-login')
def deleteBusinessGroup(request, pk):
    required_enterprice = Enterprise.objects.get(pk=pk)
    try:
        enterpriseForm = EnterpriseForm(instance=required_enterprice)
        enterprise_obj = enterpriseForm.save(commit=False)
        enterprise_obj.end_date = date.today()
        enterprise_obj.save(update_fields=['end_date'])
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{}تم حذف'.format(required_enterprice)
        else:
            success_msg = '{} successfully deleted'.format(required_enterprice)
        # success_msg = '{} successfully deleted'.format(deleted_obj)
        messages.success(request, success_msg)
    except Exception as e:
        # error_msg = '{} cannot be deleted '.format(deleted_obj)
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            error_msg = '{} لم يتم حذف '.format(required_enterprice)
        else:
            error_msg = '{} cannot be deleted '.format(required_enterprice)
        messages.error(request, error_msg)
        raise e
    return redirect('company:list-company-information')


########################################Department views###################################################################

def viewHirarchy(request):
    dept_list = Department.objects.all(request.user)
    myContext = {
        "page_title": _("list departments"),
        'dept_list': dept_list
    }
    return render(request, 'company-hierachy.html', myContext)


@login_required(login_url='home:user-login')
def viewDepartmentView(request, pk):
    required_obj = get_object_or_404(Department, pk=pk)
    dept_form = DepartmentForm(instance=required_obj)
    viewContext = {
        "page_title": '{}'.format(required_obj),
        'dept_form': dept_form
    }
    return render(request, 'department-view.html', viewContext)


@login_required(login_url='home:user-login')
def listDepartmentView(request):
    if request.method == 'GET':
        dept_list = Department.objects.filter(enterprise=request.user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True)).order_by('tree_id')
    myContext = {
        "page_title": _("list departments"),
        'dept_list': dept_list
    }
    return render(request, 'department-list.html', myContext)


@login_required(login_url='home:user-login')
def createDepartmentView(request):
    dept_formset = DepartmentInline(queryset=Department.objects.none())
    for form in dept_formset:
        form.fields['parent'].queryset = Department.objects.filter((Q(enterprise=request.user.company))).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    if request.method == 'POST':
        dept_formset = DepartmentInline(request.POST)
        success_msg = ""
        if dept_formset.is_valid():
            dept_obj = dept_formset.save(commit=False)
            for x in dept_obj:
                x.enterprise = request.user.company
                x.department_user = request.user
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            return redirect('company:list-department')
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, dept_formset.errors)]
    myContext = {"page_title": _("Create New Department"),
                 'dept_formset': dept_formset,
                 }
    return render(request, 'department-create.html', myContext)


@login_required(login_url='home:user-login')
def correctDepartmentView(request, pk):
    required_dept = Department.objects.get_department(user=request.user, dept_id=pk)
    dept_form = DepartmentForm(instance=required_dept)
    dept_form.fields['parent'].queryset = Department.objects.filter((Q(enterprise=request.user.company))).filter(
        Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    if request.method == 'POST':
        dept_form = DepartmentForm(request.POST, instance=required_dept)
        if dept_form.is_valid():
            dept_form.save()
            return redirect('company:list-department')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'

            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, dept_form.errors)]
    myContext = {
        'dept_form': dept_form,
    }
    return render(request, 'department-update.html', myContext)


@login_required(login_url='home:user-login')
def updateDepartmentView(request, pk):
    required_dept = Department.objects.get_department(user=request.user, dept_id=pk)
    dept_form = DepartmentForm(instance=required_dept)
    dept_form.fields['parent'].queryset = Department.objects.filter((Q(enterprise=request.user.company))).filter(
        Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    if request.method == 'POST':
        dept_form = DepartmentForm(request.POST, instance=required_dept)
        old_object = Department(
            enterprise=request.user.company,
            department_user=request.user,
            dept_name=required_dept.dept_name,
            parent=required_dept.parent,
            start_date=required_dept.start_date,
            end_date=date.today(),
            created_by=required_dept.created_by,
            last_update_by=required_dept.last_update_by)
        old_object.save()
        if dept_form.is_valid():
            old_obj = dept_form.save()
            return redirect('company:list-department')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, dept_form.errors)]
    myContext = {
        'dept_form': dept_form,
    }
    return render(request, 'department-update.html', myContext)


@login_required(login_url='home:user-login')
def deleteDepartmentView(request, pk):
    deleted_obj = Department.objects.get_department(user=request.user, dept_id=pk)
    try:
        department_form = DepartmentForm(instance=deleted_obj)
        department_obj = department_form.save(commit=False)
        department_obj.end_date = date.today()
        department_obj.save(update_fields=['end_date'])
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{}تم حذف'.format(deleted_obj)
        else:
            success_msg = '{} successfully deleted'.format(deleted_obj)
        # success_msg = '{} successfully deleted'.format(deleted_obj)
        messages.success(request, success_msg)
    except Exception as e:
        # error_msg = '{} cannot be deleted '.format(deleted_obj)
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            error_msg = '{} لم يتم حذف '.format(deleted_obj)
        else:
            error_msg = '{} cannot be deleted '.format(deleted_obj)
        messages.error(request, error_msg)
        raise e
    return redirect('company:list-department')


@login_required(login_url='home:user-login')
def export_department_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        department_resource = DepartmentResource()
        #queryset = Department.objects.none()
        dataset = department_resource.export()

        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="department_exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="department_exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="department_exported_data.xls"'
            return response
    export_context = {
    'page_title':'Please select format of file.',
    }
    #context['fields'] = [f.column_name for f in department_resource.get_user_visible_fields()]
    return render(request, 'export.html', export_context )
########################################Job views###################################################################
@login_required(login_url='home:user-login')
def listJobView(request):
    if request.method == 'GET':
        job_list = Job.objects.filter(enterprise=request.user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    myContext = {"page_title": _("List jobs"), 'job_list': job_list}
    return render(request, 'job-list.html', myContext)


@login_required(login_url='home:user-login')
def createJobView(request):
    job_formset = JobInline(queryset=Job.objects.none())
    user_lang = to_locale(get_language())
    if request.method == 'POST':
        job_formset = JobInline(request.POST)
        if job_formset.is_valid():
            job_obj = job_formset.save(commit=False)
            for x in job_obj:
                x.enterprise = request.user.company
                x.job_user = request.user
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            return redirect('company:list-jobs')
            # success_msg = 'Create Successfully'

            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, job_formset.errors)]
    myContext = {
        "page_title": "create new job",
        'job_formset': job_formset
    }
    return render(request, 'job-create.html', context=myContext)


@login_required(login_url='home:user-login')
def updateJobView(request, pk):
    required_job = Job.objects.get_job(user=request.user, job_id=pk)
    job_form = JobForm(instance=required_job)
    if request.method == 'POST':
        new_obj = Job(
            enterprise=request.user.company,
            job_user=request.user,
            job_name=required_job.job_name,
            job_description=required_job.job_description,
            start_date=required_job.start_date,
            end_date=date.today(),
            created_by=required_job.created_by,
            last_update_by=required_job.last_update_by,
        )
        new_obj.save()
        job_form = JobForm(request.POST, instance=required_job)
        if job_form.is_valid():
            old_obj = job_form.save()
            return redirect('company:list-jobs')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, job_form.errors)]
    myContext = {
        "page_title": 'Update Job',
        'job_form': job_form,
    }
    return render(request, 'job-update.html', context=myContext)


@login_required(login_url='home:user-login')
def correctJobView(request, pk):
    required_job = Job.objects.get_job(user=request.user, job_id=pk)
    job_form = JobForm(instance=required_job)
    if request.method == 'POST':
        job_form = JobForm(request.POST, instance=required_job)
        if job_form.is_valid():
            job_form.save()
            return redirect('company:list-jobs')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, job_form.errors)]
    myContext = {
        "page_title": 'Update Job',
        'job_form': job_form,
    }
    return render(request, 'job-update.html', context=myContext)


@login_required(login_url='home:user-login')
def deleteJobView(request, pk):
    deleted_obj = Job.objects.get_job(user=request.user, job_id=pk)
    try:
        required_form = DepartmentForm(instance=deleted_obj)
        required_obj = required_form.save(commit=False)
        required_obj.end_date = date.today()
        required_obj.save(update_fields=['end_date'])
        success_msg = '{} successfully deleted'.format(deleted_obj)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            error_msg = '{} لم يتم حذف '.format(deleted_obj)
        else:
            error_msg = '{} cannot be deleted '.format(deleted_obj)
        # error_msg = '{} cannot be deleted '.format(deleted_obj)
        messages.error(request, error_msg)
        raise e
    return redirect('company:list-jobs')


@login_required(login_url='home:user-login')
def export_job_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        job_resource = JobResource()
        #queryset = Job.objects.all(request.user)
        dataset = job_resource.export()

        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="jobs_exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="jobs_exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="jobs_exported_data.xls"'
            return response
    export_context = {
    'page_title':'Please select format of file.',
    }
    #context['fields'] = [f.column_name for f in department_resource.get_user_visible_fields()]
    return render(request, 'export.html', export_context )
#

########################################Grade views###################################################################
@login_required(login_url='home:user-login')
def listGradeView(request):
    if request.method == 'GET':
        grade_list = Grade.objects.filter(enterprise=request.user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    myContext = {"page_title": _("List grades"), 'grade_list': grade_list}
    return render(request, 'grade-list.html', myContext)


@login_required(login_url='home:user-login')
def createGradeView(request):
    grade_formset = GradeInline(queryset=Grade.objects.none())
    if request.method == 'POST':
        grade_formset = GradeInline(request.POST)
        if grade_formset.is_valid():
            grade_obj = grade_formset.save(commit=False)
            for x in grade_obj:
                x.enterprise = request.user.company
                x.grade_user = request.user
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            return redirect('company:list-grades')
            # success_msg = 'Create Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم الانشاء بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, grade_formset.errors)]
    myContext = {

        "page_title": _("create new grade"),
        'grade_formset': grade_formset,
    }
    return render(request, 'grade-create.html', context=myContext)


@login_required(login_url='home:user-login')
def updateGradeView(request, pk):
    required_grade = Grade.objects.get_job(user=request.user, grade_id=pk)
    grade_form = GradeForm(instance=required_grade)
    new_obj = Grade(
        enterprise=request.user.company,
        grade_user=request.user,
        grade_name=required_grade.grade_name,
        grade_description=required_grade.grade_description,
        start_date=required_grade.start_date,
        end_date=date.today(),
        created_by=required_grade.created_by,
        last_update_by=required_grade.last_update_by,
    )
    if request.method == 'POST':
        new_obj.save()
        grade_form = GradeForm(request.POST, instance=required_grade)
        if grade_form.is_valid():
            old_obj = grade_form.save()
            return redirect('company:list-grades')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'

            [messages.error(request, grade_form.errors)]
    myContext = {
        'grade_form': grade_form,
    }
    return render(request, 'grade-update.html', context=myContext)


@login_required(login_url='home:user-login')
def correctGradeView(request, pk):
    required_grade = Grade.objects.get_job(user=request.user, grade_id=pk)
    grade_form = GradeForm(instance=required_grade)
    if request.method == 'POST':
        grade_form = GradeForm(request.POST, instance=required_grade)
        if grade_form.is_valid():
            grade_form.save()
            return redirect('company:list-grades')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, grade_form.errors)]
    myContext = {
        'grade_form': grade_form,
    }
    return render(request, 'grade-update.html', context=myContext)


@login_required(login_url='home:user-login')
def deleteGradeView(request, pk):
    deleted_obj = Grade.objects.get_job(user=request.user, grade_id=pk)
    try:
        required_form = DepartmentForm(instance=deleted_obj)
        required_obj = required_form.save(commit=False)
        required_obj.end_date = date.today()
        required_obj.save(update_fields=['end_date'])
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{} تم حذف '.format(deleted_obj)
        else:
            success_msg = '{} successfully deleted'.format(deleted_obj)
        # success_msg = '{} successfully deleted'.format(deleted_obj)
        messages.success(request, success_msg)
    except Exception as e:
        # error_msg = '{} cannot be deleted '.format(deleted_obj)
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            error_msg = '{} لم يتم حذف '.format(deleted_obj)
        else:
            error_msg = '{} cannot be deleted '.format(deleted_obj)
        messages.error(request, error_msg)
        raise e
    return redirect('company:list-grades')



@login_required(login_url='home:user-login')
def export_grade_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        grade_resource = GradeResource()
        #queryset = Grade.objects.all(request.user)
        dataset = grade_resource.export()

        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="grads_exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="grads_exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="grads_exported_data.xls"'
            return response
    export_context = {
    'page_title':'Please select format of file.',
    }
    #context['fields'] = [f.column_name for f in department_resource.get_user_visible_fields()]
    return render(request, 'export.html', export_context )

########################################Position views###################################################################
@login_required(login_url='home:user-login')
def listPositionView(request):
    if request.method == 'GET':
        position_list = Position.objects.filter(department__enterprise=request.user.company).filter(
            Q(end_date__gt=date.today()) | Q(end_date__isnull=True))

    myContext = {"page_title": _("List positions"), 'position_list': position_list}
    return render(request, 'position-list.html', myContext)


@login_required(login_url='home:user-login')
def createPositionView(request):
    position_formset = PositionInline(queryset=Position.objects.none())
    for form in position_formset:
        form.fields['department'].queryset = Department.objects.filter((Q(enterprise=request.user.company))).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
        form.fields['job'].queryset = Job.objects.filter((Q(enterprise=request.user.company))).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
        form.fields['grade'].queryset = Grade.objects.filter((Q(enterprise=request.user.company))).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    if request.method == 'POST':
        position_formset = PositionInline(request.POST)
        if position_formset.is_valid():
            position_obj = position_formset.save(commit=False)
            for x in position_obj:
                x.position_user = request.user
                x.position_by = request.user
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            return redirect('company:list-positions')
            # success_msg = 'Create Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تم الانشاء بنجاح'
            else:
                success_msg = 'Create Successfully'

            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'

            [messages.error(request, position_formset.errors)]
    myContext = {

        "page_title": _("create new position"),
        'position_formset': position_formset,
    }
    return render(request, 'position-create.html', context=myContext)


@login_required(login_url='home:user-login')
def updatePositionView(request, pk):
    required_position = Position.objects.get_position(user=request.user, position_id=pk)
    position_form = PositionForm(instance=required_position)
    new_obj = Position(
        # position_user=request.user,
        job=required_position.job,
        department=required_position.department,
        grade=required_position.grade,
        position_name=required_position.position_name,
        position_description=required_position.position_description,
        start_date=required_position.start_date,
        end_date=date.today(),
        created_by=required_position.created_by,
        last_update_by=required_position.last_update_by,
    )
    if request.method == 'POST':
        new_obj.save()
        position_form = PositionForm(request.POST, instance=required_position)
        if position_form.is_valid():
            old_obj = position_form.save()
            return redirect('company:list-positions')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'

            [messages.error(request, position_form.errors)]
    myContext = {"page_title": _("update position"),
                 'position_form': position_form}
    return render(request, 'position-update.html', context=myContext)


@login_required(login_url='home:user-login')
def correctPositionView(request, pk):
    required_position = Position.objects.get_position(user=request.user, position_id=pk)
    position_form = PositionForm(instance=required_position)
    if request.method == 'POST':
        position_form = PositionForm(request.POST, instance=required_position)
        if position_form.is_valid():
            position_form.save()
            return redirect('company:list-positions')
            # success_msg = 'Updated Successfully'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'

            [messages.error(request, position_form.errors)]
    myContext = {"page_title": _("correct position"),
                 'position_form': position_form}
    return render(request, 'position-update.html', context=myContext)


@login_required(login_url='home:user-login')
def deletePositionView(request, pk):
    deleted_obj = Position.objects.get_position(user=request.user, position_id=pk)
    try:
        required_form = DepartmentForm(instance=deleted_obj)
        required_obj = required_form.save(commit=False)
        required_obj.end_date = date.today()
        required_obj.save(update_fields=['end_date'])
        # success_msg = '{} successfully deleted'.format(deleted_obj)
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{} تم حذف السجل'.format(deleted_obj)
        else:
            success_msg = '{} successfully deleted'.format(deleted_obj)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            error_msg = '{} لم يتم حذف '.format(deleted_obj)
        else:
            error_msg = '{} cannot be deleted '.format(deleted_obj)
        # error_msg = '{} cannot be deleted '.format(deleted_obj)
        messages.error(request, error_msg)
        raise e
    return redirect('company:list-positions')


@login_required(login_url='home:user-login')
def export_position_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        position_resource = PositionResource()
        dataset = position_resource.export()

        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="position_exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="position_exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="position_exported_data.xls"'
            return response
    export_context = {
    'page_title':'Please select format of file.',
    }
    #context['fields'] = [f.column_name for f in department_resource.get_user_visible_fields()]
    return render(request, 'export.html', export_context )


########################################Company Policies views###################################################################

@login_required(login_url='home:user-login')
def CreateWorkingPolicyView(request):
    working_policy_form = WorkingDaysForm()
    user_lang = to_locale(get_language())
    if request.method == 'POST':
        working_policy_form = WorkingDaysForm(request.POST)
        if working_policy_form.is_valid():
            policy_obj = working_policy_form.save(commit=False)
            policy_obj.enterprise = request.user.company
            policy_obj.created_by = request.user
            policy_obj.last_update_by = request.user
            policy_obj.save()

            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
            return redirect('company:working-hrs-policy-list')

        else:  # Form was not valid
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            messages.error(request, working_policy_form.errors)
    my_context = {
        "page_title": "create new working hours policy",
        'policy_form': working_policy_form,
    }
    return render(request, 'working-hrs-policy-create.html', context=my_context)


@login_required(login_url='home:user-login')
def listWorkingPolicyView(request):
    if request.method == 'GET':
        working_policy_list = Working_Days_Policy.objects.all(request.user)
    myContext = {
        "page_title": _("List working policies"),
        'policy_list': working_policy_list
    }
    return render(request, 'working-hrs-policy-list.html', myContext)


@login_required(login_url='home:user-login')
def correctWorkingPolicyView(request, pk):
    required_policy = Working_Days_Policy.objects.get(id=pk)
    policy_form = WorkingDaysForm(instance=required_policy)
    user_lang = to_locale(get_language())
    if request.method == 'POST':
        policy_form = WorkingDaysForm(request.POST, instance=required_policy)

        if policy_form.is_valid():
            policy_obj = policy_form.save(commit=False)
            policy_obj.last_update_by = request.user
            policy_obj.save()
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Updated Successfully'
            messages.success(request, success_msg)

        else:  # Form was not valid
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            messages.error(request, success_msg)
    myContext = {
        "page_title": "Update working hours policy",
        'policy_form': policy_form,
    }
    return render(request, 'working-hrs-policy-create.html', context=myContext)


@login_required(login_url='home:user-login')
def deleteWorkingPolicyView(request, pk):
    req_working_policy = Working_Days_Policy.objects.get_policy(user=request.user, policy_id=pk)
    deleted = req_working_policy.delete()
    if deleted:
        messages.success(request, 'Record successfully deleted')

    else:
        messages.error(request, 'Record is NOT deleted')

    return redirect('company:working-hrs-policy-list')


@login_required(login_url='home:user-login')
def listYearlyHolidayView(request, year_id):
    yearly_holiday_list = []
    year = Year.objects.get_year(request.user, year_id)
    if request.method == 'GET':
        yearly_holiday_list = YearlyHoliday.objects.get_year_holiday(user=request.user, year_name=year_id)

    myContext = {
        "page_title": f"List yearly holidays for {year}",
        'yearly_holiday_list': yearly_holiday_list,
        'year_id': year_id
    }
    return render(request, 'yearly-holiday-list.html', myContext)


@login_required(login_url='home:user-login')
def createYearlyHolidayView(request, year_id):
    year = Year.objects.get_year(user=request.user, year_id=year_id)
    yearly_holiday_formset = YearlyHolidayInline(queryset=YearlyHoliday.objects.none())
    user_lang = to_locale(get_language())
    if request.method == 'POST':
        yearly_holiday_formset = YearlyHolidayInline(request.POST)
        if yearly_holiday_formset.is_valid():
            fomrset = yearly_holiday_formset.save(commit=False)
            for holiday_obj in fomrset:
                holiday_obj.enterprise = request.user.company
                holiday_obj.year = year
                holiday_obj.created_by = request.user
                holiday_obj.last_update_by = request.user
                if holiday_obj.number_of_days_off is None:
                    delta = holiday_obj.end_date - holiday_obj.start_date
                    holiday_obj.number_of_days_off = delta.days
                holiday_obj.save()

            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Create Successfully'
            messages.success(request, success_msg)
            return redirect('company:yearly-holiday-list', year_id=year_id)

        else:  # Form was not valid
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            messages.error(request, success_msg)
    my_context = {
        "page_title": f"create new yearly holidays for {year}",
        'yearly_holiday_formset': yearly_holiday_formset,
        'year_id': year_id,
    }
    return render(request, 'yearly-holiday-create.html', context=my_context)


@login_required(login_url='home:user-login')
def correctYearlyHolidayView(request, pk):
    required_holiday = YearlyHoliday.objects.get_holiday(user=request.user, yearly_holiday_id=pk)
    holiday_form = YearlyHolidayForm(instance=required_holiday)
    year_id = required_holiday.year.year
    user_lang = to_locale(get_language())
    if request.method == 'POST':
        holiday_form = YearlyHolidayForm(request.POST, instance=required_holiday)

        if holiday_form.is_valid():
            holiday_obj = holiday_form.save(commit=False)
            holiday_obj.last_update_by = request.user
            # TODO: update the field number_of_days after saving the new dates
            if holiday_obj.number_of_days_off is None:
                delta = holiday_obj.end_date - holiday_obj.start_date
                holiday_obj.number_of_days_off = delta.days
            holiday_obj.save()
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Updated Successfully'
            messages.success(request, success_msg)

        else:  # Form was not valid
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            messages.error(request, success_msg)
    myContext = {
        "page_title": "Update yearly holiday",
        'holiday_form': holiday_form,
        'year_id': year_id,
    }
    return render(request, 'yearly-holiday-update.html', context=myContext)


@login_required(login_url='home:user-login')
def deleteYearlyHolidayView(request, pk):
    req_holiday = YearlyHoliday.objects.get_holiday(user=request.user, yearly_holiday_id=pk)
    year_ID = req_holiday.year.id
    deleted = req_holiday.delete()
    if deleted:
        messages.success(request, 'Record successfully deleted')

    else:
        messages.error(request, 'Record is NOT deleted')

    return redirect('company:yearly-holiday-list', year_id=year_ID)


@login_required(login_url='home:user-login')
def listYearsView(request):
    years = Year.objects.all(request.user)
    num_of_holidays = {}
    for year in years:
        num_of_holidays[year.year] = YearlyHoliday.objects.get_year_holiday(user=request.user,
                                                                            year_name=year.year).count()
    year_form = YearForm()
    if request.method == 'POST':
        year_form = YearForm(request.POST)
        if year_form.is_valid():
            year_obj = year_form.save(commit=False)
            year_obj.enterprise = request.user.company
            year_obj.created_by = request.user
            year_obj.save()
            return redirect('company:yearly-holiday-create', year_id=year_obj.year)
    context = {
        "page_title": _("Years"),
        'num_of_holidays': num_of_holidays,
        'years': years,
        'year_form': year_form,
    }
    return render(request, 'years-list.html', context=context)


@login_required(login_url='home:user-login')
def list_working_hours_deductions_view(request):
    print(request.user.company.id)
    working_deductions_list = Working_Hours_Deductions_Policy.objects.filter(
        working_days_policy__enterprise_id=request.user.company.id)
    print(working_deductions_list)
    working_hrs_deduction_form = WorkingHoursDeductionForm()
    context = {
        "page_title": _("Work Hours Deduction Policy"),
        'working_deductions_list': working_deductions_list,
    }
    return render(request, 'working-hrs-deductions-list.html', context=context)


@login_required(login_url='home:user-login')
def create_working_hours_deductions_view(request):
    working_deductions_formset = Working_Hours_Deduction_Form_Inline(
        queryset=Working_Hours_Deductions_Policy.objects.none())
    if request.method == 'POST':
        company_working_policy = Working_Days_Policy.objects.get(enterprise=request.user.company)
        working_deductions_formset = Working_Hours_Deduction_Form_Inline(request.POST)
        if working_deductions_formset.is_valid():
            try:
                formset_obj = working_deductions_formset.save(commit=False)
                for form in formset_obj:

                    form.working_days_policy_id = company_working_policy.id
                    form.created_by = request.user
                    form.save()
                messages.success(request, _('Working Hours Deductions Created Successfully'))
            except IntegrityError as e:
                messages.error(request, _('UNIQUE constraint failed'))

        else:
            messages.error(request, working_deductions_formset.errors)

    context = {
        "page_title": _("Work Hours Deduction Policy"),
        'working_deductions_formset': working_deductions_formset,
    }
    return render(request, 'working-hrs-deductions-create.html', context=context)



@login_required(login_url='home:user-login')
def update_working_hours_deductions_view(request, deduction_id):
    #required_work_deduction = Working_Hours_Deductions_Policy.objects.get(id=deduction_id)
    working_deductions_formset =Working_Hours_Deduction_Form_Inline(
        queryset=Working_Hours_Deductions_Policy.objects.get(id=deduction_id))
    if request.method == 'POST':
        company_working_policy = Working_Days_Policy.objects.get(enterprise=request.user.company)
        working_deductions_formset = Working_Hours_Deduction_Form(request.POST)
        if working_deductions_formset.is_valid():
            try:
                formset_obj = working_deductions_formset.save(commit=False)
                for form in formset_obj:
                    form.Working_Days_Policy_id = company_working_policy.id
                    form.created_by = request.user
                    form.save()
                messages.success(request, _('Working Hours Deductions Created Successfully'))
            except IntegrityError as e:
                messages.error(request, _('UNIQUE constraint failed'))

        else:
            messages.error(request, working_deductions_formset.errors)

    context = {
        "page_title": _("Work Hours Deduction Policy"),
        'working_deductions_formset': working_deductions_formset,
     }
    return render(request, 'working-hrs-deductions-create.html', context=context)


def load_lookups(user, company_id):
    """
        Copy the records from lookupType linked to the general company and create new ones for the requested company
        including the related model LookupDet

        :Params:
         "user": the user requesting the view
         "company_id" : the id of the company where the link is needed

    """
    # Get all look_ups related to the general company
    all_lookups = LookupType.objects.filter(enterprise_id=1).values()
    for item in all_lookups:
        myid = item.pop('id')
        new_item = LookupType(**item)
        new_item.enterprise_id = company_id
        new_item.start_date = date.today()
        new_item.end_date = None
        new_item.created_by = user
        new_item.last_update_by = None
        new_item.save()
        related_details = LookupDet.objects.filter(lookup_type_fk=myid).values()
        for record in related_details:
            new_record = LookupDet(**record)
            new_record.id = None
            new_record.lookup_type_fk = new_item
            new_record.start_date = date.today()
            new_record.end_date = None
            new_record.last_update_by = None
            new_record.save()


def load_tax_rules(user, company_id):
    """
        Copy the records from Taxrules linked to the general company and create new ones for the requested company
        including the related model Tax_Sections

        :Params:
         "user": the user requesting the view
         "company_id" : the id of the company where the link is needed

        """
    all_taxes = TaxRule.objects.filter(enterprise_id=1).values()
    for item in all_taxes:
        myid = item.pop('id')
        new_item = TaxRule(**item)
        new_item.enterprise_id = company_id
        new_item.start_date = date.today()
        new_item.end_date = None
        new_item.last_update_by = None
        new_item.created_by = user
        new_item.save()
        related_details = Tax_Sections.objects.filter(tax_rule_id=myid).values()
        for record in related_details:
            record.pop('id')
            new_record = Tax_Sections(**record)
            new_record.tax_rule_id = new_item
            new_record.start_date = date.today()
            new_record.end_date = None
            new_record.last_update_by = None
            new_record.save()


def load_modules(request):
    """
     Link a module to a company :model:`Defenition.LookupType,Defenition.LookDet,'Defenition.TaxRules`.

     **Context**

     ``company_form``
         An instance of :form:`Company.forms.CompanySetupForm`.
     ``title``
         A string representing the title of the rendered HTML page

     **Template:**

     :template:`company/templates/setup_new_company.html`

     """

    company_form = CompanySetupForm()
    if request.method == "POST":
        company_form = CompanySetupForm(request.POST)
        if company_form.is_valid():
            company_id = request.user.company.id
            module = company_form.cleaned_data['modules']
            # TODO: enterprise_id to copy from needs to be configurable
            # TODO: Check if company already has the module

            if "1" in module:
                loader = DatabaseLoader('LookupType', 1, company_id, 'enterprise_id')
                loader.duplicate_data()
                # load_lookups(request.user, company_id)
            if "2" in module:
                loader = DatabaseLoader('TaxRule', 1, company_id, 'enterprise_id')
                loader.duplicate_data()
                # load_tax_rules(request.user, company_id)
            messages.success(request, "Modules uploaded Successfully")
        else:
            messages.error(request, "Modules failed to upload")

    context = {"company_form": company_form, "page_title": "Upload Modules"}

    return render(request, 'setup_new_company.html', context=context)
