"""
smithsonian_api.py: functions for communicating with the Smithsonian Institute
OpenAccess API.
"""
import urllib.parse
import requests
import pprint

from werkzeug import urls

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
       
# TODO: get randome images
    # @staticmethod
    # def homepage_carousel(images=None):
        

       
    # @staticmethod   
    # def format_arrays(images=None):
    #     '''Group arrays into nested arrays with length of 6.'''
    #     image_array = []
    #     image_arrays = []
        
    #     for image in images:
    #         if len(image_array) < 7:
    #             images_array.append(image)
    #         if len(image_array) > 7:
    #             image_arrays.append(image_array)
    #             image_array = []
                
    #     return image_arrays 


# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# >> > i = format_images(n, 6, 2)
# >> > i
# [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]

    # def format_images(images=None, images_per_row=None, max_rows=None):
    #     formatted_images = []
    #     for i in range(max_rows):
    #         start = i * images_per_row
    #         stop = start + images_per_row
    #         row = images[start:stop:1]
    #         formatted_images.append(row)
    #     return formatted_images


def search(search_terms=None, max_results=None, random=False):
    '''Request images from Smithsonian API'''
    images_array = []
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

                image = ApiImage(url, title, artist, date, medium, collection, row)  
                images_array.append(image)
            else:
                pass
        else:
            pass
        
    return images_array
     
    # if random is True:    
    #     images = ApiImage.format_arrays(images_array)
    #     return images
    # elif random is False:
    #     return images_array
    # else:
    #     return 'Request error'
                
