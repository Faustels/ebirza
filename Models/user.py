from Services.Location.locationAPI import GetLocations
class User:
  def __init__(self, id, email, address, produced, setPrice, consumed):
    self.id = id
    self.email = email
    self.address = address
    temp = GetLocations(address).json()
    self.latitude = temp["results"][0]["lat"]
    self.longitude = temp["results"][0]["lon"]
    self.produced = produced
    self.setPrice = setPrice
    self.consumed = consumed