import random
#import array
import numpy as np #这个方式使用numpy的函数时，需要以np.开头。
import time
import copy
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


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


def get_h1 (now):                       #参数为【x，y】
    h = (dim-1-now[0])+(dim-1-now[1])
    return h

def A_star1(maze, mark):
    open = []
    close = []
    path = []
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
                #print(path)
                return True, len(path)

            if (temp_x<dim)and(temp_x>=0)and(temp_y<dim)and(temp_y>=0)and(maze[temp_x,temp_y] == 0):
                if mark[temp_x,temp_y] == 1:                        #已经在closelist中，不进openlist
                    continue

                if mark[temp_x,temp_y] == 0:                        #若不在closelist中，判断是否已在openlist
                    temp_h = get_h1([temp_x,temp_y])
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
    return False,0
#以上 A_star1

def get_h2 (now):                       #参数为【x，y】
    h = np.sqrt((dim-1-now[0])*(dim-1-now[0])+(dim-1-now[1])*(dim-1-now[1]))
    #h = (dim-1-now[0])+(dim-1-now[1])
    return h


def A_star2(maze, mark):
    open = []
    close = []
    path = []
    intial = [0,0,0,[0,0],[-1,-1]]
    open.append(intial)      # 初始化 放入初始位置
    g = 0                    #初始 g = 0 步数

    #print(open,'\n\n',close)
    #input()

    while len(open):

        #   print(open)

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
                return True,len(path)

            if (temp_x<dim)and(temp_x>=0)and(temp_y<dim)and(temp_y>=0)and(maze[temp_x,temp_y] == 0):
                if mark[temp_x,temp_y] == 1:                        #已经在closelist中，不进openlist
                    continue

                if mark[temp_x,temp_y] == 0:                        #若不在closelist中，判断是否已在openlist
                    temp_h = get_h2([temp_x,temp_y])
                    temp_f = temp_g + temp_h
                    temp = [temp_f, temp_g, temp_h, [temp_x,temp_y], [x,y]]      #当前点
                    exist,pos = find_list([temp_x,temp_y],open)

                    #print(exist,'   ',pos)

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
                        #input()

    print('oh,no path found')
    return False, 0
#以上A_star2

def bfs(maze,mark):
    path = []
    mark[0,0] = 1
    list = []                #用list模拟queue，进行pop和push
    father_x = np.ones((dim,dim),'int')*dim*dim
    father_y = np.ones((dim,dim),'int')*dim*dim
    list.append([0,0])
    while len(list):
        x,y= list[0]         #读取
        list.pop(0)          #pop出队列

        for i in range(0,4):
            move_x,move_y = move[i]
            temp_x = x + move_x
            temp_y = y + move_y

            #print(list,'\n')
            #print(i,'\n')
            #print(temp_x,temp_y,'abc')
            #print(maze[temp_x,temp_y],mark[temp_x,temp_y] )
            #print(mark[0,-3])
            #input

            if (temp_x<dim)and(temp_x>=0)and(temp_y<dim)and(temp_y>=0)and(maze[temp_x,temp_y] == 0)and(mark[temp_x,temp_y] == 0):
                list.append([temp_x,temp_y])      #push入队列
                mark[temp_x,temp_y] = 1           #标记走过
                father_x[temp_x,temp_y] = x              #记录父亲节点
                father_y[temp_x,temp_y] = y

                #print(list,'\n')                #测试
                #print(mark,'\n')
                #print(father_x,'\n\n',father_y,'\n')
                #input()

                if (temp_x == dim-1) and (temp_y == dim -1):      #如果找到终点
                    print("find a path!")

                    #while  (father_x[temp_x,temp_y] != 0 and father_y[temp_x,temp_y] != 0):      #倒退打路径,这行命令出错，while不循环？？？
                    while ((temp_x != 0) or (temp_y != 0)):
                    #while [temp_x,temp_y] != [0,0]:
                        path.append([temp_x,temp_y])
                        #path.append([father_x[temp_x,temp_y],father_y[temp_x,temp_y]])
                        #input()

                        temp_xo = temp_x               #先将temp_x的值保存起来，因为下一步改变temp_x
                        temp_x = father_x[temp_x,temp_y]
                        temp_y = father_y[temp_xo,temp_y]
                    #   print(father_x)               #测试
                        #print(father_y)
                        #print(temp_x,temp_y)
                    path.append([0,0])                            #最后打起点
                    return True, len(path)                       #找到路径提前结束搜索

    if (temp_x != dim-1) and (temp_y != dim -1):
        print("oh, no path!")                     #未找到路径
    return False, 0
