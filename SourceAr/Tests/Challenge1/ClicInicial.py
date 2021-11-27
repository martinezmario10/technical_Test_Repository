# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2021

@author: mmartinez
'''

import unittest
from SourceAr.Functions.Functions import Functions as Selenium


class Test(Selenium, unittest.TestCase):

    def setUp(self):
        Selenium.openBrowser(self, "Challenge1")
        Selenium.get_json_file(self, 'HomePage')

    def testInicializar(self):
        Selenium.esperar_elemento(self, "SearchBox")
        Selenium.get_elements(self, "SearchBox").send_keys("Okaaaay")
        Selenium.esperar(self, 10)


def teardown(self):
    Selenium.tearDown(self)


if __name__ == "__main__":
    unittest.main()
