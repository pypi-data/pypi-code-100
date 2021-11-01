from BTree import BTree,BTNode
def Nodes(b):
    h=1
    p=b
    while p.lchild!=None:
        h+=1
        p=p.lchild
    return 2**h-1
    
if __name__ == '__main__':
    b=BTNode('A')							        #建立各个结点
    p1=BTNode('B')
    p2=BTNode('C')
    b.lchild=p1								        #建立结点之间的关系
    b.rchild=p2
    bt=BTree()
    bt.SetRoot(b)
    print("bt:",end=' '); print(bt.DispBTree())
    print(Nodes(bt.b))
