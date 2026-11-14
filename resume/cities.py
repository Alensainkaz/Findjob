# All cities of Kazakhstan, grouped by region.
# The three cities of republican significance come first, the rest follow by region.
CITIES_BY_REGION = [
    ('Cities of republican significance', [
        ('astana', 'Astana'),
        ('almaty', 'Almaty'),
        ('shymkent', 'Shymkent'),
    ]),
    ('Abai Region', [
        ('semey', 'Semey'),
        ('ayagoz', 'Ayagoz'),
        ('kurchatov', 'Kurchatov'),
        ('shar', 'Shar'),
    ]),
    ('Akmola Region', [
        ('kokshetau', 'Kokshetau'),
        ('stepnogorsk', 'Stepnogorsk'),
        ('akkol', 'Akkol'),
        ('atbasar', 'Atbasar'),
        ('derzhavinsk', 'Derzhavinsk'),
        ('yereymentau', 'Yereymentau'),
        ('esil', 'Esil'),
        ('kosshy', 'Kosshy'),
        ('makinsk', 'Makinsk'),
        ('stepnyak', 'Stepnyak'),
        ('shchuchinsk', 'Shchuchinsk'),
    ]),
    ('Aktobe Region', [
        ('aktobe', 'Aktobe'),
        ('alga', 'Alga'),
        ('embi', 'Embi'),
        ('kandyagash', 'Kandyagash'),
        ('temir', 'Temir'),
        ('khromtau', 'Khromtau'),
        ('shalkar', 'Shalkar'),
        ('zhem', 'Zhem'),
    ]),
    ('Almaty Region', [
        ('konaev', 'Konaev (Kapshagay)'),
        ('esik', 'Esik'),
        ('kaskelen', 'Kaskelen'),
        ('talgar', 'Talgar'),
    ]),
    ('Atyrau Region', [
        ('atyrau', 'Atyrau'),
        ('kulsary', 'Kulsary'),
    ]),
    ('East Kazakhstan Region', [
        ('oskemen', 'Oskemen (Ust-Kamenogorsk)'),
        ('ridder', 'Ridder'),
        ('altai', 'Altai (Zyryanovsk)'),
        ('serebryansk', 'Serebryansk'),
        ('shemonaikha', 'Shemonaikha'),
        ('zaysan', 'Zaysan'),
    ]),
    ('Jambyl Region', [
        ('taraz', 'Taraz'),
        ('karatau', 'Karatau'),
        ('shu', 'Shu'),
        ('zhanatas', 'Zhanatas'),
    ]),
    ('Jetisu Region', [
        ('taldykorgan', 'Taldykorgan'),
        ('tekeli', 'Tekeli'),
        ('ushtobe', 'Ushtobe'),
        ('sarkand', 'Sarkand'),
        ('zharkent', 'Zharkent'),
    ]),
    ('Karaganda Region', [
        ('karaganda', 'Karaganda'),
        ('abai', 'Abai'),
        ('balkhash', 'Balkhash'),
        ('karkaraly', 'Karkaraly'),
        ('priozersk', 'Priozersk'),
        ('saran', 'Saran'),
        ('temirtau', 'Temirtau'),
        ('shakhtinsk', 'Shakhtinsk'),
    ]),
    ('Kostanay Region', [
        ('kostanay', 'Kostanay'),
        ('arkalyk', 'Arkalyk'),
        ('lisakovsk', 'Lisakovsk'),
        ('rudny', 'Rudny'),
        ('tobyl', 'Tobyl'),
        ('zhitikara', 'Zhitikara'),
    ]),
    ('Kyzylorda Region', [
        ('kyzylorda', 'Kyzylorda'),
        ('aral', 'Aral'),
        ('baikonur', 'Baikonur'),
        ('kazaly', 'Kazaly'),
    ]),
    ('Mangystau Region', [
        ('aktau', 'Aktau'),
        ('zhanaozen', 'Zhanaozen'),
        ('fort_shevchenko', 'Fort-Shevchenko'),
    ]),
    ('North Kazakhstan Region', [
        ('petropavl', 'Petropavl'),
        ('bulaevo', 'Bulaevo'),
        ('mamlyutka', 'Mamlyutka'),
        ('sergeyevka', 'Sergeyevka'),
        ('taiynsha', 'Taiynsha'),
    ]),
    ('Pavlodar Region', [
        ('pavlodar', 'Pavlodar'),
        ('aksu', 'Aksu'),
        ('ekibastuz', 'Ekibastuz'),
    ]),
    ('Turkistan Region', [
        ('turkistan', 'Turkistan'),
        ('arys', 'Arys'),
        ('kentau', 'Kentau'),
        ('lenger', 'Lenger'),
        ('saryagash', 'Saryagash'),
        ('shardara', 'Shardara'),
        ('zhetysai', 'Zhetysai'),
    ]),
    ('Ulytau Region', [
        ('zhezkazgan', 'Zhezkazgan'),
        ('karazhal', 'Karazhal'),
        ('satbayev', 'Satbayev'),
    ]),
    ('West Kazakhstan Region', [
        ('oral', 'Oral (Uralsk)'),
        ('aksai', 'Aksai'),
    ]),
]

# Django's grouped choices format: renders as <optgroup> in forms and admin.
CITY_CHOICES = [(region, cities) for region, cities in CITIES_BY_REGION]

CITY_LABELS = {value: label for _, cities in CITIES_BY_REGION for value, label in cities}


def city_groups():
    """JSON-friendly city list for the Vue islands."""
    return [
        {'region': region, 'cities': [{'value': v, 'label': l} for v, l in cities]}
        for region, cities in CITIES_BY_REGION
    ]
