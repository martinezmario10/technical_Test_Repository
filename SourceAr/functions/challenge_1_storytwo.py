from Functions.challenge_1_generic import generic_challenge1 as gc
import requests


class Challenge1_storytwo_:

    def get_attack(self, attack):
        uri = gc.get_url(self, "story2", attack)
        request = requests.get(uri, params=None)
        info = request.json()
        pp = info['pp']
        return pp

    def get_description_attack(self, attack):
        uri = gc.get_url(self, "story2", attack)
        request = requests.get(uri, params=None)
        info = request.json()
        object_information = []
        description_value = ""
        for description in info['effect_entries']:
            object_information.append(description['effect'])

        for description_ in object_information:
            description_value = description_

        return description_value

    def data_comparison(self, lista):
        count = 0
        value_pp_attack = ""
        for fact in lista:
            if count > 0:
                if (lista[count - 1]) == "pp":
                    value_pp_attack = str(fact)

            count += 1

        return value_pp_attack



