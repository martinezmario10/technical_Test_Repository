# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2021

@author: mmartinez
'''
import unittest
import pytest
from SourceAr.Functions.Functions import Functions as selenium
from Functions.challenge_1_storythree import Challenge1_storythree_ as story_three
from Functions.challenge_1_generic import generic_challenge1 as generic


class Test(selenium, unittest.TestCase):

    def setUp(self):
        # value formatting
        selenium.open_browser(self, "Challenge1")
        self.api_availability = 0
        self.ability = "protean".lower()

    def test_story_three(self):
        selenium.get_json_file(self, "Challenge1", "Initial_page")
        self.api_availability = generic.validate_status_query(self, generic.get_url(self, "story3", self.ability))

        # validate availability of initial values.
        if self.api_availability == 1:
            pytest.skip("Try again! Check your search!")
        elif self.api_availability == 0:
            pytest.skip("api not available")
        elif self.ability == "":
            pytest.skip("Try again! Check your search!")

        selenium.get_elements(self, "btn_pokemon").click()
        selenium.get_elements(self, "txt_searchbox").send_keys(self.ability)

        include_abilitie_api = story_three.get_ability(self, self.ability)
        include_abilitie_web = story_three.li_ability_result(self)

        # We validate if it is the same amount of pokémon with the selected ability.
        if len(include_abilitie_api) == len(include_abilitie_web):
            print(include_abilitie_web)
            print(include_abilitie_api)
            assert include_abilitie_api == include_abilitie_web, "The amount is not the same!!"
        else:
            assert include_abilitie_api == include_abilitie_web, "The amount is not the same!!"

    def tearDown(self):
        selenium.tearDown(self)


if __name__ == "__main__":
    unittest.main()
