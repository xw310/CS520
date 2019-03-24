import math
import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import numpy as np
import random
import copy
import time

########## user input
print("welcome!")
dim_x = int(input("please input the width of the board: "))
dim_y = int(input("please input the length of the board: "))
p = int(input("please the possibility of mines "))
##########

class Example(QWidget):
    if dim_x >= dim_y:
        block_size = math.floor(1000/(dim_x+2))
    else:
        block_size = math.floor(1000/(dim_y+2))
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        board_size_x= self.block_size*(dim_x+2)
        board_size_y= self.block_size*(dim_y+2)
        self.setGeometry(1000-board_size_y/2,100,board_size_y,board_size_x)
        self.setWindowTitle('MineSweeper')
        self.show()
        #self.text = u'\u041b\u0435\u0432 \u041d\u0438\u043a\u043e\u043b\u0430\
 # \u0435\u0432\u0438\u0447 \u0422\u043e\u043b\u0441\u0442\u043e\u0439: \n\
 # \u0410\u043d\u043d\u0430 \u041a\u0430\u0440\u0435\u043d\u0438\u043d\u0430'
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        block_size = self.block_size
        for i in range(dim_x):
            for j in range(dim_y):
                cell = int(status[i,j])
                if cell==-1:
                    qp.fillRect(block_size+block_size*j,block_size+block_size*i,block_size,block_size,QBrush(Qt.red))
                elif cell==0:
                    qp.fillRect(block_size+block_size*j,block_size+block_size*i,block_size,block_size,QBrush(Qt.gray))
                elif cell==1:
                    qp.fillRect(block_size+block_size*j,block_size+block_size*i,block_size,block_size,QBrush(Qt.white))
                elif cell==-2:
                    qp.fillRect(block_size+block_size*j,block_size+block_size*i,block_size,block_size,QBrush(Qt.black))
                elif cell==4:
                    qp.fillRect(block_size+block_size*j,block_size+block_size*i,block_size,block_size,QBrush(Qt.yellow))
        for i in range(dim_y+1):
            qp.drawLine(block_size*i+block_size  ,block_size,  block_size*i+block_size,  block_size+block_size*dim_x)
        for i in range(dim_x+1):
            qp.drawLine(block_size,  block_size*i+block_size,  block_size+block_size*dim_y,  block_size*i+block_size)

        #self.drawText(event, qp)
        qp.end()
'''
    def drawText(self, event, qp):
        block_size = self.block_size
        qp.setPen(QtGui.QColor('black'))
        qp.setFont(QtGui.QFont('Decorative', 10))

        if len(list_safe) != 0:

            for i in range (0,len(list_safe)):
                [x,y] = list_safe.pop()
                print(x,y)
                input()
                KB_value = KB[x,y]
                print(KB_value)
                input()
                qp.drawText(y*block_size,x*block_size,f'{KB_value}')
'''
        #qp.setPen(QtGui.QColor('black'))
        #qp.setFont(QtGui.QFont('Decorative', 10))
        #qp.drawText(20*block_size,30*block_size, f'{KB[15,15]}')

app = QApplication(sys.argv)



########## initialization
MineBoard = np.zeros((dim_x,dim_y),'int')
# -1 mine     0 clear
for i in range(0,dim_x):
    for j in range(0,dim_y):
        if (random.randint(0,100))> p:
            MineBoard[i][j] = 0
        else:
            MineBoard[i][j] = -1

print(MineBoard,'\n')

#initialize KB
#get MineBoard_big 1 block bigger than MineBoard in both row and column on both left and right， it's easier to calculate KB
MineBoard_big = np.zeros((dim_x+2,dim_y+2),'int')
MineBoard_big[1:dim_x+1,1:dim_y+1] = copy.deepcopy(MineBoard)      #a : b   from a to b-1
KB = np.zeros((dim_x,dim_y),'int')

#print(MineBoard_big,'\n')

for i in range(1,dim_x+1):
    for j in range(1,dim_y+1):

        MineBoard_part = MineBoard_big[i-1:i+2,j-1:j+2]
        #print(MineBoard_part,'\n')

        if not MineBoard_big[i,j]:             # current position is clear
            count = -MineBoard_part.sum()        # number of mines arount (i,j)
            KB[i-1,j-1] = count
        else:
            KB[i-1,j-1] = -1

print (KB,'\n')


list = []
for i in range(0,dim_x):
    for j in range(0,dim_y):
        list.append([i,j])
