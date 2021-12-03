from Functions.Functions import Functions as selenium

import requests


class generic_challenge1:

    def get_status_code(self, uri):
        response = requests.get(uri, params=None)
        return response.status_code

    def get_url(self, story, pokemon):
        if story == "story1":
            self.url = selenium.get_api_endpoint(self, "general")
            self.url += "/api/v2/pokemon/" + pokemon
            return self.url
        elif story == "story2":
            self.url = selenium.get_api_endpoint(self, "general")
            self.url += "/api/v2/move/" + pokemon
            return self.url

    def validate_status(self, url):
        response_search = generic_challenge1.get_status_code(self, url)
        response_api = generic_challenge1.get_status_code(self, selenium.get_api_endpoint(self, "general"))
        count = 0
        if response_api == 200:
            count = 1

        if response_search == 200:
            count = 2

        return count

    def replace_list(self, element_list, first_character, second_character):
        list_return = []
        for objetc_list in element_list:
            list_return.append(str(objetc_list).replace(first_character, second_character))

        return list_return

    def minus_list(self, element_list):
        list_return = []
        for objetc_list in element_list:
            list_return.append(str(objetc_list).lower())

        return list_return

    def li_list(self, value_to_compare):
        html_list = selenium.get_elements(self, "lst_result")
        items = html_list.find_elements_by_tag_name("li")
        for item in items:
            new_item = item.text.replace("\n", ",")
            minusculas = new_item.lower()
            if minusculas.find(value_to_compare.lower()) == 0:
                name = minusculas.split(",")
                return name