#以上BFS


def solve(maze_local):
    maze = maze_local
    size = 200
    #DFS
    fringe=[[0,0]] #gray
    path=[] #black
    solvable = False
    while (len(fringe) > 0):
        local = fringe.pop() #current location
        if local[0] == size-1 and local[1] == size-1:
            solvable = True
            path.append(0)
            maze[local[0],local[1]] = 3
            return solvable,len(path)
            break

        neighbors =[[local[0],local[1]-1],[local[0]-1,local[1]],[local[0],local[1]+1],[local[0]+1,local[1]]]
        have_way = False
        for neighbor in neighbors:
            if neighbor[0]>=0 and neighbor[0]<size and neighbor[1]>=0 and neighbor[1]<size:
                num = maze[neighbor[0],neighbor[1]]
                if num == 0:
                    maze[neighbor[0],neighbor[1]] = 2   #numpy [i,j]
                    fringe.append(neighbor)
                    have_way = True
                if num == 2:
                    if neighbor == fringe[-1]: ###
                        have_way = True        ###

        if have_way == True:
            maze[local[0],local[1]] = 3
            path.append(local)
        else:
            if len(path) == 0:
                maze[local[0],local[1]] = 4
                return solvable,0
                break
            else:
                maze[local[0],local[1]] = 4
                fringe.append(path.pop())


running_time = []
sum = 0
average = 0
p = []
list1=[]
list2=[]
list3=[]
list4=[]
for l in range(0,5):

    p.append((0.1+0.05*l)*100)
    count1=count2=count3=count4 = 0.001
    sum1=sum2=sum3=sum4 = 0

    for k in range(0,50):
        #初始化迷宫/标记阵/父亲节点矩阵

        dim=200

        maze0 = np.zeros((dim,dim),'int')

        #p.append((0.1+0.05*l)*100)
        #p = int(input("input possibility of block (please in range 0 - 100 ) "))
        for i in range(0,dim):
            for j in range(0,dim):
                if (random.randint(0,100))> p[l]:
                    maze0[i][j] = 0
                else:
                    maze0[i][j] = 1
        maze0[0,0] = 0
        maze0[dim-1,dim-1] = 0

        maze1 = copy.deepcopy(maze0)
        maze2 = copy.deepcopy(maze0)
        maze3 = copy.deepcopy(maze0)

        move = [[0,1],[1,0],[0,-1],[-1,0]]   #order right/down/left/up

        #open = []    #f=g+h, g, h, 当前坐标， 父亲节点  #parents可以拿出来 像bfs一样
        mark0 = np.zeros((dim,dim),'int')   #判断点是否被放在closelist中
        mark1 = copy.deepcopy(mark0)
        mark2 = copy.deepcopy(mark0)
        mark3 = copy.deepcopy(mark0)
        #close = []   #访问过的点放在里面，用来反向打印路径
        #path = []


        #start = time.clock()
        exist1,lon1 = A_star1(maze0,mark0)
        if exist1:
            count1+=1
            sum1=sum1+lon1


        exist2,lon2 = A_star2(maze1,mark1)
        if exist2:
            count2+=1
            sum2=sum2+lon2


        exist3,lon3 = bfs(maze2,mark2)
        if exist3:
            count3+=1
            sum3=sum3+lon3


        exist4,lon4 = solve(maze3)
        if exist4:
            count4+=1
            sum4=sum4+lon4


    aver1 = sum1/count1
    list1.append(aver1)

    aver2 = sum2/count2
    list2.append(aver2)


    aver3 = sum3/count3
    list3.append(aver3)


    aver4 = sum4/count4
    list4.append(aver4)


print(p)
print(list1)
plt.xlabel('value of p')
plt.ylabel('average path length')
plt.plot(p,list1,color='red',linewidth=2,linestyle='-',label="A_star1")
plt.plot(p,list2,color='green',linewidth=2.5,linestyle='-',label="A_star2")
plt.plot(p,list3,color='orange',linewidth=2.5,linestyle='-',label="BFS")
plt.plot(p,list4,color='blue',linewidth=2.5,linestyle='-',label="DFS")
plt.legend()
plt.show()
