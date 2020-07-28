"""
smithsonian_api.py: functions for communicating with the Smithsonian Institute
OpenAccess API.
"""
import urllib.parse
import requests
import pprint

from secure import api_key

API_BASE_URL = 'https://api.si.edu/openaccess/api/v1.0/search'

class ApiImage:
    """Create API image."""
    def __init__(self, url, title, 
                 artist, 
                 date, 
                 medium, collection, raw_response):        
        self.url = url
        self.title = title
        self.artist = artist
        self.date = date
        self.medium = medium 
        self.collection = collection
        self.raw_response = raw_response
        
    # def get_images(search=None):
    #     """Request random images from smithsonian API for homepage"""
    #     # test API requests

    #     # request using keyword
    #     q = 'data_source="American Art"&online_media_type=images&images=jpeg'
    #     rows_ = 1

    #     # search for items
    #     resp = requests.get(url=API_BASE_URL,
    #                         params={"q": q,
    #                                 "api_key": api_key,
    #                                 "rows": rows_})
        
    #     # iterate through the items for image URL
    #     rows = resp.json()["response"]["rows"]
    #     for row in rows:
    #         if "online_media" in row["content"]["descriptiveNonRepeating"]:

    #             url = rows[0]["content"]["descriptiveNonRepeating"]["online_media"]["media"][0]["resources"][2]["url"]
    #             title = rows[0]["content"]["descriptiveNonRepeating"]["title"]["content"]
    #             artist = rows[0]["content"]["descriptiveNonRepeating"]["title"]["content"]
    #             date = rows[0]["content"]["freetext"]["date"][0]["content"]
    #             medium = rows[0]["content"]["freetext"]["physicalDescription"][0]["content"]
    #             collection = rows[0]["content"]["freetext"]["setName"][0]["content"]

    #             ApiImage(url, title, artist, date, medium, collection)


def search(search_terms=None, max_results=None):
    images = []
    for i in range(max_results):
        params = {
            "api_key": api_key,
            "q": search_terms + "&online_media_type=images&images=jpeg",
            "start": i,
            "rows": 1
        }
        resp = requests.get(url=API_BASE_URL,
                            params=params)
        content_found = True if resp.json()["response"].get("message", False) == "content found" else False
        if content_found:
            # row = resp.json()["response"].get("rows", "N/A")
            # print(f"row: {row}")
            
            # if row != "N/A" and len(row) > 0:
                # print("**********************************")            
            row = resp.json()["response"]["rows"][0]
            descriptive = row["content"].get("descriptiveNonRepeating", "N/A")
            freetext = row["content"].get("freetext", "N/A")
            indexed = row["content"].get("indexedStructured", "N/A")
            # print(f"row: {row}")
            if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
                # content = row["content"]
                if descriptive != "N/A":
                    data_source = descriptive["data_source"]
                    # url = descriptive["online_media"]["media"][0].get("resources", "N/A")
                    
                    url = descriptive["online_media"]["media"][0].get("content", "N/A")
                    if url == "N/A":
                        url = descriptive["online_media"]["media"][0].get("thumbnail", "N/A")
                    # print(f"url: {url}")
                    artist = descriptive.get("name", "N/A")
                    if artist != "N/A" and len(artist) > 0:
                        artist = artist[0] 
                    # print(f"artist: {artist}")                   
                    date = descriptive.get("date", "N/A")
                    if date != "N/A" and len(date) > 0:
                        date = date[0]
                    # print(f"date: {date}")
                    title = descriptive["title"]
                # print(f"titel: {title}")
                medium = freetext.get("physicalDescription", "N/A")
                if medium != "N/A":
                    if medium != "N/A" and len(medium) > 0:
                        medium = medium[0]["content"]
                # print(f"medium: {medium}")
                collection = freetext.get("setName", "N/A")
                if collection != "N/A":
                    collection = freetext["setName"][0]["content"]
                # print(url)
                # print(title)
                # print(artist)
                # print(date)
                # print(medium)
                # print(collection)
                image = ApiImage(url, title, artist, date, medium, collection, row)  
                images.append(image)
            else:
                pass
        else:
            pass  
    return images
                


# def get_images(category=None):
#     """Request random images from smithsonian API for homepage"""
#     # test API requests
#     # request using keyword
#     # q = 'data_source="American Art"&online_media_type=images&images=jpeg'
#     # q = 'data_source="Dogs"&online_media_type=images&images=jpeg'
#     q = f'data_source="{category}"&online_media_type=images&images=jpeg'
#     number_of_rows=1
#     # search for items
#     resp = requests.get(url=API_BASE_URL,
#                         params={"q": q,
#                                 "api_key": api_key,
#                                 "rows": number_of_rows})    
#     # iterate through the items for image URL
#     rows = resp.json()["response"]["rows"]
#     images = []
#     for row in rows:
#         pprint.pprint(row)
#         if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
#             url = rows[0]["content"]["descriptiveNonRepeating"]["online_media"]["media"][0]["resources"][2]["url"]
#             title = rows[0]["content"]["descriptiveNonRepeating"]["title"]["content"]
#             artist = rows[0]["content"]["freetext"]["name"][0]["content"]\
#                 .split(",")[0]
#             # artist = rows[0]["content"]["descriptiveNonRepeating"]["title"]["content"]
#             date = rows[0]["content"]["freetext"]["date"][0]["content"]
#             medium = rows[0]["content"]["freetext"]["physicalDescription"][0]["content"]
#             collection = rows[0]["content"]["freetext"]["setName"][0]["content"]
#             image = ApiImage(url, title, artist, date, medium, collection)
#             images.append(image)
#     return images
