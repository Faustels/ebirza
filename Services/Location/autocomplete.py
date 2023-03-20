import requests

key = None

def GetAutocomplete(text):
    arguments = {"text": text, "filter": "countrycode:lt", "format": "json", "apiKey": key}
    r = requests.get("https://api.geoapify.com/v1/geocode/autocomplete", params = arguments)
    return (r.text)
