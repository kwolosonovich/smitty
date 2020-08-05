"""
smithsonian_api.py: functions for communicating with the Smithsonian Institute
OpenAccess API.
"""
import urllib.parse
import requests
import random


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
       

    def format_images(images=None, images_per_row=None, max_rows=None):
        formatted_images = []
        for i in range(max_rows):
            start = i * images_per_row
            stop = start + images_per_row
            row = images[start:stop:1]
            formatted_images.append(row)
        return formatted_images


def filter_search_results(search_results=None, dev=False):
    if dev:
        return search_results
    images_array = []
    for resp in search_results:
        content_found = True if resp.json()["response"].get("message", False) == "content found" else False
        if content_found:          
            row = resp.json()["response"]["rows"][0]
            descriptive = row["content"].get("descriptiveNonRepeating", "N/A")
            freetext = row["content"].get("freetext", "N/A")
            indexed = row["content"].get("indexedStructured", "N/A")
            if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
                if descriptive != "N/A":
                    data_source = descriptive["data_source"]
                    url = descriptive["online_media"]["media"][0].get("content", "N/A")
                    if url == "N/A":
                        url = descriptive["online_media"]["media"][0].get("thumbnail", "N/A")
                    artist = descriptive.get("name", "N/A")
                    if artist != "N/A" and len(artist) > 0:
                        artist = artist[0] 
                    date = descriptive.get("date", "N/A")
                    if date != "N/A" and len(date) > 0:
                        date = date[0]
                    title = descriptive["title"]['content']      
                # artist = indexed.get("name", "N/A")
                # if artist != "N/A":
                #     if artist != "N/A" and len(artist) > 0:
                #         artist = artist[0]['name'][0]    
                medium = freetext.get("physicalDescription", "N/A")
                if medium != "N/A":
                    if medium != "N/A" and len(medium) > 0:
                        medium = medium[0]["content"]
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


def search(search_terms=None, max_results=None, dev=False, images_per_row=None,
           max_rows=None, is_homepage=False):
    '''Request images from Smithsonian API'''
    randoms = list(range(100))
    
    if search_terms is None:
        search_terms = random_search_category()
    
    if dev:
        search_results = \
            create_test_response(max_results=max_results)
            
        filtered_search_results = filter_search_results(search_results=search_results,
                 dev=dev)    
    else:
        search_results = []        
        for i in range(max_results):
            start = i
            if is_homepage:
                start = random.choice(randoms)
            params = {
                "api_key": api_key,
                "q": search_terms + "&online_media_type=images&images=jpeg",
                "start": start,
                "rows": 1
            }
            resp = requests.get(url=API_BASE_URL,
                                params=params)
            
            search_results.append(resp)
    filtered_search_results = \
        filter_search_results(search_results=search_results, dev=dev)
    
    
    formatted_results = \
        format_images(images=filtered_search_results,
                        images_per_row=images_per_row,
                        max_rows=max_rows)        
            
    return formatted_results
                
class ApiImageMock(object):
    def __init__(self, version=None):
        if version == 1:
            self.url = 'https://ids.si.edu/ids/deliveryService?max_w=800&id=HMSG-66.2399'
            self.title = 'In the Sunlight'
            self.artist = 'Childe Hassam'
            self.date = '1897'
            self.medium = 'Oil on canvas'
            self.collection = 'Hirshhorn Museum and Sculpture Garden'
            self.raw_response = ''
        elif version == 2:
            self.url = 'https://ids.si.edu/ids/deliveryService?max_w=800&id=NPG-NPG_65_61Pocahontas_d1'
            self.title = 'Pocahontas'
            self.artist = 'Unidentified Artist'
            self.date = 'Unidentified'
            self.medium = 'Oil on canvas'
            self.collection = 'National Portrait Gallery'
            self.raw_response = ''
    
    
def create_test_response(max_results=None):
    responses = []
    for i in range(max_results):
        version = 2 if i % 2 == 0 else 1
        mock_image = ApiImageMock(version=version)
        responses.append(mock_image)
        
    return responses


def format_images(images=None, images_per_row=None, max_rows=None):    
    formatted_images = []    
    for i in range(max_rows):
        start = i * images_per_row
        stop = start + images_per_row
        row = images[start:stop:1]
        formatted_images.append(row)        
    return formatted_images



def random_search_category():
    '''Generate random categories'''
    categories = [
        "photograpy",
        "painting",
        "design",
        "sculpture"
    ]
    
    random_category = random.choice(categories)
    
    return random_category
