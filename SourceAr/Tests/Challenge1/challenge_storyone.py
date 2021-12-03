# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2021

@author: mmartinez
'''
import time
import unittest

import pytest

from SourceAr.Functions.Functions import Functions as selenium
from Functions.challenge_1_storyone import Challenge1_storyone_ as story_one
from Functions.challenge_1_generic import generic_challenge1 as generic


class Test(selenium, unittest.TestCase):

    def setUp(self):
        selenium.open_browser(self, "Challenge1")
        self.api_availability = 0
        self.pokemon = "xurkitree".lower()
        self.ability_count_eq = 0
        self.ability_count_site = 0

    def test_story_one(self):
        selenium.get_json_file(self, "Challenge1", "Initial_page")
        self.api_availability = generic.validate_status(self, generic.get_url(self, "story1", self.pokemon))

        if self.api_availability == 1:
            pytest.skip("Try again! Check your search!")
        elif self.api_availability == 0:
            pytest.skip("api not available")

        selenium.get_elements(self, "txt_searchbox").send_keys(self.pokemon)
        selenium.send_especific_keys(self, "txt_searchbox", "ENTER")

        list_abilities_stats = generic.li_list(self, self.pokemon)
        abilities = story_one.get_abilities(self, self.pokemon)

        list_abilities_stats = generic.replace_list(self, list_abilities_stats, "-", " ")
        abilities = generic.replace_list(self, abilities, "-", " ")

        for obj_abilities_api in abilities:
            for obj_abilities_web in list_abilities_stats:
                if (obj_abilities_api == obj_abilities_web):
                    self.ability_count_eq += 1

        if (len(abilities) == self.ability_count_eq):
            dictionary_api_statistics = story_one.get_stats(self, self.pokemon)
            dictionary_web_statistics = story_one.data_comparison(self, list_abilities_stats)
            flag_statistics = (dictionary_api_statistics == dictionary_web_statistics)
            if flag_statistics:
                print("Pokemon: " + str(self.pokemon))
                print("Abilities: " + str(abilities))
                print("Stats: " + str(dictionary_api_statistics))

            assert flag_statistics, "Stats do not match, test failed!"
        else:
            assert len(abilities) == self.ability_count_eq, "Abilities do not match, test failed!"

    def tearDown(self):
        selenium.tearDown(self)


if __name__ == "__main__":
    unittest.main()
