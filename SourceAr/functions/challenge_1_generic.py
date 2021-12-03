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

    def validate_status(self, url):
        response_search = generic_challenge1.get_status_code(self, url)
        response_api = generic_challenge1.get_status_code(self, selenium.get_api_endpoint(self, "general"))
        count = 0
        if response_api == 200:
            count = 1

        if response_search == 200:
            count = 2

        return count
