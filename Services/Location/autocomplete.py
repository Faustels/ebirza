import requests

key = None

def GetAutocomplete(text):
    arguments = {"text": text, "lang": "lt", "limit": "10", "filter": "countrycode:lt", "format": "json", "apiKey": key}
    r = requests.get("https://api.geoapify.com/v1/geocode/search", params = arguments)
    return r