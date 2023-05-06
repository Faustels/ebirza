from Services.Location.locationAPI import GetLocations
class User:
  def __init__(self, id, email, address, produced, setPrice, consumed, balance):
    self.id = id
    self.email = email
    self.address = address
    self.latitude = None
    self.longitude = None
    temp = GetLocations(address).json()
    if len(temp["results"]) != 0:
      self.latitude = temp["results"][0]["lat"]
      self.longitude = temp["results"][0]["lon"]
    self.produced = produced
    self.setPrice = setPrice
    self.consumed = consumed
    self.balance = balance