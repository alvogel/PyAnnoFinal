import numpy as np
from functions import *
import os.path
import string

class CLayer:

    # constructor of this layer with n-neurons
    # n = number of neurons in this layer
    # inputs = number of neurons from layer before

    def __init__(self, layerType, neurons, inputs):

        # I = INPUT; H = HIDDEN; O = OUTPUT;
        self.layerType = layerType

        # number of neurons in this layer
        self.neurons = neurons

        self.state = 0
        self.x = 0

        if layerType == "I":

            # create eye matrix for input layer because input from first layer should equal the output
            self.weights = np.eye(neurons)

        else:
            # create random but gaussian distributed weights with a distance from 1 around 0
            self.weights = np.random.normal(0, 1, (inputs, neurons))



    # ------------------------------------------------------------------------------------------------------------------

    def forward(self, input):

        # if input layer set output = input
        if self.layerType == "I":
            input = input/255 # normalize data
            self.x = input.dot(self.weights)
            self.state = input.dot(self.weights)

        # else use weights and activation function
        else:

            self.x = input.dot(self.weights)
            self.state = sigmoid(input.dot(self.weights))

    # ------------------------------------------------------------------------------------------------------------------

    def getError(self, target):
        error = np.sum((target - self.getY()) ** 2) / 2
        return error

    # ------------------------------------------------------------------------------------------------------------------

    def setWeights(self, new_weights):
        self.weights = new_weights

    # ------------------------------------------------------------------------------------------------------------------

    def getX(self):
        return self.x

    # ------------------------------------------------------------------------------------------------------------------

    def getY(self):
        return self.state

    # ------------------------------------------------------------------------------------------------------------------

    def getWeights(self):
        return self.weights

    # ------------------------------------------------------------------------------------------------------------------

    # return quantity of neurons
    def getNeuronCount(self):
        return self.neurons

    # ------------------------------------------------------------------------------------------------------------------

    # stores weights of this layer to file
    def saveToFile(self, id):

        f = open("data/weight_matrices/"+str(id)+".wgt", 'w')
        for r in range(self.weights.shape[0]):
            line = ""
            for c in range(self.weights.shape[1]):
                line += str(self.weights[r][c])+":"

            line = line[0:-1]
            f.write(line+'\n')
        f.close()

    # ------------------------------------------------------------------------------------------------------------------

    def loadFromFile(self, id):

        if os.path.exists("data/weight_matrices/" + str(id) + ".wgt"):
            lines = [line.rstrip('\n') for line in open("data/weight_matrices/"+str(id)+".wgt")]
            for index, l in enumerate(lines):
                elements = l.split(":")
                row = []

                for e in elements:
                    row.append(float(e))

                if index == 0:
                    matrix = np.array([row])
                else:
                    matrix = np.vstack([matrix, row])

            self.weights = matrix