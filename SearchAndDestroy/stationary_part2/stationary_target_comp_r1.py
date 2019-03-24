import numpy as np
import random
import copy
import operator
import sys
from sys import argv
from stationary_target_travel_r1 import *
from stationary_target_change_r1 import *

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
    search_travel = SearchAndDestroy_travel_r1()
    search_travel.Initialization()
    list_terrain_copy= copy.deepcopy(search_travel.list_terrain)
    list_possibility_copy = copy.deepcopy(search_travel.list_possibility)
    list_for_sort_copy = copy.deepcopy(search_travel.list_for_sort)
    real_pos_x_copy = search_travel.real_pos_x
    real_pos_y_copy = search_travel.real_pos_y
    search_travel.SearchDestroy()
    count_r1 += search_travel.step


    sys.stderr = f2
    print(f'loop = {i}',file = sys.stderr)
    search_change = SearchAndDestroy_change_r1()
    #search_r2.Initialization()
    search_change.list_terrain = copy.deepcopy(list_terrain_copy)
    search_change.list_possibility = copy.deepcopy(list_possibility_copy)
    search_change.list_for_sort = copy.deepcopy(list_for_sort_copy)
    search_change.real_pos_x = real_pos_x_copy
    search_change.real_pos_y = real_pos_y_copy
    search_change.SearchDestroy()
    count_r2 += search_change.step


f1.close()
f2.close()

sys.stderr = __con__
averstep_r1 = count_r1/loop
averstep_r2 = count_r2/loop
print(f'travel takes average {averstep_r1} step and change takes average {averstep_r2} step')
print(f'ratio is {averstep_r1/averstep_r2}')
