import numpy as np
import copy
import sys
from sys import argv

script,log = argv
f = open(log,'w')
__con__ = sys.stderr
sys.stderr = f

class Iteration():

    def __init__(self):
        self.times = 2000
        self.rate = 0.9

        self.new = 0
        self.dead = 0
        self.u = [0,0,0,0,0,0,0,0,self.dead]

        self.step = {}
        self.step.setdefault('new', [])
        self.step.setdefault('dead', [])
        self.step.setdefault('u1', [])
        self.step.setdefault('u2', [])
        self.step.setdefault('u3', [])
        self.step.setdefault('u4', [])
        self.step.setdefault('u5', [])
        self.step.setdefault('u6', [])
        self.step.setdefault('u7', [])
        self.step.setdefault('u8', [])

    def update(self):
        for i in range(0, self.times):
            new = 100+self.rate*self.u[0]
            dead = -250+self.rate*self.new
            self.step['new'].append('use')
            self.step['dead'].append('replace')

            u = []
            for j in range(0,8):
                #print(self.u[j])
                #input()
                e1 = (100-10*(j+1))+self.rate*((1-0.1*(j+1))*self.u[j]+0.1*(j+1)*self.u[j+1])
                e2 = -250+self.rate*self.new
                if e1>=e2:
                    u.append(e1)
                    name = f'u{j+1}'
                    self.step[name].append('use')
                else:
                    u.append(e2)
                    name = f'u{j+1}'
                    self.step[name].append('replace')

            if i>0 and i%20 == 0:
                print(f'iteration times: {i} times',file=sys.stderr)
                #input('press any to go on')
                bias = [abs(self.u[i]-u[i]) for i in range(0,8)]
                bias.append(abs(self.new-new))
                bias.append(abs(self.dead-dead))
                if max(bias) < 0.001:
                    print('now the iteration converges',file=sys.stderr)
                    break

            self.new = new
            self.dead = dead
            u.append(self.dead)
            self.u = copy.deepcopy(u)
            #print(u)
            #input()

    def print_iteration(self):
        ###### print utility
        print(f'optimal for "new": {self.new}',file=sys.stderr)
        print('\n',file=sys.stderr)
        for i in range(0,8):
            print(f'optimal for used{i+1}: {self.u[i]}',file=sys.stderr)
            print('\n',file=sys.stderr)
        print(f'optimal for "dead": {self.dead}',file=sys.stderr)

        print('\n'*3,file=sys.stderr)

        ###### print iteration
        for item in self.step:
            print(f'iteration for {item}: {self.step[item]}',file=sys.stderr)
            print('\n',file=sys.stderr)

if __name__ == '__main__':

    iteration = Iteration()
    iteration.update()
    iteration.print_iteration()
