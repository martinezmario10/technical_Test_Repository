from Functions.Functions import Functions as Selenium


class Challenge2:

    def calculation_month(self, loan_term):
        month_number = int(loan_term * 12)
        return month_number

    def mortgage_calculation(self, home_price, down_payment, months, interest_rate):

        # INITIAL Formula = M ( r(1 + r)^n ) / ( (1 + r)^n – 1 )
        # C = Fee to be paid monthly.
        # M = Total amount of the mortgage (less the down payment)
        # i = Monthly interest rate.I = 4 % DIVIDED 12 = 0.04 / 12 = 0.0033333
        # n = Total months in which the mortgage will be paid.

        # sectioned formula
        m = home_price - (home_price * (down_payment / 100))
        r = round(((interest_rate / 100) / 12), 7)
        n = months

        internal_acumulation = 1 + r
        internal_power = pow(internal_acumulation, n)
        internal_multiplication = (r * internal_power)
        internal_subtraction = (internal_power - 1)
        result_part_one = internal_multiplication / internal_subtraction
        final_multiplication = m * result_part_one

        return round(final_multiplication, 2)

    def clean_fields(self):
        Selenium.get_json_file(self, "Challenge2", "home_page")
        # Selenium.get_elements(self, "btn_com").click()
        # Selenium.get_elements(self, "txt_interest_rate").clear()
        # Selenium.get_elements(self, "txt_zip").clear()
        Selenium.get_elements(self, "txt_home_price").clear()
        Selenium.get_elements(self, "txt_dollar_down_payment").clear()
        Selenium.get_elements(self, "chk_down_payment").click()

    # data formatting for integers or floats is validated.
    def numeric_validation(self, home_price, down_payment, loan_term_years, interest_rate, zip_code):
        count = 0
        all_values = [home_price, down_payment, loan_term_years, interest_rate]
        for i in all_values:
            if type(i) == str:
                count -= 1
            else:
                if type(i) == int or type(i) == float:
                    count += 1

        if zip_code.isdigit():
            if len(zip_code) == 5:
                count += 1

        if count == 5:
            if (
                    self.home_price <= 0 or self.down_payment > 100 or self.interest_rate <= 0 or self.interest_rate > 10.0):
                count -= 1

        return count

    def convert_result(self, value):
        new_value = value.lstrip("$")
        new_value_x = new_value.replace(",", "")
        return new_value_x

    def compliance_percentage(self, result_formula, result_website):
        flag = True
        new_total = (float(result_website) * 100) / float(result_formula)

        if (float(new_total) <= 99.99):
            flag = False

        return flag
