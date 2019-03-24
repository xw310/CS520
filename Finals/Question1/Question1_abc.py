import numpy as np
import random
import copy
import sys
from sys import argv

#script,log = argv
#f = open(log,'w')
#__con__ = sys.stderr
#sys.stderr = f

class Localization():

    def __init__(self):
        self.maze_list= []
        self.maze = np.array(self.maze_list)
        self.x = 0
        self.y = 0
        self.count = 0

        self.Gx = 0
        self.Gy = 0

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
        print('initialization of possibility successful', file=sys.stderr)
        #print(f'initial possibility of every blank is {1/self.count}')
        #print(self.maze, file=sys.stderr)
        #print(np.size(self.maze,0),np.size(self.maze,1))

    def up(self):
        for i in range(self.x+1):
            #line1 = self.maze[i]
            #line2 = self.maze[i+1]
            for j in range(self.y+1):
                if self.maze[i][j]!= -1 and self.maze[i+1][j]!= -1:
                    self.maze[i][j] += self.maze[i+1][j]
                    self.maze[i+1][j] = 0
                #if line1[j] != -1 and line2[j] != -1:
                    #line1[j] += line2[j]
                    #line2[j] = 0
                else:
                    pass

        print('up successful once', file=sys.stderr)
        #print(self.maze, file=sys.stderr)

    def down(self):
        for i in range(self.x+1):
            for j in range(self.y+1):
                if self.maze[self.x-i][j]!= -1 and self.maze[self.x-i-1][j]!= -1:
                    self.maze[self.x-i][j] += self.maze[self.x-i-1][j]
                    self.maze[self.x-i-1][j] = 0

                else:
                    pass

        print('down successful once', file=sys.stderr)
        #print(self.maze, file=sys.stderr)

    def left(self):
        for j in range(self.y+1):
            for i in range(self.x+1):
                if self.maze[i,j] != -1 and self.maze[i,j+1] != -1:
                    self.maze[i,j] += self.maze[i,j+1]
                    self.maze[i,j+1] = 0

                else:
                    pass

        print('left successful once', file=sys.stderr)
        #print(self.maze, file=sys.stderr)

    def right(self):
        for j in range(self.y+1):
            for i in range(self.x+1):
                if self.maze[i,self.y-j] != -1 and self.maze[i,self.y-j-1] != -1:
                    self.maze[i,self.y-j] += self.maze[i,self.y-j-1]
                    self.maze[i,self.y-j-1] = 0
                else:
                    pass

        print('right successful once', file=sys.stderr)
        #print(self.maze, file=sys.stderr)

    def find_dis(self):
        max_dis = 0
        for i in range(self.x):
            for j in range(self.y):
                if self.maze[i][j] != -1 and self.maze[i][j] != 0:
                    dis = abs(i-self.Gx)+abs(j-self.Gy)
                    if dis > max_dis:
                        max_dis = dis
        return max_dis

    def find_maxelem(self):
        max_elem_list = []
        max = np.max(self.maze)
        p1,p2 = np.where(self.maze==max)
        for i in range(len(p1)):
            max_elem_list.append([p1[i],p2[i]])
        return max,max_elem_list

if __name__ == '__main__':
    localization = Localization()
    localization.load_file()
    localization.init_possibility()
    #localization.up()
    #localization.down()
    #localization.left()
    #localization.right()
    step = []
    #max_dis = 150
    max_dis = abs(1-localization.Gx)+abs(1-localization.Gy)
    #print(max_dis)
    while True:
        #input()
        maze = copy.deepcopy(localization.maze)
        localization.down()
        max = localization.find_dis()
        print(f'the longest distance to G: {max}', file=sys.stderr)
        #input('stop')
        if max<max_dis:
            step.append('down')
            max_dis = max
        else:
            if random.random()<0.25:
                step.append('down')

            else:
                print('down refused', file=sys.stderr)
                localization.maze = copy.deepcopy(maze)
                localization.right()
                max = localization.find_dis()
                print(f'the longest distance to G: {max}', file=sys.stderr)
                if max<max_dis:
                    step.append('right')
                    max_dis = max

                else:
                    if random.random()<0.25:
                        step.append('right')

                    else:
                        print('right refused', file=sys.stderr)
                        localization.maze = copy.deepcopy(maze)
                        localization.up()
                        max = localization.find_dis()
                        print(f'the longest distance to G: {max}', file=sys.stderr)
                        if max<max_dis:
                            step.append('up')
                            max_dis = max

                        else:
                            if random.random()<0.2:
                                step.append('up')

                            else:
                                print('up refused', file=sys.stderr)
                                localization.maze = copy.deepcopy(maze)
                                localization.left()
                                max = localization.find_dis()
                                print(f'the longest distance to G: {max}', file=sys.stderr)
                                if max<max_dis:
                                    step.append('left')
                                    max_dis = max

                                else:
                                    if random.random()<0.2:
                                        step.append('left')

                                    else:
                                        print('left refused', file=sys.stderr)
                                        localization.maze = copy.deepcopy(maze)

        print('one iteration completed \n', file=sys.stderr)
        #input()
        max_elem,max_elem_list = localization.find_maxelem()
        print(f'the maximum possibility is {max_elem}', file=sys.stderr)
        if max_elem>=0.8:
            print('possobility converges bigger than 0.5\n\n', file=sys.stderr)
            print(f'cells with possibility bigger than 0.5: {max_elem_list} \n\n', file=sys.stderr)
            print(f'{len(step)} steps taken to converge', file=sys.stderr)
            print(f'steps: {step}\n\n', file=sys.stderr)

            list=[]
            for i in range(localization.x+1):
                for j in range(localization.y+1):
                    if localization.maze[i,j]!=0 and localization.maze[i,j]!=-1:
                        list.append([i,j])
            print('now only following cell has probability', file=sys.stderr)
            print(list, file=sys.stderr)
            break
