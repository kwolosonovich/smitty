"""
smithsonian_api.py: functions for communicating with the Smithsonian Institute
OpenAccess API.
"""
import requests
import pprint

from secure import api_key

API_BASE_URL = 'https://api.si.edu/openaccess/api/v1.0/search'


def get_images(keyword=None):
    """Request random images from smithsonian API for homepage"""
    # test API requests
   
    # request using keyword
    q = "painting"
    rows_ = 1000
    type = "images"

    # search for items
    resp = requests.get(url=API_BASE_URL,
                        params={"q": q,
                                "api_key": api_key,
                                "rows": rows_})

    # iterate through the items for image URL
    rows = resp.json()["response"]["rows"]
    image_urls = []
    for row in rows:
        # if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
        #     if "resources" in row["content"]["descriptiveNonRepeating"]["online_media"]["media"][0].keys():
        #         url = row["content"]["descriptiveNonRepeating"]["online_media"]["media"][0]["resources"][0]["url"]
        #         image_urls.append(url)
                

        if "online_media" in row["content"]["descriptiveNonRepeating"]:
            online_media = row["content"]["descriptiveNonRepeating"].get('online_media')
            if online_media and online_media["media"][0].get("resources"):
                url = online_media["media"][0]["resources"][0]["url"]
                image_urls.append(url)        
        
    
    return image_urls
