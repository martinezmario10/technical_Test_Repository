import os


class Initialize():
    basedir = os.path.abspath(os.path.join(__file__, "../../"))
    date_format = '%d/%m/%y'
    hour_format = '%H%M%S'

    # JsonData
    Json = basedir + u'\Pages'
    environment = 'QA'

    # Test Browser
    browser = u'FIREFOX'

    # Directory / Evidence Storage During Execution
    path_evidences = basedir + u'\Data\ScreenShots'

    # Environment variable
    if environment == 'QA':
        url = {"Challenge1": "https://dex.pokemonshowdown.com",
               "Challenge2": "https://www.rocketmortgage.com/calculators/mortgage-calculator?qlsource=RMTextLink"}

        api_endpoint = {"general": "https://pokeapi.co"}
