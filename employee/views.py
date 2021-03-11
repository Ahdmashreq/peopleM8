from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import to_locale, get_language
from element_definition.models import Element_Master, Element_Link, Element
from employee.models import (
    Employee, JobRoll, Payment, Employee_Element, EmployeeStructureLink, Employee_File , Employee_Depandance)
from employee.forms import (EmployeeForm, JobRollForm, Employee_Payment_formset,
                            EmployeeElementForm, Employee_Element_Inline, EmployeeStructureLinkForm
                            ,EmployeeFileForm,Employee_Files_inline , Employee_depandance_inline)
from payroll_run.models import Salary_elements
from payroll_run.forms import SalaryElementForm
from employee.fast_formula import FastFormula
from manage_payroll.models import Payment_Method
from custom_user.models import User
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from company.models import Position
from .resources import *
from leave.models import *
from django.db.models import Count
from .resources_two import *

############################Employee View #################################
@login_required(login_url='home:user-login')
def createEmployeeView(request):
    emp_form = EmployeeForm()
    emp_form.fields['user'].queryset = User.objects.filter(
        company=request.user.company)
    jobroll_form = JobRollForm(user_v=request.user)
    payment_form = Employee_Payment_formset(queryset=Payment.objects.none())
    files_formset = Employee_Files_inline()
    depandance_formset = Employee_depandance_inline()
    for payment in payment_form:
        payment.fields['payment_method'].queryset = Payment_Method.objects.filter(
            payment_type__enterprise=request.user.company).filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True))
    emp_element_form = Employee_Element_Inline(
        queryset=Employee_Element.objects.none())
    for element in emp_element_form:
        element.fields['element_id'].queryset = Element_Master.objects.none()
    if request.method == 'POST':
        emp_form = EmployeeForm(request.POST,request.FILES)
        jobroll_form = JobRollForm(request.user, request.POST)
        payment_form = Employee_Payment_formset(request.POST)
        files_formset = Employee_Files_inline(request.POST , request.FILES)
        depandance_formset = Employee_depandance_inline(request.POST)

        if emp_form.is_valid() and jobroll_form.is_valid() and payment_form.is_valid() and files_formset.is_valid() and depandance_formset.is_valid():
            emp_obj = emp_form.save(commit=False)
            emp_obj.enterprise = request.user.company
            emp_obj.created_by = request.user
            emp_obj.last_update_by = request.user
            emp_obj.save()
            job_obj = jobroll_form.save(commit=False)
            job_obj.emp_id_id = emp_obj.id
            job_obj.created_by = request.user
            job_obj.last_update_by = request.user
            job_obj.save()
            payment_form = Employee_Payment_formset(
                request.POST, instance=emp_obj)
            if payment_form.is_valid():
                emp_payment_obj = payment_form.save(commit=False)
                for x in emp_payment_obj:
                    x.created_by = request.user
                    x.last_update_by = request.user
                    x.save()
            else:
                user_lang = user_lang = to_locale(get_language())
                if user_lang == 'ar':
                    error_msg = '{}, لم يتم التسجيل'.format(emp_payment_obj)
                else:
                    error_msg = '{}, has somthig wrong'.format(emp_payment_obj)
                # error_msg = '{}, has somthig wrong'.format(emp_payment_obj)
                messages.success(request, success_msg)

                user_lang = to_locale(get_language())
                if user_lang == 'ar':
                    error_msg = '{}, لم يتم التسجيل'.format(element_obj)
                    success_msg = ' {},تم تسجيل الموظف'.format(
                        emp_obj.emp_name)
                else:
                    error_msg = '{}, has somthig wrong'.format(element_obj)
                    success_msg = 'Employee {}, has been created successfully'.format(
                        emp_obj.emp_name)

                    messages.success(request, success_msg)
            
            files_obj = files_formset.save(commit=False)
            for file_obj in files_obj:
                file_obj.created_by = request.user
                file_obj.last_update_by = request.user
                file_obj.emp_id = emp_obj
                file_obj.save()
    
            # add depandances
            depandances_obj = depandance_formset.save(commit=False)
            for depandance_obj in depandances_obj:
                depandance_obj.created_by = request.user
                depandance_obj.last_update_by = request.user
                depandance_obj.emp_id = emp_obj
                depandance_obj.save()

            return redirect('employee:update-employee', pk=job_obj.id)
        else:
            messages.error(request, emp_form.errors)
            messages.error(request, jobroll_form.errors)
            messages.error(request, files_formset.errors)
            messages.error(request,depandance_formset.errors)
    myContext = {
        "page_title": _("create employee"),
        "emp_form": emp_form,
        "jobroll_form": jobroll_form,
        "payment_form": payment_form,
        "files_formset" : files_formset,
        "depandance_formset" : depandance_formset,
        "create_employee": True,
        "flage" : 0,
    }
    return render(request, 'create-employee.html', myContext)


