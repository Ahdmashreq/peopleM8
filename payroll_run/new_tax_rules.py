from defenition.models import TaxRule, Tax_Sections


class Tax_Deduction_Amount:
    def __init__(self, exemption, round_down_to_nearest_10):
        self.exemption = exemption
        self.round_down_to_nearest_10 = round_down_to_nearest_10

    def _tax_special_sextion(self, salary, section_seq_start):
        tax_sections = Tax_Sections.objects.filter(section_execution_sequence__gte=section_seq_start)
        employee_sections = {}
        tax_values = []
        for section in tax_sections:
            if salary >= section.salary_from:
                if salary <= section.salary_to:
                    employee_sections[section.section_execution_sequence] = salary - section.salary_from + 1
                else:
                    if salary > 600000 and section.section_execution_sequence == section_seq_start:
                        employee_sections[section.section_execution_sequence] = section.salary_to
                    else:
                        employee_sections[section.section_execution_sequence] = section.tax_difference
            else:
                break
            for key, values in employee_sections.items():
                if section.section_execution_sequence == key:
                    tax_values.append(values * (section.tax_percentage / 100))
        return sum(tax_values)

    def _tax_calaulation(self, annual_tax_salary):
        employee_sections = {}
        tax_values = []
        # هل المرتب اكثر من 600 الف ؟
        tax_sections = Tax_Sections.objects.filter()
        if annual_tax_salary < 600000:
            return self._tax_special_sextion(annual_tax_salary, 0)
        else:
            # salary from 600,000 to 700,000
            if annual_tax_salary >= 600000 and annual_tax_salary <= 700000:
                return self._tax_special_sextion(annual_tax_salary, 2)
            # salary from 700,000 to 800,000
            elif annual_tax_salary >= 700000 and annual_tax_salary <= 800000:
                return self._tax_special_sextion(annual_tax_salary, 3)
            # salary from 800,000 to 900,000
            elif annual_tax_salary >= 600000 and annual_tax_salary <= 900000:
                return self._tax_special_sextion(annual_tax_salary, 4)
            # salary from 900,000 to 1,000,000
            elif annual_tax_salary >= 600000 and annual_tax_salary <= 1000000:
                return self._tax_special_sextion(annual_tax_salary, 5)
            # salary from 1,000,000 and more
            else:
                return self._tax_special_sextion(annual_tax_salary, 6)

        return Dcimal.from_float(0.0)

    def _calc_annual_tax_salary(self, monthly_salary):
        salary = monthly_salary * 12
        tax_salary = salary - self.exemption
        return self._tax_calaulation(tax_salary)

    def _calculate_monthly_tax(self, yearly_tax_amount):
        if self.round_down_to_nearest_10:
            return round(yearly_tax_amount / 12, 2)
        else:
            return yearly_tax_amount / 12

    def run_tax_calc(self, monthly_salary):
        return self._calculate_monthly_tax(self._calc_annual_tax_salary(monthly_salary))
