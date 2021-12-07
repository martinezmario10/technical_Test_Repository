# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2021

@author: mmartinez
'''
import unittest
import pytest
from SourceAr.Functions.Functions import Functions as selenium
from Functions.challenge_1_storytwo import Challenge1_storytwo_ as story_two
from Functions.challenge_1_generic import generic_challenge1 as generic


class Test(selenium, unittest.TestCase):

    def setUp(self):
        # value formatting
        selenium.open_browser(self, "Challenge1")
        self.api_availability = 0
        self.attack = "pound".lower()

    def test_story_two(self):
        selenium.get_json_file(self, "Challenge1", "Initial_page")
        self.api_availability = generic.validate_status_query(self, generic.get_url(self, "story2", self.attack))

        # validate availability of initial values.
        if self.api_availability == 1:
            pytest.skip("Try again! Check your search!")
        elif self.api_availability == 0:
            pytest.skip("api not available")
        elif self.attack == "":
            pytest.skip("Try again! Check your search!")

        selenium.get_elements(self, "btn_move").click()
        selenium.get_elements(self, "txt_searchbox").send_keys(self.attack)
        selenium.send_especific_keys(self, "txt_searchbox", "ENTER")
        selenium.get_elements(self, "spn_result").click()

        # get attack value
        value_pp_api = story_two.get_attack(self, self.attack)
        value_description_api = story_two.get_description_attack(self, self.attack)

        # get pp value
        value_pp_web = selenium.extract_pp(self).split()
        value_description_web = selenium.get_elements(self, "lbl_description").text

        # attack value and pp are compared
        if int(value_pp_api) == int(value_pp_web[0]):
            if str(value_description_api).replace("'", "") == str(value_description_web).replace("'", ""):

                print("Attack: " + str(self.attack))
                print("PP: " + str(value_pp_api))
                print("Description: " + str(value_description_web))
            assert value_description_api == value_description_web, "Description is not the same!!"
        else:
            assert int(value_pp_api) == int(value_pp_web[0]), "PP is not the same!!"

    def tearDown(self):
        selenium.tearDown(self)


if __name__ == "__main__":
    unittest.main()
