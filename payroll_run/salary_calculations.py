from .models import Taxes
from django.db.models import Count, Q
from datetime import date
from django.db.models import Count, Sum
from attendance.models import Attendance
from company.models import Working_Days_Policy, YearlyHoliday
from leave.models import Leave
from service.models import Bussiness_Travel
from employee.models import Employee, JobRoll, Employee_Element, Employee_Element_History
from element_definition.models import Element_Batch
from manage_payroll.models import Assignment_Batch, Payroll_Master
from payroll_run.new_tax_rules import Tax_Deduction_Amount
from django.utils.translation import ugettext_lazy as _
from .payslip_functions import PayslipFunction
import datetime
import calendar


class Salary_Calculator:

    def __init__(self, company, employee,elements):
        self.company = company
        self.employee = employee
        self.elements = elements

    def workdays_weekends_number(self, month, year):
        output = dict()
        workdays = 0
        weekends = 0
        holidays = 0
        holidays_list = []
        cal = calendar.Calendar()
        company_weekends = self.company_weekends()
        for week in cal.monthdayscalendar(year, month):
            for i, day in enumerate(week):
                # Check if is a weekday and the day is from this month
                if calendar.day_name[i] not in company_weekends and day != 0:
                    workdays += 1

                if calendar.day_name[i] in company_weekends and day != 0:
                    weekends += 1
        yearly_holidays = YearlyHoliday.objects.filter(
            enterprise=self.company, year__year=year).filter(Q(start_date__month=month) | Q(end_date__month=month))
        for x in yearly_holidays:
            if x.start_date.month != month or x.end_date.month != month:
                holidays += x.end_date.day
            else:
                holidays += x.number_of_days_off
            # holidays_list.append(x.start_date)
        output['workdays'] = workdays
        output['weekends'] = weekends
        output['holidays'] = holidays
        return output

    def company_weekends(self):
        company_policy = Working_Days_Policy.objects.get(
            enterprise=self.company)
        company_weekends = company_policy.week_end_days
        weekend_days = []
        for x in company_weekends:
            weekend_days.append(calendar.day_name[int(x)])
        return weekend_days

    def is_day_a_weekend(self, day):
        day_name = calendar.day_name[day.weekday()]
        if day_name in self.company_weekends():
            return True
        else:
            return False

    def holidays_of_the_month(self, year, month):
        holidays_list = []
        holidays = YearlyHoliday.objects.filter(
            enterprise=self.company, year__year=month).filter(Q(start_date__month=month) |
                                                              Q(end_date__month=month))
        for x in holidays:
            holidays_list.append(x.start_date)
        return holidays_list

    def is_day_a_holiday(self, year, month, day):
        if day in self.holidays_of_the_month(year, month):
            return True
        else:
            return False

    def is_day_a_leave(self, year, month, day):
        leave_list = Leave.objects.filter(
            Q(user__id=self.employee.user) & ((Q(startdate__month=month) & Q(startdate__year=month)) | (
                Q(enddate__month=month) & Q(enddate__year=month))))
        for leave in leave_list:
            if (leave.startdate <= date_v <= leave.enddate) and leave.is_approved:
                return True
        return False

    def is_day_a_service(self, year, month, day):
        services_list = Bussiness_Travel.objects.filter(
            Q(emp=self.employee) & (
                (Q(estimated_date_of_travel_from__month=month) & Q(estimated_date_of_travel_from__year=month)) | (
                    Q(estimated_date_of_travel_to__month=month) & Q(estimated_date_of_travel_from__year=month))))
        for service in services_list:
            if (
                    service.estimated_date_of_travel_from <= day <= service.estimated_date_of_travel_to__month) and service.is_approved:
                return True
        return False

    # def employee_absence_days(self, month, year):
    #     # return list of absence days that will deduct from the employee
    #     attendances = Attendance.objects.filter(date__month=month, date__year=year, employee=self.employee)
    #     absence_days = []
    #     number_of_days = calendar.monthrange(year, month)[1]
    #     # list all the days in that month
    #     days = [datetime.date(year, month, day) for day in range(1, number_of_days + 1)]
    #     attendance_list = list()
    #     for date in attendances:
    #         attendance_list.append(date.date)
    #     missing = sorted(set(days) - set(attendance_list))
    #
    #     for day in missing:
    #         if self.is_day_a_weekend(day):
    #             print("this day is weekend", day)
    #             pass
    #         elif self.is_day_a_holiday(day.year, day.month, day):
    #             print("this day is Holiday", day)
    #             pass
    #         elif self.is_day_a_leave(day.year, day.month, day.day):
    #             print("this day is a leave", day)
    #             pass
    #         elif self.is_day_a_service(day.year, day.month, day.day):
    #             print("this day is a service", day)
    #             pass
    #         else:
    #             absence_days.append(day)
    #     return absence_days
    # calculate total employee earnings
    def calc_emp_income(self):
        #TODO filter employee element with start date
        emp_allowance = Employee_Element.objects.filter(element_id__in=self.elements,element_id__classification__code='earn',
                                                        emp_id=self.employee).filter(
            (Q(end_date__gt=date.today()) | Q(end_date__isnull=True)))

        total_earnnings = 0.0
        #earning | type_amount | mounthly
        for x in emp_allowance:
            payslip_func = PayslipFunction()
            if payslip_func.get_element_classification(x.element_id.id) == 'earn' and \
                    payslip_func.get_element_amount_type(x.element_id.id) == 'fixed amount' and \
                    payslip_func.get_element_scheduled_pay(x.element_id.id) == 'monthly':
                if x.element_value:
                    total_earnnings += x.element_value
                else:
                    total_earnnings += 0.0
        return total_earnnings

    # حساب اجر اليوم و سعر الساعة
    def calc_daily_rate(self):
        company_policy = Working_Days_Policy.objects.get(
            enterprise=self.company)
        # عدد ساعات العمل للشركة
        company_working_hrs = company_policy.number_of_daily_working_hrs
        emp_allowance = Employee_Element.objects.filter(element_id__in=self.elements,element_id__classification__code='earn',
                                                        emp_id=self.employee).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True))).get(element_id__basic_flag=True)
        emp_basic = emp_allowance.element_value  # المرتب الاساسي للعامل
        hour_rate = (emp_basic / 30) / company_working_hrs
        return hour_rate

    # calculate employee deductions without social insurance
    #3 + deduction
    def calc_emp_deductions_amount(self):
        # TODO : Need to filter with start date
        emp_deductions = Employee_Element.objects.filter(element_id__in=self.elements,
            element_id__classification__code='deduct', emp_id=self.employee).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        total_deductions = 0
        payslip_func = PayslipFunction()
        for x in emp_deductions:
            if payslip_func.get_element_classification(x.element_id.id) == 'deduct' and \
                payslip_func.get_element_amount_type(x.element_id.id) == 'fixed amount' and \
                payslip_func.get_element_scheduled_pay(x.element_id.id) == 'monthly':
                if x.element_value:
                    total_deductions += x.element_value
                else:
                    total_deductions += 0.0
        return total_deductions

    # calculate social insurance
    def calc_employee_insurance(self):
        if self.employee.insured:
            required_employee = Employee.objects.get(id=self.employee.id)
            insurance_deduction = 0
            if required_employee.insurance_salary:
                insurance_deduction = required_employee.insurance_salary * 0.11
            else:
                insurance_deduction = 0.0
            total_insurance_amount = insurance_deduction
            return round(total_insurance_amount, 3)
        else:
            return 0.0

    # calculate gross salary
    def calc_gross_salary(self):
        gross_salary = self.calc_emp_income() - (self.calc_emp_deductions_amount() +
                                                 self.calc_employee_insurance())
        return gross_salary

    # calculate tax amount
    #
    def calc_taxes_deduction(self):
        required_employee = Employee.objects.get(id=self.employee.id)
        tax_rule_master = Payroll_Master.objects.get(
            enterprise=required_employee.enterprise)
        personal_exemption = tax_rule_master.tax_rule.personal_exemption
        round_to_10 = tax_rule_master.tax_rule.round_down_to_nearest_10
        tax_deduction_amount = Tax_Deduction_Amount(
            personal_exemption, round_to_10)
        taxable_salary = self.calc_gross_salary()
        taxes = tax_deduction_amount.run_tax_calc(taxable_salary)
        self.tax_amount = taxes
        return round(taxes, 2)

    # calculate net salary
    def calc_net_salary(self):
        net_salary = self.calc_gross_salary() - self.calc_taxes_deduction()
        return net_salary


    def net_to_gross(self):

        taxes=0
        diffrence=0
        percent=0    
        basic_net =Employee_Element.objects.filter(element_id__element_name="Basic Net", emp_id=self.employee).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))[0].element_value
        
        allowence = self.calc_emp_income()
        deductions = self.calc_emp_deductions_amount()
        insurence = self.calc_employee_insurance()
        final_net = ( basic_net + allowence - (deductions + insurence) )
        year_net = (final_net * 12) - 9000
        values = Taxes.objects.all()
        for x in values :
            if float(year_net)>x.start_range and float(year_net)<=x.end_range:
                percent = x.percent
                break
            else:
                taxes+=x.tax
                diffrence+=x.diffrence
        dummy = float(year_net)+taxes-diffrence
        dummy2= dummy/(1-percent)
        dummy3= dummy2*percent 
        #print(taxes)
        #print(dummy3)
        final_tax=round(taxes + dummy3,3)/12
        gross_salary = round(final_tax +float(final_net),3)





        print("################")
        print(final_net)
        print(final_tax)
        print(gross_salary)
        

        

