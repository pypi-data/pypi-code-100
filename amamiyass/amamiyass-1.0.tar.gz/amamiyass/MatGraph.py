import copy
MAXV=100							    #表示最多顶点个数
INF=0x3f3f3f3f				            #表示∞
class MatGraph:				            #图邻接矩阵类
    def __init__(self,n=0,e=0):         #构造方法
        self.edges=[]		            #邻接矩阵数组
        self.vexs=[]		            #存放顶点信息，暂时未用
        self.n=n                        #顶点数
        self.e=e			            #边数
    def CreateMatGraph(self,a,n,e):  	#通过数组a、n和e建立图的邻接矩阵
        self.n=n                        #置顶点数和边数
        self.e=e
        self.edges=copy.deepcopy(a)     #深拷贝
    def DispMatGraph(self):			    #输出图
        for i in range(self.n):
            for j in range(self.n):
                if self.edges[i][j]==INF:
                    print("%4s"%("∞"),end=' ')
                else:
                    print("%5d" %(self.edges[i][j]),end=' ')
            print()

if __name__ == '__main__':
    g=MatGraph()
    n,e=5,5
    a=[ [0,8,INF,5,INF],
        [INF,0,3,INF,INF],
		[INF,INF,0,INF,6],
        [INF,INF,9,0,INF],
        [INF,INF,INF,INF,0]]
    g.CreateMatGraph(a,n,e)
    g.DispMatGraph()
