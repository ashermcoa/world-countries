import graphene
from graphene_django import DjangoObjectType

from .models import Country, CountryLanguage, City, continents


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class CountryLanguageType(DjangoObjectType):
    class Meta:
        model = CountryLanguage


class CityType(DjangoObjectType):
    class Meta:
        model = City


class CountryRegion(graphene.ObjectType):
    regions = graphene.List(graphene.String)


class Continent(graphene.ObjectType):
    continents = graphene.List(graphene.String)


class Query(graphene.ObjectType):
    languages = graphene.List(CountryLanguageType)
    cities_by_country = graphene.List(CityType, country_code=graphene.String())
    countries_by_region = graphene.List(CountryType, region=graphene.String())
    regions_by_continent = graphene.Field(CountryRegion,
                                          continent=graphene.String())
    all_continents = graphene.Field(Continent)

    @staticmethod
    def resolve_cities_by_country(_, country_code):
        return City.objects.filter(country_code=country_code)

    @staticmethod
    def resolve_regions_by_continent(_, continent):
        continent_regions = Country.objects.filter(continent=continent).values(
            'region')
        regions = set(map(lambda reg: reg['region'], continent_regions))
        return CountryRegion(regions=regions)

    @staticmethod
    def resolve_countries_by_region(_, region):
        return Country.objects.filter(region=region)

    @staticmethod
    def resolve_all_continents(_):
        return Continent(continents=sorted(continents))


class CreateCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        name = graphene.String()
        country_code = graphene.String()
        district = graphene.String()
        population = graphene.Int()

    @staticmethod
    def mutate(self, _, name, country_code, district, population):
        city = City(name=name, country_code=country_code, district=district,
                    population=population)
        city.save()
        return CreateCity(city=city)


class UpdateCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        city_id = graphene.String(required=True)
        name = graphene.String(required=False)
        country_code = graphene.String(required=False)
        district = graphene.String(required=False)
        population = graphene.String(required=False)

    @staticmethod
    def mutate(self, _, city_id, **kwargs):
        city = City.objects.get(id=city_id)
        city.name = kwargs.get('name', city.name)
        city.country_code = kwargs.get('country_code', city.country_code)
        city.district = kwargs.get('district', city.district)
        city.population = kwargs.get('population', city.population)
        city.save()
        return UpdateCity(city=city)


class DeleteCity(graphene.Mutation):
    city_id = graphene.String()

    class Arguments:
        city_id = graphene.String(required=True)

    @staticmethod
    def mutate(self, _, city_id):
        city = City.objects.get(id=city_id)
        print(city)
        city.delete()
        return DeleteCity(city_id=city_id)


class Mutation(graphene.ObjectType):
    create_city = CreateCity.Field()
    update_city = UpdateCity.Field()
    delete_city = DeleteCity.Field()
