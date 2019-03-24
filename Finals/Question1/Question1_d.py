import numpy as np
import random
import copy
import sys
from sys import argv
np.set_printoptions(threshold=np.inf)
script,log = argv
f = open(log,'w')
__con__ = sys.stderr
sys.stderr = f

class Localization():

    def __init__(self):
        self.maze_list= []
        self.maze = np.array(self.maze_list)
        self.x = 0
        self.y = 0
        self.count = 0

    def load_file(self):
        file = 'Maze.txt'
        f = open(file,'r')

        for i, dataline in enumerate(f):
            dataline = dataline.strip('\r\n')
            line = []
            for j in range(0,len(dataline)):
                if dataline[j] == '0':
                    self.count += 1
                if dataline[j] == 'G':
                    self.Gx = i
                    self.Gy = j
                    self.count += 1
                    line.append(0)
                    continue
                line.append(int(dataline[j]))
            self.maze_list.append(line)
            self.x = i
            self.y = len(dataline)-1

        f.close()
        print('load maze successful', file=sys.stderr)
        #print(self.x,self.y)
        #print(self.count)

    def init_possibility(self):

        self.maze = np.array(self.maze_list,float)
        #print(self.maze, file=sys.stderr)
        for i in range(0,self.x+1):
            for j in range(0,self.y+1):
                if self.maze[i][j] == 0:
                    self.maze[i][j] = 1/self.count
                    #print(self.maze[i][j])
                    #input()
                else:
                    self.maze[i][j] = -1
        print('initialization of possibility successful \n', file=sys.stderr)
        #print(f'initial possibility of every blank is {1/self.count}')
        #print(self.maze, file=sys.stderr)
        #print(np.size(self.maze,0),np.size(self.maze,1))

    def observation_and_redistribution(self,obs):
        ###observation model
        move = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        for i in range(0,self.x+1):
            for j in range(0,self.y+1):
                if self.maze[i,j] != -1:
                    count = 0
                    for elem in move:
                        temp_x = i+elem[0]
                        temp_y = j+elem[1]
                        if temp_x<=self.x and temp_x>=0 and temp_y<=self.y and temp_y>=0 and self.maze[temp_x,temp_y] == -1:
                            count += 1
                    if count == obs:
                        self.maze[i,j] = self.maze[i,j]
                    else:
                        self.maze[i,j] = 0

        ###redistribution
        sum = 0
        for i in range(0,self.x+1):
            for j in range(0,self.y+1):
                if self.maze[i,j] != -1:
                    sum += self.maze[i,j]

        for i in range(0,self.x+1):
            for j in range(0,self.y+1):
                if self.maze[i,j] != -1 and self.maze[i,j] != 0:
                    self.maze[i,j] /= sum

    def left(self):
        ###transition model
        for j in range(self.y+1):
            for i in range(self.x+1):
                if self.maze[i,j] != -1 and self.maze[i,j+1] != -1:
                    self.maze[i,j] += self.maze[i,j+1]
                    self.maze[i,j+1] = 0

                else:
                    pass

if __name__ == '__main__':
    localization = Localization()
    localization.load_file()
    localization.init_possibility()

    localization.observation_and_redistribution(5)
    print('observation and redistribution successful ',file=sys.stderr)
    localization.left()
    print('move left successful ',file=sys.stderr)
    localization.observation_and_redistribution(5)
    print('observation and redistribution successful ',file=sys.stderr)
    localization.left()
    print('move left successful ',file=sys.stderr)
    localization.observation_and_redistribution(5)
    print('observation and redistribution successful ',file=sys.stderr)

    print('now the probability distribution is shown below',file=sys.stderr)

    print(localization.maze,file=sys.stderr)
