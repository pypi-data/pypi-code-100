import gettext
import re
import iroin_pycountry
import iroin_pycountry.db
import pytest


@pytest.fixture(autouse=True, scope='session')
def logging():
    import logging
    logging.basicConfig(level=logging.DEBUG)


def test_country_list():
    assert len(iroin_pycountry.countries) == 249
    assert isinstance(list(iroin_pycountry.countries)[0], iroin_pycountry.db.Data)


def test_country_fuzzy_search():
    results = iroin_pycountry.countries.search_fuzzy(u'England')
    assert len(results) == 1
    assert results[0] == iroin_pycountry.countries.get(alpha_2='GB')

    # Match alternative names exactly and thus GB ends up with Wales
    # before Australia.
    results = iroin_pycountry.countries.search_fuzzy(u'Wales')
    assert len(results) == 2
    assert results[0] == iroin_pycountry.countries.get(alpha_2='GB')
    assert results[1] == iroin_pycountry.countries.get(alpha_2='AU')

    # Match with accents removed, first a country with a partial match in the
    # country name, then a country with multiple subdivision partial matches,
    # and then a country with a single subdivision match.
    results = iroin_pycountry.countries.search_fuzzy(u'Cote')
    assert len(results) == 3
    assert results[0] == iroin_pycountry.countries.get(alpha_2='CI')
    assert results[1] == iroin_pycountry.countries.get(alpha_2='FR')
    assert results[2] == iroin_pycountry.countries.get(alpha_2='HN')

    # A somewhat carefully balanced point system allows for a (bias-based)
    # graceful sorting of common substrings being used in multiple matches:
    results = iroin_pycountry.countries.search_fuzzy(u'New')
    assert results[0] == iroin_pycountry.countries.get(alpha_2='NC')
    assert results[1] == iroin_pycountry.countries.get(alpha_2='NZ')
    assert results[2] == iroin_pycountry.countries.get(alpha_2='PG')
    assert results[3] == iroin_pycountry.countries.get(alpha_2='GB')
    assert results[4] == iroin_pycountry.countries.get(alpha_2='US')
    assert results[5] == iroin_pycountry.countries.get(alpha_2='CA')
    assert results[6] == iroin_pycountry.countries.get(alpha_2='AU')
    assert results[7] == iroin_pycountry.countries.get(alpha_2='MH')

    # bug #34, likely about capitalization that was broken
    results = iroin_pycountry.countries.search_fuzzy(u'united states of america')
    assert len(results) == 1
    assert results[0] == iroin_pycountry.countries.get(alpha_2='US')


def test_historic_country_fuzzy_search():
    results = iroin_pycountry.historic_countries.search_fuzzy(u'burma')
    assert len(results) == 1
    assert results[0] == iroin_pycountry.historic_countries.get(alpha_4='BUMM')


def test_germany_has_all_attributes():
    germany = iroin_pycountry.countries.get(alpha_2='DE')
    assert germany.alpha_2 == u'DE'
    assert germany.alpha_3 == u'DEU'
    assert germany.numeric == u'276'
    assert germany.name == u'Germany'
    assert germany.official_name == u'Federal Republic of Germany'


def test_subdivisions_directly_accessible():
    assert len(iroin_pycountry.subdivisions) == 4883
    assert isinstance(list(iroin_pycountry.subdivisions)[0], iroin_pycountry.db.Data)

    de_st = iroin_pycountry.subdivisions.get(code='DE-ST')
    assert de_st.code == u'DE-ST'
    assert de_st.name == u'Sachsen-Anhalt'
    assert de_st.type == u'State'
    assert de_st.parent is None
    assert de_st.parent_code is None
    assert de_st.country is iroin_pycountry.countries.get(alpha_2='DE')


def test_subdivisions_have_subdivision_as_parent():
    al_bu = iroin_pycountry.subdivisions.get(code='AL-BU')
    assert al_bu.code == u'AL-BU'
    assert al_bu.name == u'Bulqiz\xeb'
    assert al_bu.type == u'District'
    assert al_bu.parent_code == u'AL-09'
    assert al_bu.parent is iroin_pycountry.subdivisions.get(code='AL-09')
    assert al_bu.parent.name == u'Dib\xebr'


def test_query_subdivisions_of_country():
    assert len(iroin_pycountry.subdivisions.get(country_code='DE')) == 16
    assert len(iroin_pycountry.subdivisions.get(country_code='US')) == 57


def test_scripts():
    assert len(iroin_pycountry.scripts) == 182
    assert isinstance(list(iroin_pycountry.scripts)[0], iroin_pycountry.db.Data)

    latin = iroin_pycountry.scripts.get(name='Latin')
    assert latin.alpha_4 == u'Latn'
    assert latin.name == u'Latin'
    assert latin.numeric == u'215'


def test_currencies():
    assert len(iroin_pycountry.currencies) == 170
    assert isinstance(list(iroin_pycountry.currencies)[0], iroin_pycountry.db.Data)

    argentine_peso = iroin_pycountry.currencies.get(alpha_3='ARS')
    assert argentine_peso.alpha_3 == u'ARS'
    assert argentine_peso.name == u'Argentine Peso'
    assert argentine_peso.numeric == u'032'


