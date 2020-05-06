import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import Country, CountryLanguage, City


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class CountryLanguageType(DjangoObjectType):
    class Meta:
        model = CountryLanguage


class CityType(DjangoObjectType):
    class Meta:
        model = City


class Query(graphene.ObjectType):
    countries = graphene.List(CountryType, search=graphene.String())
    cities = graphene.List(CityType)
    languages = graphene.List(CountryLanguageType)

    def resolve_countries(self, info, search=None):
        return Country.objects.all()

    def resolve_cities(self, info):
        return City.objects.all()


class CreateCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        name = graphene.String()
        countrycode = graphene.String()
        district = graphene.String()
        population = graphene.Int()

    def mutate(self, _, name, country_code, district, population):
        city = City(name=name, countrycode=country_code, district=district, population=population)
        city.save()
        return CreateCity(city=city)


class UpdateCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        city_id = graphene.Int(required=True)
        name = graphene.String()
        country_code = graphene.String()
        district = graphene.String()
        population = graphene.String()

    def mutate(self, _, city_id, name, country_code, district, population):
        city = City.objects.get(id=city_id)
        city.name = name
        city.countrycode = country_code
        city.district = district
        city.population = population
        city.save()
        return UpdateCity(city=city)


class DeleteCity(graphene.Mutation):
    city_id = graphene.Int()

    def mutate(self, _, city_id):
        city = City.objects.get(id=city_id)
        city.delete()
        return DeleteCity(city_id=city_id)


class Mutation(graphene.ObjectType):
    create_city = CreateCity.Field()
    update_city = UpdateCity.Field()
    delete_city = DeleteCity.Field()
