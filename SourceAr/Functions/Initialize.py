import os


class Initialize():
    basedir = os.path.abspath(os.path.join(__file__, "../../"))
    DateFormat = '%d/%m/%y'
    HourFormat = '%H%M%S'

    # JsonData
    Json = basedir + u'\Pages'
    environment = 'QA'

    # Test Browser
    browser = u'FIREFOX'

    # Directory / Evidence Storage During Execution
    pathEvidences = basedir + u'\data\ScreenShots'

    # Environment variable
    if environment == 'QA':

        url = {"Challenge1": "https://dex.pokemonshowdown.com",
               "Challenge2": "https://www.rocketmortgage.com/calculators/mortgage-calculator?qlsource=RMTextLink"}
