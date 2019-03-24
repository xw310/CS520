import random
#import array
import numpy as np #这个方式使用numpy的函数时，需要以np.开头。
import time


def add_list(new,original = []):              #加入openlist 并进行排序
    if len(original) == 0:
        original.append(new)
    else:
        for i in range(0,len(original)):
            if original[i][0] > new[0]:               #  > 还是 >= ？？？
                original.insert(i,new)
                return original
        original.append(new)
    return original


def find_list(new,original = []):             #判断下一步是否在openlist中,参数为【x，y】
    if len(original) == 0:
        return False, len(original)+1      #若下一步不在openlist，其实不用返回第二项
    else:
        for i in range(0,len(original)):
            if original[i][3] == new:
                return True, i
        return False,len(original)+1


def get_h (now):                       #参数为【x，y】
    h = (dim-1-now[0])+(dim-1-now[1])
    return h

def A_star():
    global open,close,path
    intial = [0,0,0,[0,0],[-1,-1]]
    open.append(intial)      # 初始化 放入初始位置
    g = 0                    #初始 g = 0 步数

    while len(open):

        now = open[0]       #读取弹出元素
        x,y= now[3]         #读取位置
        close.append(now)   #存入closelist
        open.pop(0)          #pop出openlist

        mark[x,y] = 1           #标记走过

        for i in range(0,4):

            move_x,move_y = move[i]
            temp_x = x + move_x
            temp_y = y + move_y
            temp_g = now[1]+1

            if (temp_x == dim-1) and (temp_y == dim -1):      #如果找到终点

                mark[x,y] = 1

                print(f"find a path!,need {temp_g} steps")
                #input()
                #打印路径
                path=[]
                path.append([dim-1,dim-1])
                path.append([x,y])
                path.append(now[4])
                b_x,b_y = now[4]
                while (b_x != 0) or (b_y != 0):
                    exist,before = find_list([b_x,b_y],close)
                    b_x,b_y = close[before][4]
                    path.append(close[before][4])
                    #print(path)
                print(path)
                return

            if (temp_x<dim)and(temp_x>=0)and(temp_y<dim)and(temp_y>=0)and(maze[temp_x,temp_y] == 0):
                if mark[temp_x,temp_y] == 1:                        #已经在closelist中，不进openlist
                    continue

                if mark[temp_x,temp_y] == 0:                        #若不在closelist中，判断是否已在openlist
                    temp_h = get_h([temp_x,temp_y])
                    temp_f = temp_g + temp_h
                    temp = [temp_f, temp_g, temp_h, [temp_x,temp_y], [x,y]]      #当前点
                    exist,pos = find_list([temp_x,temp_y],open)

                    #   print(exist,'   ',pos)

                    if exist:                                       #若已经在openlist中，判断是否要更新
                        #print(open[pos][0]>temp_f)
                        if open[pos][0]>temp_f:
                            del open[i]
                            add_list(temp,open)
                            #print(open)
                            #input()


                    else:                                           #若不在openlist中，添加进openlist
                        add_list(temp,open)      #push入队列
                        #print('add后',open)

    print('oh,no path found')


running_time = []
sum = 0
average = 0
for k in range(0,50):
    #初始化迷宫/标记阵/父亲节点矩阵
    dim=500
    #dim = int(input("input dim "))
    #maze=[[None for i in range(dim)] for i in range(dim)]
    #mark = [[0 for i in range(dim)] for i in range(dim)]
    #father = [[[0,0] for i in range(dim)] for i in range(dim)]
    maze = np.zeros((dim,dim),'int')
    p=10
    #p = int(input("input possibility of block (please in range 0 - 100 ) "))
    for i in range(0,dim):
        for j in range(0,dim):
            if (random.randint(0,100))> p:
                maze[i][j] = 0
            else:
                maze[i][j] = 1
    maze[0,0] = 0
    maze[dim-1,dim-1] = 0

    move = [[0,1],[1,0],[0,-1],[-1,0]]   #order right/down/left/up

    open = []    #f=g+h, g, h, 当前坐标， 父亲节点  #parents可以拿出来 像bfs一样
    mark = np.zeros((dim,dim),'int')   #判断点是否被放在closelist中
    close = []   #访问过的点放在里面，用来反向打印路径
    path = []

    start = time.clock()
    A_star()
    #input()
    end = time.clock()

    running_time.append(end-start)

    print(f"time of running is {end-start}")

print(running_time)

for k in range(len(running_time)):

    sum=sum+running_time[k]

print(sum)

average = sum/50        

print(f'average time is {average}')
