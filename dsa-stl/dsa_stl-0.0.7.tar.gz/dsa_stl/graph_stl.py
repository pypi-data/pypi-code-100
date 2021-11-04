import sys
import copy
from queue import PriorityQueue
import math

sys.setrecursionlimit(1000000)
def get_ints():
    return map(int,sys.stdin.readline().strip().split())

def get_string():
    return sys.stdin.readline().strip()

class Graph:
    def __init__(self, n=0, e=0):
        self.n = n
        self.e = e
        self.INFINITY = 1000000007
        self.indexed = 1
        self.adj_list = [[] for i in range(n)]

    def build_adjList(self, directed=False, indexed=1):
        self.indexed = indexed
        for _ in range(self.e):
            u, v = get_ints()

            u = u - self.indexed
            v = v - self.indexed

            self.adj_list[u].append(v)
            if (not directed):
                self.adj_list[v].append(u)

    def print(self, pl):
        for i in pl:
            print(i + self.indexed, end=" ")
        print()

    def dfs_one(self, n, visited=None, pl=None):

        def dfs(n, visited, pl):
            pl.append(n)
            visited[n] = True
            for i in self.adj_list[n]:
                if (not visited[i]):
                    dfs(i, visited, pl)

        if (visited == None):
            visited = [False] * self.n
        if (pl == None):
            pl = []
        dfs(n, visited, pl)
        return pl

    def dfs(self):
        visited = [False] * self.n
        pl = []
        for i in range(self.n):
            if (not visited[i]):
                self.dfs_one(i, visited, pl)

        return pl

    def bfs_one(self, n, visited=None, pl=None):

        def bfs(n, visited, pl):
            que = [n]
            visited[n] = True
            while (que):
                currNode = que[0]
                pl.append(currNode)
                que.pop(0)
                for i in self.adj_list[currNode]:
                    if (not visited[i]):
                        visited[i] = True
                        que.append(i)

        if (visited == None):
            visited = [False] * self.n
        if (pl == None):
            pl = []
        bfs(n, visited, pl)
        return pl

    def bfs(self):
        visited = [False] * self.n
        pl = []
        for i in range(self.n):
            if (not visited[i]):
                self.bfs_one(i, visited, pl)

        return pl

    def find_number_of_connected_components(self):
        visited = [False] * n
        count_components = 0
        for i in range(self.n):
            if (not visited[i]):
                count_components += 1
                self.dfs_one(i, visited)
        return count_components

    def single_source_shortest_path(self, n):
        visited = [False] * self.n
        shortest_path = [self.INFINITY] * self.n
        shortest_path[n] = 0

        def dfs(ni, visited, count, shortest_path):
            # shortest_path[ni] = count
            visited[ni] = True
            for i in self.adj_list[ni]:
                if (shortest_path[i] > (count + 1)):
                    shortest_path[i] = count + 1
                if (not visited[i]):
                    dfs(i, visited, count + 1, shortest_path)

        dfs(n, visited, 0, shortest_path)
        return shortest_path

    def isTree(self):
        nc = self.find_number_of_connected_components()
        if (nc == 1 and self.n == self.e + 1):
            return True
        else:
            return False

    def isBipartite(self, connected=False):
        visited = [False] * self.n
        color = [-1] * self.n
        color[0] = 0

        def dfs(ni, visited, c, color):
            visited[ni] = True
            for i in self.adj_list[ni]:
                if (not visited[i]):
                    color[i] = 1 - c
                    return dfs(i, visited, 1 - c, color)
                else:
                    if (color[i] == color[ni]):
                        return False
            return True

        if (not connected):
            ans = True
            for i in range(self.n):
                if (not visited[i]):
                    color[i] = 0
                    ans = ans and dfs(i, visited, 0, color)
            return ans

        return dfs(0, visited, 0, color)

    def isCycle(self):
        visited = [False] * self.n

        def dfs(ni, par):
            visited[ni] = True
            for child in self.adj_list[ni]:
                if (not visited[child]):
                    return dfs(child, ni)
                else:
                    if (child != par):
                        return True
            return False

        for i in range(self.n):
            if (not visited[i]):
                if (dfs(i, -1)):
                    return True
        return False

    def in_and_out(self):
        visited = [False] * self.n
        in_time = [-1] * self.n
        out_time = [-1] * self.n
        timer = [1]

        def dfs(ni, in_time, out_time, visited, timer):
            visited[ni] = True
            in_time[ni] = timer[0]
            timer[0] += 1
            for i in self.adj_list[ni]:
                if (not visited[i]):
                    dfs(i, in_time, out_time, visited, timer)

            out_time[ni] = timer[0]
            timer[0] += 1

        for i in range(self.n):
            if (not visited[i]):
                dfs(i, in_time, out_time, visited, timer)
        return in_time, out_time

    def diameter(self):
        visited = [False] * self.n
        temp = [0]
        node_v = [-1]

        def dfs(ni, visited, count, temp, node_v):
            visited[ni] = True
            if (count >= temp[0]):
                temp[0] = count
                node_v[0] = ni
            for i in self.adj_list[ni]:
                if (not visited[i]):
                    dfs(i, visited, count + 1, temp, node_v)

        for i in range(self.n):
            if (not visited[i]):
                dfs(0, visited, 0, temp, node_v)
        temp = [0]

        visited = [False] * self.n
        for i in range(self.n):
            if not visited[i]:
                dfs(node_v[0], visited, 0, temp, [0])

        return temp[0]

    def findBridges(self):
        visited = [False] * self.n
        in_time = [0] * self.n
        low = [0] * self.n
        timer = [0]
        ans = []

        def dfs(ni, visited, par, in_time, low, timer, ans):
            visited[ni] = True
            timer[0] += 1
            low[ni] = timer[0]
            in_time[ni] = timer[0]
            for _, i in enumerate(self.adj_list[ni]):
                if (i == par):
                    continue
                if (not visited[i]):
                    dfs(i, visited, ni, in_time, low, timer, ans)
                    if (low[i] > in_time[ni]):
                        ans.append([ni + self.indexed, i + self.indexed])
                    low[ni] = min(low[i], low[ni])
                else:
                    low[ni] = min(low[i], in_time[ni])

        dfs(0, visited, -1, in_time, low, timer, ans)
        return ans

    def findArticulation_vertex(self):
        visited = [False] * self.n
        in_time = [-1] * self.n
        low = [-1] * self.n
        ans = set()
        timer = [0]

        def dfs(ni, visited, par, in_time, low, timer, ans):
            visited[ni] = True
            children = 0
            in_time[ni] = timer[0]
            low[ni] = timer[0]
            timer[0] += 1

            for i in self.adj_list[ni]:
                if (i == par):
                    continue
                elif (not visited[i]):
                    dfs(i, visited, ni, in_time, low, timer, ans)
                    if (low[i] >= in_time[ni]):
                        if (ni != 0):
                            ans.add(ni + self.indexed)
                    low[ni] = min(low[ni], low[i])
                    children += 1
                else:
                    low[ni] = min(in_time[i], low[ni])

            if (children > 1 and par == -1):
                ans.add(0 + self.indexed)

        dfs(0, visited, -1, in_time, low, timer, ans)
        return ans

    def build_directed_graph_with_indegree(self, indexed=1):
        self.indexed = indexed
        indegree = [0] * (self.n)
        self.adj_list = [[] for _ in range(self.n)]
        for _ in range(self.e):
            u, v = get_ints()
            u = u - self.indexed
            v = v - self.indexed
            self.adj_list[u].append(v)
            indegree[v] += 1
        return indegree

    def topologicalsort(self, indegree):
        que = []
        ans = []
        for i in range(len(indegree)):
            if (indegree[i] == 0):
                que.append(i)
        while (que):
            curr = que.pop(0)
            ans.append(curr)
            for i in self.adj_list[curr]:
                indegree[i] -= 1
                if (indegree[i] == 0):
                    que.append(i)
        return ans

if __name__=="__main__":
    pass