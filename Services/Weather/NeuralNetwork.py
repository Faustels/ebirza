import numpy as np
import json

def Shuffle(inputs, outputs):
   newInputs = []
   newOutputs = []
   pos = [i for i in range(len(inputs))]
   np.random.shuffle(pos)
   for i in pos:
      newInputs.append(inputs[i])
      newOutputs.append(outputs[i])
   return np.array(newInputs), np.array(newOutputs)

def Nonlin(x, deriv = False):
   if (deriv == True):
      return x * (1 - x)
   return 1 / (1 + np.exp(-x))

def GenSyn(x, y):
   return 2 * np.random.random((x,y)) - 1

class NeuralNetwork:
   def __init__(self, weightCount = []):
      self.synapses = []
      for i in range(len(weightCount) - 1):
         self.synapses.append(GenSyn(weightCount[i] ,weightCount[i+1]))

   def Train(self, inputs, outputs, epochs, batchSize = 0, shuffle = False):
      if shuffle:
         inputs, outputs = Shuffle(inputs, outputs)
      if batchSize != 0:
         batches = len(inputs) // batchSize
         for i in range(epochs):
            for batch in range(batches):
               self.TrainBatch(inputs[batch * batchSize: (batch + 1) * batchSize]
                            , outputs[batch * batchSize: (batch + 1) * batchSize])
            self.TrainBatch(inputs[batchSize * batches:]
                            , outputs[batchSize * batches:])
      else:
         for i in range(epochs):
            self.TrainBatch(inputs, outputs)

   def TrainBatch(self, inputs, outputs):
      layers = self.Input(inputs)
         
      errors, deltas = self.ErrorsAndDeltas(layers, outputs)
      self.UpdateSynapses(layers,deltas)

   def Input(self, inputs):
      layers = []
      layers.append(inputs)
      for synapse in self.synapses:
         layers.append(Nonlin(np.dot(layers[-1], synapse)))
      return layers

   def ErrorsAndDeltas(self, layers, outputs):
      errors = []
      deltas = []
      errors.append(outputs - layers[-1])
      deltas.append(errors[0] * Nonlin(layers[-1], deriv=True))

      for i in range(1, len(self.synapses)):
         errors.append(deltas[-1].dot(self.synapses[-i].T))
         deltas.append(errors[-1] * Nonlin(layers[-i-1], deriv = True))
      errors.reverse()
      deltas.reverse()

      return errors, deltas

   def UpdateSynapses(self, layers, deltas):
      for i in range(len(self.synapses)):
         self.synapses[i] += layers[i].T.dot(deltas[i])

   def GetR(self, inputs, outputs):
      prediction = self.Input(inputs)[-1]
      errors = outputs - prediction
      errors = errors ** 2
      errors = sum(errors)
      averages = sum(outputs) / len(outputs)
      averages = sum((outputs - averages)**2)
      return 1 - errors/averages  

   def SaveNetwork(self, fileName):
      ans = []
      for i in self.synapses:
         ans.append(i.tolist())
      networkJson = json.dumps(ans, indent=4)
      with open(fileName, "w") as file:
         file.write(networkJson)

   def LoadNetwork(fileName):
      with open(fileName, "r") as file:
         networkJson = json.load(file)
      newNetwork = NeuralNetwork([])
      newNetwork.synapses = []
      for i in networkJson:
         newNetwork.synapses.append(np.array(i))
      return newNetwork

