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
        #print(self.real_pos_x,self.real_pos_y,'\n',file = sys.stderr)


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


    def recalculating(self,maxpos_i,maxpos_j,pivot):

        #print("move on",file = sys.stderr)
        #print("recalculating the possibility",'\n',file = sys.stderr)
        sum = 0
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                if [i,j] == [maxpos_i,maxpos_j]:
                    self.list_possibility[i*self.dim+j] *= pivot/100
                    sum += self.list_possibility[i*self.dim+j]
                    #self.list_for_sort update later
                else:
                    sum += self.list_possibility[i*self.dim+j]

        coefficient = 1/sum

        for i in range(0,self.dim*self.dim):
            self.list_possibility[i] *= coefficient
            self.list_for_sort[i][1] = self.list_possibility[i]
        #print(f'list_possibility={self.list_possibility}','\n\n\n',file = sys.stderr)


    def update(self):
        #input()
        ### pick the position with biggest possibility of finding target in the cell

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


        maxlist = sorted(list_for_sort_r2,key=operator.itemgetter(1),reverse=True)
        maxlist_1 = []
        for i in range(0,self.dim*self.dim):
            temp = maxlist[0][1]
            if maxlist[i][1] == temp:
                maxlist_1.append(maxlist[i])
            else:
                break
        #print(f'maxlist_1={maxlist_1}','\n',file = sys.stderr)

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
                self.recalculating(maxpos_i,maxpos_j,pivot)

        else:
            self.recalculating(maxpos_i,maxpos_j,pivot)


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
