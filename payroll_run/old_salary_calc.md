def _get_insured_emp_basic(self):
    emp_element = Employee_Element.objects.filter(
        emp_id=self.emp, element_id__db_name='001', emp_id__insured=1).filter((Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    emp_basic = 0.0
    for x in emp_element:
        emp_basic += x.element_value
    return emp_basic

def _get_uninsured_emp_basic(self):
    emp_element = Employee_Element.objects.filter(
        emp_id=self.emp, element_id__db_name='001', emp_id__insured=0).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    emp_basic = 0.0
    for x in emp_element:
        emp_basic += x.element_value
    return emp_basic

def _get_emp_income(self):
    emp_allowance = Employee_Element.objects.filter(element_id__classification__code='earn', emp_id=self.emp).filter(
        (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    self.incomes = 0
    for x in emp_allowance:
        self.incomes += x.element_value
    return self.incomes

def _get_emp_deduction_elements(self):
    emp_deductions = Employee_Element.objects.filter(
        element_id__classification__code='deduct', emp_id=self.emp).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
    self.deductions = 0
    for x in emp_deductions:
        self.deductions += x.element_value
    return self.deductions

def _calc_all_incomes(self):
    total_incomes = (
        self._get_emp_income()
    )
    return total_incomes

def _calc_all_deductions(self):
    total_deductions = (
        self._get_emp_deduction_elements()
    )
    return total_deductions

def _calc_variable_salary(self):
    if self.emp.insured == 1:
        total_variable = (self._calc_all_incomes() -
                          self._get_insured_emp_basic())
    else:
        total_variable = (self._calc_all_incomes() -
                          self._get_uninsured_emp_basic())
    return total_variable

def _calc_insurance(self):
    if self.emp.insured == 1:
        emp_job_roll = JobRoll.objects.get(emp_id=self.emp)
        insurance_rule_master = Payroll_Master.objects.get(id=emp_job_roll.payroll.id)
        constant_amount_ratio = insurance_rule_master.social_insurance.basic_deduction_percentage / 100
        variable_amount_ratio = insurance_rule_master.social_insurance.variable_deduction_percentage / 100
        if self._get_insured_emp_basic() <= insurance_rule_master.social_insurance.maximum_insurable_basic_salary:
            constant_amount = self._get_insured_emp_basic() * constant_amount_ratio
        else:
            constant_amount = insurance_rule_master.social_insurance.maximum_insurable_basic_salary * \
                constant_amount_ratio
        if self._calc_variable_salary() <= insurance_rule_master.social_insurance.maximum_insurable_variable_salary:
            variable_amount = self._calc_variable_salary() * variable_amount_ratio
        else:
            variable_amount = insurance_rule_master.social_insurance.maximum_insurable_variable_salary * \
                variable_amount_ratio
        insurance_deduction = constant_amount + variable_amount
        self.insurance_amount = insurance_deduction
        return round(insurance_deduction, 2)
    else:
        return 0.0

def _calc_taxes_deduction(self):
    emp_job_roll = JobRoll.objects.get(emp_id=self.emp)
    tax_rule_master = Payroll_Master.objects.get(id=emp_job_roll.payroll.id)
    personal_exemption = tax_rule_master.tax_rule.personal_exemption
    round_to_10 = tax_rule_master.tax_rule.round_down_to_nearest_10
    tax_deduction_amount = Tax_Deduction_Amount(
        personal_exemption, round_to_10)
    taxable_salary = self._calc_gross_salary()
    taxes = tax_deduction_amount.run_tax_calc(taxable_salary)
    self.tax_amount = taxes
    return round(taxes, 2)

def _calc_gross_salary(self):
    self.gross_salary = self._calc_all_incomes() - self._calc_all_deductions() - \
        self._calc_insurance()
    return self.gross_salary

def _calc_net_salary(self):
    self.net_salary = self._calc_gross_salary() - self._calc_taxes_deduction()
    return self.net_salary

def _validate_is_latest_record(self):
    later_records = Salary_elements.objects.filter(
        salary_month__gte=self.salary_month).filter(salary_year__gte=self.salary_year).filter(is_final=True)
    if len(later_records) > 0:
        raise ValidationError(
            _('There is another Salary record that is later than this one'), code='invalid_date')

def _recalculate_salary(self):
    get_salary = Salary_elements.objects.filter(salary_month=self.salary_month,
                                                salary_year=self.salary_year,
                                                is_final=self.is_final,
                                                element_batch=self.element_batch,
                                                assignment_batch=self.assignment_batch)
    for x in get_salary:
        x.delete()

def clean(self):
    self._validate_is_latest_record()
    self._recalculate_salary()

def save(self):
    self._calc_net_salary()
    super().save()
