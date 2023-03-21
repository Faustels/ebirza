from Services.Location.autocomplete import GetAutocomplete
class User:
  def __init__(self, id, email, address):
    self.id = id
    self.email = email
    self.address = address
    temp = GetAutocomplete(address).json()
    self.latitude = temp["results"][0]["lat"]
    self.longitude = temp["results"][0]["lon"]