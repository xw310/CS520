##############
# add transition model; observation model is different from stationary model
##############

import numpy as np
import random
import copy
import operator
import sys
#from sys import argv

#script, filename = argv
#f= open(filename,'w')
#__con__=sys.stderr
#sys.stderr = f

class SearchAndDestroy_r2():
    '''   '''
    def __init__(self):
        self.dim = 50
        self.initial = 1/(self.dim*self.dim)
        self.list_terrain = []
        self.list_possibility = []
        self.list_for_sort = []
        self.pivotforflat = 10
        self.pivotforhill = 30
        self.pivotforforest = 70
        self.pivotforcaves = 90
        self.FindKey = False
        self.real_pos_x = random.randint(0,self.dim-1)
        self.real_pos_y = random.randint(0,self.dim-1)
        #print(f'real position is at {self.real_pos_x,self.real_pos_y}','\n',file = sys.stderr)

        self.cross_edge = []
        self.neighbor = []


    def Initialization(self):
        '''initialization'''

        for i in range(0,self.dim):
            for j in range(0,self.dim):
                value = random.randint(0,100)
                if value <= 20:
                    type = 'flat'
                    self.list_terrain.append(type)
                    self.list_possibility.append(self.initial)
                    self.list_for_sort.append([[i,j],self.initial])
                elif value <= 50:
                    type = 'hill'
                    self.list_terrain.append(type)
                    self.list_possibility.append(self.initial)
                    self.list_for_sort.append([[i,j],self.initial])
                elif value <= 80:
                    type = 'forest'
                    self.list_terrain.append(type)
                    self.list_possibility.append(self.initial)
                    self.list_for_sort.append([[i,j],self.initial])
                else:
                    type = 'cave'
                    self.list_terrain.append(type)
                    self.list_possibility.append(self.initial)
                    self.list_for_sort.append([[i,j],self.initial])

        array_terrain = np.array(self.list_terrain).reshape(self.dim,self.dim)
        array_possibility = np.array(self.list_possibility).reshape(self.dim,self.dim)
        #print(array_terrain,'\n',file = sys.stderr)
        #print(array_possibility,'\n',file = sys.stderr)
        return array_terrain, array_possibility


    def recalculating(self,pivot):

        self.neighbor = []
        #print("move on",file = sys.stderr)
        #print("recalculating the possibility",'\n',file = sys.stderr)
        sum = 0
        direction = [[0,1],[1,0],[0,-1],[-1,0]]
        #array_terrain = np.array(self.list_terrain).reshape(self.dim,self.dim)

        # observation model part
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                if self.list_terrain[i*self.dim+j]==self.cross_edge[0]:
                    count = 0
                    neighbors = []
                    for dir in direction:
                        if (i+dir[0])>=0 and (i+dir[0])<self.dim and (j+dir[1])>=0 and (j+dir[1])<self.dim :
                            if self.list_terrain[(i+dir[0])*self.dim+j+dir[1]]==self.cross_edge[1] :
                                count += 1
                                neighbors.append([i+dir[0],j+dir[1]])
                            else:
                                pass
                        else:
                            pass

                    if count>0:
                        self.neighbor.append([[i,j],neighbors,count])

                    else:
                        # not consist with observation , set possibility to 0
                        self.list_possibility[i*self.dim+j] = 0
                        #self.list_for_sort[i*self.dim+j][1] = 0

                    #print('情况1',neighbors,'\n',file = sys.stderr)

                elif self.list_terrain[i*self.dim+j]==self.cross_edge[1]:
                    count = 0
                    neighbors = []
                    for dir in direction:
                        if (i+dir[0])>=0 and (i+dir[0])<self.dim and (j+dir[1])>=0 and (j+dir[1])<self.dim :
                            if self.list_terrain[(i+dir[0])*self.dim+j+dir[1]]==self.cross_edge[0] :
                                count += 1
                                neighbors.append([i+dir[0],j+dir[1]])
                            else:
                                pass
                        else:
                            pass

                    if count>0:
                        self.neighbor.append([[i,j],neighbors,count])

                    else:
                        # not consist with observation , set possibility to 0
                        self.list_possibility[i*self.dim+j] = 0
                        #self.list_for_sort[i*self.dim+j][1] = 0

                    #print('情况2',neighbors,'\n',file = sys.stderr)

                else:   # not consist with observation , set possibility to 0
                    self.list_possibility[i*self.dim+j] = 0
                    #self.list_for_sort[i*self.dim+j][1] = 0

                    #print('情况3','\n',file = sys.stderr)

        #print('after observation', self.list_possibility,file = sys.stderr)
        #print('after observation', self.neighbor,file = sys.stderr)

        # transition model part
        flow_list=[]
        for elem in self.neighbor:
            flow = 0
            pos_x,pos_y = elem[0]
            n_b = elem[1]
            for elem1 in n_b:
                for i in range(0,len(self.neighbor)):
                    if self.neighbor[i][0] == elem1:
                        flow += self.list_possibility[elem1[0]*self.dim+elem1[1]]/self.neighbor[i][2]
                        break
                    else:
                        pass
            flow_list.append([elem[0],flow])
            #print(f'flow for {elem[0]} is {flow}',file = sys.stderr)

        for elem in flow_list:
            self.list_possibility[elem[0][0]*self.dim+elem[0][1]] = elem[1]
        #print('after transition', self.list_possibility,file = sys.stderr)


        for i in range(0,self.dim*self.dim):
            sum += self.list_possibility[i]
        coefficient = 1/sum

        for i in range(0,self.dim*self.dim):
            self.list_possibility[i] *= coefficient
            self.list_for_sort[i][1] = self.list_possibility[i]
        #print(f'after transition list_possibility={self.list_possibility}','\n\n\n',file = sys.stderr)


    def random_move(self):
        direction = [[0,1],[1,0],[0,-1],[-1,0]]
        while True:
            move = direction.pop(random.randint(0,len(direction)-1))
            temp_i = self.real_pos_x+move[0]
            temp_j = self.real_pos_y+move[1]
            if temp_i>=0 and temp_i<self.dim and temp_j>=0 and temp_j<self.dim:
                self.cross_edge = [self.list_terrain[self.real_pos_x*self.dim+self.real_pos_y],self.list_terrain[temp_i*self.dim+temp_j]]
                self.real_pos_x = temp_i
                self.real_pos_y = temp_j
                break

            else:
                pass
        #print(f'cross_edge is {self.cross_edge}','\n',file = sys.stderr)
        #print(f'real position is at {self.real_pos_x,self.real_pos_y}','\n',file = sys.stderr)


    def update(self):

        ### pick the position with biggest possibility of being in the cell

        ######### this part different from rule1
        list_possibility_r2 = []
        list_for_sort_r2 = []

        for i in range(0,self.dim*self.dim):
            type = self.list_terrain[i]
            if type == 'flat':
                pivot = self.pivotforflat
                P = 1 - pivot/100

            elif type == 'hill':
                pivot = self.pivotforhill
                P = 1 - pivot/100

            elif type == 'forest':
                pivot = self.pivotforforest
                P = 1 - pivot/100

            else:
                pivot = self.pivotforcaves
                P = 1 - pivot/100

            list_possibility_r2.append(self.list_possibility[i]*P)
            list_for_sort_r2.append([[int(i/self.dim),i%self.dim],self.list_possibility[i]*P])
        ########
        maxlist = sorted(self.list_for_sort,key=operator.itemgetter(1),reverse=True)
        maxlist_1 = []
        for i in range(0,self.dim*self.dim):
            temp = maxlist[0][1]
            if maxlist[i][1] == temp:
                maxlist_1.append(maxlist[i])
            else:
                break
        #print(f'maxlist_1={maxlist_1}','\n\n',file = sys.stderr)

        ### randomly pick one from maxlist_1
        max = maxlist_1.pop(random.randint(0,len(maxlist_1)-1))
        maxpos_i,maxpos_j = max[0]    #position
        type = self.list_terrain[maxpos_i*self.dim+maxpos_j]
        maxP = max[1]      #possibility
        #print([maxpos_i,maxpos_j],type,maxP,'\n',file = sys.stderr)

        if type == 'flat':
            pivot = self.pivotforflat

        elif type == 'hill':
            pivot = self.pivotforhill

        elif type == 'forest':
            pivot = self.pivotforforest

        else:
            pivot = self.pivotforcaves

        if max[0] == [self.real_pos_x,self.real_pos_y]:
            P_of_finding = random.randint(0,100)
            #print(f'P_of_finding is {P_of_finding}','\n',file = sys.stderr)

            if P_of_finding >= pivot:
                self.FindKey = True
                #print(f"find the target in {max[0]}",'\n',file = sys.stderr)
            else:
                self.list_possibility[maxpos_i*self.dim+maxpos_j] *= pivot/100
                #print('after update', self.list_possibility,file = sys.stderr)
                self.random_move()
                self.recalculating(pivot)


        else:
            self.list_possibility[maxpos_i*self.dim+maxpos_j] *= pivot/100
            #print('after update', self.list_possibility,file = sys.stderr)
            self.random_move()
            self.recalculating(pivot)


    def SearchDestroy(self):
        step = 0
        while not self.FindKey:
            #print(f'step={step}','\n',file = sys.stderr)
            self.update()
            step +=1
        return step

    ######binary heap to get the biggest
    #def Build_Heap(list):
    #    i = int(len(list)/2)
    #    heap = list
    #    while i > 0:
    #        Sift_Down(heap,i)
    #        i -= 1

    #def Sift_Down(heap,i):
    ######

if __name__ == '__main__':
    search = SearchAndDestroy_r2()
    search.Initialization()
    search.SearchDestroy()
