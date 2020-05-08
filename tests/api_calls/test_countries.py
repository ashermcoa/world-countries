from graphene_django.utils.testing import GraphQLTestCase
from world.schema import schema


class RegionsTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_valid_country_query(self):
        response = self.query(
            '''
            query countriesByRegion($region: String!) {
                countriesByRegion(region: $region) {
                        code
                        name
                        population
                    }
                }
            ''',
            op_name='countriesByRegion',
            variables={'region': 'region B'}
        )
        self.assertResponseNoErrors(response)

    def test_invalid_query_field_in_country_query(self):
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
            variables={'region': 'region A'}
        )
        self.assertResponseHasErrors(response)
