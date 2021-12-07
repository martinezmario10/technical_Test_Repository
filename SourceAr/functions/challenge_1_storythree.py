from Functions.challenge_1_generic import generic_challenge1 as gc
from Functions.Functions import Functions as selenium
import requests


class Challenge1_storythree_:

    def get_ability(self, ability):
        uri = gc.get_url(self, "story3", ability)
        request = requests.get(uri, params=None)
        info = request.json()
        object_information = []
        for interval in info['pokemon']:
            object_information.append(str(interval['pokemon']['name']).replace("-", " "))

        return object_information

    # Skills are obtained from the search result.
    def li_ability_result(self):
        html_list = selenium.get_elements(self, "lst_result")
        listq = html_list.find_elements_by_xpath("//span[@class='col pokemonnamecol']")
        abiliti_response = []
        for item in listq:
            new_item = str(item.text.replace("-", " ")).lower()
            abiliti_response.append(new_item)

        return abiliti_response

