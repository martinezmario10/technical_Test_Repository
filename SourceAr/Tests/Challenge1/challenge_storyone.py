# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2021

@author: mmartinez
'''
import unittest
import pytest
from SourceAr.Functions.Functions import Functions as selenium
from Functions.challenge_1_storyone import Challenge1_storyone_ as story_one
from Functions.challenge_1_generic import generic_challenge1 as generic


class Test(selenium, unittest.TestCase):

    def setUp(self):
        # value formatting
        selenium.open_browser(self, "Challenge1")
        self.api_availability = 0
        self.pokemon = "pikachu".lower()
        self.ability_count_eq = 0
        self.ability_count_site = 0

    def test_story_one(self):
        selenium.get_json_file(self, "Challenge1", "Initial_page")
        self.api_availability = generic.validate_status_query(self, generic.get_url(self, "story1", self.pokemon))

        # validate availability of initial values.
        if self.api_availability == 1:
            pytest.skip("Try again! Check your search!")
        elif self.api_availability == 0:
            pytest.skip("api not available")
        elif self.pokemon == "":
            pytest.skip("Try again! Check your search!")

        selenium.get_elements(self, "txt_searchbox").send_keys(self.pokemon)
        selenium.send_especific_keys(self, "txt_searchbox", "ENTER")

        list_abilities_stats_web = generic.li_list(self, self.pokemon)
        list_abilities_stats_api = story_one.get_abilities(self, self.pokemon)

        # character replacement
        list_abilities_stats_web = generic.replace_list(self, list_abilities_stats_web, "-", " ")
        list_abilities_stats_api = generic.replace_list(self, list_abilities_stats_api, "-", " ")

        # comparison of the count of skills that are identical from both the api and pokédex
        for obj_abilities_api in list_abilities_stats_api:
            for obj_abilities_web in list_abilities_stats_web:
                if (obj_abilities_api == obj_abilities_web):
                    self.ability_count_eq += 1

        if (len(list_abilities_stats_api) == self.ability_count_eq):
            dictionary_statistics_api = story_one.get_stats(self, self.pokemon)
            dictionary_statistics_web = story_one.data_comparison(self, list_abilities_stats_web)

            # verification of identical statistics.
            flag_statistics = (dictionary_statistics_api == dictionary_statistics_web)
            if flag_statistics:
                print("Pokemon: " + str(self.pokemon))
                print("Abilities: " + str(list_abilities_stats_api))
                print("Stats: " + str(dictionary_statistics_api))

            assert flag_statistics, "Stats do not match, test failed!"
        else:
            assert len(list_abilities_stats_api) == self.ability_count_eq, "Abilities do not match, test failed!"

    def tearDown(self):
        selenium.tearDown(self)


if __name__ == "__main__":
    unittest.main()
