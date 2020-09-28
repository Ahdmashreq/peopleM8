from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import DetailView, ListView, View
from django.contrib import messages
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils.translation import to_locale, get_language
from django.db.models import Q
import calendar
from django.db.models import Avg, Count
from payroll_run.models import Salary_elements
from payroll_run.forms import SalaryElementForm, Salary_Element_Inline
from element_definition.models import Element_Master, Element_Detail, Element_Batch, Element_Batch_Master
from manage_payroll.models import Assignment_Batch, Assignment_Batch_Include, Assignment_Batch_Exclude
from employee.models import Employee_Element, Employee, JobRoll, Payment
from employee.forms import Employee_Element_Inline
from django.utils.translation import ugettext_lazy as _
# ############################################################
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
# ############################################################
from .new_tax_rules import Tax_Deduction

@login_required(login_url='/login')
def listSalaryView(request):
    new_tax = Tax_Deduction(9000,True)
    print('*****************************************************')
    print(new_tax.run_tax_calc(10000))
    salary_list = Salary_elements.objects.filter(
        (Q(end_date__gt=date.today()) | Q(end_date__isnull=True))).values(
            'salary_month', 'salary_year',
            'is_final').annotate(num_salaries=Count('salary_month'))
    salaryContext = {
        "page_title": _("salary list"),
        "salary_list": salary_list,
    }
    return render(request, 'list-salary.html', salaryContext)


