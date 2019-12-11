import numpy as np
import math
def sigmoid(x):
    return 1/(1+pow(math.e, -x))
class neuralNetwork:
    def __init__(self, inputnodes = 3, hiddennodes = 3, outputnodes = 3, learningrate = 0.3):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        self.lr = learningrate
        #简单的权重初始方法
        #self.wih = np.random.rand(self.hnodes, self.inodes) - 0.5
        #self.who = np.random.rand(self.onodes, self.hnodes) - 0.5
        #较为复杂的权重初始方法，但更加有效
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        self.activation_function = lambda x: sigmoid(x)
        pass

    def nn_load(self, inodes, hnodes, onodes, lr, wih, who):
        self.inodes = inodes
        self.hnodes = hnodes
        self.onodes = onodes
        self.lr = lr
        self.wih = wih
        self.who = who

    def nn_dump(self):
        return [self.inodes, self.hnodes, self.onodes, self.lr, self.wih, self.who]

    def train(self, inputs_list, targets_list):
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        output_errors = targets - final_outputs
        hidden_errors = np.dot(self.who.T, output_errors)
        self.who = self.who + self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))
        self.wih = self.wih + self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))
        pass

    #forward the net
    def query(self, inputs_list):
        #convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        #calculate the signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_input = np.dot(self.who, hidden_outputs)
        final_output = self.activation_function(final_input)
        return final_output
        pass