@login_required(login_url='home:user-login')
def copy_element_values():
    element_master_obj = Element_Master.objects.filter().exclude(global_value=0)
    emp_element = Employee_Element.objects.filter()
    for x in element_master_obj:
        for z in emp_element:
            if z.element_id_id == x.id:
                z.element_value = x.global_value
                z.save()


@login_required(login_url='home:user-login')
def listEmployeeView(request):
    emp_list = Employee.objects.filter(enterprise=request.user.company).filter(
        (Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))
    emp_job_roll_list = JobRoll.objects.filter(
        emp_id__enterprise=request.user.company)
    myContext = {
        "page_title": _("List employees"),
        "emp_list": emp_list,
        'emp_job_roll_list': emp_job_roll_list,
    }
    return render(request, 'list-employees.html', myContext)


@login_required(login_url='home:user-login')
def listEmployeeCardView(request):
    emp_list = Employee.objects.filter(enterprise=request.user.company).filter(
        (Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))
    myContext = {
        "page_title": _("List employees"),
        "emp_list": emp_list,
    }
    return render(request, 'list-employees-card.html', myContext)


@login_required(login_url='home:user-login')
def viewEmployeeView(request, pk):
    required_employee = get_object_or_404(Employee, pk=pk)
    required_jobRoll = JobRoll.objects.filter(emp_id=pk)
    all_jobRoll = JobRoll.objects.filter(emp_id=pk).order_by('-id')
    all_payment = Payment.objects.filter(emp_id=pk, end_date__isnull=True).order_by('-id')
    all_elements = Employee_Element.objects.filter(
        emp_id=pk, end_date__isnull=True)
    myContext = {
        "page_title": _("view employee"),
        "required_employee": required_employee,
        "required_jobRoll": required_jobRoll,
        "all_payment": all_payment,
        "all_elements": all_elements,
        "all_jobRoll": all_jobRoll,
    }
    return render(request, 'view-employee.html', myContext)


