import sys
import copy
from queue import PriorityQueue
import math

sys.setrecursionlimit(1000000)
def get_ints():
    return map(int,sys.stdin.readline().strip().split())

def get_string():
    return sys.stdin.readline().strip()





class DSU:
    def __init__(self, n):
        self.n = n
        self.parent = [-1 for i in range(n)]
        self.rank = [1 for i in range(n)]

    def find(self, n):
        update_list = []
        while (1):
            if (self.parent[n] < 0):
                for i in update_list:
                    self.parent[i] = n
                return n
            else:
                update_list.append(n)
                n = self.parent[n]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if (a == b):
            return False
        else:
            self.parent[b] += self.parent[a]
            self.parent[a] = b
            return True

    def union_by_rank(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if (a == b):
            return False
        else:
            if (self.rank[a] > self.rank[b]):
                self.parent[a] += self.parent[b]
                self.rank[a] += self.rank[b]
                self.parent[b] = a

            else:
                self.parent[b] += self.parent[a]
                self.rank[b] += self.rank[a]
                self.parent[a] = b

            return True

if __name__=="__main__":
    pass