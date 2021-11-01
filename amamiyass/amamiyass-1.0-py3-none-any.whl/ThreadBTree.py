class ThNode:							            #线索二叉树结点类型
    def __init__(self,d=None):     		            #构造方法
        self.data=d						            #结点值
        self.ltag=0							        #左标志
        self.rtag=0                                 #右标志
        self.lchild=None				            #左指针
        self.rchild=None				            #右指针
    
class ThreadTree:                                   #中序线索化二叉树类
    def __init__(self,d=None):     		            #构造方法
        self.b=None                                 #根结点指针
        self.root=None						        #线索二叉树的头结点
        self.pre=None							        #用于中序线索化,指向中序前驱结点

    #二叉树的基本操作
    def SetRoot(self,r):                            #设置根结点为r
        self.b=r
    def DispBTree(self):					        #返回二叉链的括号表示串
        return self._DispBTree1(self.b)
    def _DispBTree1(self,t):		                #被DispBTree方法调用
        if t==None:                                 #空树返回空串
            return ""
        else:
            bstr=t.data							    #输出根结点值
            if t.lchild!=None or t.rchild!=None:
                bstr+="("							#有孩子结点时输出"("
                bstr+=self._DispBTree1(t.lchild)	#递归输出左子树
                if t.rchild!=None:
                    bstr+=","						#有右孩子结点时输出","
                bstr+=self._DispBTree1(t.rchild)	#递归输出右子树
                bstr+=")"							#输出")"
            return bstr
    #中序线索二叉树的基本操作
    def CreateThread(self):			            	#建立以root为头结点的中序线索二叉树
        self.root=ThNode()       					#创建头结点root
        self.root.ltag=0                            #头结点标志置初值
        self.root.rtag=1
        if self.b==None:						    #b为空树时
            self.root.lchild=self.root
            self.root.rchild=None
        else:										#b不为空树时
            self.root.lchild=self.b
            self.pre=self.root						#pre是p的前驱结点,用于线索化
            self._Thread(self.b)					#中序遍历线索化二叉树
            self.pre.rchild=self.root				#最后处理,加入指向根结点的线索
            self.pre.rtag=1
            self.root.rchild=self.pre				#根结点右线索化

    def _Thread(self,p):      			            #对以p为根结点的二叉树进行中序线索化
        if p!=None:
            self._Thread(p.lchild)					#左子树线索化
            if p.lchild==None:					    #前驱线索
                p.lchild=self.pre					#给结点p添加前驱线索
                p.ltag=1
            else: p.ltag=0
            if self.pre.rchild==None:
                self.pre.rchild=p					#给结点pre添加后继线索
                self.pre.rtag=1
            else:self.pre.rtag=0;
            self.pre=p								#置p结点为下一次访问结点的前驱结点
            self._Thread(p.rchild)					#右子树线索化

    def ThInOrder(self):						    #中序线索二叉树的中序遍历
        p=self.root.lchild						    #p指向根结点
        while p!=self.root:
            while p!=self.root and p.ltag==0:		#找中序开始结点
                p=p.lchild
            print(p.data,end=' ')				    #访问p结点
            while p.rtag==1 and p.rchild!=self.root:
                p=p.rchild							#如果是线索，一直找下去
                print(p.data,end=' ')			    #访问p结点
            p=p.rchild								#如果不再是线索，转向其右子树



if __name__ == '__main__':
    b=ThNode('A')							#建立各个结点
    p1=ThNode('B')
    p2=ThNode('C')
    p3=ThNode('D')
    p4=ThNode('E')
    p5=ThNode('F')
    p6=ThNode('G')
    b.lchild=p1								#建立结点之间的关系
    b.rchild=p2
    p1.lchild=p3
    p3.rchild=p6
    p2.lchild=p4
    p2.rchild=p5
    bt=ThreadTree()
    bt.SetRoot(b)
    print("建立二叉树bt")
    print("bt:",end=' '); print(bt.DispBTree())
    print("中序线索化二叉树")
    bt.CreateThread()
    print("中序序列:",end=' ');bt.ThInOrder()
    
