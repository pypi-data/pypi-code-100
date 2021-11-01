from MatGraph import MatGraph,INF,MAXV
def Prim(g,v):      		                    #求最小生成树
    lowcost=[0]*MAXV	        		            #建立数组lowcost
    closest=[0]*MAXV			                #建立数组closest
    for i in range(g.n):					    #给lowcost[]和closest[]置初值
        lowcost[i]=g.edges[v][i]
        closest[i]=v
    for i in range(1,g.n):				        #找出最小生成树的n-1条边
        min=INF
        k=-1
        for j in range(g.n):				    #在(V-U)中找出离U最近的顶点k
            if lowcost[j]!=0 and lowcost[j]<min:
                min=lowcost[j]
                k=j						        #k记录最小顶点的编号
        print("(%d,%d):%d" %(closest[k],k,+min),end=' ')    #输出最小生成树的边
        lowcost[k]=0						    #将顶点k加入U中
        for j in range(g.n):				    #修改数组lowcost和closest
            if lowcost[j]!=0 and g.edges[k][j]<lowcost[j]:
                lowcost[j]=g.edges[k][j]
                closest[j]=k


#主程序
g=MatGraph()
n,e=6,10
a=[[0,6,1,5,INF,INF], [6,0,5,INF,3,INF], [1,5,0,5,6,4], \
    [5,INF,5,0,INF,2], [INF,3,6,INF,0,6], [INF,INF,4,2,6,0]]  #图7.31(a)的边数组
g.CreateMatGraph(a,n,e)
print("图G1")
g.DispMatGraph()
print("求解结果");
Prim(g,0)