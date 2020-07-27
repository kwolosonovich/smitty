"""
smithsonian_api.py: functions for communicating with the Smithsonian Institute
OpenAccess API.
"""
import requests
import pprint

from secure import api_key

API_BASE_URL = 'https://api.si.edu/openaccess/api/v1.0/search'

class ApiImage:
    """Create API image."""
    def __init__(self, url, title, artist, date, medium, collection):
        
        self.url = url
        self.title = title
        self.artist = artist
        self.date = date
        self.medium = medium 
        self.collection = collection
        
    def get_images(search=None):
        """Request random images from smithsonian API for homepage"""
        # test API requests

        # request using keyword
        q = 'data_source="American Art"&online_media_type=images&images=jpeg'
        rows_ = 1

        # search for items
        resp = requests.get(url=API_BASE_URL,
                            params={"q": q,
                                    "api_key": api_key,
                                    "rows": rows_})
        
        # iterate through the items for image URL
        rows = resp.json()["response"]["rows"]
        for row in rows:
            if "online_media" in row["content"]["descriptiveNonRepeating"]:

                url = rows[0]["content"]["descriptiveNonRepeating"]["online_media"]["media"][0]["resources"][2]["url"]
                title = rows[0]["content"]["descriptiveNonRepeating"]["title"]["content"]
                artist = rows[0]["content"]["descriptiveNonRepeating"]["title"]["content"]
                date = rows[0]["content"]["freetext"]["date"][0]["content"]
                medium = rows[0]["content"]["freetext"]["physicalDescription"][0]["content"]
                collection = rows[0]["content"]["freetext"]["setName"][0]["content"]

                ApiImage(url, title, artist, date, collection, date, medium)