list_safe = []
list_undecidable = []
status = np.ones((dim_x,dim_y),'int')

#program begins to explore
def MineSweep():
    """ main  """

    global list,list_safe,list_undecidable,status

    logic_judge_flag = True
    take_risk = 0
    while(len(list)):

        if logic_judge_flag:
            logic_judge_flag = False
            rd = random.randint(1,len(list))
            [step_x,step_y] = list.pop(rd-1)
            take_risk+=1
            print(take_risk)
            #print(step_x,step_y)             ##################################
            #input()

            if KB[step_x,step_y] == -1:             #first step is random
                status[step_x,step_y] = -2
                print ("oh computer loses")
                return False

            else:
                status[step_x,step_y] = 0
                knowledge = KB[step_x,step_y]
                unexplored = 0
                mines = 0
                clear = 0

                #要判断边界
                for i in range(step_x-1,step_x+2):
                    for j in range(step_y-1,step_y+2):
                        if i>-1 and j>-1 and i<dim_x and j<dim_y :

                            if status[i,j] == 1:
                                unexplored += 1
                            if status[i,j] == -1:
                                mines += 1
                            if status[i,j] == 0:
                                clear += 1
                clear = clear -1

                #print(status)

                if mines == knowledge:
                    for i in range(step_x-1,step_x+2):
                        for j in range(step_y-1,step_y+2):
                            if i>-1 and j>-1 and i<dim_x and j<dim_y :
                                if status[i,j] == 1:
                                    status[i,j] = 0
                                    list_safe.append([i,j])      #确定安全，加进safe, 移出list
                                    list.remove([i,j])


                elif (mines+unexplored) == knowledge :      #探索点周围已查明雷数+未探索数=KB，说明未探索点全是雷，status标为mine，全部移出list
                    for i in range(step_x-1,step_x+2):
                        for j in range(step_y-1,step_y+2):
                            if i>-1 and j>-1 and i<dim_x and j<dim_y :
                                if status[i,j] == 1:
                                    status[i,j] = -1
                                    list.remove([i,j])

                elif (mines+unexplored) > knowledge :
                    list_safe.append([step_x,step_y])
                    #list.remove([step_x,step_y])

                    #print(list_safe)
                    #print(list)
                    #input('while len(list)')


        count = 0   #用于判断list_safe是否更新
        return_from_logic = 0   #用于逻辑判断返回有用值后，在while内将count置0
        while len(list_safe) and not logic_judge_flag:

            if return_from_logic ==1:
                count = 0
            return_from_logic = 0

            #print('回到list_safe')
            #input()

            [step_x,step_y] = list_safe.pop(0)   #从头pop，因为随即取点情况三，周围无法判断的点放到list_safe队尾

            knowledge = KB[step_x,step_y]
            unexplored = 0
            mines = 0
            clear = 0
            for i in range(step_x-1,step_x+2):
                for j in range(step_y-1,step_y+2):
                    if i>-1 and j>-1 and i<dim_x and j<dim_y :

                        if status[i,j] == 1:
                            unexplored += 1
                        if status[i,j] == -1:
                            mines += 1
                        if status[i,j] == 0:
                            clear += 1
            clear = clear -1

            if mines == knowledge:
                for i in range(step_x-1,step_x+2):
                    for j in range(step_y-1,step_y+2):
                        if i>-1 and j>-1 and i<dim_x and j<dim_y :
                            if status[i,j] == 1:
                                status[i,j] = 0
                                list_safe.append([i,j])      #确定安全，加进safe, 移出list
                                list.remove([i,j])
                count = 0   #list_safe更新了，重新计数

                #input('if mines == knowledge')
                #print(list_safe)
                #input('list_safe')

            elif (mines+unexplored) == knowledge :      #探索点周围已查明雷数+未探索数=KB，说明未探索点全是雷，status标为mine，全部移出list
                for i in range(step_x-1,step_x+2):
                    for j in range(step_y-1,step_y+2):
                        if i>-1 and j>-1 and i<dim_x and j<dim_y :
                            if status[i,j] == 1:
                                status[i,j] = -1
                                list.remove([i,j])
                count = 0  #同上

                #input('(mines+unexplored) == knowledge')
                #print(list_safe)
                #input('list_safe')

            elif (mines+unexplored) >= knowledge :
                list_safe.append([step_x,step_y])
                count += 1

                #print(count)
                #input('(mines+unexplored) >= knowledge')
                #print(list_safe)
                #input('list_safe')

                if count == len(list_safe):   #list_safe没有点能更新，需要进行逻辑判断

                    #print("进入逻辑判断预备阶段")
                    #input()

                    count == 0   #count置0
                    list_safe_copy = copy.deepcopy(list_safe)
                    list_undecidable = []
                    get_info = 1
                    while len(list_safe_copy):
                        [x,y] = list_safe_copy.pop(0)
                        knowledge = KB[x,y]
                        unexplored = 0
                        mines = 0
                        add = []
                        for i in range(x-1,x+2):
                            for j in range(y-1,y+2):
                                if i>-1 and j>-1 and i<dim_x and j<dim_y :
                                    if status[i,j] == 1:
                                        unexplored += 1
                                        add.append([i,j])
                                    if status[i,j] == -1:
                                        mines += 1
                        remain = knowledge - mines
                        #for i in range(0,len(list_undecidable))   #需不需要按len(add)排序
                        list_undecidable.append([add,remain])

                        #print("list_undecidable",list_undecidable)
                        #input()

                        #if remain >= unexplored:    #用于测试
                            #print('error')
                            #return

                    while get_info == 1:

                        #print("进入逻辑判断")
                        #input()

                        length = len(list_undecidable)
                        count1 = 0
                        if length == 1:
                            get_info = 0   #逻辑判断得不到结果
                            logic_judge_flag = True

                            #print('length = 1')
                            #input()

                        else:
                            flag = 0
                            for i in range(0,length):
                                if flag == 1:
                                    break
                                for j in range(i+1,length):
                                    first = list_undecidable[i]
                                    #first_copy = copy.deepcopy(first)
                                    second = list_undecidable[j]
                                    #second_copy = copy.deepcopy(second)

                                    TF, f = subtraction(first,second)

                                    #print(f)
                                    #input()

                                    if TF == True:

                                        #print('可以相减')
                                        #input()

                                        if f not in list_undecidable:

                                            #print('出现更新')
                                            #print(f)
                                            #input()


                                            list_undecidable.append(f)

                                            #print(list_undecidable)
                                            #input()

                                            if len(f[0]) == f[1]:
                                                for i in range(0,len(f[0])):

                                                    [logic_x,logic_y] = f[0][i]
                                                    status[logic_x,logic_y] = -1

                                                #print('出现可直接判断情况1',f[0])
                                                #input()

                                                #if f[1] <0:   #用于测试
                                                    #print('an error occured')
                                                    #input()
                                                flag = 1   #用于跳出第一个for循环，回到while(len(list_safe_copy))
                                                get_info = 0   #用于跳出while(len(list_safe_copy))，回到while(len(list_safe))
                                                return_from_logic = 1   #用于回到while(len(list_safe))后，将count置0
                                                break

                                            if f[1] == 0:
                                                for i in range(0,len(f[0])):

                                                    [logic_x,logic_y] = f[0][i]
                                                    status[logic_x,logic_y] = -0

                                                #print('出现可直接判断情况2',f[0])
                                                #input()

                                                flag = 1   #同上
                                                get_info = 0   #同上
                                                return_from_logic = 1
                                                break

                                        else:
                                            count1+=1

                                            #print(TF,count1)
                                            #input()

                                    if TF == False:
                                        count1+=1

                                        #print(TF,count1)
                                        #input()

                            if count1 == length*(length-1)/2:
                                get_info = 0   #逻辑判断得不到结果
                                logic_judge_flag = True



def subtraction(first,second):   #可优化，父节点距离过远的话，周围点肯定不重合，不用比较，直接返回false
    subtractable = 1
    error = []
    if len(first[0]) > len(second[0]):
        pass
    if len(first[0]) < len(second[0]):   #让first是较长的一个，方便底下比较
        temp = copy.deepcopy(first)
        first = copy.deepcopy(second)
        second =copy.deepcopy(temp)

    if len(first[0]) == len(second[0]):   #相同长度无法相减
        return False,error

    for i in range(0,len(second[0])):
        if second[0][i] in first[0]:

            #print(i,len(second[0]))
            #print(second[0][i],first[0])
            #input()

            #[x,y] = second[0][i]
            #first[0].remove(second[0][i])
            first[0].remove(second[0][i])
        #if second[0][i] not in first[0]:   #典型错误，两个if同时执行
        else:
            return False,error

    first[1] = first[1] - second[1]
    return True,first


MineSweep()
print(status)
ex = Example()
app.exec_();
