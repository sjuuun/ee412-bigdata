import sys
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Fully_Connected_Layer:
    def __init__(self, learning_rate):
        self.InputDim = 784
        self.HiddenDim = 128
        self.OutputDim = 10
        self.learning_rate = learning_rate

        '''Weight Initialization'''
        self.W1 = np.random.randn(self.InputDim, self.HiddenDim)
        self.W2 = np.random.randn(self.HiddenDim, self.OutputDim)

        '''Step Initialization'''
        self.u = None
        self.u_sig = None
        self.v = None

    def Forward(self, Input):
        '''Implement forward propagation'''
        self.u = Input.dot(self.W1)
        self.u_sig = sigmoid(self.u)
        self.v = self.u.dot(self.W2)
        return sigmoid(self.v)

    def Backward(self, Input, Label, Output):
        '''Implement backward propagation'''
        '''Update parameters using gradient descent'''
        #loss = 0.5 * np.square(Output - Label).sum()
        #print loss
        
        grad_y = Output - Label
        #print grad_y
        #print np.shape(grad_y)
        grad_v = (Output * (1 - Output)) * grad_y
        #print np.shape(grad_v)
        grad_W2 = self.u_sig.T.dot(grad_v)
        #print np.shape(grad_W2)
        grad_u_sig = grad_v.dot(self.W2.T)
        grad_u = (self.u_sig * (1 - self.u_sig)) * grad_u_sig
        grad_W1 = Input.T.dot(grad_u)

        self.W1 -= self.learning_rate * grad_W1
        self.W2 -= self.learning_rate * grad_W2


    def Train(self, Input, Label):
        Output = self.Forward(Input)
        self.Backward(Input, Label, Output)

    def Test(self, Input, Label):
        Output = self.Forward(Input)
        assert (np.shape(Label) == np.shape(Output))
        count = 0.0
        for i in range(len(Label)):
            if np.argmax(Label[i]) == np.argmax(Output[i]):
                count += 1
        print count
        return count / len(Label)


'''Construct a fully-connected network'''
learning_rate = 5e-2
Network = Fully_Connected_Layer(learning_rate)

'''Get input - train set and test set'''
f_train = open(sys.argv[1], 'r')
f_test = open(sys.argv[2], 'r')
train_set = np.array([list(map(float, line.split(','))) for line in f_train.readlines()])
test_set =  np.array([list(map(float, line.split(','))) for line in f_test.readlines()])

'''Train the network for the number of iterations'''
'''Implement function to measure the accuracy'''
train_data = train_set[:, :-1]
train_label = np.zeros((1000,10))
train_label[np.arange(1000), list(map(int,train_set[:, -1]))] = 1
test_data = test_set[:, :-1]
test_label = np.zeros((len(test_set), 10))
test_label[np.arange(len(test_set)), list(map(int, test_set[:, -1]))] = 1

epoch = 100
for j in range(epoch):
    #iteration = len(train_set)
    iteration = 100
    for i in range(iteration):
        '''
        train_data = train_set[:, :-1]
        #train_data = train_data.reshape(1000, 784)
        train_label = np.zeros((1000,10))
        train_label[np.arange(1000), list(map(int,train_set[:, -1]))] = 1
        '''
        Network.Train(train_data, train_label)

    '''Test the network with test_set'''
    '''
    test_data = test_set[:, :-1]
    test_label = np.zeros((len(test_set), 10))
    test_label[np.arange(len(test_set)), list(map(int, test_set[:, -1]))] = 1
    '''
    print "Accuracy %d: %f" % (j, Network.Test(test_data, test_label))
