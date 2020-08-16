from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.translation import to_locale, get_language
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from custom_user.models import User
from company.forms import (EnterpriseForm, DepartmentInline, DepartmentForm, JobInline,
                           JobForm, GradeInline, GradeForm, PositionInline, PositionForm, WorkingHoursForm,
                           YearlyHolidayInline, YearlyHolidayForm)
from company.models import (Enterprise, Department, Job, Grade, Position, YearlyHoliday, WorkingHoursPolicy)
from django.utils.translation import ugettext_lazy as _
from cities_light.models import City, Country


########################################Enterprise views###################################################################
def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def listCompanyInformation(request):
    if request.method == 'GET':
        bgList = Enterprise.objects.all(request.user)
    myContext = {
        'page_title': _('Enterprises'),
        'bgList': bgList,
    }
    return render(request, 'company-list.html', myContext)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def listAssignmentView(request):
    num_of_dept = Department.objects.all(request.user).count()
    num_of_jobs = Job.objects.all(request.user).count()
    num_of_grades = Grade.objects.all(request.user).count()
    num_of_positions = Position.objects.all(request.user).count()
    context = {

        "page_title": _("Company Structure Definition"),
        'num_of_dept': num_of_dept,
        'num_of_jobs': num_of_jobs,
        'num_of_grades': num_of_grades,
        'num_of_positions': num_of_positions,
    }
    return render(request, 'assinment-list.html', context=context)


########################################Department views###################################################################

def viewHirarchy(request):
    return render(request, 'company-hierachy.html')


@login_required(login_url='/login')
def viewDepartmentView(request, pk):
    required_obj = get_object_or_404(Department, pk=pk)
    dept_form = DepartmentForm(instance=required_obj)
    viewContext = {
        "page_title": '{}'.format(required_obj),
        'dept_form': dept_form
    }
    return render(request, 'department-view.html', viewContext)


@login_required(login_url='/login')
def listDepartmentView(request):
    if request.method == 'GET':
        dept_list = Department.objects.all(request.user)

    myContext = {
        "page_title": _("list departments"),
        'dept_list': dept_list
    }
    return render(request, 'department-list.html', myContext)


@login_required(login_url='/login')
def createDepartmentView(request):
    dept_formset = DepartmentInline(queryset=Department.objects.none())
    for form in dept_formset:
        form.fields['parent_dept'].queryset = Department.objects.filter((Q(enterprise=request.user.company)),
                                                                        parent_dept__isnull=True).filter(
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
    myContext = {"page_title": "Create New Department",
                 'dept_formset': dept_formset,
                 }
    return render(request, 'department-create.html', myContext)


@login_required(login_url='/login')
def correctDepartmentView(request, pk):
    required_dept = Department.objects.get_department(user=request.user, dept_id=pk)
    dept_form = DepartmentForm(instance=required_dept)
    dept_form.fields['parent_dept'].queryset = Department.objects.filter((Q(enterprise=request.user.company)),
                                                                         parent_dept__isnull=True).filter(
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


@login_required(login_url='/login')
def updateDepartmentView(request, pk):
    required_dept = Department.objects.get_department(user=request.user, dept_id=pk)
    dept_form = DepartmentForm(instance=required_dept)
    dept_form.fields['parent_dept'].queryset = Department.objects.filter((Q(enterprise=request.user.company)),
                                                                         parent_dept__isnull=True).filter(
        Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    if request.method == 'POST':
        dept_form = DepartmentForm(request.POST, instance=required_dept)
        old_object = Department(
            enterprise=request.user.company,
            department_user=request.user,
            dept_name=required_dept.dept_name,
            parent_dept=required_dept.parent_dept,
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


@login_required(login_url='/login')
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


########################################Job views###################################################################
@login_required(login_url='/login')
def listJobView(request):
    if request.method == 'GET':
        job_list = Job.objects.all(request.user)

    myContext = {"page_title": _("List jobs"), 'job_list': job_list}
    return render(request, 'job-list.html', myContext)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


########################################Grade views###################################################################
@login_required(login_url='/login')
def listGradeView(request):
    if request.method == 'GET':
        grade_list = Grade.objects.all(request.user)

    myContext = {"page_title": _("List grades"), 'grade_list': grade_list}
    return render(request, 'grade-list.html', myContext)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


########################################Position views###################################################################
@login_required(login_url='/login')
def listPositionView(request):
    if request.method == 'GET':
        position_list = Position.objects.all(request.user)

    myContext = {"page_title": _("List positions"), 'position_list': position_list}
    return render(request, 'position-list.html', myContext)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def CreateWorkingPolicyView(request):
    working_policy_form = WorkingHoursForm()
    user_lang = to_locale(get_language())
    if request.method == 'POST':
        working_policy_form = WorkingHoursForm(request.POST)
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
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, working_policy_form.errors)]
    my_context = {
        "page_title": "create new working hours policy",
        'policy_form': working_policy_form,
    }
    return render(request, 'working-hrs-policy-create.html', context=my_context)


@login_required(login_url='/login')
def listWorkingPolicyView(request):
    if request.method == 'GET':
        working_policy_list = WorkingHoursPolicy.objects.all(request.user)

    myContext = {"page_title": _("List working policies"), 'policy_list': working_policy_list}
    return render(request, 'working-hrs-policy-list.html', myContext)


@login_required(login_url='/login')
def correctPolicyView(request, pk):
    required_policy = WorkingHoursPolicy.objects.get_policy(user=request.user, policy_id=pk)
    policy_form = WorkingHoursForm(instance=required_policy)

    if request.method == 'POST':
        policy_form = WorkingHoursForm(request.POST, instance=required_policy)

        if policy_form.is_valid():
            policy_form.last_update_by = request.user
            policy_form.save()
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Updated Successfully'
            messages.success(request, success_msg)
            return redirect('company:working-hrs-policy-list')

        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, policy_form.errors)]
    myContext = {
        "page_title": "Update working hours policy",
        'policy_form': policy_form,
    }
    return render(request, 'working-hrs-policy-create.html', context=myContext)


