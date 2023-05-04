import os
import sys
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from queries import SUGGESTED_TITLES
from queries import TITLE_OFFERS
from queries import URL_TITLE_DETAILS
from queries import NEW_TITLE_BUCKETS

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


class JustWatchAPI:

    def __init__(self):
        self.base_url: str = 'https://apis.justwatch.com/graphql'
        self.transport = AIOHTTPTransport(url=self.base_url)
        self.client = Client(transport=self.transport,
                             fetch_schema_from_transport=False)

    def search_item(self, title: str):
        params = {
            "country": "US",
            "language": "en",
            "first": 4,
            "filter": {
                "searchQuery": title
            }
        }
        
        return self.client.execute(SUGGESTED_TITLES, variable_values=params)

    def get_providers(self, node_id: str):
        params = {
            "platform": "WEB",
            "nodeId": node_id,
            "country": "US",
            "language": "en",
            "filterBuy": {
                "monetizationTypes": [
                    "BUY"
                ],
                "bestOnly": True
            },
            "filterFlatrate": {
                "monetizationTypes": [
                    "FLATRATE",
                    "FLATRATE_AND_BUY",
                    "ADS",
                    "FREE"
                ],
                "bestOnly": True
            },
            "filterRent": {
                "monetizationTypes": [
                    "RENT"
                ],
                "bestOnly": True
            },
            "filterFree": {
                "monetizationTypes": [
                    "ADS",
                    "FREE"
                ],
                "bestOnly": True
            }
        }

        return self.client.execute(TITLE_OFFERS, variable_values=params)

    def get_title(self, full_path: str):
        params = {
            "platform": "WEB",
            "fullPath": full_path,
            "language": "en",
            "country": "US",
            "episodeMaxLimit": 20
        }

        return self.client.execute(URL_TITLE_DETAILS, variable_values=params)

    def new_titles(self, after=None):
        params = {
                "allowSponsoredRecommendations": {
                  "country": "PL",
                  "platform": "ANDROID"
                },
                "country": "PL",
                "filter": {
                  "excludeIrrelevantTitles": False,
                  "objectTypes": [
                    "MOVIE"
                  ],
                  "packages": []
                },
                "first": 5,
                "imageFormat": "WEBP",
                "language": "en-US",
                "packages": [],
                "pageType": "NEW",
                "platform": "ANDROID",
                "priceDrops": False
              }
        if after:
            params['after'] = after

        return self.client.execute(NEW_TITLE_BUCKETS, variable_values=params)
