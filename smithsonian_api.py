"""
smithsonian_api.py: functions for communicating with the Smithsonian Institute
OpenAccess API.
"""

import requests
import pprint

from secure import api_key


def get_images(keyword=None):
    """Request random images from smithsonian API for homepage"""
    # test API requests
   
    # request using keyword
    q = "edward hopper"
    rows_ = 1000

    # search for items
    resp = requests.get(url=API_BASE_URL,
                        params={"q": q,
                                "api_key": api_key,
                                "rows": rows_})

    # iterate through the items for image URL
    rows = resp.json()["response"]["rows"]
    image_urls = []
    for row in rows:
        if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
            if "resources" in row["content"]["descriptiveNonRepeating"]["online_media"]["media"][0].keys():
                url = row["content"]["descriptiveNonRepeating"]["online_media"]["media"][0]["resources"][0]["url"]
                image_urls.append(url)
        # if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
        #    link = row["content"]["descriptiveNonRepeating"]["online_media"][
        #          "media"][0]["content"]
        #    image_links.append(link)

    print(resp)
    print(len(image_urls))
    
    return image_urls