@login_required(login_url='home:user-login')
def updateEmployeeView(request, pk):
    required_jobRoll = JobRoll.objects.get(id = pk)
    required_employee = get_object_or_404(Employee, pk=required_jobRoll.emp_id.id)
    emp_form = EmployeeForm(instance=required_employee)
    files_formset = Employee_Files_inline(instance=required_employee)
    depandance_formset = Employee_depandance_inline(instance=required_employee)
    # filter the user fk list to show the company users only.
    emp_form.fields['user'].queryset = User.objects.filter(
        company=request.user.company)
    jobroll_form = JobRollForm(user_v=request.user, instance=required_jobRoll)

    payment_form = Employee_Payment_formset(instance=required_employee)
    get_employee_salary_structure = ""


    '''
        updateing employee element part to show the elements & values for that Employee
        (removing the formset) and adding a button to link salary structure to that employee.
        By: Ahd Hozayen
        Date: 29-12-2020
    '''
    employee_element_qs = Employee_Element.objects.filter(
        emp_id=required_employee, end_date__isnull=True)
    employee_has_structure = False
    files = Employee_File.objects.filter(emp_id=required_employee)
    

    try:
        employee_salary_structure = EmployeeStructureLink.objects.get(
            employee=required_employee, end_date__isnull=True)
        employee_has_structure = True
        get_employee_salary_structure = employee_salary_structure.salary_structure
        # emp_form.fields['salary_structure'].initial = employee_salary_structure.salary_structure
    except EmployeeStructureLink.DoesNotExist:
        employee_has_structure = False

    employee_element_form = EmployeeElementForm()


    if request.method == 'POST':
        jobroll_form = JobRollForm(request.user, request.POST, instance=required_jobRoll)
        emp_form = EmployeeForm(request.POST, request.FILES, instance=required_employee)
        payment_form = Employee_Payment_formset(
            request.POST, instance=required_employee)
        files_formset = Employee_Files_inline(request.POST , request.FILES
        ,instance=required_employee)
        depandance_formset = Employee_depandance_inline(request.POST
        ,instance=required_employee)

        if EmployeeStructureLink.DoesNotExist:
            emp_link_structure_form = EmployeeStructureLinkForm(request.POST)
        else:
            emp_link_structure_form = EmployeeStructureLinkForm(
                request.POST, instance=employee_salary_structure)

        employee_element_form = EmployeeElementForm(request.POST)

        if emp_form.is_valid() and jobroll_form.is_valid() and payment_form.is_valid() and files_formset.is_valid() and depandance_formset.is_valid():
            emp_obj = emp_form.save(commit=False)
            emp_obj.created_by = request.user
            emp_obj.last_update_by = request.user
            emp_obj.save()
            #
            job_obj = jobroll_form.save(commit=False)
            job_obj.emp_id_id = emp_obj.id
            job_obj.created_by = request.user
            job_obj.last_update_by = request.user
            job_obj.save()
            #
            payment_form = Employee_Payment_formset(request.POST, instance=emp_obj)
            emp_payment_obj = payment_form.save(commit=False)
            for x in emp_payment_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            #
            files_obj = files_formset.save(commit=False)
            for file_obj in files_obj:
                file_obj.created_by = request.user
                file_obj.last_update_by = request.user
                file_obj.emp_id = emp_obj
                file_obj.save()
            #
            depandances_obj = depandance_formset.save(commit=False)
            for depandance_obj in depandances_obj:
                depandance_obj.created_by = request.user
                depandance_obj.last_update_by = request.user
                depandance_obj.emp_id = emp_obj
                depandance_obj.save()
            #
            """
            emp_element_obj = employee_element_form.save(commit=False)
            emp_element_obj.emp_id = required_employee
            emp_element_obj.created_by = request.user
            emp_element_obj.last_update_by = request.user
            emp_element_obj.save()
            """
            user_lang = to_locale(get_language())

            if user_lang == 'ar':
                success_msg = ' {},تم تسجيل الموظف'.format(required_employee)
            else:
                success_msg = 'Employee {}, has been created successfully'.format(
                    required_employee)
            return redirect('employee:list-employee')

        elif not emp_form.is_valid():
            messages.error(request, emp_form.errors)
        elif not jobroll_form.is_valid():
            messages.error(request, jobroll_form.errors)
        elif not payment_form.is_valid():
            messages.error(request, payment_form.errors)
        elif not files_formset.is_valid():
            messages.error(request,files_formset.errors)
        elif not depandance_formset.is_valid():
            messages.error(request, depandance_formset.errors)


    myContext = {
        "page_title": _("update employee"),
        "emp_form": emp_form,
        "jobroll_form": jobroll_form,
        "payment_form": payment_form,
        "required_employee": required_employee,
        "employee_element_qs": employee_element_qs,
        "employee_has_structure": employee_has_structure,
        "employee_element_form": employee_element_form,
        "get_employee_salary_structure": get_employee_salary_structure,
        "emp" : pk,
        "required_jobRoll" : required_jobRoll,
        "flage" : 1,
        "files_formset" : files_formset,
        "depandance_formset" :  depandance_formset,
    }
    return render(request, 'create-employee.html', myContext)

