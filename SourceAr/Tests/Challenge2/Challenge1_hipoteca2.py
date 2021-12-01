# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2021

@author: mmartinez
'''

import unittest
import pytest
import selenium.webdriver.support.select

from Functions.Functions import Functions as selenium
from Functions.challenge_2_mortage_calculation_operations import Challenge2 as challenge2


class Test(selenium, unittest.TestCase):

    def setUp(self):
        self.home_price = 250000
        self.down_payment = 50
        self.loan_term_years = 30
        self.interest_rate = 4
        self.zip_code = 11011
        self.flag_selection = True
        selenium.open_browser(self, "Challenge2")
        selenium.get_json_file(self, "Challenge2", "home_page")

    def test_initialize(self):
        challenge2.clean_fields(self)
        months = challenge2.calculation_month(self, self.loan_term_years)
        result = challenge2.mortgage_calculation(self, self.home_price, self.down_payment, months, self.interest_rate)
        selenium.get_elements(self, "txt_home_price").send_keys(self.home_price)
        down_payment = selenium.get_elements(self, "txt_down_payment")
        down_payment.clear()
        down_payment.send_keys(self.down_payment)
        select_element = selenium.get_elements(self, "slt_loan_term")
        self.flag_selection = selenium.select_option(self, select_element, self.loan_term_years)
        if self.flag_selection:
            selenium.scroll_to(self, "txt_interest_rate")
            selenium.get_elements(self, "txt_interest_rate").send_keys(self.interest_rate)
            selenium.get_elements(self, "txt_zip").send_keys(self.zip_code)
            selenium.get_elements(self, "chk_taxes_no").click()
            selenium.scroll_to(self, "btn_calculate")
            selenium.get_elements(self, "btn_calculate").click()
            selenium.scroll_to(self, "lbl_fee")
            resulte = selenium.get_elements(self, "lbl_fee").text


            pass
        else:
            pytest.skip("Value not found in loan term")


    def tearDown(self):
        selenium.tear_down(self)


if __name__ == "__main__":
    unittest.main()
