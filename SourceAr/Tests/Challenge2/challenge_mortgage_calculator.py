# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2021

@author: mmartinez
'''
import time
import unittest
import pytest
import selenium.webdriver.support.select
from Functions.Functions import Functions as selenium
from Functions.challenge_2_mortage_calculation_operations import Challenge2 as challenge2


class Test(selenium, unittest.TestCase):

    def setUp(self):
        # value formatting
        selenium.open_browser(self, "Challenge2")
        self.home_price = 250000
        self.down_payment = 20
        self.loan_term_years = 30
        self.interest_rate = 4
        self.zip_code = "00914"
        self.flag_selection = True

    def test_initialize(self):
        if challenge2.numeric_validation(self, self.home_price, self.down_payment, self.loan_term_years,
                                         self.interest_rate, self.zip_code) < 5:
            pytest.skip("Invalid value")

        # Test start, we clean fields,
        selenium.get_json_file(self, "Challenge2", "home_page")
        challenge2.clean_fields(self)
        months = challenge2.calculation_month(self, self.loan_term_years)

        # internal result
        result_formula = challenge2.mortgage_calculation(self, self.home_price, self.down_payment, months, self.interest_rate)
        selenium.get_elements(self, "txt_home_price").send_keys(str(self.home_price))

        if self.down_payment == 0:
            selenium.get_elements(self, "chk_down_payment_amount").click()
            selenium.get_elements(self, "txt_dollar_down_payment").clear()
            selenium.get_elements(self, "txt_dollar_down_payment").send_keys("0")
            selenium.get_elements(self, "chk_down_payment").click()

        down_payment = selenium.get_elements(self, "txt_down_payment")
        down_payment.clear()
        down_payment.send_keys(str(self.down_payment))
        select_element = selenium.get_elements(self, "slt_loan_term")
        self.flag_selection = selenium.select_option(self, select_element, months)
        if self.flag_selection:
            selenium.get_elements(self, "txt_interest_rate").clear()
            selenium.get_elements(self, "txt_interest_rate").send_keys(str(self.interest_rate))
            selenium.get_elements(self, "txt_zip").clear()
            selenium.get_elements(self, "txt_zip").send_keys(str(self.zip_code))
            selenium.click_js(self, selenium.get_elements(self, "chk_taxes_no"))
            selenium.click_js(self, selenium.get_elements(self, "btn_calculate"))
            selenium.scroll_to(self, "txt_home_price")

            # result obtained on website
            result_website = selenium.get_elements(self, "lbl_fee").text
            result_convert_website = challenge2.convert_result(self, result_website)

            # formula compliance verification
            flag_final_result = challenge2.compliance_percentage(self, float(result_formula),
                                                                 float(result_convert_website))

            if flag_final_result:
                print("Formula result: $" + str(result_formula))
                print("Web site result: " + str(result_website))
                time.sleep(15)

                print("The calculation performed complies with the formula in a 99.99%")

            assert flag_final_result, "The calculation performed does NOT comply with the formula in a 99.99%"

        else:
            pytest.skip("Value not found in loan term")

    def tearDown(self):
        selenium.tearDown(self)


if __name__ == "__main__":
    unittest.main()
