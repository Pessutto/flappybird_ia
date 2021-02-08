class Neuron:
  weights = []
  error = 0.0
  output = 0.0
  amountConnections = 0

class Layer:
  neuronList = None
  amountNeuron = 0


class NeuralNetwork:
  inputLayer = None
  hiddenLayerList = None
  outputLayer = None

  amountHidden = 0

  def addNeuronEntry(self, imputList):
    for i in range(0, (self.inputLayer.amountNeuron - BIAS)):
      self.inputLayer.neuronList[i].output = imputList[i]

  def getOutput(self):
    for i in range(0, (self.hiddenLayerList[0].amountNeuron - BIAS)):
      total = 0
      for n in range(0, self.inputLayer.amountNeuron):
        total += self.inputLayer.neuronList[n].output * self.hiddenLayerList[0].neuronList[i].weights[n]

      self.hiddenLayerList[0].neuronList.output = relu(total)

    for i in range(1, self.amountHidden):
      for n in range(0, (self.hiddenLayerList[i].amountNeuron - BIAS)):
        total = 0
        for j in range(0, self.inputLayer[i-1].amountNeuron):
          total += self.hiddenLayerList[i-1].neuronList[j].output * self.hiddenLayerList.neuronList[n].weights[j]

        self.hiddenLayerList[i].neuronList[i].output = relu(total)

    for i in range(0, self.outputLayer.amountNeuron)
      total = 0
        for j in range(0, self.hiddenLayerList[k-1].amountNeuron):
          total += self.hiddenLayerList[k-1].neuronList[j].output * self.outputLayer.neuronList[i].weights[j]
        }
        self.outputLayer.neuronList[i].outpot = relu(total)



def relu(x):
  if x < 0:
    return 0
  else:
    if x < 10000:
      return x
    else:
      return 10000