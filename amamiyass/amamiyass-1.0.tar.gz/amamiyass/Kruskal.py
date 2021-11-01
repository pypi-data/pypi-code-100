from MatGraph import MatGraph,INF,MAXV
from operator import itemgetter,attrgetter
#基本的Kruskal算法
def Kruskal1(g):        	                    #求最小生成树
    vset=[-1]*MAXV					            #建立数组vset
    E=[]					                    #建立存放所有边的列表E
    for i in range(g.n):					    #由邻接矩阵g产生的边集数组E
        for j in range(i+1,g.n):		        #对于无向图仅考虑上三角部分的边
            if g.edges[i][j]!=0 and g.edges[i][j]!=INF:
                E.append([i,j,g.edges[i][j]])   #添加[i,j,w]元素
    for i in range(len(E)):
        print("(%d,%d): %d" %(E[i][0],E[i][1],E[i][2]))
    E.sort(key=itemgetter(2))  	                #按权值递增排序
    for i in range(g.n):vset[i]=i		        #初始化辅助数组
    cnt=1									    #cnt表示当前构造生成树的第几条边,初值为1
    j=0									        #取E中边的下标,初值为0
    while cnt<g.n:								#生成的边数小于n时循环
        u1,v1=E[j][0],E[j][1]			        #取一条边的头尾顶点
        sn1=vset[u1]
        sn2=vset[v1]						    #分别得到两个顶点所属的集合编号
        if sn1!=sn2:							#两顶点属于不同的集合,加入不会构成回路
            print("(%d,%d):%d" %(u1,v1,E[j][2]),end=' ')    #输出最小生成树的边
            cnt+=1								#生成边数增1
            for i in range(g.n):			    #两个集合统一编号
                if vset[i]==sn2:				#集合编号为sn2的改为sn1
                    vset[i]=sn1
        j+=1								    #继续取E的下一条边

#改进的Kruskal算法
parent=[-1]*MAXV		                #并查集存储结构
rank=[0]*MAXV			                #存储结点的秩
def Init(n):					            #并查集初始化 
    #global parent
    #global rank
    for i in range(0,n):
        parent[i]=i
        rank[i]=0
def Find(x:int):							#查找x结点的根结点
    rx=x
    while parent[rx]!=rx:					#找到x的根rx
        rx=parent[rx]
    y=x
    while y!=rx:							#路径压缩
        parent[y]=rx
        y=parent[y]
    return rx								#返回根
    
def Union(x:int,y:int):		            #并查集中x和y的两个集合的合并
    #global parent
    #global rank
    rx=Find(x)
    ry=Find(y)
    if rx==ry:							#x和y属于同一棵树的情况 
        return
    if rank[rx]<rank[ry]:
        parent[rx]=ry					#rx结点作为ry的孩子 
    else:
        if rank[rx]==rank[ry]:			#秩相同，合并后rx的秩增1
            rank[rx]+=1
        parent[ry]=rx					#ry结点作为rx的孩子  
def Kruskal2(g):        	                    #求最小生成树
    E=[]					                    #建立存放所有边的列表E
    for i in range(g.n):					    #由邻接矩阵g产生的边集数组E
        for j in range(i+1,g.n):		        #对于无向图仅考虑上三角部分的边
            if g.edges[i][j]!=0 and g.edges[i][j]!=INF:
                E.append([i,j,g.edges[i][j]])   #添加[i,j,w]元素
    for i in range(len(E)):
        print("(%d,%d): %d" %(E[i][0],E[i][1],E[i][2]))
    E.sort(key=itemgetter(2))  	                #按权值递增排序
    Init(g.n)
    cnt=1									    #cnt表示当前构造生成树的第几条边,初值为1
    j=0									        #取E中边的下标,初值为0
    while cnt<g.n:								#生成的边数小于n时循环
        u1,v1=E[j][0],E[j][1]			        #取一条边的头尾顶点
        sn1=Find(u1)
        sn2=Find(v1)						    #分别得到两个顶点所属连通分量编号
        if sn1!=sn2:							#两顶点属于不同的集合,加入不会构成回路
            print("(%d,%d):%d" %(u1,v1,E[j][2]),end=' ')    #输出最小生成树的边
            cnt+=1								#生成边数增1
            Union(u1,v1);						#合并
        j+=1								    #继续取E的下一条边


#主程序
g=MatGraph()
n,e=6,10
a=[[0,6,1,5,INF,INF], [6,0,5,INF,3,INF], [1,5,0,5,6,4], \
    [5,INF,5,0,INF,2], [INF,3,6,INF,0,6], [INF,INF,4,2,6,0]]  #图7.31(a)的边数组
g.CreateMatGraph(a,n,e)
print("图G1")
g.DispMatGraph()
print("求解结果");
Kruskal2(g)