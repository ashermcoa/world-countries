import json

from graphene_django.utils.testing import GraphQLTestCase
from world.schema import schema


class RegionsTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def create_city(self, variables):
        response = self.query(
            '''
              mutation CreateCity(
                $name: String!
                $countryCode: String!
                $district: String!
                $population: Int!
              ) {
                createCity(
                  name: $name
                  countryCode: $countryCode
                  district: $district
                  population: $population
                ) {
                  city {
                    id
                  }
                }
              }
            ''',
            op_name='CreateCity',
            variables=variables
        )
        content = json.loads(response.content)
        return content

    def test_valid_city_query(self):
        response = self.query(
            '''
              query GetCitiesByCountry($countryCode: String!) {
                citiesByCountry(countryCode: $countryCode) {
                  district
                  population
                  name
                }
              }
            ''',
            op_name='citiesByCountry',
            variables={'countryCode': 'KCE'}
        )
        self.assertResponseNoErrors(response)

    def test_invalid_input_type_parameter_in_city_query(self):
        response = self.query(
            '''
            query countriesByRegion($region: String!) {
                countriesByRegion(region: $region) {
                        code
                        name
                        race
                    }
                }
            ''',
            op_name='countriesByRegion',
            variables={'region': 800}
        )
        self.assertResponseHasErrors(response)

    def test_valid_city_creation_mutation(self):
        response = self.query(
            '''
              mutation CreateCity(
                $name: String!
                $countryCode: String!
                $district: String!
                $population: Int!
              ) {
                createCity(
                  name: $name
                  countryCode: $countryCode
                  district: $district
                  population: $population
                ) {
                  city {
                    name
                    countryCode
                    district
                    population
                  }
                }
              }
            ''',
            op_name='CreateCity',
            variables={'name': 'City A', 'countryCode': 'KCE',
                       'district': 'DS', 'population': 4565}
        )
        content = json.loads(response.content)
        self.assertIn('name', content['data']['createCity']['city'])
        self.assertEqual(content['data']['createCity']['city']['name'],
                         'City A')
        self.assertResponseNoErrors(response)

    def test_invalid_variable_in_city_creation_mutation(self):
        response = self.query(
            '''
              mutation CreateCity(
                $name: String!
                $countryCode: String!
                $district: String!
                $type: String!
              ) {
                createCity(
                  name: $name
                  countryCode: $countryCode
                  district: $district
                  population: $population
                ) {
                  city {
                    name
                    countryCode
                    district
                    population
                  }
                }
              }
            ''',
            op_name='CreateCity',
            variables={'name': 'City A', 'countryCode': 'KCE',
                       'district': 'DS', 'type': 'metropolitan'}
        )
        self.assertResponseHasErrors(response)

    def test_valid_city_update_mutation(self):
        prev_city_variables = {'name': 'City A', 'countryCode': 'KCE',
                     'district': 'DS', 'population': 4565}
        prev_content = self.create_city(prev_city_variables)
        city_id = prev_content['data']['createCity']['city']['id']
        response = self.query(
            '''
              mutation UpdateCity(
                $id: String!
                $name: String
                $countryCode: String
                $district: String
                $population: String
              ) {
                updateCity(
                  cityId: $id
                  name: $name
                  countryCode: $countryCode
                  district: $district
                  population: $population
                ) {
                  city {
                    id
                    name
                    countryCode
                    district
                    population
                  }
                }
              }
            ''',
            op_name='UpdateCity',
            variables={'id': city_id, 'name': 'City B', 'population': 8000}
        )
        content = json.loads(response.content)
        self.assertEqual(content['data']['updateCity']['city']['name'],
                         'City B')
        self.assertEqual(content['data']['updateCity']['city']['population'],
                         8000)
        self.assertResponseNoErrors(response)

    def test_invalid_city_update_mutation(self):
        response = self.query(
            '''
              mutation UpdateCity(
                $name: String
                $countryCode: String
                $district: String
                $population: String
              ) {
                updateCity(
                  name: $name
                  countryCode: $countryCode
                  district: $district
                  population: $population
                ) {
                  city {
                    id
                    name
                    countryCode
                    district
                    population
                  }
                }
              }
            ''',
            op_name='UpdateCity',
            variables={'name': 'City B', 'population': 8000}
        )
        self.assertResponseHasErrors(response)

    def test_valid_city_delete_mutation(self):
        city_variables = {'name': 'City A', 'countryCode': 'KCE',
                               'district': 'DS', 'population': 4565}
        city = self.create_city(city_variables)
        city_id = city['data']['createCity']['city']['id']
        response = self.query(
            '''
           mutation DeleteCity($cityId: String!) {
            deleteCity(cityId: $cityId) {
              cityId
            }
          }           
            ''',
            op_name='DeleteCity',
            variables={'cityId': str(city_id)}
        )
        content = json.loads(response.content)
        self.assertEqual(content['data']['deleteCity']['cityId'], city_id)
        self.assertResponseNoErrors(response)

    def test_invalid_city_delete_mutation(self):
        response = self.query(
            '''
           mutation DeleteCity($cityId: String!) {
            deleteCity(cityId: $cityId) {
              cityId
            }
          }           
            ''',
            op_name='DeleteCity'
        )
        self.assertResponseHasErrors(response)