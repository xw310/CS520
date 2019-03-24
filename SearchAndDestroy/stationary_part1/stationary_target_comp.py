import numpy as np
import random
import copy
import operator
import sys
from sys import argv
from stationary_target_rule1 import *
from stationary_target_rule2 import *

script, filename1, filename2 = argv
f1 = open(filename1,'w')
f2 = open(filename2,'w')
__con__=sys.stderr

loop = 100
count_r1 = 0
count_r2 = 0

for i in range(0,loop):

    sys.stderr = f1
    print(f'loop = {i}',file = sys.stderr)
    search_r1 = SearchAndDestroy_r1()
    search_r1.Initialization()
    list_terrain_copy= copy.deepcopy(search_r1.list_terrain)
    list_possibility_copy = copy.deepcopy(search_r1.list_possibility)
    list_for_sort_copy = copy.deepcopy(search_r1.list_for_sort)
    real_pos_x_copy = search_r1.real_pos_x
    real_pos_y_copy = search_r1.real_pos_y
    step_r1 = search_r1.SearchDestroy()
    count_r1 += step_r1
    print(search_r1.list_terrain[search_r1.real_pos_x*search_r1.dim+search_r1.real_pos_y])


    sys.stderr = f2
    print(f'loop = {i}',file = sys.stderr)
    search_r2 = SearchAndDestroy_r2()
    #search_r2.Initialization()
    search_r2.list_terrain = copy.deepcopy(list_terrain_copy)
    #print(len(search_r1.list_terrain))
    #print(len(search_r2.list_terrain))
    search_r2.list_possibility = copy.deepcopy(list_possibility_copy)
    search_r2.list_for_sort = copy.deepcopy(list_for_sort_copy)
    search_r2.real_pos_x = real_pos_x_copy
    search_r2.real_pos_y = real_pos_y_copy
    step_r2 = search_r2.SearchDestroy()
    count_r2 += step_r2


f1.close()
f2.close()

sys.stderr = __con__
averstep_r1 = count_r1/loop
averstep_r2 = count_r2/loop
print(f'rule1 takes average {averstep_r1} step and rule2 takes average {averstep_r2} step')
