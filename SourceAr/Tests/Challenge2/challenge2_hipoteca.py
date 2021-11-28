# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2021

@author: mmartinez
'''

import unittest
from SourceAr.Functions.Functions import Functions as Selenium
from SourceAr.Functions.challenge2_operations import Challenge2 as challenge2


class Test(Selenium, unittest.TestCase):

    def setUp(self):
        Selenium.open_browser(self, "Challenge2")
        Selenium.get_json_file(self, 'Challenge2', 'HomePage')
        self.home_price = 250000
        self.down_payment = 20
        self.loan_term_years = 30
        self.interest_rate = 4



    def test_initialize(self):
        months = challenge2.calculation_month(self, self.loan_term_years)
        result = challenge2.mortgage_calculation(self, self.home_price, self.down_payment, months, self.interest_rate)


        #Selenium.wait_element(self, "chk_taxes_no")
        #Selenium.get_elements(self, "chk_taxes_no").click()
        #Selenium.wait(self, 8)

    def tear_down(self):
        Selenium.tear_down(self)




if __name__ == "__main__":
    unittest.main()
