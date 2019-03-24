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
        self.dim = 10
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
        ###print(f'real position is at {self.real_pos_x,self.real_pos_y}','\n',file = sys.stderr)

        self.now_pos_x = random.randint(0,self.dim-1)
        self.now_pos_y = random.randint(0,self.dim-1)
        self.step = 0

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
        ###print(array_terrain,'\n',file = sys.stderr)
        ###print(array_possibility,'\n',file = sys.stderr)
        return array_terrain, array_possibility


    def recalculating(self,pivot):

        ###print("move on",file = sys.stderr)
        ###print("recalculating the possibility",'\n',file = sys.stderr)
        sum = 0
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                if [i,j] == [self.now_pos_x,self.now_pos_y]:
                    self.list_possibility[i*self.dim+j] *= pivot/100
                    sum += self.list_possibility[i*self.dim+j]
                    #self.list_for_sort update later
                else:
                    sum += self.list_possibility[i*self.dim+j]

        coefficient = 1/sum

        for i in range(0,self.dim*self.dim):
            self.list_possibility[i] *= coefficient
            self.list_for_sort[i][1] = self.list_possibility[i]
        ###print(f'list_possibility={self.list_possibility}','\n\n\n',file = sys.stderr)


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
        #print(f'x,y is {self.now_pos_x,self.now_pos_y}','\n',file = sys.stderr)
        #print(f'maxlist_1 is {maxlist_1}','\n',file = sys.stderr)
        elem = maxlist_1.pop(random.randint(0,len(maxlist_1)-1))
        self.now_pos_x,self.now_pos_y = elem[0]
        self.step += elem[2]+1

        #print(f'choose {elem}','\n',file = sys.stderr)

    def update(self):

        self.choose()
        ### pick the position with biggest possibility of being in the cell
        #maxlist = sorted(self.list_for_sort,key=operator.itemgetter(1),reverse=True)
        #maxlist_1 = []
        #for i in range(0,self.dim*self.dim):
            #temp = maxlist[0][1]
            #if maxlist[i][1] == temp:
                #maxlist_1.append(maxlist[i])
            #else:
                #break
        #print(f'maxlist_1={maxlist_1}','\n\n',file = sys.stderr)

        ### randomly pick one from maxlist_1
        #max = maxlist_1.pop(random.randint(0,len(maxlist_1)-1))
        #maxpos_i,maxpos_j = max[0]    #position
        #type = self.list_terrain[maxpos_i*self.dim+maxpos_j]
        #maxP = max[1]      #possibility
        #print([maxpos_i,maxpos_j],type,maxP,'\n',file = sys.stderr)
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
                print(f"find the target in {self.now_pos_x,self.now_pos_y}",'\n',file = sys.stderr)
            else:
                self.recalculating(pivot)

        else:
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
    loop = 5
    for i in range(0,loop):
        search = SearchAndDestroy_change_r1()
        search.Initialization()
        search.SearchDestroy()
        count_step += search.step
    print(count_step/loop)
    f.close()
