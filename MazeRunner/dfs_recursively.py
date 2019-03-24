#
#
#网上资源 递归版本dfs，没有使用栈

import random

dim = int(input("input dim "))
maze=[[None for i in range(dim)] for i in range(dim)]
mark = [[0 for i in range(dim)] for i in range(dim)]
#print(maze)
#print(mark)

for i in range(0,dim):
    for j in range(0,dim):
        if (random.randint(0,100))>20:
            maze[i][j] = 0
        else:
            maze[i][j] = 1

test = [[0,0,0,0,0],[1,0,1,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,1,0]]
dim = 5

min = dim*dim
#path = stack() #路径
dir = [[0,1],[1,0],[0,-1],[-1,0]]
def dfs(step,x,y):
    global min
    if (x==dim-1)and(y==dim-1):
        if step < min:
            min = step
        return min

    for i in range(0,4):
        tx = x+dir[i][0]
        ty = y+dir[i][1]
        if tx<0 or tx>4 or ty<0 or ty>4:
            continue
        if (test[ty][tx]==0)and(mark[ty][tx]==0):
            mark[ty][tx]=1
            dfs(step+1,tx,ty)
            mark[ty][tx]=0

dfs(0,0,0)
print(test,min)
