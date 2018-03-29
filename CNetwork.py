from CLayer import *
import numpy as np
from functions import *

# Not yet that flexible neural network class

class CNetwork:

    def __init__(self, learn_rate):

        # Layer list which stores all layer
        self.layers = []
        self.learn_rate = learn_rate

        # create input layer with 400 neurons and append to list
        self.layers.append(CLayer("I", 400, 400))

        # create hidden layer with 10 neurons and append to list
        self.layers.append(CLayer("H", 10, self.layers[0].getNeuronCount()))

        # create output layer with 10 neurons and append to list
        self.layers.append(CLayer("O", 10, self.layers[1].getNeuronCount()))

        # loading layer matrices for each layer from disk
        for index, l in enumerate(self.layers):
            l.loadFromFile(index)

    def guess(self, input):

        # put input in input layer
        self.layers[0].forward(input)

        # get output of input layer and put it as input in the second layer
        self.layers[1].forward(self.layers[0].getY())

        # get output of hidden layer and put it as input in the third layer
        self.layers[2].forward(self.layers[1].getY())

        return self.layers[2].getY()


    # feedforward the input matrix trough the network compares the output with the target
    def learn(self, input, target):

        output = self.guess(input)

        # only learn if error is over 0.1 to not overlearn the network
        if self.getError(target) > 0.1:

            # direct error of output to target
            l3_error = target - output
            l3_delta = l3_error * dsigmoid(self.layers[2].getX())

            # error from output of the second layer
            l2_error = l3_delta.dot(self.layers[2].getWeights().T)
            l2_delta = l2_error * dsigmoid(self.layers[1].getX())

            # calculate new weights between second and third layer
            new_weight_23 = self.layers[2].getWeights() + (self.layers[1].getY().T.dot(l3_delta) * self.learn_rate)

            # calculate new weights between first and second layer
            new_weight_12 = self.layers[1].getWeights() + (self.layers[0].getY().T.dot(l2_delta) * self.learn_rate)

            # sets new weights between second and third layer
            self.layers[2].setWeights(new_weight_23)

            # sets new weights between first and second layer
            self.layers[1].setWeights(new_weight_12)

    # ------------------------------------------------------------------------------------------------------------------

    # Returns the Error of the Output Layer to the given target

    def getError(self, target):
        return self.layers[2].getError(target)

    # ------------------------------------------------------------------------------------------------------------------

    # Saves each weight matrix for each layer of the network to file
    def saveToFile(self):
        for index, l in enumerate(self.layers):
            l.saveToFile(index)