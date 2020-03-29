import time
import urllib,json
import urllib.request as ur
import giphy_client
from urllib.parse import quote
from giphy_client.rest import ApiException
from pprint import pprint

class GiphyAPI:
    __api_key = ""
    __instance = None

    def __init__(self, api_key_file='api_key'):
        with open(api_key_file) as f:
            self.__api_key = f.read().rstrip('\n')
        self.__instance = giphy_client.DefaultApi()

    def searchGif(self, searchTerm, limit=1, offset=0):
        try: 
            # Search Endpoint
            api_response = self.__instance.gifs_search_get(self.__api_key, searchTerm, limit=limit, offset=offset)
            # https://github.com/Giphy/giphy-python-client/blob/master/docs/InlineResponse200.md
            # return the original url for now, but other options available
            return api_response.data[0].images.original.url
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)