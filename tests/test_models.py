from django.test import TestCase

from api.models import City, Country, CountryLanguage


class CityModelTest(TestCase):

    def test_str_representation(self):
        city = City(name='ABC', country_code='TEN', population=3454,
                    district='District A')
        self.assertEqual(str(city), city.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(City._meta.verbose_name_plural), 'Cities')


class CountryModelTest(TestCase):
    def test_str_representation(self):
        city = City(name='ABC', country_code='TEN', population=3454,
                    district='District A')
        country = Country(name='Country A', code='CAN',
                          continent='Some Continent',
                          region='Region A', surface_area=2389.90,
                          population=9999, life_expectancy=80,
                          gnp=90.8, gnp_old=88.78, local_name='Country A',
                          government_form='Republic',
                          head_of_state='CCandidate A', code_2='CA',
                          capital=city)
        self.assertEqual(str(country), country.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Country._meta.verbose_name_plural), 'Countries')


class CountryLanguageModelTest(TestCase):
    def setUp(self):
        city = City(name='ABC', country_code='TEN', population=3454,
                    district='District A')
        self.country = Country(name='Country A', code='CAN',
                               continent='Some Continent',
                               region='Region A', surface_area=2389.90,
                               population=9999, life_expectancy=80,
                               gnp=90.8, gnp_old=88.78, local_name='Country A',
                               government_form='Republic',
                               head_of_state='CCandidate A', code_2='CA',
                               capital=city)
        self.country_language = CountryLanguage(country_code=self.country,
                                                is_official=True,
                                                language='Lang',
                                                percentage=83.2)

    def test_verbose_name_plural(self):
        self.assertEqual(str(CountryLanguage._meta.verbose_name_plural),
                         'Country Languages')

    def test_language_country_code_correct(self):
        self.assertEqual(self.country_language.country_code, self.country)
