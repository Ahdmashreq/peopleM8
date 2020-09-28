from defenition.models import TaxRule, New_Tax_Section


class Tax_Deduction:
    def __init__(self, exemption, round_down_to_nearest_10):
        self.exemption = exemption
        self.round_down_to_nearest_10 = round_down_to_nearest_10


    def _tax_calaulation(self, annual_tax_salary):
        employee_sections = {}
        tax_values = []
        # هل المرتب اكثر من 600 الف ؟
        tax_sections = New_Tax_Section.objects.filter()
        if annual_tax_salary < 600000:
            for section in tax_sections:
                # تحديد المرتب في انهي بالشريحة
                if annual_tax_salary >= section.salary_from:
                    if annual_tax_salary <= section.salary_to:
                        employee_sections[section.section_execution_sequence] = annual_tax_salary-section.salary_from+1
                    else:
                        employee_sections[section.section_execution_sequence] = section.tax_difference
                else:
                    break

                for key,values in employee_sections.items():
                    if section.section_execution_sequence == key:
                        tax_values.append(values*(section.tax_percentage/100))
        else:
            pass
        return sum(tax_values)

    def _calc_annual_tax_salary(self, monthly_salary):
        salary = monthly_salary * 12
        tax_salary = salary - self.exemption
        return self._tax_calaulation(tax_salary)


    def _calculate_monthly_tax(self, yearly_tax_amount):
        if self.round_down_to_nearest_10:
            return round(yearly_tax_amount/12, 2)
        else:
            return yearly_tax_amount/12

    def run_tax_calc(self, monthly_salary):
        return self._calculate_monthly_tax(self._calc_annual_tax_salary(monthly_salary))
