from django.db.models import Count, Q
from employee.models import Employee
from attendance.models import Attendance
from company.models import Working_Days_Policy, YearlyHoliday
from leave.models import Leave
from service.models import Bussiness_Travel
import datetime
import calendar


class Salary_Calculator:

    def __init__(self, company, employee):
        self.company = company
        self.employee = employee

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

    def employee_absence_days(self, month, year):
        # return list of absence days that will deduct from the employee
        attendances = Attendance.objects.filter(date__month=month, date__year=year, employee=self.employee)
        absence_days = []
        number_of_days = calendar.monthrange(year, month)[1]
        # list all the days in that month
        days = [datetime.date(year, month, day) for day in range(1, number_of_days + 1)]
        attendance_list = list()
        for date in attendances:
            attendance_list.append(date.date)
        missing = sorted(set(days) - set(attendance_list))

        for day in missing:
            if self.is_day_a_weekend(day):
                print("this day is weekend", day)
                pass
            elif self.is_day_a_holiday(day.year, day.month, day):
                print("this day is Holiday", day)
                pass
            elif self.is_day_a_leave(day.year, day.month, day.day):
                print("this day is a leave", day)
                pass
            elif self.is_day_a_service(day.year, day.month, day.day):
                print("this day is a service", day)
                pass
            else:
                absence_days.append(day)
        return absence_days

    # 3- convert dayes from step 1 to hours >> ex: 2(days)*8(working hours policy)=16 hrs
    # 4- get all employee elements and values
    # 5- seperate the adding elements from deductions in []
    # 6- check if element is recaruing or one time element
    # 7- calculate social insurance
    # 8- calculate the gross salary
    # 9- calculate employee hour rate and calculate the deductions value based on step 3
    # 10- recalculate gross salary
    # 11- calculate the tax amount
    # 12- return the net salary
