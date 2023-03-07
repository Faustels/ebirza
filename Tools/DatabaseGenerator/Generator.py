import random as r
from string import ascii_lowercase

amount = 10
onlyProducer = 5
onlyConsumer = 50

class User:
  def __init__(self, id, name, lastName):
    self.id = id
    self.name = name
    self.lastName = lastName
    self.email = name + lastName + "@ktu.edu"
    self.password = ""
    self.address = ""
    self.producer = 0
    self.consumer = 0

class Consumer:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount

class Producer:
    def __init__(self, id, amount, price):
        self.id = id
        self.amount = amount
        self.price = price

def getNames():
    files = ['male.txt', 'female.txt']
    names = []
    for fileName in files:
        f = open(fileName, "r", encoding="utf-8")
        temp = f.readlines()
        for i in range(len(temp)):
            if (temp[i][-1] == '\n'):
                temp[i]=temp[i][:-1]
        names.extend(temp)
        f.close()
    return names



def generateUser(id):
    global names
    return User(id + 1, r.choice(names), ''.join([r.choice(ascii_lowercase) for _ in range(5)]))

def generateProducer(user):
    global producerIndex
    producer = Producer(producerIndex, r.randrange(100), r.randint(1,10000) / 100)
    user.producer = producerIndex
    producerIndex += 1
    return producer
def generateConsumer(user):
    global consumerIndex
    consumer = Consumer(consumerIndex, r.randrange(100))
    user.consumer = consumerIndex
    consumerIndex += 1
    return consumer

names = getNames()
users = []
producers = []
consumers = []
producerIndex = 1
consumerIndex = 1

for i in range(amount):
    temp = r.randrange(100)
    user = generateUser(i)
    if (temp < onlyProducer):
        producers.append(generateProducer(user))
    elif (temp < onlyConsumer + onlyProducer):
        consumers.append(generateConsumer(user))
    else:
        producers.append(generateProducer(user))
        consumers.append(generateConsumer(user))
    users.append(user)