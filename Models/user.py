from Services.Location.locationAPI import GetLocations
class User:
  def __init__(self, id, email, address, isConsumer, isProducer):
    self.id = id
    self.email = email
    self.address = address
    self.latitude = None
    self.longitude = None
    temp = GetLocations(address).json()
    if len(temp["results"]) != 0:
      self.latitude = temp["results"][0]["lat"]
      self.longitude = temp["results"][0]["lon"]
    self.isConsumer = isConsumer
    self.isProducer = isProducer