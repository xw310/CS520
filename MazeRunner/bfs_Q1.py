import random
import array
import numpy as np #这个方式使用numpy的函数时，需要以np.开头。
import time


#bfs算法
def bfs():
    global path,mark
    mark[0,0] = 1
    list = []                #用list模拟queue，进行pop和push
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
                    return                            #找到路径提前结束搜索
    if (temp_x != dim-1) and (temp_y != dim -1):
        print("oh, no path!")                     #未找到路径



running_time = []
sum = 0
average = 0
for k in range(0,100):

    #初始化迷宫/标记阵/父亲节点矩阵
    #dim = int(input("input dim "))
    dim = 300
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

    print(maze,'\n')

    mark = np.zeros((dim,dim),'int')
    father_x = np.ones((dim,dim),'int')*dim*dim
    father_y = np.ones((dim,dim),'int')*dim*dim

    move = [[0,1],[1,0],[0,-1],[-1,0]]   #order right/down/left/up
    #print(father_x)
    #input()
    path = []

    #print(mark,'\n',father_x,'\n',father_y)


    start = time.clock()

    bfs()
    print(path)
    print(len(path))

    end = time.clock()

    running_time.append(end-start)

    print(f"time of running is {end-start}")
    
print(running_time)

for k in range(len(running_time)):

    sum=sum+running_time[k]

print(sum)

average = sum/100

print(f'average time is {average}')
