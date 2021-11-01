from AdjGraph import AdjGraph,INF,MAXV
from collections import deque
#拓扑排序:栈实现
def TopSort(G):	                            #拓扑排序
    ind=[0]*MAXV            				#记录每个顶点的入度
    for i in range(G.n):					#求顶点i的入度
        for j in range(len(G.adjlist[i])):  #处理顶点i的所有出边
            w=G.adjlist[i][j].adjvex        #取顶点i的第j个出边邻接点w
            ind[w]+=1                       #有边<i,w>，顶点w的入度增1
    st=deque()                              #用双端队列实现栈
    for i in range(G.n):					#所有入度为0的顶点进栈
        if ind[i]==0:st.append(i)
    while len(st)>0:            		    #栈不为空时循环
        i=st.pop()							#出栈一个顶点i
        print("%d" %(i),end=' ')			#输出顶点i
        for j in range(len(G.adjlist[i])):  #处理顶点i的所有出边
            w=G.adjlist[i][j].adjvex        #取顶点i的第j个出边邻接点w
            ind[w]-=1						#顶点w的入度减1
            if ind[w]==0:st.append(w)		#入度为0的邻接点进栈


#拓扑排序:栈队列
def TopSort1(G):	                        #拓扑排序
    ind=[0]*MAXV            				#记录每个顶点的入度
    for i in range(G.n):					#求顶点i的入度
        for j in range(len(G.adjlist[i])):  #处理顶点i的所有出边
            w=G.adjlist[i][j].adjvex        #取顶点i的第j个出边邻接点w
            ind[w]+=1                       #有边<i,w>，顶点w的入度增1
    qu=deque()                              #用双端队列实现队列
    for i in range(G.n):					#所有入度为0的顶点进队
        if ind[i]==0:qu.append(i)
    while len(qu)>0:            		    #队不为空时循环
        i=qu.popleft()						#出队一个顶点i
        print("%d" %(i),end=' ')			#输出顶点i
        for j in range(len(G.adjlist[i])):  #处理顶点i的所有出边
            w=G.adjlist[i][j].adjvex        #取顶点i的第j个出边邻接点w
            ind[w]-=1						#顶点w的入度减1
            if ind[w]==0:qu.append(w)		#入度为0的邻接点进队列



#主程序
G=AdjGraph()
n,e=6,6
a=[[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0], \
		[0,0,0,0,0,0],[0,1,0,0,0,1],[0,0,0,1,0,0]]
G.CreateAdjGraph(a,n,e)
print("图G");G.DispAdjGraph()
print("拓扑序列: ",end=' ')
TopSort1(G)

