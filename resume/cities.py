from django.utils.translation import gettext_lazy as _

# All cities of Kazakhstan, grouped by region.
# The three cities of republican significance come first, the rest follow by region.
CITIES_BY_REGION = [
    (_('Cities of republican significance'), [
        ('astana', _('Astana')),
        ('almaty', _('Almaty')),
        ('shymkent', _('Shymkent')),
    ]),
    (_('Abai Region'), [
        ('semey', _('Semey')),
        ('ayagoz', _('Ayagoz')),
        ('kurchatov', _('Kurchatov')),
        ('shar', _('Shar')),
    ]),
    (_('Akmola Region'), [
        ('kokshetau', _('Kokshetau')),
        ('stepnogorsk', _('Stepnogorsk')),
        ('akkol', _('Akkol')),
        ('atbasar', _('Atbasar')),
        ('derzhavinsk', _('Derzhavinsk')),
        ('yereymentau', _('Yereymentau')),
        ('esil', _('Esil')),
        ('kosshy', _('Kosshy')),
        ('makinsk', _('Makinsk')),
        ('stepnyak', _('Stepnyak')),
        ('shchuchinsk', _('Shchuchinsk')),
    ]),
    (_('Aktobe Region'), [
        ('aktobe', _('Aktobe')),
        ('alga', _('Alga')),
        ('embi', _('Embi')),
        ('kandyagash', _('Kandyagash')),
        ('temir', _('Temir')),
        ('khromtau', _('Khromtau')),
        ('shalkar', _('Shalkar')),
        ('zhem', _('Zhem')),
    ]),
    (_('Almaty Region'), [
        ('konaev', _('Konaev (Kapshagay)')),
        ('esik', _('Esik')),
        ('kaskelen', _('Kaskelen')),
        ('talgar', _('Talgar')),
    ]),
    (_('Atyrau Region'), [
        ('atyrau', _('Atyrau')),
        ('kulsary', _('Kulsary')),
    ]),
    (_('East Kazakhstan Region'), [
        ('oskemen', _('Oskemen (Ust-Kamenogorsk)')),
        ('ridder', _('Ridder')),
        ('altai', _('Altai (Zyryanovsk)')),
        ('serebryansk', _('Serebryansk')),
        ('shemonaikha', _('Shemonaikha')),
        ('zaysan', _('Zaysan')),
    ]),
    (_('Jambyl Region'), [
        ('taraz', _('Taraz')),
        ('karatau', _('Karatau')),
        ('shu', _('Shu')),
        ('zhanatas', _('Zhanatas')),
    ]),
    (_('Jetisu Region'), [
        ('taldykorgan', _('Taldykorgan')),
        ('tekeli', _('Tekeli')),
        ('ushtobe', _('Ushtobe')),
        ('sarkand', _('Sarkand')),
        ('zharkent', _('Zharkent')),
    ]),
    (_('Karaganda Region'), [
        ('karaganda', _('Karaganda')),
        ('abai', _('Abai')),
        ('balkhash', _('Balkhash')),
        ('karkaraly', _('Karkaraly')),
        ('priozersk', _('Priozersk')),
        ('saran', _('Saran')),
        ('temirtau', _('Temirtau')),
        ('shakhtinsk', _('Shakhtinsk')),
    ]),
    (_('Kostanay Region'), [
        ('kostanay', _('Kostanay')),
        ('arkalyk', _('Arkalyk')),
        ('lisakovsk', _('Lisakovsk')),
        ('rudny', _('Rudny')),
        ('tobyl', _('Tobyl')),
        ('zhitikara', _('Zhitikara')),
    ]),
    (_('Kyzylorda Region'), [
        ('kyzylorda', _('Kyzylorda')),
        ('aral', _('Aral')),
        ('baikonur', _('Baikonur')),
        ('kazaly', _('Kazaly')),
    ]),
    (_('Mangystau Region'), [
        ('aktau', _('Aktau')),
        ('zhanaozen', _('Zhanaozen')),
        ('fort_shevchenko', _('Fort-Shevchenko')),
    ]),
    (_('North Kazakhstan Region'), [
        ('petropavl', _('Petropavl')),
        ('bulaevo', _('Bulaevo')),
        ('mamlyutka', _('Mamlyutka')),
        ('sergeyevka', _('Sergeyevka')),
        ('taiynsha', _('Taiynsha')),
    ]),
    (_('Pavlodar Region'), [
        ('pavlodar', _('Pavlodar')),
        ('aksu', _('Aksu')),
        ('ekibastuz', _('Ekibastuz')),
    ]),
    (_('Turkistan Region'), [
        ('turkistan', _('Turkistan')),
        ('arys', _('Arys')),
        ('kentau', _('Kentau')),
        ('lenger', _('Lenger')),
        ('saryagash', _('Saryagash')),
        ('shardara', _('Shardara')),
        ('zhetysai', _('Zhetysai')),
    ]),
    (_('Ulytau Region'), [
        ('zhezkazgan', _('Zhezkazgan')),
        ('karazhal', _('Karazhal')),
        ('satbayev', _('Satbayev')),
    ]),
    (_('West Kazakhstan Region'), [
        ('oral', _('Oral (Uralsk)')),
        ('aksai', _('Aksai')),
    ]),
]

# Django's grouped choices format: renders as <optgroup> in forms and admin.
CITY_CHOICES = [(region, cities) for region, cities in CITIES_BY_REGION]

CITY_LABELS = {value: label for _, cities in CITIES_BY_REGION for value, label in cities}


def city_groups():
    """JSON-friendly city list for the Vue islands."""
    return [
        {'region': str(region), 'cities': [{'value': v, 'label': str(l)} for v, l in cities]}
        for region, cities in CITIES_BY_REGION
    ]
