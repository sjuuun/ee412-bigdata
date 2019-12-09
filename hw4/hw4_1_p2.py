import sys
import numpy as np

class Fully_Connected_Layer:
    def __init__(self, learning_rate):
        self.InputDim = 784
        self.HiddenDim = 128
        self.OutputDim = 10
        self.learning_rate = learning_rate
        
        '''Weight Initialization'''
        self.W1 = np.random.randn(self.InputDim, self.HiddenDim)
        self.W2 = np.random.randn(self.HiddenDim, self.OutputDim) 
        
    def Forward(self, Input):
        '''Implement forward propagation'''
        return Output
    
    def Backward(self, Input, Label, Output):
        '''Implement backward propagation'''
        '''Update parameters using gradient descent'''
    
    def Train(self, Input, Label):
        Output = self.Forward(Input)
        self.Backward(Input, Label, Output)        

'''Construct a fully-connected network'''        
#Network = Fully_Connected_Layer(learning_rate)

'''Get input - train set and test set'''
f_train = open(sys.argv[1], 'r')
f_test = open(sys.argv[2], 'r')
train_set = [np.array(list(map(float, line.split(',')))) for line in f_train.readlines()]
test_set =  [np.array(list(map(float, line.split(',')))) for line in f_test.readlines()]

'''Train the network for the number of iterations'''
'''Implement function to measure the accuracy'''
#iteration = len(train_set)
iteration = 1
for i in range(iteration):
    train_data = train_set[i][:-1]
    train_label = np.zeros(10)
    train_label[int(train_set[i][-1])] = 1
#    Network.Train(train_data, train_label)
    
