import numpy as np
import copy
import sys
from sys import argv

script,log = argv
f = open(log,'a')
__con__ = sys.stderr
sys.stderr = f

class KNNclassify():

    def __init__(self):
        self.k = 5
        a1 = [ 1,-1,-1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1,-1,-1, 1,-1,-1, 1, 1,-1,-1,-1,-1, 1]
        a2 = [-1,-1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1,-1,-1,-1,-1]
        a3 = [ 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1,-1,-1,-1,-1,-1,-1,-1, 1, 1,-1,-1,-1,-1, 1]
        a4 = [-1,-1, 1, 1, 1, 1,-1,-1,-1,-1, 1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1,-1,-1,-1,-1]
        a5 = [-1,-1,-1, 1, 1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1]
        b1 = [ 1, 1,-1,-1, 1, 1, 1,-1,-1, 1,-1, 1,-1, 1, 1,-1,-1,-1, 1, 1, 1,-1,-1, 1, 1]
        b2 = [ 1,-1,-1, 1, 1,-1,-1,-1,-1, 1,-1,-1,-1,-1, 1, 1,-1,-1, 1,-1, 1, 1, 1, 1,-1]
        b3 = [ 1,-1, 1,-1,-1, 1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 1, 1, 1, 1,-1, 1]
        b4 = [ 1, 1, 1, 1,-1, 1,-1,-1, 1,-1,-1,-1,-1, 1, 1,-1,-1, 1, 1,-1,-1,-1, 1, 1,-1]
        b5 = [ 1,-1, 1, 1,-1,-1,-1,-1, 1,-1,-1, 1,-1, 1,-1, 1, 1,-1, 1,-1, 1, 1,-1, 1,-1]
        c1 = [ 1,-1,-1, 1,-1, 1,-1,-1,-1,-1,-1,-1, 1, 1, 1,-1,-1, 1,-1, 1, 1,-1, 1,-1, 1]
        c2 = [ 1, 1,-1,-1,-1,-1, 1,-1,-1,-1, 1,-1, 1, 1,-1,-1,-1, 1,-1, 1,-1, 1, 1, 1, 1]
        c3 = [-1,-1, 1, 1, 1, 1, 1, 1,-1, 1,-1,-1,-1,-1, 1, 1, 1, 1, 1,-1,-1,-1,-1, 1, 1]
        c4 = [ 1,-1,-1,-1, 1, 1,-1,-1,-1, 1,-1,-1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1]
        c5 = [-1, 1, 1, 1, 1,-1, 1,-1,-1, 1, 1, 1, 1, 1,-1, 1,-1,-1, 1,-1, 1, 1, 1, 1, 1]
        self.train = np.array([a1,a2,a3,a4,a5,b1,b2,b3,b4,b5])
        self.test = [c1,c2,c3,c4,c5]
        self.labels = ['A','A','A','A','A','B','B','B','B','B']
        print(f'initialization successful, k = {self.k}',file=sys.stderr)

    def classify(self):
        result = [] ###record the final classification
        detail = [] ###record the similar pictures

        datasize = self.train.shape[0]
        for ith, elem in enumerate(self.test):
            diff = np.tile(elem,(datasize,1)) - self.train
            square = diff**2
            square_dis = np.sum(square, axis = 1)
            dis = square_dis*0.5

            sort_dis = np.argsort(dis)[:self.k]
            detail_each = []
            for i, elem in enumerate(sort_dis):
                if elem <=4:
                    detail_each.append(f'A{elem+1}')
                else:
                    detail_each.append(f'B{elem-4}')

            dict = {}
            for i in range(self.k):
                label = self.labels[sort_dis[i]]
                dict.setdefault(label,0)
                dict[label] += 1

            max = 0
            for label, count in dict.items():
                if count > max:
                    max = count
                    maxlabel = label
                else:
                    pass

            result.append(maxlabel)
            detail.append(detail_each)
        return result,detail

if __name__ == '__main__':
    knn = KNNclassify()
    #print(knn.train.shape[1])
    result, detail = knn.classify()

    for i, elem in enumerate(result):
        print(f'c{i+1} belongs to class {elem}', file=sys.stderr)

    for i, elem in enumerate(detail):
        print(f"c{i+1}'s most similar picture are {elem}", file=sys.stderr)