@login_required(login_url='/login')
def listPoliciesView(request):
    num_of_working_policy = WorkingHoursPolicy.objects.all(request.user).count()
    num_of_yearly_holidays = YearlyHoliday.objects.all(request.user).count()

    context = {

        "page_title": _("Company Working Policy Definition"),
        'num_of_working_policy': num_of_working_policy,
        'num_of_yearly_holidays': num_of_yearly_holidays,
    }
    return render(request, 'policy-list.html', context=context)


@login_required(login_url='/login')
def listYearlyHolidayView(request):
    if request.method == 'GET':
        yearly_holiday_list = YearlyHoliday.objects.all(request.user)

    myContext = {"page_title": _("List yearly holidays"), 'yearly_holiday_list': yearly_holiday_list}
    return render(request, 'yearly-holiday-list.html', myContext)


@login_required(login_url='/login')
def CreateYearlyHolidayView(request):
    yearly_holiday_formset = YearlyHolidayInline(queryset=YearlyHoliday.objects.none())
    user_lang = to_locale(get_language())
    if request.method == 'POST':
        yearly_holiday_formset = YearlyHolidayInline(request.POST)
        if yearly_holiday_formset.is_valid():
            fomrset = yearly_holiday_formset.save(commit=False)
            for holiday_obj in fomrset:
                holiday_obj.enterprise = request.user.company
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
            return redirect('company:yearly-holiday-list')

        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, yearly_holiday_formset.errors)]
    my_context = {
        "page_title": "create new yearly holiday",
        'yearly_holiday_formset': yearly_holiday_formset,
    }
    return render(request, 'yearly-holiday-create.html', context=my_context)


@login_required(login_url='/login')
def correctYearlyHolidayView(request, pk):
    required_holiday = YearlyHoliday.objects.get_holiday(user=request.user, yearly_holiday_id=pk)
    holiday_form = YearlyHolidayForm(instance=required_holiday)

    if request.method == 'POST':
        holiday_form = YearlyHolidayForm(request.POST, instance=required_holiday)

        if holiday_form.is_valid():
            holiday_form.last_update_by = request.user
            if holiday_form.number_of_days_off is None:
                delta = holiday_form.end_date - holiday_form.start_date
                holiday_form.number_of_days_off = delta.days
            holiday_form.save()
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'تمت العملية بنجاح'
            else:
                success_msg = 'Updated Successfully'
            messages.success(request, success_msg)
            return redirect('company:yearly-holiday-list')

        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang = to_locale(get_language())
            if user_lang == 'ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg = 'The form is not valid.'
            [messages.error(request, holiday_form.errors)]
    myContext = {
        "page_title": "Update yearly holiday",
        'holiday_form': holiday_form,
    }
    return render(request, 'yearly-holiday-update.html', context=myContext)

