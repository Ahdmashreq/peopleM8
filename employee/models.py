from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from defenition.models import LookupType, LookupDet
from company.models import (Enterprise, Department, Grade, Position, Job)
from manage_payroll.models import (Bank_Master, Payroll_Master)
from element_definition.models import Element_Master, Element_Detail, Element_Link
from employee.fast_formula import FastFormula
from django.utils.translation import ugettext_lazy as _

payment_type_list = [("c", _("Cash")), ("k", _("Check")),
                     ("b", _("Bank transfer")), ]
account_type_list = [('c', _('Company account')), ('e', _('Employee account'))]


class Employee(models.Model):
    identification_type_list = [("N", _("National Id")), ("P", _("Passport"))]
    gender_list = [("M", _("Male")), ("F", _("Female"))]
    social_status_list = [("M", _("Married")), ("S", _("Single"))]
    military_status_list = [("E", _("Exemption")), ("C", _("Complete the service")), ("P", _("Postponed"))]
    religion_list = [("M", _("Muslim")), ("C", _("Chrestin"))]
    # ##########################################################################
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='employee_user')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE,related_name='enterprise_employee', verbose_name=_('Department'))
    emp_number = models.IntegerField(default=0, blank=True, null=True, verbose_name=_('Employee Number'))
    emp_name = models.CharField(max_length=60, verbose_name=_('Employee Name'))
    address1 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('address1'))
    address2 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('address2'))
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('phone'))
    mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('mobile'))
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Birthdate'))
    hiredate = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Hire Date'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    picture = models.ImageField(null=True, blank=True, verbose_name=_('picture'))
    is_active = models.BooleanField(blank=True, default=True, verbose_name=_('Is Active'))
    identification_type	= 	models.CharField(max_length=5, choices=identification_type_list, null=True, blank=True, verbose_name=_('ID Type'))
    id_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('ID Number'))
    place_of_birth = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Place of Birth'))
    nationality = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Nationality'))
    field_of_study = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Field of Study'))
    education_degree = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Eductaion Degree'))
    gender = models.CharField(max_length=5, choices=gender_list, null=True, blank=True, verbose_name=_('Gender'))
    social_status	= 	models.CharField(max_length=5, choices=social_status_list, null=True, blank=True, verbose_name=_('Social Status'))
    military_status	= 	models.CharField(max_length=5, choices=military_status_list, null=True, blank=True, verbose_name=_('Milatery Status'))
    religion	= 	models.CharField(max_length=5, choices=religion_list, null=True, blank=True, verbose_name=_('Religion'))
    insured = models.BooleanField(verbose_name=_('Insured'))
    insurance_number = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Insurance Number'))
    insurance_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Insurance Date'))
    has_medical = models.BooleanField(verbose_name=_('Has Medical'))
    medical_number = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Medical Number'))
    medical_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Medical Date'))
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="emp_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE)
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse("list-employee", kwargs={"pk": self.id})

    def __str__(self):
        return self.emp_name


class Medical(models.Model):
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Employee'))
    medical_code = models.CharField(
        max_length=20, verbose_name=_('Medical Code'))
    medical_name = models.CharField(
        max_length=20, verbose_name=_('Medical Name'))
    medical_company = models.CharField(
        max_length=20, verbose_name=_('Medical Company'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="medical_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="medical_last_update_by")

    def __str__(self):
        return self.emp_id.emp_name


class JobRoll(models.Model):
    emp_type_list = [("A", _("Admin")),
                       ("E", _("Employee")) ]
    # ###########################################################################################
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE,
                               null=True, blank=True, related_name='job_roll_emp_id', verbose_name=_('Employee'))
    manager = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='manager_id', verbose_name=_('Manager'))
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Position'))
    contract_type	= 	models.ForeignKey(LookupDet, on_delete=models.CASCADE, null=True, blank=True, related_name='jobroll_contract_type', verbose_name=_('Contract Type'))
    payroll = models.ForeignKey(Payroll_Master, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Payroll'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="jobRoll_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="jobroll_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)


class Payment(models.Model):
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    payment_method = models.ForeignKey(
        'manage_payroll.Payment_Method', on_delete=models.CASCADE, related_name='emp_payment_method', verbose_name=_('Payment Method'))
    account_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_('Account Number'))
    percentage = models.IntegerField(default=100, validators=[
                                     MaxValueValidator(100), MinValueValidator(0)], verbose_name=_('Percentage'))
    bank_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_('Bank Name'))
    swift_code = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_('Swift Code'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="payment_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="payment_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.payment_method.payment_type.type_name


class Employee_Element(models.Model):
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    element_id = models.ForeignKey(
        Element_Master, on_delete=models.CASCADE, verbose_name=_('Element'))
    element_value = models.FloatField(
        blank=True, null=True, verbose_name=_('Element Value'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="emp_element_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="emp_element_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def set_formula_amount(emp):
        print("inside set_formula_amount")
        formula_element = Employee_Element.objects.filter(emp_id=emp.id,element_id__element_formula__isnull=False)
        # emp_element = Employee_Element.objects.filter(emp_id=emp.id)
        for x in formula_element:
            print("inside set_formula_amount in the foor loop")
            if x.element_value ==0:
                print("inside set_formula_amount in the if statement")
                value = FastFormula(emp.id, x.element_id, Employee_Element)
                x.element_value = value.get_formula_amount()
                # for z in emp_element:
                #     if x.element_id == z.element_id:
                #         z.element_value = value.get_formula_amount()
                x.save()

    def get_element_value(self):
        element_dic = {}
        element_master_obj = Element_Master.objects.filter().exclude(fixed_amount=0)
        for element in element_master_obj:
            element_dic[element.id]=(element.fixed_amount)
        emp_elements = Employee_Element.objects.filter(emp_id=self.emp_id)
        for element in element_dic:
            if self.element_id.id == element:
                self.element_value = element_dic[element]

    def save(self):
        self.get_element_value()
        super().save()

    def __str__(self):
        return self.element_id.element_name
