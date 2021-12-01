# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2021

@author: mmartinez
'''

import unittest
from SourceAr.Functions.Functions import Functions as Selenium


class Test(Selenium, unittest.TestCase):

    def setUp(self):
        Selenium.open_browser(self, "Challenge1")
        Selenium.get_json_file(self, 'Challenge1', 'HomePage')

    def test_initialize(self):
        Selenium.wait_element(self, "SearchBox")
        Selenium.get_elements(self, "SearchBox").send_keys("Okaaaay")
        Selenium.wait(self, 3)

    def tear_down(self):
        Selenium.tear_down(self)


if __name__ == "__main__":
    unittest.main()
