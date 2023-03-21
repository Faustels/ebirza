from Services.Location.locationAPI import GetLocations
class User:
  def __init__(self, id, email, address):
    self.id = id
    self.email = email
    self.address = address
    temp = GetLocations(address).json()
    self.latitude = temp["results"][0]["lat"]
    self.longitude = temp["results"][0]["lon"]