import heapq                                    #导入优先队列模块
class HTNode: 									#哈夫曼树结点类
    def __init__(self,d=" ",w=None):     	    #构造方法
        self.data=d						        #结点值
        self.weight=w							#权值
        self.parent=-1						    #指向双亲结点
        self.lchild=-1							#指向左孩子结点
        self.rchild=-1							#指向右孩子结点
        self.flag=True							#标识是双亲的左(True)或者右(False)孩子

def CreateHT():							        #构造哈夫曼树
    global ht,n0,D,W                            #全局列表，存放哈夫曼树
    ht=[None]*(2*n0-1)                          #初始为含2n0-1个空结点
    heap=[]                                     #优先队列元素为[w,i]，按w权值建立小根堆
    for i in range(n0):                         #i从0到n0-1循环建立n0个叶子结点并进队
        ht[i]=HTNode(D[i],W[i])                 #建立一个叶子结点
        heapq.heappush(heap,[W[i],i])           #将[W[i],i]进队
    for i in range(n0,2*n0-1):					#i从n0到2n0-2循环做n0-1次合并操作
        p1=heapq.heappop(heap)				    #出队两个权值最小的结点p1和p2
        p2=heapq.heappop(heap)
        ht[i]=HTNode()							#新建ht[i]结点
        ht[i].weight=ht[p1[1]].weight+ht[p2[1]].weight	#求权值和
        ht[p1[1]].parent=i                      #设置p1的双亲为ht[i]
        ht[i].lchild=p1[1]                      #将p1作为双亲ht[i]的左孩子
        ht[p1[1]].flag=True
        ht[p2[1]].parent=i                      #设置p2的双亲为ht[i]
        ht[i].rchild=p2[1]                      #将p2作为双亲ht[i]的右孩子
        ht[p2[1]].flag=False 
        heapq.heappush(heap,[ht[i].weight,i])   #将新结点ht[i]进队

def DispHT():                                    #输出哈夫曼树
    global n0
    global ht
    print("  i      ",end=' ')
    for i in range(2*n0-1):
        print("%3d" %(i),end=' ')
    print()
    print("  D[i]   ",end=' ')
    for i in range(2*n0-1):
        print("%3s" %(ht[i].data),end=' ')
    print()
    print("  W[i]   ",end=' ')
    for i in range(2*n0-1):
        print("%3g" %(ht[i].weight),end=' ')
    print()
    print("  parent ",end=' ')
    for i in range(2*n0-1):
        print("%3d" %(ht[i].parent),end=' ')
    print()
    print("  lchild ",end=' ')
    for i in range(2*n0-1):
        print("%3d" %(ht[i].lchild),end=' ')
    print()
    print("  rchild ",end=' ')
    for i in range(2*n0-1):
        print("%3d" %(ht[i].rchild),end=' ')
    print()
        
def CreateHCode():						#根据哈夫曼树求哈夫曼编码
    global n0,ht,hcd                    #hcd存放哈夫曼编码
    hcd=[]
    for i in range(n0):				    #遍历下标从0到n0-1的叶子结点
        code=[]
        j=i							    #从ht[i]开始找双亲结点
        while ht[j].parent!=-1:
            if ht[j].flag:				#ht[j]结点是双亲的左孩子
                code.append("0")
            else:						#ht[j]结点是双亲的右孩子
                code.append("1")
            j=ht[j].parent
        code.reverse()
        hcd.append(''.join(code))       #将code转换为字符串并添加到hcd中
def DispHCode():						#输出哈夫曼编码
    global hcd
    for i in range(len(hcd)):
        print("  "+ht[i].data+": "+hcd[i])
if __name__ == '__main__':
    n0=4                                #编码的字符个数
    D=['a','b','c','d']                 #字符列表
    W=[1,3,5,7]                         #权值列表
    print("(1)建立哈夫曼树")
    CreateHT()
    print("(2)输出哈夫曼树")
    DispHT()
    print("(3)建立哈夫曼编码")
    CreateHCode()
    print("(4)输出哈夫曼编码")
    DispHCode()
