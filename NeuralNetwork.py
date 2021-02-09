import random as rd

BIAS = 1

def relu(x):
  if x < 0:
    return 0
  else:
    if x < 10000:
      return x
    else:
      return 10000

class Neuron:
  weights = []
  error = 0
  output = 0
  amountConnections = 0

  def __init__(self) -> None:
      pass

class Layer:
  neuronList = None
  amountNeuron = 0

  def __init__(self) -> None:
      pass

class NeuralNetwork: # Cerebro
  inputLayer = None
  hiddenLayerList = None
  outputLayer = None

  amountHidden = 0


  # RNA_CopiarParaEntrada
  def addNeuronInput(self, imputList):
    for i in range(0, (self.inputLayer.amountNeuron - BIAS)):
      self.inputLayer.neuronList[i].output = imputList[i]

  # RNA_CalcularSaida
  def calculateOutput(self):

    # Calculando saidas entre a camada de entrada e a primeira camada escondida
    for i in range(0, (self.hiddenLayerList[0].amountNeuron - BIAS)):
      total = 0
      for n in range(0, self.inputLayer.amountNeuron):
        total += self.inputLayer.neuronList[n].output * self.hiddenLayerList[0].neuronList[i].weights[n]

      self.hiddenLayerList[0].neuronList.output = relu(total)

    # Calculando saidas entre a camada escondida k e a camada escondida k-1
    for i in range(1, self.amountHidden):
      for n in range(0, (self.hiddenLayerList[i].amountNeuron - BIAS)):
        total = 0
        for j in range(0, self.inputLayer[i-1].amountNeuron):
          total += self.hiddenLayerList[i-1].neuronList[j].output * self.hiddenLayerList.neuronList[n].weights[j]

        self.hiddenLayerList[i].neuronList[i].output = relu(total)

    # Calculando saidas entre a camada de saida e a ultima camada escondida 
    for i in range(0, self.outputLayer.amountNeuron):
      total = 0
      for j in range(0, self.hiddenLayerList[k-1].amountNeuron):
        total += self.hiddenLayerList[k-1].neuronList[j].output * self.outputLayer.neuronList[i].weights[j]

        self.outputLayer.neuronList[i].outpot = relu(total)

  # RNA_CopiarDaSaida
  def getOutput(self):
    output = []
    for i in range (0, self.outputLayer.amountNeuron):
      output.append(self.outputLayer.neuronList[i].output)

    return output

  # RNA_CopiarVetorParaCamadas
  def setWeigths(self, vetor):
    j = 0
    for i, in range(0, self.amountHidden):
      for k in range(0, self.hiddenLayerList[i].amountNeuron):
        for l in range(0, self.hiddenLayerList[i].neuronList[k].amountNeuron):
          self.hiddenLayerList[i].neuronList[k].weights[l] = vetor[j]
          j += 1

    #######
    k = 0
    for k in range(0, self.outputLayer.amountNeuron):
      for n in range(0, self.outputLayer.neuronList[k].amountConnections):
        self.outputLayer.neuronList[k].weights[n] = vetor[j]
        j += 1

  # RNA_CopiarCamadasParaVetor
  def getWeights(self):
    j = 0
    vetor = []
    for i in range(0, self.amountHidden):
      for k in range(0, self.hiddenLayerList[i].amountNeuron):
        for l in range(0, self.hiddenLayerList[i].neuronList[k].amountConnections):
          vetor.append(self.hiddenLayerList[i].neuronList[k].weights[l])
          j += 1

    #####
    k = 0
    for k in range(0, self.outputLayer.amountNeuron):
      for n in range(0, self.outputLayer.neuronList[k].amountConnections):
        vetor.append(self.outputLayer.neuronList[k].weights[n])
        j += 1

    return vetor

  # RNA_QuantidadePesos
  def getAmountWeights(self):
    total = 0
    for i in range(0, self.amountHidden):
      for j in range(0, self.hiddenLayerList[i].amountNeuron):
        total += self.hiddenLayerList[i].neuronList[j].amountConnections

    for k in range(0, self.outputLayer.amountNeuron):
      total += self.outputLayer.neuronList.amountConnections

    return total

  # RNA_CriarNeuronio
  def makeNeuron(self, neuron, amountConnections):
    neuron.amountConnections = amountConnections

    for i in range(0, amountConnections):
      neuron.weights.append(rd.randrange(-1000, 1000))

    neuron.error = 0
    neuron.output = 1

  # RNA_CriarRedeNeural
  def __init__(self, amountHidden, amountNeuronInput, amountNeuronHidden, amountNeuronOutput):
    amountNeuronInput += BIAS
    amountNeuronHidden += BIAS

    self.inputLayer = Layer()
    self.inputLayer.amountNeuron = amountNeuronInput

    self.inputLayer.neuronList = []
    for i in range(0, amountNeuronInput):
      self.inputLayer.neuronList.append(Neuron())
      self.inputLayer.neuronList[i].output = 1.0

    self.amountHidden = amountHidden

    self.hiddenLayerList = []
    for n in range(0, amountHidden):
      self.hiddenLayerList.append(Layer())
      self.hiddenLayerList[n].amountNeuron = amountNeuronHidden

      self.hiddenLayerList[n].neuronList = []
      for k in range(0, amountNeuronHidden):
        self.hiddenLayerList[n].neuronList.append(Neuron())

        if n == 0:
          self.makeNeuron(self.hiddenLayerList[n].neuronList[k], amountNeuronInput)
        else:
          self.makeNeuron(self.hiddenLayerList[n].neuronList[k], amountNeuronHidden)

    self.outputLayer = Layer()
    self.outputLayer.amountNeuron = amountNeuronOutput

    self.outputLayer.neuronList = []
    for i in range(0, amountNeuronInput):
      self.outputLayer.neuronList.append(Neuron())
      self.makeNeuron(self.outputLayer.neuronList[i], amountNeuronOutput)




rn = NeuralNetwork(2, 9, 10, 1)


#     Rede->CamadaSaida.QuantidadeNeuronios = QtdNeuroniosSaida;
#     Rede->CamadaSaida.Neuronios = (Neuronio*)malloc(QtdNeuroniosSaida*sizeof(Neuronio));

#     for(j=0; j < QtdNeuroniosSaida; j++)
#     {
#         RNA_CriarNeuronio(&Rede->CamadaSaida.Neuronios[j], QtdNeuroniosEscondida);
#     }

#     //printf("Criada uma Rede Neural com:\n\n1 Camada de entrada com %d neuronio(s) + 1 BIAS.\n%d Camada(s) escondida(s), cada uma com %d neuronio(s) + 1 BIAS.\n1 Camada de saida com %d neuronio(s).\n", QtdNeuroniosEntrada-1, QuantidadeEscondidas, QtdNeuroniosEscondida-1, QtdNeuroniosSaida);

#     return Rede;
# }
