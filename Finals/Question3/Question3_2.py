import numpy as np
import random
import copy
import sys
from sys import argv

script,log = argv
f = open(log,'w')
__con__ = sys.stderr
sys.stderr = f

class Perceptron():

    def __init__(self):
        a1 = [np.array([ 1,-1,-1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1,-1,-1, 1,-1,-1, 1, 1,-1,-1,-1,-1, 1]),0]
        a2 = [np.array([-1,-1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1,-1,-1,-1,-1]),0]
        a3 = [np.array([ 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1,-1,-1,-1,-1,-1,-1,-1, 1, 1,-1,-1,-1,-1, 1]),0]
        a4 = [np.array([-1,-1, 1, 1, 1, 1,-1,-1,-1,-1, 1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1,-1,-1,-1,-1]),0]
        a5 = [np.array([-1,-1,-1, 1, 1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1]),0]
        b1 = [np.array([ 1, 1,-1,-1, 1, 1, 1,-1,-1, 1,-1, 1,-1, 1, 1,-1,-1,-1, 1, 1, 1,-1,-1, 1, 1]),1]
        b2 = [np.array([ 1,-1,-1, 1, 1,-1,-1,-1,-1, 1,-1,-1,-1,-1, 1, 1,-1,-1, 1,-1, 1, 1, 1, 1,-1]),1]
        b3 = [np.array([ 1,-1, 1,-1,-1, 1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 1, 1, 1, 1,-1, 1]),1]
        b4 = [np.array([ 1, 1, 1, 1,-1, 1,-1,-1, 1,-1,-1,-1,-1, 1, 1,-1,-1, 1, 1,-1,-1,-1, 1, 1,-1]),1]
        b5 = [np.array([ 1,-1, 1, 1,-1,-1,-1,-1, 1,-1,-1, 1,-1, 1,-1, 1, 1,-1, 1,-1, 1, 1,-1, 1,-1]),1]
        c1 = np.array([ 1,-1,-1, 1,-1, 1,-1,-1,-1,-1,-1,-1, 1, 1, 1,-1,-1, 1,-1, 1, 1,-1, 1,-1, 1])
        c2 = np.array([ 1, 1,-1,-1,-1,-1, 1,-1,-1,-1, 1,-1, 1, 1,-1,-1,-1, 1,-1, 1,-1, 1, 1, 1, 1])
        c3 = np.array([-1,-1, 1, 1, 1, 1, 1, 1,-1, 1,-1,-1,-1,-1, 1, 1, 1, 1, 1,-1,-1,-1,-1, 1, 1])
        c4 = np.array([ 1,-1,-1,-1, 1, 1,-1,-1,-1, 1,-1,-1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1])
        c5 = np.array([-1, 1, 1, 1, 1,-1, 1,-1,-1, 1, 1, 1, 1, 1,-1, 1,-1,-1, 1,-1, 1, 1, 1, 1, 1])
        self.train = [a1,a2,a3,a4,a5,b1,b2,b3,b4,b5]
        self.test = [c1,c2,c3,c4,c5]
        #self.labels = ['A','A','A','A','A','B','B','B','B','B']

        self.weight = []
        [self.weight.append(random.random()) for i in range(0,25)]
        self.weight = np.array(self.weight)
        self.bias = random.random()

        self.rate = 0.05
        self.times = 2000

        self.error = []

        print('initialization successful',file=sys.stderr)

    def training(self):
        for i in range(0,self.times):
            elem, label = random.choice(self.train)
            #print(elem,label)
            res = np.dot(elem,self.weight)
            #print(res)
            #input()
            if res>=0:
                res = 1
            else:
                res = 0

            error = abs(res-label)
            self.error.append(error)

            self.weight -= self.rate*error*elem

    def classify(self):
        for ith, elem in enumerate(self.test):
            res = np.dot(elem,self.weight)
            if res>=0:
                res = 'A'
            else:
                res = 'B'
            print(f'c{ith+1} belongs to {res}',file=sys.stderr)


if __name__ == '__main__':
    perceptron = Perceptron()
    print(perceptron.weight)
    perceptron.training()
    perceptron.classify()
