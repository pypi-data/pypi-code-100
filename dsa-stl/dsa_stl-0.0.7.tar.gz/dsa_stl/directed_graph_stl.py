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


class DGraph:
    def __init__(self, n=0, e=0):
        self.n = n
        self.e = e
        self.INFINITY = 1000000007
        self.adj_list = [[] for _ in range(self.n)]
        self.edge_list = []

    def buildGraph(self):
        u, v = get_ints()
        u = u - 1
        v = v - 1
        self.adj_list[u].append(v)

    def build_kruskal_graph(self):
        for _ in range(self.e):
            u, v, w = get_ints()
            u = u - 1
            v = v - 1
            self.edge_list.append((u, v, w))

        self.edge_list.sort(key=lambda x: x[2])

    def msp_kruskal(self):
        dsu = DSU(self.n)
        cost = 0
        for u, v, w in self.edge_list:
            if (dsu.union_by_rank(u, v)):
                cost += w
        return cost

    def build_dijkstre_graph(self):
        for _ in range(self.e):
            u, v, w = get_ints()
            u = u - 1
            v = v - 1
            self.adj_list[u].append([w, v])

    def dijkstre_sssp(self, ni):
        dist = [self.INFINITY] * self.n
        dist[ni] = 0
        que = PriorityQueue()
        que.put([0, ni])
        while (que.qsize() != 0):
            w, v = que.get()
            for iw, i in self.adj_list[v]:
                if (dist[i] > (w + iw)):
                    que.put([iw + w, i])
                    dist[i] = w + iw
        return dist

    def buildBellmanford_graph(self):
        for _ in range(self.e):
            u, v, w = map(int, input().split())
            u = u - 1
            v = v - 1
            self.edge_list.append([u, v, w])

    def bellmanford_sssp(self, ni):
        dist = [self.INFINITY] * (self.n)
        dist[ni] = 0
        for _ in range(self.n - 1):
            flg = True
            for u, v, w in self.edge_list:
                if ((dist[u] != self.INFINITY) and (dist[v] > dist[u] + w)):
                    dist[v] = dist[u] + w
                    flg = False
            if flg:
                return dist
        return dist

    def build_Edmand_karp_graph(self):
        self.capacity = [[0 for _ in range(self.n)] for __ in range(self.n)]
        for _ in range(self.e):
            u, v, w = get_ints()
            u, v = u - 1, v - 1
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            self.capacity[u][v] = w

    def edmand_karp_maxflow(self, s, t):
        def bfs(s, t):
            global parent
            parent = [-1 for i in range(self.n)]
            parent[s] = -2
            que = [[s, self.INFINITY]]
            while (que):

                curr, curr_flow = que.pop(0)
                for i in self.adj_list[curr]:
                    if (parent[i] == -1 and self.capacity[curr][i] != 0):
                        next_flow = min(self.capacity[curr][i], curr_flow)
                        que.append([i, next_flow])
                        parent[i] = curr
                        if (i == t):
                            return next_flow
            return 0

        max_flow = 0

        while (1):
            min_flow = bfs(s, t)
            if (min_flow == 0):
                break
            max_flow += min_flow
            path_v = t
            while (path_v != -2):
                # print(path_v,end = " ")  # path
                par = parent[path_v]
                self.capacity[par][path_v] -= min_flow
                self.capacity[path_v][par] += min_flow
                path_v = parent[path_v]
            # print()
        return max_flow

if __name__=="__main__":
    pass