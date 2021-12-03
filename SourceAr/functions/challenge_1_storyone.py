import Functions.challenge_1_storyone
import Functions.challenge_1_generic as gc
from Functions.Functions import Functions as selenium
import requests


class Challenge1_storyone_:

    def get_abilities(self, pokemon):
        uri = gc.generic_challenge1.get_url(self, "story1", pokemon)
        request = requests.get(uri, params=None)
        info = request.json()
        object_information = []
        for interval in info['abilities']:
            object_information.append(interval['ability']['name'])

        return object_information

    def get_stats(self, pokemon):
        uri = gc.generic_challenge1.get_url(self, "story1", pokemon)
        request = requests.get(uri, params=None)
        info = request.json()
        array_stat = []
        array_base_state = []
        for interval in info['stats']:
            array_base_state.append(interval['base_stat'])
            array_stat.append(interval['stat']['name'])

        object_information_stats = dict(zip(array_stat, array_base_state))
        print(object_information_stats)
        return object_information_stats

    def li_list(self, pokemon):
        html_list = selenium.get_elements(self, "lst_pokemon_result")
        items = html_list.find_elements_by_tag_name("li")
        for item in items:
            new_item = item.text.replace("\n", ",")
            minusculas = new_item.lower()
            if minusculas.find(pokemon.lower()) == 0:
                name = minusculas.split(",")
                return name

    def minus_list(self, element_list):
        list_return = []
        for objetc_list in element_list:
            list_return.append(str(objetc_list).lower())

        return list_return

    def replace_list(self, element_list, first_character, second_character):
        list_return = []
        for objetc_list in element_list:
            list_return.append(str(objetc_list).replace(first_character, second_character))

        return list_return

    def data_comparison(self, lista):
        count = 0
        header_statistics = []
        statistical_data = []
        for fact in lista:
            if count > 0:
                if (lista[count - 1]) == "hp":
                    header_statistics.append("hp")
                    statistical_data.append(int(fact))
                elif (lista[count - 1]) == "atk":
                    header_statistics.append("attack")
                    statistical_data.append(int(fact))
                elif (lista[count - 1]) == "def":
                    header_statistics.append("defense")
                    statistical_data.append(int(fact))
                elif (lista[count - 1]) == "spa":
                    header_statistics.append("special-attack")
                    statistical_data.append(int(fact))
                elif (lista[count - 1]) == "spd":
                    header_statistics.append("special-defense")
                    statistical_data.append(int(fact))
                elif (lista[count - 1]) == "spe":
                    header_statistics.append("speed")
                    statistical_data.append(int(fact))

            count += 1

        object_information_stats = dict(zip(header_statistics, statistical_data))
        print(object_information_stats)
        return object_information_stats



