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

class SearchAndDestroy_change_r1():
    '''   '''
    def __init__(self):
        self.dim = 20
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

        self.now_pos_x = random.randint(0,self.dim-1)
        self.now_pos_y = random.randint(0,self.dim-1)
        self.step = 0

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

                    #print('situation 1',neighbors,'\n',file = sys.stderr)

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

                    #print('situation 2',neighbors,'\n',file = sys.stderr)

                else:   # not consist with observation , set possibility to 0
                    self.list_possibility[i*self.dim+j] = 0
                    #self.list_for_sort[i*self.dim+j][1] = 0

                    #print('situation 3','\n',file = sys.stderr)

        #print('after observation list_possibility', self.list_possibility,file = sys.stderr)
        #print('after observation neighbor', self.neighbor,file = sys.stderr)

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
        #print('after transition list_possibility=', self.list_possibility,file = sys.stderr)


        for i in range(0,self.dim*self.dim):
            sum += self.list_possibility[i]
        coefficient = 1/sum

        for i in range(0,self.dim*self.dim):
            self.list_possibility[i] *= coefficient
            self.list_for_sort[i][1] = self.list_possibility[i]
        #print(f'after transition list_possibility={self.list_possibility}','\n',file = sys.stderr)


    def choose(self):

        Dis_weight = []
        maxlist = []
        maxlist_1 = []
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                #if not((i==self.now_pos_x and j==self.now_pos_y+1) or (i==self.now_pos_x and j==self.now_pos_y-1) or (i==self.now_pos_x+1 and j==self.now_pos_y) or (i==self.now_pos_x-1 and j==self.now_pos_y))
                if (i==self.now_pos_x and j==self.now_pos_y):
                    pass
                else:
                    #print(i, j, self.now_pos_x,self.now_pos_y)
                    # in this way of setting distance, including neighbors at the same time
                    dis = abs(i-self.now_pos_x)+abs(j-self.now_pos_y)
                    #print(f'dis = {dis}')
                    Dis_weight.append([[i,j],1/(dis**0.5)*self.list_possibility[i*self.dim+j],dis])

        Dis_weight = sorted(Dis_weight,key=operator.itemgetter(1),reverse=True)
        #print(f'Dis_weight {Dis_weight}','\n',file = sys.stderr)
        for elem in Dis_weight:
            temp = Dis_weight[0][1]
            if elem[1]==temp:
                maxlist.append(elem)
            else:
                break

        maxlist = sorted(maxlist,key=operator.itemgetter(2),reverse=False)
        for elem in maxlist:
            temp = maxlist[0][2]
            if elem[2] == temp:
                maxlist_1.append(elem)
            else:
                break
        #print(f'now x,y is {self.now_pos_x,self.now_pos_y}','\n',file = sys.stderr)
        #print(f'maxlist_1 is {maxlist_1}','\n',file = sys.stderr)
        elem = maxlist_1.pop(random.randint(0,len(maxlist_1)-1))
        self.now_pos_x,self.now_pos_y = elem[0]
        self.step += elem[2]+1

        #print(f'choose {elem}','\n',file = sys.stderr)


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

        self.choose()

        type = self.list_terrain[self.now_pos_x*self.dim+self.now_pos_y]
        if type == 'flat':
            pivot = self.pivotforflat

        elif type == 'hill':
            pivot = self.pivotforhill

        elif type == 'forest':
            pivot = self.pivotforforest

        else:
            pivot = self.pivotforcaves

        if [self.now_pos_x,self.now_pos_y] == [self.real_pos_x,self.real_pos_y]:
            P_of_finding = random.randint(0,100)
            ###print(f'P_of_finding is {P_of_finding}','\n',file = sys.stderr)

            if P_of_finding >= pivot:
                self.FindKey = True
                #print(f"find the target in {self.now_pos_x,self.now_pos_y}",'\n',file = sys.stderr)
            else:
                self.list_possibility[self.now_pos_x*self.dim+self.now_pos_y] *= pivot/100
                self.random_move()
                self.recalculating(pivot)

        else:
            self.list_possibility[self.now_pos_x*self.dim+self.now_pos_y] *= pivot/100
            self.random_move()
            self.recalculating(pivot)


    def SearchDestroy(self):
        while not self.FindKey:
            ###print(f'step={self.step}','\n',file = sys.stderr)
            self.update()

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
    count_step = 0
    loop = 20
    for i in range(0,loop):
        print(f'loop is {i}\n',file = sys.stderr)
        search = SearchAndDestroy_change_r1()
        search.Initialization()
        search.SearchDestroy()
        print(f'total step is {search.step}\n\n\n',file = sys.stderr)
        count_step += search.step
    print(count_step/loop)
    f.close()
