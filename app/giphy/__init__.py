import time
import urllib,json
import urllib.request as ur
import giphy_client
import random
from urllib.parse import quote
from giphy_client.rest import ApiException
from pprint import pprint

HAPPY_KEYWORDS = ["happy", "positive", "happy dance", "excited", "joy", "amazing", "puppy"]
# if some error happens, just return this gif. Gotta love hackathons
DEFAULT_GIF = "https://media.giphy.com/media/glvyCVWYJ21fq/giphy.gif"

class GiphyAPI:
    __api_key = ""
    __instance = None
    __id_cache = None

    def __init__(self, api_key_file='api_key'):
        self.__id_cache = set()
        with open(api_key_file) as f:
            self.__api_key = f.read().rstrip('\n')
        self.__instance = giphy_client.DefaultApi()

    def searchHappyGif(self):
        # Using a random keyword, find a unique gif
        keyword = HAPPY_KEYWORDS[random.randrange(len(HAPPY_KEYWORDS))]
        results = None
        try: 
            # Search Endpoint: api_key, keyword, results, offset
            api_response = self.__instance.gifs_search_get(self.__api_key, keyword, limit=50, offset=0)
            # https://github.com/Giphy/giphy-python-client/blob/master/docs/InlineResponse200.md
            # return the original url for now, but other options available
            results = api_response.data
            
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
            return DEFAULT_GIF

        # find unique gif
        for gifResult in results:
            if gifResult.id not in self.__id_cache:
                self.__id_cache.add(gifResult.id)
                return gifResult.images.original.url

        # Not likely, can fix later with pagination
        return DEFAULT_GIF
