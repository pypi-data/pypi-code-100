from MatGraph import MatGraph,INF,MAXV
def Floyd(g):           	                #输出所有两个顶点之间的最短路径
    A=[[0]*MAXV for i in range(MAXV)]       #建立A数组
    path=[[0]*MAXV for i in range(MAXV)]    #建立path数组
    for i in range(g.n):					#给数组A和path置初值即求A-1[i][j]
        for j in range(g.n): 
            A[i][j]=g.edges[i][j]
            if i!=j and g.edges[i][j]<INF:
                path[i][j]=i				#i和j顶点之间有边时
            else:	
                path[i][j]=-1				#i和j顶点之间没有边时
    for k in range(g.n):					#求Ak[i][j]
        for i in range(g.n):
            for j in range(g.n):
                if A[i][j]>A[i][k]+A[k][j]:
                    A[i][j]=A[i][k]+A[k][j]
                    path[i][j]=path[k][j]   #修改最短路径
    Dispath(A,path,g)						#生成最短路径和长度

def Dispath(A,path,g):          	        #输出所有的最短路径和长度
    for i in range(g.n):
        for j in range(g.n):
            if A[i][j]!=INF and i!=j:		#若顶点i和j之间存在路径
                print("  顶点%d到%d的最短路径长度: %d\t路径:" %(i,j,A[i][j]),end='')
                k=path[i][j]
                apath=[j]			        #路径上添加终点
                while k!=-1 and k!=i:		#路径上添加中间点
                    apath.append(k)         #顶点k加入到路径中
                    k=path[i][k]
                apath.append(i)             #路径上添加起点
                apath.reverse()             #逆置
                print(apath)                #输出最短路径


#主程序
g=MatGraph()
n,e=4,8
a=[[0,5,INF,7],[INF,0,4,2],[3,3,0,2],[INF,INF,1,0]]   #图7.40的边数组
g.CreateMatGraph(a,n,e)
print("图g")
g.DispMatGraph()
print("Floyd求解结果");
Floyd(g)