@login_required(login_url='/login')
def includeAssignmentEmployeeFunction(id):
    included_emps = set()
    include_query = Assignment_Batch_Include.objects.filter(
        include_batch_id=id).exclude(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    dept_set = set()
    job_set = set()
    position_set = set()
    emp_set = set()
    for x in include_query:
        if x.dept_id is not None:
            dept_set.add(x.dept_id.id)
        if x.position_id is not None:
            position_set.add(x.position_id.id)
        if x.job_id is not None:
            job_set.add(x.job_id.id)
        if x.emp_id is not None:
            emp_set.add(x.emp_id.id)
    filtered_emps = JobRoll.objects.filter(
        (Q(department__id__in=dept_set) | Q(position__id__in=position_set)
         | Q(job_name__id__in=job_set) | Q(emp_id__id__in=emp_set)))
    for emp in filtered_emps:
        included_emps.add(emp.emp_id)
    return included_emps


@login_required(login_url='/login')
def excludeAssignmentEmployeeFunction(id):
    excluded_emps = set()
    exclude_query = Assignment_Batch_Exclude.objects.filter(
        exclude_batch_id=id).exclude(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    dept_set = set()
    job_set = set()
    position_set = set()
    emp_set = set()
    for x in exclude_query:
        if x.dept_id is not None:
            dept_set.add(x.dept_id.id)
        if x.position_id is not None:
            position_set.add(x.position_id.id)
        if x.job_id is not None:
            job_set.add(x.job_id.id)
        if x.emp_id is not None:
            emp_set.add(x.emp_id.id)
    filtered_emps = JobRoll.objects.filter(
        (Q(department__id__in=dept_set) | Q(position__id__in=position_set)
         | Q(job_name__id__in=job_set) | Q(emp_id__id__in=emp_set)))
    for emp in filtered_emps:
        excluded_emps.add(emp.emp_id)
    return excluded_emps


@login_required(login_url='/login')
def createSalaryView(request):
    sal_form = SalaryElementForm()
    if request.method == 'POST':
        sal_form = SalaryElementForm(request.POST)
        if sal_form.is_valid():
            sal_obj = sal_form.save(commit=False)
            # run employee on all emps.
            if sal_obj.element_batch == None and sal_obj.assignment_batch == None:
                for x in Employee.objects.filter(
                                                 (Q(end_date__gte=date.today())
                                                  |Q(end_date__isnull=True))
                                                        ):
                    # calculate all furmulas elements for 'x' employee
                    Employee_Element.set_formula_amount(x)
                    # ################################################
                    s = Salary_elements(
                        emp=x,
                        salary_month=sal_obj.salary_month,
                        salary_year=sal_obj.salary_year,
                        run_date=sal_obj.run_date,
                        num_days=sal_obj.num_days,
                        element_batch=sal_obj.element_batch,
                        created_by=request.user,
                        last_update_by=request.user,
                    )
                    s.save()
                user_lang = to_locale(get_language())
                if user_lang == 'ar':
                    success_msg = 'تم تشغيل راتب شهر {} بنجاح'.format(
                        calendar.month_name[sal_obj.salary_month])
                else:
                    success_msg = 'Payroll for month {} done successfully'.format(
                        calendar.month_name[sal_obj.salary_month])
                messages.success(request, success_msg)
            # the user select element batch to run on without assignment batch.
            elif sal_obj.element_batch and sal_obj.assignment_batch == None:
                elements_in_batch = get_list_or_404(
                    ElementBatchMaster, element_batch_fk=sal_obj.element_batch)
                emp_in_batch = Employee_Element.objects.filter(
                    element_id__elementMaster__in=elements_in_batch)
                emps = set()
                for x in emp_in_batch:
                    emps.add(x.emp_id)
                for x in emps:
                    # calculate all furmulas elements for 'x' employee
                    Employee_Element.set_formula_amount(x)
                    # # ################################################
                    # # # getting informations for the salary
                    s = Salary_elements(
                        emp=x,
                        salary_month=sal_obj.salary_month,
                        salary_year=sal_obj.salary_year,
                        run_date=sal_obj.run_date,
                        num_days=sal_obj.num_days,
                        element_batch=sal_obj.element_batch,
                        created_by=request.user,
                        last_update_by=request.user,
                    )
                    s.save()
                user_lang = to_locale(get_language())
                if user_lang == 'ar':
                    success_msg = 'تم تشغيل الراتب بنجاح {} '.format(
                        sal_obj.salary_month)
                else:
                    success_msg = 'Payroll for month {} done successfully'.format(
                        sal_obj.salary_month)
                messages.success(request, success_msg)
            # the user select assignment batch without element batch to run on.
            elif sal_obj.assignment_batch and sal_obj.element_batch == None:
                emps = Employee.objects.filter(
                    id__in=includeAssignmentEmployeeFunction(
                        sal_obj.assignment_batch.id)).exclude(
                            id__in=excludeAssignmentEmployeeFunction(
                                sal_obj.assignment_batch.id))
                for x in emps:
                    # calculate all furmulas elements for 'x' employee
                    Employee_Element.set_formula_amount(x)
                    # # ################################################
                    # # # getting informations for the salary
                    s = Salary_elements(
                        emp=x,
                        salary_month=sal_obj.salary_month,
                        salary_year=sal_obj.salary_year,
                        run_date=sal_obj.run_date,
                        num_days=sal_obj.num_days,
                        element_batch=sal_obj.element_batch,
                        created_by=request.user,
                        last_update_by=request.user,
                    )
                    s.save()
                user_lang = to_locale(get_language())
                if user_lang == 'ar':
                    success_msg = 'تم تشغيل الراتب بنجاح {} '.format(
                        sal_obj.salary_month)
                else:
                    success_msg = 'Payroll for month {} done successfully'.format(
                        sal_obj.salary_month)
                messages.success(request, success_msg)
            # the user select both assignment batch and element batch to run on.
            elif sal_obj.assignment_batch and sal_obj.element_batch:
                all_emps = set()
                emp_in_assignment = Employee.objects.filter(
                    id__in=includeAssignmentEmployeeFunction(
                        sal_obj.assignment_batch.id)).exclude(
                            id__in=excludeAssignmentEmployeeFunction(
                                sal_obj.assignment_batch.id))
                for emp in emp_in_assignment:
                    all_emps.add(emp)
                elements_in_batch = get_list_or_404(
                    ElementBatchMaster, element_batch_fk=sal_obj.element_batch)
                emp_in_element_batch = Employee_Element.objects.filter(
                    element_id__elementMaster__in=elements_in_batch)
                for emp in emp_in_element_batch:
                    all_emps.add(x.emp_id)
                for x in all_emps:
                    # calculate all furmulas elements for 'x' employee
                    Employee_Element.set_formula_amount(x)
                    # # ################################################
                    # # # getting informations for the salary
                    s = Salary_elements(
                        emp=x,
                        salary_month=sal_obj.salary_month,
                        salary_year=sal_obj.salary_year,
                        run_date=sal_obj.run_date,
                        num_days=sal_obj.num_days,
                        element_batch=sal_obj.element_batch,
                        created_by=request.user,
                        last_update_by=request.user,
                    )
                    s.save()
                user_lang = to_locale(get_language())
                if user_lang == 'ar':
                    success_msg = 'تم تشغيل الراتب بنجاح {} '.format(
                        sal_obj.salary_month)
                else:
                    success_msg = 'Payroll for month {} done successfully'.format(
                        sal_obj.salary_month)
                messages.success(request, success_msg)
        else:  # Form was not valid
            messages.error(request, sal_form.errors)
        # return redirect('payroll_run:create-salary')
    salContext = {
        'page_title': _('create salary'),
        'sal_form': sal_form,
    }
    return render(request, 'create-salary.html', salContext)


def month_name(month_number):
    return calendar.month_name[month_number]


@login_required(login_url='/login')
def listSalaryFromMonth(request, month, year):
    salaries_list = Salary_elements.objects.filter(
        salary_month=month, salary_year=year)
    monthSalaryContext = {
        'page_title': _('salaries for month {}').format(month_name(month)),
        'salaries_list': salaries_list,
        'v_month': month,
        'v_year': year
    }
    return render(request, 'list-salary-month.html', monthSalaryContext)


@login_required(login_url='/login')
def changeSalaryToFinal(request, month, year):
    draft_salary = Salary_elements.objects.filter(
        salary_month=month, salary_year=year)
    for draft in draft_salary:
        draft.is_final = True
        draft.save()
    return redirect('payroll_run:list-salary')


@login_required(login_url='/login')
def userSalaryInformation(request, month_number, salary_year, salary_id,emp_id):
    salary_obj = get_object_or_404(
                                   Salary_elements,
                                   salary_month=month_number,
                                   salary_year=salary_year,
                                   pk=salary_id
                                   )
    emp_elements_incomes = Employee_Element.objects.filter(
                                                           emp_id=emp_id,
                                                           element_id__classification__code='earn',
                                                           start_date__month=month_number
                                                           )
    emp_elements_deductions = Employee_Element.objects.filter(emp_id=emp_id,
                                                              element_id__classification__code='deduct',
                                                              start_date__month=month_number
                                                              )
    emp_payment = Payment.objects.filter((Q(end_date__gte=date.today()) | Q(end_date__isnull=True)),emp_id=emp_id)
    monthSalaryContext = {
        'page_title': _('salary information for {}').format(salary_obj.emp),
        'salary_obj': salary_obj,
        'emp_elements_incomes': emp_elements_incomes,
        'emp_elements_deductions': emp_elements_deductions,
        'emp_payment': emp_payment,
    }
    return render(request, 'emp-payslip.html', monthSalaryContext)


@login_required(login_url='/login')
def render_emp_payslip(request, month, year, salary_id, emp_id):
    template_path = 'payslip.html'
    salary_obj = get_object_or_404(
        Salary_elements, salary_month=month, salary_year=year, pk=salary_id)
    emp_elements = Employee_Element.objects.filter(emp_id=emp_id)
    context = {
        'salary_obj': salary_obj,
        'emp_elements': emp_elements,
        'company_name': request.user.company,
    }
    response = HttpResponse(content_type="application/pdf")
    response[
        'Content-Disposition'] = "inline; filename={date}-donation-receipt.pdf".format(
            date=date.today().strftime('%Y-%m-%d'), )
    html = render_to_string(template_path, context)
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response


@login_required(login_url='/login')
def render_all_payslip(request, month, year):
    template_path = 'all-payslip.html'
    all_salary_obj = get_list_or_404(
        Salary_elements, salary_month=month, salary_year=year)
    new_thing = {}
    for sal in all_salary_obj:
        emp_elements = Employee_Element.objects.filter(emp_id=sal.emp.id)
        new_thing['emp_salary'] = sal
        new_thing['emp_elements'] = emp_elements
    context = {
        'all_salary_obj': all_salary_obj,
        'emp_elements': new_thing['emp_elements'],
        'company_name': request.user.company,
    }
    response = HttpResponse(content_type="application/pdf")
    response[
        'Content-Disposition'] = "inline; filename={date}-donation-receipt.pdf".format(
            date=date.today().strftime('%Y-%m-%d'), )
    html = render_to_string(template_path, context)
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response

@login_required(login_url='/login')
def delete_salary_view(request, month, year):
    required_salary = Salary_elements.objects.filter(salary_month=month, salary_year=year)
    for sal in required_salary:
        sal.end_date = date.today()
        sal.save()
    return redirect('payroll_run:list-salary')