@login_required(login_url='home:user-login')
def create_link_employee_structure(request, pk):
    required_jobRoll = JobRoll.objects.get(id = pk)
    required_employee = get_object_or_404(Employee, pk=required_jobRoll.emp_id.id)
    emp_link_structure_form = EmployeeStructureLinkForm()
    if request.method == 'POST':
        emp_link_structure_form = EmployeeStructureLinkForm(request.POST)
        if emp_link_structure_form.is_valid():
            emp_structure_obj = emp_link_structure_form.save(commit=False)
            emp_structure_obj.employee = required_employee
            emp_structure_obj.created_by = request.user
            emp_structure_obj.last_update_by = request.user
            emp_structure_obj.save()
            return redirect('employee:update-employee', pk=pk)
        else:
            print('Form is not valid')
    my_context = {
        "page_title": _("Link Employee Structure"),
        "required_employee": required_employee,
        "emp_link_structure_form": emp_link_structure_form,
    }
    return render(request, 'link-structure.html', my_context)


@login_required(login_url='home:user-login')
def update_link_employee_structure(request, pk):
    required_jobRoll = JobRoll.objects.get(id = pk)
    required_employee = get_object_or_404(Employee, pk=required_jobRoll.emp_id.id)
    employee_salary_structure = EmployeeStructureLink.objects.get(
        employee=required_employee)
    emp_link_structure_form = EmployeeStructureLinkForm(
        instance=employee_salary_structure)
    if request.method == 'POST':
        emp_link_structure_form = EmployeeStructureLinkForm(
            request.POST, instance=employee_salary_structure)
        if emp_link_structure_form.is_valid():
            emp_structure_obj = emp_link_structure_form.save(commit=False)
            emp_structure_obj.employee = required_employee
            emp_structure_obj.created_by = request.user
            emp_structure_obj.last_update_by = request.user
            emp_structure_obj.save()
            return redirect('employee:update-employee', pk=pk)
        else:
            print('Form is not valid')
    my_context = {
        "page_title": _("Link Employee Structure"),
        "required_employee": required_employee,
        "emp_link_structure_form": emp_link_structure_form,
    }
    return render(request, 'link-structure.html', my_context)


@login_required(login_url='home:user-login')
def deleteEmployeeView(request, pk):
    required_jobRoll = get_object_or_404(JobRoll, pk=pk)
    required_employee = required_jobRoll.emp_id
    try:
        jobroll_form = JobRollForm(user_v=request.user, instance=required_jobRoll)
        end_date_jobroll_obj = jobroll_form.save(commit=False)
        end_date_jobroll_obj.end_date = date.today()
        end_date_jobroll_obj.save(update_fields=['end_date'])

        emp_form = EmployeeForm(instance=required_employee)
        end_date_obj = emp_form.save(commit=False)
        end_date_obj.end_date = date.today()
        end_date_obj.save(update_fields=['end_date'])

        user_lang = to_locale(get_language())
        if user_lang == 'ar':

            success_msg = ' {},تم حذف الموظف'.format(required_employee)
        else:

            success_msg = 'Employee {} was deleted successfully'.format(
                required_employee)

        # success_msg = 'Employee {} was deleted successfully'.format(
            # required_employee)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{} لم يتم حذف '.format(required_employee)
        else:
            success_msg = '{} cannot be deleted '.format(required_employee)
        # success_msg = 'Employee {} cannot be deleted'.format(
            # required_employee)
        messages.error(request, success_msg)
        raise e
    return redirect('employee:list-employee')



@login_required(login_url='home:user-login')
def deleteEmployeePermanently(request, pk):
    required_employee = get_object_or_404(Employee, pk=pk)
    #required_jobRoll = get_object_or_404(JobRoll, emp_id=pk)
    try:
        required_employee.delete()
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = ' {},تم حذف الموظف'.format(required_employee)
        else:

            success_msg = 'Employee {} was deleted permanently successfully'.format(
                required_employee)
        messages.success(request, success_msg)
    except Exception as e:
        user_lang = to_locale(get_language())
        if user_lang == 'ar':
            success_msg = '{} لم يتم حذف '.format(required_employee)
        else:
            success_msg = '{} cannot be deleted '.format(required_employee)
        # success_msg = 'Employee {} cannot be deleted'.format(
            # required_employee)
        messages.error(request, success_msg)
        raise e
    return redirect('employee:list-employee')