def test_languages():
    assert len(iroin_pycountry.languages) == 7847
    assert isinstance(list(iroin_pycountry.languages)[0], iroin_pycountry.db.Data)

    aragonese = iroin_pycountry.languages.get(alpha_2='an')
    assert aragonese.alpha_2 == u'an'
    assert aragonese.alpha_3 == u'arg'
    assert aragonese.name == u'Aragonese'

    bengali = iroin_pycountry.languages.get(alpha_2='bn')
    assert bengali.name == u'Bengali'
    assert bengali.common_name == u'Bangla'

    # this tests the slow search path in lookup()
    bengali2 = iroin_pycountry.languages.lookup('bAngLa')
    assert bengali2 == bengali


def test_language_families():
    assert len(iroin_pycountry.language_families) == 115
    assert isinstance(list(iroin_pycountry.language_families)[0], iroin_pycountry.db.Data)

    aragonese = iroin_pycountry.languages.get(alpha_3='arg')
    assert aragonese.alpha_3 == u'arg'
    assert aragonese.name == u'Aragonese'


def test_locales():
    german = gettext.translation(
        'iso3166', iroin_pycountry.LOCALES_DIR, languages=['de'])
    german.install()
    assert __builtins__['_']('Germany') == 'Deutschland'


def test_removed_countries():
    ussr = iroin_pycountry.historic_countries.get(alpha_3='SUN')
    assert isinstance(ussr, iroin_pycountry.db.Data)
    assert ussr.alpha_4 == u'SUHH'
    assert ussr.alpha_3 == u'SUN'
    assert ussr.name == u'USSR, Union of Soviet Socialist Republics'
    assert ussr.withdrawal_date == u'1992-08-30'


def test_repr():
    assert re.match("Country\\(alpha_2=u?'DE', "
                    "alpha_3=u?'DEU', "
                    "name=u?'Germany', "
                    "numeric=u?'276', "
                    "official_name=u?'Federal Republic of Germany'\\)",
                    repr(iroin_pycountry.countries.get(alpha_2='DE')))


def test_dir():
    germany = iroin_pycountry.countries.get(alpha_2='DE')
    for n in 'alpha_2', 'alpha_3', 'name', 'numeric', 'official_name':
        assert n in dir(germany)


def test_get():
    c = iroin_pycountry.countries
    with pytest.raises(TypeError):
        c.get(alpha_2='DE', alpha_3='DEU')
    assert c.get(alpha_2='DE') == c.get(alpha_3='DEU')
    assert c.get(alpha_2='Foo') is None
    tracer = object()
    assert c.get(alpha_2='Foo', default=tracer) is tracer


def test_lookup():
    c = iroin_pycountry.countries
    g = c.get(alpha_2='DE')
    assert g == c.get(alpha_2='de')
    assert g == c.lookup('de')
    assert g == c.lookup('DEU')
    assert g == c.lookup('276')
    assert g == c.lookup('germany')
    assert g == c.lookup('Federal Republic of Germany')
    # try a generated field
    bqaq = iroin_pycountry.historic_countries.get(alpha_4='BQAQ')
    assert bqaq == iroin_pycountry.historic_countries.lookup('atb')
    german = iroin_pycountry.languages.get(alpha_2='de')
    assert german == iroin_pycountry.languages.lookup('De')
    euro = iroin_pycountry.currencies.get(alpha_3='EUR')
    assert euro == iroin_pycountry.currencies.lookup('euro')
    latin = iroin_pycountry.scripts.get(name='Latin')
    assert latin == iroin_pycountry.scripts.lookup('latn')
    al_bu = iroin_pycountry.subdivisions.get(code='AL-BU')
    assert al_bu == iroin_pycountry.subdivisions.lookup('al-bu')
    with pytest.raises(LookupError):
        iroin_pycountry.countries.lookup('bogus country')
    with pytest.raises(LookupError):
        iroin_pycountry.countries.lookup(12345)
    with pytest.raises(LookupError):
        iroin_pycountry.countries.get(alpha_2=12345)


def test_subdivision_parent():
    s = iroin_pycountry.subdivisions
    sd = s.get(code='CV-BV')
    assert sd.parent_code == 'CV-B'
    assert sd.parent is s.get(code=sd.parent_code)


def test_subdivision_missing_code_raises_keyerror():
    s = iroin_pycountry.subdivisions
    assert s.get(code='US-ZZ') is None


def test_subdivision_empty_list():
    s = iroin_pycountry.subdivisions
    assert len(s.get(country_code='DE')) == 16
    assert len(s.get(country_code='JE')) == 0
    assert s.get(country_code='FOOBAR') is None


def test_has_version_attribute():
    assert iroin_pycountry.__version__ != 'n/a'
    assert len(iroin_pycountry.__version__) >= 5
    assert '.' in iroin_pycountry.__version__
