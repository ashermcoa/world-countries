from graphene_django.utils.testing import GraphQLTestCase
from world.schema import schema


class RegionsTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_valid_regions_query(self):
        response = self.query(
            '''
            query regionsByContinent($continent: String!) {
                regionsByContinent(continent: $continent) {
                    regions
                    }
                }
            ''',
            op_name='regionsByContinent',
            variables={"continent": "Asia"}
        )
        self.assertResponseNoErrors(response)

    def test_invalid_variable_name_in_regions_query(self):
        response = self.query(
            '''
            query RegionsByContinent($continent: String!){
                regionsByContinent(continent: $continent) {
                    regions { }
                    }
                }
            ''',
            op_name='RegionsByContinent',
            variables={'continent_name': 'Asia'}
        )
        self.assertResponseHasErrors(response)