def change_element_value(request):
    element = request.GET.get('element')
    element_value = request.GET.get('value')
    Employee_Element.objects.filter(id=element).update(element_value=element_value)
    element_after_update = Employee_Element.objects.get(id=element)
    element_after_update_element_value = element_after_update.element_value
    data = {'element_after_update_element_value' : element_after_update_element_value,
           'element_value' : element_value
            }
    if element_after_update_element_value !=  element_value :
        data['error_message'] = "Employee Element didn't save "

    return JsonResponse(data)

@login_required(login_url='home:user-login')
def export_employee_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = EmployeeResource()
        dataset = employee_resource.export()

        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="employee_exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="employee_exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="employee_exported_data.xls"'
            return response
    export_context = {
    'page_title':'Please select format of file.',
    }
    #context['fields'] = [f.column_name for f in department_resource.get_user_visible_fields()]
    return render(request, 'export.html', export_context )




@login_required(login_url='home:user-login')
def createJobROll(request, job_id):
    jobroll_form = JobRollForm(user_v=request.user)
    required_jobRoll = JobRoll.objects.get(id=job_id)
    if request.method == "POST":
        jobroll_form = JobRollForm(request.user, request.POST)
        if jobroll_form.is_valid():
            required_jobRoll.end_date = date.today()
            required_jobRoll.save()
            
            job_obj = jobroll_form.save(commit=False)
            job_obj.emp_id = required_jobRoll.emp_id
            job_obj.created_by = request.user
            job_obj.save()
        else:
            print(jobroll_form.errors)
        return redirect('employee:update-employee',
         pk = job_obj.id)

    else:
        return render(request , 'create-jobroll.html' , {'jobroll_form':jobroll_form
        , 'required_employee' :required_jobRoll.emp_id})


@login_required(login_url='home:user-login')
def list_employee_leave_requests(request):
    """
        view to list all approved leave requests for all employees
        author: Ahmed Mamdouh
        created at: 04/03/2021
    """
    employees = Employee.objects.all()
    employees_leaves_approaved_requests = []
    for employee in employees:
        leave_requests = Leave.objects.filter(status='Approved',user=employee.user).values('leavetype__type','startdate','enddate').annotate(x=Count('leavetype__type'))
        leave_masters = LeaveMaster.objects.all()
        z = {
            'employee':employee.emp_name,
            'leave_requests':{}
        }
        z['leave_requests']['total'] = 0
        for master in leave_masters:
            leaves = [dictionary for dictionary in leave_requests if dictionary["leavetype__type"] == master.type]
            if len(leaves) == 0:
                b = 0
            else:
                b = abs((leaves[0]['enddate']-leaves[0]['startdate']).days)
            z['leave_requests'][master.type] = b
            z['leave_requests']['total'] = b + z['leave_requests']['total']
        employees_leaves_approaved_requests.append(z)
        
    context = {
        "leave_requests" : employees_leaves_approaved_requests,
        "leave_masters" : leave_masters,
    }
    return render(request , "list-leaves-history.html" , context)

@login_required(login_url='home:user-login')
def create_employee_element(request, job_id):
    required_jobRoll = JobRoll.objects.get(id = job_id)
    required_employee = get_object_or_404(Employee, pk=required_jobRoll.emp_id.id)
    emp_element_form = EmployeeElementForm()
    if request.method == "POST":
        emp_element_form = EmployeeElementForm(request.POST)
        if emp_element_form.is_valid():
            emp_obj = emp_element_form.save(commit=False)
            emp_obj.emp_id = required_employee
            emp_obj.created_by = request.user
            emp_obj.last_update_by = request.user
            emp_obj.save()
        else:
            print(emp_element_form.errors)
        return redirect('employee:update-employee',
         pk = required_jobRoll.id)

