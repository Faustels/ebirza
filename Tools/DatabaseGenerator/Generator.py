import random as r
from string import ascii_lowercase
from hashlib import sha256

amount = 10
onlyProducer = 5
onlyConsumer = 50
fileName = "data.txt"

class User:
    def __init__(self, id, name, lastName, salt):
        self.id = id
        self.name = name
        self.lastName = lastName
        self.email = name + lastName + "@ktu.edu"
        self.address = "no"
        self.salt = salt
        self.password = sha256(("password" + salt).encode('utf-8')).hexdigest()
        self.producer = 0
        self.consumer = 0
    def ToSQL(self):
        ans = "("
        ans += str(self.id) + ","
        ans += "\'" + str(self.name) + "\',"
        ans += "\'" + str(self.lastName) + "\',"
        ans += "\'" + str(self.email) + "\',"
        ans += "\'" + str(self.address) + "\',"
        ans += "\'" + str(self.password) + "\',"
        ans += "\'" + str(self.salt) + "\',"

        if self.producer == 0:
            ans += "NULL,"
        else:
            ans += str(self.producer) + ","

        if self.consumer == 0:
            ans += "NULL),\n"
        else:
            ans += str(self.consumer) + "),\n"
        return ans

class Consumer:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount
    def ToSQL(self):
        ans = "("
        ans += str(self.id) + ","
        ans += str(self.amount) + "),\n"
        return ans

class Producer:
    def __init__(self, id, amount, price):
        self.id = id
        self.amount = amount
        self.price = price
    def ToSQL(self):
        ans = "("
        ans += str(self.id) + ","
        ans += str(self.amount) + ","
        ans += str(self.price) + "),\n"
        return ans

def GetNames():
    files = ['male.txt', 'female.txt']
    names = []
    for fileName in files:
        f = open(fileName, "r", encoding="utf-8")
        temp = f.readlines()
        for i in range(len(temp)):
            if temp[i][-1] == '\n':
                temp[i]=temp[i][:-1]
        names.extend(temp)
        f.close()
    return names

def GenerateUser(id, names):
    return User(id + 1, r.choice(names), ''.join([r.choice(ascii_lowercase) for _ in range(5)]), ''.join([r.choice(ascii_lowercase) for _ in range(32)]))

def GenerateProducer(user, index):
    producer = Producer(index, r.randrange(100), r.randint(1,1000) / 1000)
    user.producer = index
    return producer
def GenerateConsumer(user, index):
    consumer = Consumer(index, r.randrange(100))
    user.consumer = index
    return consumer

def ProducerInsert(producers):
    ans = "Insert into producer(id, amount, price) values \n"
    for i in producers:
        ans += i.ToSQL()
    ans = ans[:-2]
    ans += ";"
    return ans

def ConsumerInsert(consumers):
    ans = "Insert into consumer(id, amount) values \n"
    for i in consumers:
        ans += i.ToSQL()
    ans = ans[:-2]
    ans += ";"
    return ans

def UserInsert(users):
    ans = "Insert into user(id, name, lastName, email, address, password, salt, producer, consumer) values \n"
    for i in users:
        ans += i.ToSQL()
    ans = ans[:-2]
    ans += ";"
    return ans

def WriteToFile(fileName, users, consumers, producers):
    f = open(fileName, "w", encoding="utf-8")
    f.write(ConsumerInsert(consumers))
    f.write("\n\n")
    f.write(ProducerInsert(producers))
    f.write("\n\n")
    f.write(UserInsert(users))
    f.close()


def Generate(amount, onlyProducer, onlyConsumer, fileName):
    names = GetNames()
    users = []
    producers = []
    consumers = []
    producerIndex = 1
    consumerIndex = 1
    for i in range(amount):
        temp = r.randrange(100)
        user = GenerateUser(i, names)
        if temp < onlyProducer:
            producers.append(GenerateProducer(user, producerIndex))
            producerIndex += 1
        elif temp < onlyConsumer + onlyProducer:
            consumers.append(GenerateConsumer(user, consumerIndex))
            consumerIndex += 1
        else:
            producers.append(GenerateProducer(user, producerIndex))
            producerIndex += 1
            consumers.append(GenerateConsumer(user, consumerIndex))
            consumerIndex += 1
        users.append(user)
    WriteToFile(fileName, users, consumers, producers)

Generate(amount, onlyProducer, onlyConsumer, fileName)