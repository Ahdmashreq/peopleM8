from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, post_init
from django.dispatch import receiver
from notifications.signals import notify
from .models import LeaveMaster, Leave, Employee_Leave_balance
from employee.models import Employee, JobRoll, Employee_Element, Employee_Element_History
from datetime import date
from django.utils.translation import ugettext_lazy as _
from .manager import LeaveManager
from company.models import Enterprise
from datetime import date, datetime
from custom_user.models import User

"""
Ziad
11/3/2021
Class to check employee balance and do all leaves calculations
"""


class Check_Balance():
    def check_balance(emp_id, start_date, end_date , leave):
        month_absence=0
        leave_type_id = Leave.objects.filter(id=leave).values()[0].get("leavetype_id")
        leave_valuee = LeaveMaster.objects.get(id=leave_type_id).leave_value
        print("#######")
        print(leave_valuee)
        employee_leave_balance = Employee_Leave_balance.objects.get(
            employee=emp_id)
        total_balance = employee_leave_balance.total_balance
        employee = Employee.objects.get(id=emp_id.id)
        needed_days = int((end_date.day - start_date.day)) +1
        balance_deductions = needed_days * leave_valuee
        print(total_balance)

        print("casual", employee_leave_balance.casual,
              "usual", employee_leave_balance.usual, "total", total_balance, "needed", needed_days)
        if total_balance >= balance_deductions:
            if employee_leave_balance.casual > 0:
                if employee_leave_balance.casual > balance_deductions:
                    new_balance = employee_leave_balance.casual-balance_deductions
                    Employee_Leave_balance.objects.filter(
                        employee=emp_id).update(casual=new_balance)
                    print("casual", employee_leave_balance.casual,
                          "usual", employee_leave_balance.usual)
                    return True
                else:
                    new_balance = 0
                    # calcuate the new balance
                    new_balance += balance_deductions-employee_leave_balance.casual

                    # set cascual=0
                    Employee_Leave_balance.objects.filter(
                        employee=emp_id).update(casual=0)
                    # calcuate the usual balance
                    new_usual_balance = employee_leave_balance.usual-new_balance
                    # update
                    Employee_Leave_balance.objects.filter(
                        employee=emp_id).update(usual=new_usual_balance)
                    print("casual", employee_leave_balance.casual,
                          "usual", employee_leave_balance.usual)
                    return True
            elif employee_leave_balance.usual > 0:
                if employee_leave_balance.usual > balance_deductions:
                    new_balance = employee_leave_balance.usual-balance_deductions
                    Employee_Leave_balance.objects.filter(
                        employee=emp_id).update(usual=new_balance)
                    print("casual", employee_leave_balance.casual,
                        "usual", employee_leave_balance.usual)
                else:
                    new_balance = 0
                    # calcuate the new balance
                    new_balance += balance_deductions-employee_leave_balance.usual

                    # set cascual=0
                    Employee_Leave_balance.objects.filter(
                        employee=emp_id).update(usual=0)
                    # calcuate the usual balance
                    new_forward_balance = employee_leave_balance.carried_forward-new_balance
                    # update
                    Employee_Leave_balance.objects.filter(
                        employee=emp_id).update(carried_forward=new_forward_balance)

                return True
            else :
                new_balance = employee_leave_balance.carried_forward-balance_deductions
                Employee_Leave_balance.objects.filter(
                    employee=emp_id).update(carried_forward=new_balance)
                return True
        else:
            emp_allowance = Employee_Element.objects.filter(element_id__classification__code='earn',
                                                        emp_id=emp_id).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True))).get(element_id__is_basic=True)
            emp_basic = emp_allowance.element_value
            day_rate = emp_basic / 30
            Employee_Leave_balance.objects.filter(
                    employee=emp_id).update(usual=0)
            Employee_Leave_balance.objects.filter(
                    employee=emp_id).update(casual=0)
            Employee_Leave_balance.objects.filter(
                    employee=emp_id).update(carried_forward=0)
            absence = balance_deductions - total_balance
            total_absence_value = absence*day_rate
            obj = EmployeeAbsence(
                employee = employee ,
                num_of_days = absence ,
                value = total_absence_value  , #We want change to the value of one day absence
                #created_by = request.user
            )
            obj.save()
            total_absence_obj = EmployeeAbsence.objects.filter(
               employee = employee
            )
            total_absence=0
            for i in total_absence_obj:
                total_absence+=i.num_of_days
            Employee_Leave_balance.objects.filter(
                employee=emp_id).update(absence=total_absence)
            return False
