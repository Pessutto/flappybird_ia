import random as rd

BIAS = 1
p_weights = 0
p_error = 1
p_output = 2


def relu(x):
    if x < 0:
        return 0
    else:
        if x < 10000:
            return x
        else:
            return 10000


def writeDictFromJson(file, dict):
    with open(file, 'w') as arquivo:
        arquivo.write(json.dumps(dict, indent=2))

# [0] = weights, [1] = error, [2] = output
def addNeuron(weights):
    neuron = [[], 0, 1.0]
    for i in range(weights):
        neuron[0].append(rd.randrange(-1000, 1000))

    return neuron


def createNeuralNetwork(inputs, hiddenLayers, hiddenNeurons, output):
    neural = {
        "score": 0,
        "inputLayer": [],
        "hiddenLayers": [],
        "outputLayer": []
    }

    inputs += BIAS
    hiddenNeurons += BIAS

    # Cria i quantidade de neuronios de entrada sem nenhum weights
    for i in range(inputs):
        neural["inputLayer"].append(addNeuron(0))

    # Cria i quantidades de camadas escondias
    for i in range(hiddenLayers):
        tmpLayer = []

        # Cria n quantidades de neuronios em cada camada escondida
        for n in range(hiddenNeurons):
            tmpNeuron = None

            # Se for primeira camada tera "inputs" quantidade pesos
            if i == 0 :
              tmpNeuron = addNeuron(inputs)
            else:
              tmpNeuron = addNeuron(hiddenNeurons)

            # Adiciona tmpNeuron criado a tmpLayer
            tmpLayer.append(tmpNeuron)

        # Adicona tmpLayer a camadas escondidas
        neural["hiddenLayers"].append(tmpLayer)

    # Cria i quantidadr de neuronios com "hiddenNeurons" quantidade de pesos
    for i in range(output):     
        neural["outputLayer"].append(addNeuron(hiddenNeurons))

    return neural


def getOutput(neural):
    # Entra na primeira camada escondida, e percorre todos neuronios dela, multiplicando todos pesos de cada neuronio por cada output da camada de entrada
    for i in range(len(neural["hiddenLayers"][0]) - BIAS):
        result = 0
        for n in range(len(neural["inputLayer"])):
            result += neural["inputLayer"][n][p_output] * neural["hiddenLayers"][0][i][p_weights][n]

        neural["hiddenLayers"][0][i][p_output] = relu(result)

    # Faz o mesmo calculo partindo da segunda camada oculta com output da primeira (i - 1), ate a ultima camada oculta
    for i in range(1, len(neural["hiddenLayers"])):
        for n in range(len(neural["hiddenLayers"][i]) - BIAS):
            result = 0
            for k in range(len(neural["hiddenLayers"][i - 1])):
                result += neural["hiddenLayers"][i - 1][k][p_output] * neural["hiddenLayers"][i][n][p_weights][k]

        # print(result)
        neural["hiddenLayers"][i][n][p_output] = relu(result)

    output = []
    # Faz mesmo calculo com a ultima camada escondida e a camada de saida armazena no output de saida	
    for i in range(len(neural["outputLayer"])):
        result = 0
        for n in range(len(neural["hiddenLayers"][i - 1])):
            result += neural["hiddenLayers"][i - 1][n][p_output] * neural["outputLayer"][i][p_weights][n]

        # print(result)
        neural["outputLayer"][i][p_output] = relu(result)
        output.append(neural["outputLayer"][i][p_output])

    return output


def modifyWeights(neural, type):
    neural["score"] = 0
    hiddenLayers = neural["hiddenLayers"]
    outputLayer = neural["outputLayer"]

    if type == 0:
        for i in range(len(hiddenLayers)):
            for n in range(len(hiddenLayers[i])):
                for w in range(len(hiddenLayers[i][n][p_weights])):
                    hiddenLayers[i][n][p_weights][w] *= (rd.randrange(0, 10001) / 10000 + 0.5)

        for n in range(len(outputLayer)):
            for w in range(len(outputLayer[n][p_weights])):
                outputLayer[n][p_weights][w] *= (rd.randrange(0, 10001) / 10000 + 0.5)

    elif type == 1:
        for i in range(len(hiddenLayers)):
            for n in range(len(hiddenLayers[i])):
                for w in range(len(hiddenLayers[i][n][p_weights])):
                    hiddenLayers[i][n][p_weights][w] += (((rd.randrange(0, 20001) / 10.0) - 1000.0) / 100)

        for n in range(len(outputLayer)):
            for w in range(len(outputLayer[n][p_weights])):
                outputLayer[n][p_weights][w] += (((rd.randrange(0, 20001) / 10.0) - 1000.0) / 100)

    elif type == 2:
        for i in range(len(hiddenLayers)):
            for n in range(len(hiddenLayers[i])):
                for w in range(len(hiddenLayers[i][n][p_weights])):
                    hiddenLayers[i][n][p_weights][w] += ((rd.randrange(0, 20001) / 10.0) - 1000.0)

        for n in range(len(outputLayer)):
            for w in range(len(outputLayer[n][p_weights])):
                outputLayer[n][p_weights][w] += ((rd.randrange(0, 20001) / 10.0) - 1000.0)


def addInputs(neural, sensorList):
    for i in range(len(neural["inputLayer"]) - BIAS):
        neural["inputLayer"][i][p_output] = sensorList[i]