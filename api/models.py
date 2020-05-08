from django.db import models
from django.db.models import Q

continents = ['Asia', 'Europe', 'North America', 'Africa', 'Oceania',
              'Antarctica', 'South America']


class City(models.Model):
    name = models.TextField(max_length=255)
    country_code = models.CharField(max_length=3, db_column='countrycode')
    district = models.TextField()
    population = models.IntegerField()

    class Meta:
        db_table = 'city'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Country(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.TextField()
    continent = models.TextField()
    region = models.TextField()
    surface_area = models.FloatField(db_column='surfacearea')
    indep_year = models.SmallIntegerField(blank=True, null=True,
                                          db_column='indepyear')
    population = models.IntegerField()
    life_expectancy = models.FloatField(db_column='lifeexpectancy', blank=True,
                                        null=True,
                                        )
    gnp = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                              null=True)
    gnp_old = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                  null=True, db_column='gnpold')
    local_name = models.TextField(db_column='localname')
    government_form = models.TextField(db_column='governmentform')
    head_of_state = models.TextField(blank=True, null=True,
                                     db_column='headofstate')
    capital = models.ForeignKey(City, models.CASCADE,
                                related_name="Capital",
                                db_column='capital',
                                blank=True,
                                null=True)
    code_2 = models.CharField(max_length=2, db_column='code2')

    class Meta:
        db_table = 'country'
        verbose_name_plural = 'Countries'
        constraints = [
            models.CheckConstraint(check=Q(continent__in=continents),
                                   name='country_continent_check')
        ]

    def __str__(self):
        return self.name


class CountryLanguage(models.Model):
    country_code = models.ForeignKey(Country, models.CASCADE,
                                     db_column='countrycode')
    language = models.TextField()
    is_official = models.BooleanField(db_column='isofficial')
    percentage = models.FloatField()

    class Meta:
        db_table = 'countrylanguage'
        verbose_name_plural = 'Country Languages'
