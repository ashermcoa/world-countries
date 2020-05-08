from graphene_django.utils.testing import GraphQLTestCase
from world.schema import schema


class ContinentsTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_continents_query(self):
        response = self.query(
            '''
            query {
            allContinents {
                continents
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)

    def test_continents_query_with_error(self):
        response = self.query(
            '''
            query {
            allContinents {
                continent
                }
            }
            '''
        )
        self.assertResponseHasErrors(response)
