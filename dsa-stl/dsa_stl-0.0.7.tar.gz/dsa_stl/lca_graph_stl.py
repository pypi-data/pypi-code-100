import sys
import copy
from queue import PriorityQueue
import math

sys.setrecursionlimit(1000000)
def get_ints():
    return map(int,sys.stdin.readline().strip().split())

def get_string():
    return sys.stdin.readline().strip()


class LCA:
    def __init__(self, n=0, e=0):
        self.n = n
        self.e = e
        self.adj_list = [[] for _ in range(self.n)]

    def addEdge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def buildTree(self):
        for _ in range(self.e):
            u, v = map(int, input().split())
            u = u - 1
            v = v - 1
            self.addEdge(u, v)

    def dfs_level_parent(self, ni, level, parent, lev):
        def dfs(ni, level, parent, lev):
            level[ni] = lev

            for i in self.adj_list[ni]:
                if (i != parent[ni]):
                    parent[i] = ni
                    dfs(i, level, parent, lev + 1)

        dfs(ni, level, parent, lev)
        self.parent = parent
        self.level = level

    def lcaNaive(self, u, v, level, parent):
        if (level[u] > level[v]):
            u, v = v, u
        d = level[v] - level[u]
        for _ in range(d):
            v = parent[v]

        if (u == v):
            return u
        else:
            while (parent[u] != parent[v]):
                u = parent[u]
                v = parent[v]
            return parent[u]

    def binary_lifting(self, parent, max_level):
        max_level = int(math.log2(max_level))
        self.binary_list = [[-1 for _ in range(max_level + 1)] for __ in range(self.n)]
        for num, i in enumerate(parent):
            self.binary_list[num][0] = i

        for i in range(1, self.n):
            for j in range(1, max_level + 1):
                self.binary_list[i][j] = self.binary_list[self.binary_list[i][j - 1]][j - 1]

    def lcaFast(self, u, v, level, parent):
        if (level[u] > level[v]):
            u, v = v, u

        d = level[v] - level[u]

        while (d > 0):
            i = int(math.log2(d))
            v = self.binary_list[v][i]
            d = d - (1 << i)

        if (u == v):
            return u
        else:
            lev = level[u]
            while (lev > 0):
                i = int(math.log2(lev))
                if (self.binary_list[u][i] != self.binary_list[v][i]):
                    u = self.binary_list[u][i]
                    v = self.binary_list[v][i]
                else:
                    lev = lev - (1 << i)

            return self.binary_list[u][0]

    def distance_between_2_node(self, u, v):
        return self.level[u] + self.level[v] - 2 * self.level[(self.lcaFast(u, v, self.level, self.parent))]

if __name__=="__main__":
    pass