class BST_TreeNode:
    def __init__(self,val):
        self.data = val
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def isNode(self,val):
        tempNode = self.root
        while(tempNode!=None):
            if(tempNode.data==val):
                return True
            elif(val>tempNode.data):
                tempNode = tempNode.right
            else:
                tempNode = tempNode.left
        return False
    
    def insertNode(self,val):
        newNode = BST_TreeNode(val)
        if(self.root==None):
            self.root = newNode
        else:
            prevtempNode = self.root
            tempNode = self.root
            right = False
            left = False
            while(tempNode!=None):
                prevtempNode = tempNode
                if(val>=tempNode.data):
                    right = True
                    left = False
                    tempNode = tempNode.right
                else:
                    left = True
                    right = False
                    tempNode = tempNode.left
            if(right==True):
                prevtempNode.right = newNode
            else:
                prevtempNode.left = newNode
    def findInorderSuccessor(self,node):
        while(node.left!=None):
            node = node.left            
        return node
    
    
    def __delete_one_node(self,node,val):
        if(val>node.data):
            node.right = self.__delete_one_node(node.right,val)
        elif(val<node.data):
            node.left = self.__delete_one_node(node.left,val)
         
        else:
            if(node.left==None and node.right==None):   
                return None
            elif(node.left==None):
                return node.right
            elif(node.right==None):
                return node.left
            else:
                insucNode = self.findInorderSuccessor(node.right)
                node.data = insucNode.data
                node.right = self.__delete_one_node(node.right,insucNode.data)
        return node
    
                
    def deleteNode(self,val):
        nodeFlag = self.isNode(val)
        if(not nodeFlag):
            return
        tempNode = self.root
        self.root = self.__delete_one_node(tempNode,val)
    
    def inorderTraversal(self,node,inlist):
        if(node==None): return
        self.inorderTraversal(node.left,inlist)
        inlist.append(node.data)
        self.inorderTraversal(node.right,inlist)
        
    def printTree(self,get=False):
        tempNode = self.root
        inlist = []
        self.inorderTraversal(tempNode,inlist)
        if(get==True):
            return inlist
        else:
            print(*inlist)




class AVL_TreeNode:
    def __init__(self,val):
        self.data = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    
    def isNode(self,val):
        tempNode = self.root
        while(tempNode!=None):
            if(tempNode.data==val):
                return True
            elif(val>tempNode.data):
                tempNode = tempNode.right
            else:
                tempNode = tempNode.left
        return False
    
    def getHeight(self,node):
        if(node==None):
            return 0
        else:
            return node.height
    def balancefactor(self,node):
        left = 0
        right = 0
        if(node.left!=None):
            left = node.left.height
        if(node.right!=None):
            right = node.right.height
        return left-right
    
    def __insertNode(self,node,val):
        if(node==None):
            newNode = AVL_TreeNode(val)
            return newNode
        
        if(val>node.data):
            node.right = self.__insertNode(node.right,val)
        elif(val<node.data):
            node.left = self.__insertNode(node.left,val)
        
        node.height = 1+ max(self.getHeight(node.left),self.getHeight(node.right))
        
        bfactor = self.balancefactor(node)
    
        # Left Left Case
        if(bfactor>1 and val<node.left.data):
            node = self.rightrotate(node)
        
        # Left Right Case
        elif(bfactor>1 and val>node.left.data):
            node.left = self.leftrotate(node.left)
            node = self.rightrotate(node)
        
        # Right Right Case
        elif(bfactor<-1 and val>node.right.data):
            node = self.leftrotate(node)
        
        # Right Left Case
        elif(bfactor<-1 and val<node.right.data):
            node.right = self.rightrotate(node.right)
            node = self.leftrotate(node)
    
        return node
    
      
    def leftrotate(self,node):
        unbal = node
        temp = unbal.right
        unbal.right = temp.left
        temp.left = unbal
        
        unbal.height = 1+ max(self.getHeight(unbal.left),self.getHeight(unbal.right))
        temp.height = 1+ max(self.getHeight(temp.left),self.getHeight(temp.right))   
        
        return temp

    def rightrotate(self,node):
        unbal = node
        temp = unbal.left
        unbal.left = temp.right
        temp.right = unbal
        
        unbal.height = 1+ max(self.getHeight(unbal.left),self.getHeight(unbal.right))
        temp.height = 1+ max(self.getHeight(temp.left),self.getHeight(temp.right))        
        
        
        return temp
        
    def insertNode(self,val):
        self.root = self.__insertNode(self.root,val)
        
    def findInorderSuccessor(self,node):
        while(node.left!=None):
            node = node.left            
        return node
    
    def __checkBalance(self,node):
        if(node==None):
            return True
        bfactor = self.balancefactor(node)
       
        if(bfactor>1 or bfactor<-1):
            return False
        flg = True        
        flg = flg and self.__checkBalance(node.left)
        flg = flg and self.__checkBalance(node.right)
        return flg
    
    def __deleteNode(self,node,val):
        if(node==None): return 
        if(val>node.data):
            node.right = self.__deleteNode(node.right,val)
        elif(val<node.data):
            node.left = self.__deleteNode(node.left,val)
         
        else:
            if(node.left==None and node.right==None):   
                return None
            elif(node.left==None):
                return node.right
            elif(node.right==None):
                return node.left
            else:
                insucNode = self.findInorderSuccessor(node.right)
                node.data = insucNode.data
                node.right = self.__deleteNode(node.right,insucNode.data)

        if(node==None):
            return None
        node.height = 1 + max(self.getHeight(node.left),self.getHeight(node.right))
        bfactor = self.balancefactor(node)
        
        
        # Left Left
        if(bfactor>1 and self.balancefactor(node.left)>=0):
            node = self.rightrotate(node)
         
        # left Right   
        elif(bfactor>1 and self.balancefactor(node.left)<0):
            node.left = self.leftrotate(node.left)
            node = self.rightrotate(node)
            
        # Right Right
        elif(bfactor<-1 and self.balancefactor(node.right)<=0):
            node = self.leftrotate(node)
        
        # Right Left
        elif(bfactor<-1 and self.balancefactor(node.right)>0):
            node.right = self.rightrotate(node.right)
            node = self.leftrotate(node)
        
        return node
    
                
    def deleteNode(self,val):
        nodeFlag = self.isNode(val)
        if(not nodeFlag):
            return
        tempNode = self.root
        self.root = self.__deleteNode(tempNode,val)
    
    def inorderTraversal(self,node,inlist):
        if(node==None): return
        self.inorderTraversal(node.left,inlist)
        inlist.append(node.data)
        self.inorderTraversal(node.right,inlist)
    
    def bfstraversal(self,node,inlist):
        if(node==None): return
        tempNode = node
        que = [tempNode]
        while(len(que)!=0):
            newque = []
            for tnode in que:
                inlist.append(tnode.data if tnode!=None else "N")
                if(tnode!=None):
                    newque.append(tnode.left)
                    newque.append(tnode.right)
                    
            que = newque.copy()
                    
        
        
            
    def printTree(self,bfs=False,get=False):
        tempNode = self.root
        inlist = []
        if(not bfs):
            self.inorderTraversal(tempNode,inlist)
        else:
            self.bfstraversal(tempNode,inlist)
      
        if(get==True):
            return inlist
        else:
            print(*inlist)
        


