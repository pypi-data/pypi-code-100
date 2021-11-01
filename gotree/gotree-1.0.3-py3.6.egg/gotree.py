# encoding=utf8
# 机构：79软件
# 作者：Newman

import numpy as np
from pymysql import *
from graphviz import Digraph
import os
import string
import random
import openpyxl
from openpyxl.styles import Font,Alignment,Side,Border
import json
import csv


os.environ["PATH"] += os.pathsep + r'C:\Program Files (x86)\Graphviz\bin'
#os.environ["PATH"] += os.pathsep + r'D:\Program Files (x86)\graphviz2.38\release\bin'
#Graphviz安装在C:\Program Files (x86)\Graphviz\bin，已经添加路径到系统路径中


class GoTree(object):
    # 数据库连接参数，可以定义多个，比如conn_params1，conn_params2，用于连接多个数据库，在类实例化时指定
    #conn_params1 = {'host': 'localhost', 'port': 3306, 'user': 'newman', 'passwd': '123456', 'db': 'gotree',
    #                'charset': 'utf8'}

    #conn_params2 = {'host': 'localhost', 'port': 3306, 'user': 'newman', 'passwd': '123456', 'db': 'website',
    #                'charset': 'utf8'}

    # 类的构造函数，主要用于类的初始化，传递MySQL数据库连接参数，由调用程序提供，格式如上面的示例
    def __init__(self, conn_params):
        self.__host = conn_params['host']
        self.__port = conn_params['port']
        self.__db = conn_params['db']
        self.__user = conn_params['user']
        self.__passwd = conn_params['passwd']
        self.__charset = conn_params['charset']

    # 建立数据库连接和打开游标
    def __connect(self):
        self.__conn = connect(host=self.__host, port=self.__port, db=self.__db, user=self.__user, passwd=self.__passwd,
                              charset=self.__charset)
        self.__cursor = self.__conn.cursor()

    # 关闭游标和关闭连接
    def __close(self):
        self.__cursor.close()
        self.__conn.close()

    # 取一条数据
    def get_one(self, sql, params):
        result = None

        try:
            self.__connect()
            self.__cursor.execute(sql, params)
            result = self.__cursor.fetchone()
            self.__close()
        except Exception as e:
            print(e)
            exit(1)
        return result

    # 取所有数据
    def get_all(self, sql, params):
        lst = ()
        try:
            self.__connect()
            self.__cursor.execute(sql, params)
            lst = self.__cursor.fetchall()
            self.__close()
        except Exception as e:
            print(e)
            exit(1)
        return lst

    # 增加数据
    def insert(self, sql, params):
        return self.__edit(sql, params)

    # 修改数据
    def update(self, sql, params):
        return self.__edit(sql, params)

    # 删除数据
    def delete(self, sql, params):
        return self.__edit(sql, params)

    # 写数据操作具体实现，增删改操作都是调用这个方法来实现，这是个私有方法，不允许类外部调用
    def __edit(self, sql, params):
        count = 0
        try:
            self.__connect()
            count = self.__cursor.execute(sql, params)
            self.__conn.commit()
            self.__close()
        except Exception as e:
            print(e)
            exit(1)
        return count

    # 生成新节点的坐标
    def genndname_dimession(self,fndname_rw,fndname_cl,fndname_ovcl,sibling):
        lst=[]
        lst.append(fndname_rw+1)
        if sibling == 0: #插入第一个子节点，左节点
            wk_cl=fndname_cl*2 - 1
        elif sibling == 1: #插入第二个子节点，右节点
            wk_cl = fndname_cl * 2
        else:              #插入中节点
            wk_cl = fndname_cl * 2 - 1

        wk_ovcl = 0
        if fndname_ovcl != 0 or sibling > 1:
            wk_ovcl = np.random.randint(1,2147483647) #int类型占，4个字节  范围(-2147483648~2147483647)，无符号数最大值#2

        lst.append(wk_cl)
        lst.append(wk_ovcl)
        return lst


class Node:
    def __init__(self, parent=None, children=None, data=None, tag=None):
        """
        结点数据结构
        :param parent:  父节点
        :param children: 子节点，列表结构
        :param data: 数据域， 类型string
        """
        if children is None:
            children = []
        self.tag = tag if tag is not None else ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.parent = parent
        self.data = data
        self.children = children


class Tree:
    def __init__(self, rootdata):
        self.root = Node(data=rootdata)

    def insert(self, parent_node, children_node):
        children_node.parent = parent_node
        parent_node.children.append(children_node)
        print('insert',parent_node.data,children_node.data)
        print('insert,P.C',parent_node.children)
        print('insert,C.P',children_node.parent.data)

    def search(self, node, data):
        """
        以node为根节点查找值为data的结点，返回
        :param node: 根节点
        :param data: 值域
        :return:
        """
        if node.data == data:
            return node
        elif len(node.children) == 0:
            return None
        else:
            for child in node.children:
                res = self.search(child, data)
                if res is not None:
                    return res
            return None

    def show(self, save_path=None):
        """
        显示该树形结构
        :return:
        """
        from random import sample

        colors = ['skyblue', 'tomato', 'orange', 'purple', 'green', 'yellow', 'pink', 'red']
        plt = Digraph(comment='Tree')

        def print_node(node):
            color = sample(colors, 1)[0]
            if len(node.children) > 0:
                for child in node.children:
                    plt.node(child.tag, child.data, style='filled', color=color, fontname="Sans Not-Rotated")
                    plt.edge(node.tag, child.tag)
                    print('node.tag is:',node.tag)
                    print('child.tag is:',child.tag)
                    print('child is:',child)
                    print('child data is:',child.data)
                    print_node(child)

        plt.node(self.root.tag, self.root.data, style='filled', color=sample(colors, 1)[0])
        print_node(self.root)
        plt.view()
        if save_path is not None:
            print('save_path is:',save_path)
            plt.render(save_path)

#公共函数--------------------*********************************---------------------------------
# 检查根节点是否存在
def check_root_exist(conn_params1,tablename):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from '  + tablename + ' where rw=%s and cl=%s and ovcl=%s'
    print(sql)
    params = (1, 1, 0)
    result = gt.get_one(sql, params)

    if result==None:
        root_exist = False
        print('root record not exist!')
    elif len(result) == 0:
        root_exist = False
        print('root record not exist!')
    else:
        root_exist = True
        print('root record exist!')
        print('result:', result)
    print(root_exist)
    return root_exist

def insert_root(conn_params1,tablename,ndname,nddata):
    gt = GoTree(conn_params1)
    sql = 'insert into ' + tablename + ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    #print(sql)
    params = (1, 1, 0, 0, 0, 0, ndname,"", nddata)
    rowcount = gt.insert(sql, params)
    print("已增加" + str(rowcount) + "条数据")
    return rowcount

def getfname_dimession(conn_params1,tablename,fndname):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename + ' where ndname=%s'
    print(sql)
    params = (fndname)
    print(params)
    result = gt.get_one(sql, params)

    if result != None:
        if len(result) == 0:
            print('fndname record not found')
        else:
            print('result:', result)
    return result

def getnode_sibling(conn_params1,tablename,fndname):
    gt = GoTree(conn_params1)
    sql = 'select count(*) from  ' + tablename + ' where fndname = %s'
    params = (fndname)
    result = gt.get_one(sql, params)
    sibling = result
    #print('sibling is:=================',sibling)
    return sibling

def insert_ndname(conn_params1,tablename,wk_rw,wk_cl,wk_ovcl,fndname_rw,fndname_cl,fndname_ovcl,ndname,fndname,nddata):
    rowcount = 0
    while rowcount == 0:
        gt = GoTree(conn_params1)
        sql = 'insert into ' + tablename + ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (wk_rw,wk_cl,wk_ovcl,fndname_rw,fndname_cl,fndname_ovcl,ndname,fndname,nddata)
        rowcount = gt.insert(sql, params)
        if rowcount > 0:
            print("已增加" + str(rowcount) + "条数据")
            break
        else:
            wk_ovcl = np.random.randint(1, 2147483647)  # int类型占，4个字节  范围(-2147483648~2147483647)，无符号数最大值#2

# 插入一个新节点到围棋树中
def build_one_node(conn_params1,tablename,ndname,nddata,fndname,root=False):
    if root==True:
        root_exist = check_root_exist(conn_params1,tablename)
        if root_exist==True:
            print('Root already exist')
            exit(1)
        else:
            rowcount=insert_root(conn_params1,tablename,ndname,nddata)
            if rowcount > 0:
                print('Root insert ok!')
    else:
        lst=getfname_dimession(conn_params1,tablename,fndname)
        fndname_rw=lst[0]
        fndname_cl=lst[1]
        fndname_ovcl=lst[2]

        result=getnode_sibling(conn_params1,tablename,fndname)
        sibling=result[0]

        gt = GoTree(conn_params1)
        lst=gt.genndname_dimession(fndname_rw,fndname_cl,fndname_ovcl,sibling)
        if len(lst) > 0:
            for item in lst:
                wk_rw=lst[0]
                wk_cl=lst[1]
                wk_ovcl=lst[2]
            insert_ndname(conn_params1,tablename,wk_rw,wk_cl,wk_ovcl,fndname_rw,fndname_cl,fndname_ovcl,ndname,fndname,nddata)
        else:
            print('Gen node dimession error!')

# 插入Excel文件中的数据到到围棋树中
def excel2tree(conn_params1,tablename,filename,headers=1):
    workbook = openpyxl.load_workbook(filename)
    sheet=workbook.active   #指定活动的工作表，当只有一个sheet时用

    # 跳过标题行，获取所有数据行
    headers_count = 0
    rows = sheet.rows
    for row in rows:
        if headers_count < headers:
            headers_count+=1
            continue
        else:
            #print('all rows:', row)
            ndname=row[0].value
            nddata=row[1].value
            fndname=row[2].value
            if row[3].value== 'Y':
                root = True
            else:
                root = False
        build_one_node(conn_params1,tablename,ndname,nddata,fndname,root)

# 插入Json文件中的数据到到围棋树中
def json2tree(conn_params1,tablename,filename):
    with open(filename, 'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)

    #print(load_dict)
    for item in load_dict:
        ndname = item['ndname']
        nddata = item['nddata']
        fndname = item['fndname']
        if item['root'] == 'Y':
            root = True
        else:
            root = False
        build_one_node(conn_params1,tablename,ndname, nddata, fndname, root)

# 插入CSV文件中的数据到到围棋树中
def csv2tree(conn_params1,tablename,filename):
    with open(filename, 'r',encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')       #指定分号；为分隔符
        for item in reader:
            ndname = item[0]
            nddata = item[1]
            fndname = item[2]
            if item[3] == 'Y':
                root = True
            else:
                root = False
            build_one_node(conn_params1,tablename,ndname, nddata, fndname, root)

# 将围棋树数据下载到Excel文件中
def tree2excel(conn_params1,tablename,filename):
    h11='节点名字（ndname）'
    h12='节点数据（nddata）'
    h13='父节点名字（fndname）'
    h14='是否根节点（root = False）'

    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename
    print(sql)
    params = ()
    #print(params)
    result = gt.get_all(sql, params)
    print(result)

    if len(result) == 0:
        print('empty tree!')
    else:
        # 存放到一个新的excel文件中
        new_workbook = openpyxl.Workbook()  # 建立一个新的工作簿
        new_sheet = new_workbook.active  # 激活一个工作表

        #写excel标题
        new_sheet.append([h11,h12,h13,h14])
        font_h1 = Font(name='宋体', size=16, bold=True)
        new_sheet['A1'].font = font_h1
        new_sheet['B1'].font = font_h1
        new_sheet['C1'].font = font_h1
        new_sheet['D1'].font = font_h1

        for item in result:
            #print(item)
            wk_rw=item[0]
            wk_cl=item[1]
            wk_ovcl=item[2]
            wk_frw=item[3]
            wk_fcl=item[4]
            wk_fovcl=item[5]
            wk_ndname=item[6]
            wk_fndname=item[7]
            wk_nddata=item[8]
            if wk_rw==1 and wk_cl==1 and wk_ovcl==0:
                wk_root='Y'
            else:
                wk_root='N'
            lst = []
            lst.append(wk_ndname)
            lst.append(wk_nddata)
            lst.append(wk_fndname)
            lst.append(wk_root)
            #print(lst)
            new_sheet.append(lst)

        # 保存工作簿
        new_workbook.save(filename)  # 保存工作簿

# 将围棋树数据下周到csv文件中
#
def tree2csv(conn_params1,tablename,filename):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename
    print(sql)
    params = ()
    #print(params)
    result = gt.get_all(sql, params)
    print(result)

    if len(result) == 0:
        print('empty tree!')
    else:
        # 存放到一个新的csv文件中
        with open(filename, 'w',newline='') as f:
            writer=csv.writer(f,delimiter=';',dialect='excel')

        #       with open(filename, 'w',newline='') as f:
        #           writer=csv.writer(f,dialect='excel',delimiter=';',quoting=csv.QUOTE_MINIMAL)

            for item in result:
                #print(item)
                wk_rw=item[0]
                wk_cl=item[1]
                wk_ovcl=item[2]
                wk_frw=item[3]
                wk_fcl=item[4]
                wk_fovcl=item[5]
                wk_ndname=item[6]
                wk_fndname=item[7]
                wk_nddata=item[8]
                if wk_rw==1 and wk_cl==1 and wk_ovcl==0:
                    wk_root='Y'
                else:
                    wk_root='N'
                lst = []
                lst.append([wk_ndname,wk_nddata,wk_fndname,wk_root])
                #print(lst)
                #df=pd.DataFrame(lst)
                #df.to_csv(f, index=False, header=False,sep=';')
                #s=pd.Series(lst)
                #s.to_csv(f,sep=';',index=False,header=False)

                writer.writerows(lst)

# 将围棋树数据下载到json文件中
def tree2json(conn_params1,tablename,filename):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename
    print(sql)
    params = ()
    #print(params)
    result = gt.get_all(sql, params)
    print(result)

    if len(result) == 0:
        print('empty tree!')
    else:
        json_all = []
        for item in result:
            #print(item)
            wk_rw=item[0]
            wk_cl=item[1]
            wk_ovcl=item[2]
            wk_frw=item[3]
            wk_fcl=item[4]
            wk_fovcl=item[5]
            wk_ndname=item[6]
            wk_fndname=item[7]
            wk_nddata=item[8]
            if wk_rw==1 and wk_cl==1 and wk_ovcl==0:
                wk_root='Y'
            else:
                wk_root='N'
            dirt = {'ndname': 'test', 'nddata': 'test', 'fndname': 'test', 'root': 'test'}
            dirt['ndname'] = wk_ndname
            dirt['nddata'] = wk_nddata
            dirt['fndname'] = wk_fndname
            dirt['root'] = wk_root
            json_all.append(dirt)

            #print(json_all)

        # 写入json文件
        with open(filename, "w",encoding='utf-8') as f:
            json.dump(json_all,f,ensure_ascii=False)
            print("加载json文件完成...")

#修改节点信息
def updnamedata(conn_params1,tablename,ndname,nddata):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename + ' where ndname=%s'
    print(sql)
    params = (ndname)
    print(params)
    result = gt.get_one(sql, params)

    if result==None:
        print('ndname record not found')
        exit(1)
    elif len(result) == 0:
        print('ndname record not found')
        exit(1)
    else:
        gt = GoTree(conn_params1)
        sql = 'update ' + tablename + ' set nddata=%s where ndname=%s'
        print(sql)
        params = (nddata,ndname)
        print(params)
        result = gt.update(sql, params)
        print('result:', result)
    return result

#获取节点信息
def getnamedata(conn_params1,tablename,ndname):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename + ' where ndname=%s'
    print(sql)
    params = (ndname)
    print(params)
    result = gt.get_one(sql, params)

    if result == None:
        print('ndname record not found')
        exit(1)
    elif len(result) == 0:
        print('ndname record not found')
        exit(1)
    #print('result:', result)
    return result

#获取树的高度
def getheight(conn_params1,tablename,):
    gt = GoTree(conn_params1)
    sql = 'select max(rw) from ' + tablename
    print(sql)
    params = ()
    print(params)
    result = gt.get_one(sql, params)

    if len(result) == 0:
        print('empty tree!')
    #print('result:', result)
    return result[0]

#获取树的节点总数
def getnodecount(conn_params1,tablename,):
    gt = GoTree(conn_params1)
    sql = 'select count(*) from ' + tablename
    print(sql)
    params = ()
    print(params)
    result = gt.get_one(sql, params)

    if len(result) == 0:
        print('empty tree!')
    #print('result:', result)
    return result[0]

#树的逆向生长
def inversegrowth(conn_params1,tablename,newndname,newnddata):
    root_exist = check_root_exist(conn_params1,tablename)
    if root_exist != True:
        print('empty tree!please check again!')
    else:
        height=getheight(conn_params1,tablename)
        while height>0:
            gt = GoTree(conn_params1)
            sql = 'update ' + tablename + ' set rw=rw+1,frw=frw+1 where rw=%s'
            print(sql)
            params = (height)
            print(params)
            result = gt.update(sql, params)
            print('result:', result)
            height-=1

        insert_root(conn_params1,tablename,newndname,newnddata)

        gt = GoTree(conn_params1)
        sql = 'update ' + tablename + ' set fndname=%s, frw=%s,fcl=%s,fovcl=%s where rw=%s and cl=%s and ovcl=%s'
        print(sql)
        params = (newndname,1,1,0,2,1,0)
        print(params)
        result = gt.update(sql, params)
        print('result:', result)


#获取根节点的第n代子孙的个数和名字
def getrootdescendant(conn_params1,tablename,n):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename + ' where rw=%s'
    print(sql)
    params = (n+1)
    #print(params)
    result = gt.get_all(sql, params)
    print(result)

    if len(result) == 0:
        print('no descendant for root!')
    else:
        print('后代个数为：',len(result))
    lst=[]
    lst.append(len(result))
    for i in range(len(result)):
        lst.append(result[i][6])
    return lst

#获取节点的儿女个数和名字
def getndnamechildren(conn_params1,tablename,ndname):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename + ' where fndname=%s'
    print(sql)
    params = (ndname)
    # print(params)
    result = gt.get_all(sql, params)
    print(result)

    if len(result) == 0:
        print('no children for this node!')
    else:
        print('后代个数为：', len(result))
    lst = []
    lst.append(len(result))
    for i in range(len(result)):
        lst.append(result[i][6])
    return lst

#获取节点的父节点名字
def getndnameparent(conn_params1,tablename,ndname):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename + ' where ndname=%s'
    print(sql)
    params = (ndname)
    # print(params)parent
    result = gt.get_all(sql, params)
    print(result)

    if len(result) == 0:
        print('node not exist!')
    else:
        print('父节点个数为：', len(result))
    lst = []
    lst.append(len(result))
    lst.append(result[0][7])
    return lst

#获取节点的第n代子孙的个数和名字
def getndnamedescendant(conn_params1,tablename,ndname,n):
    result=getnamedata(conn_params1,tablename,ndname)
    wk_rw=result[0]
    print('wk_rw:',wk_rw)
    height=getheight(conn_params1,tablename,)
    if (wk_rw+n)>height:
        print('超过树的范围，请再次检查！')
    else:
        lst=[]
        lst.append(ndname)
        for i in range(1,n+1):
            lst1=[]
            for ndname in lst:
                print('ndname:',ndname)
                print('i:',i)
                lst2=getndnamechildren(conn_params1,tablename,ndname)
                print('lst2:',lst2)
                lst1=lst1+lst2[1:]
                print('lst1:',lst1)
            lst=lst1
            print('lst:',lst)
        lst1.insert(0,len(lst1))
        print(lst1)
        return lst1

#获取节点的第n代祖先的个数和名字
def getndnameancestors(conn_params1,tablename,ndname,n):
    result=getnamedata(conn_params1,tablename,ndname)
    wk_rw=result[0]
    print('wk_rw:',wk_rw)
    #height=getheight()
    if (wk_rw-n)<1:
        print('超过树的范围，请再次检查！')
    else:
        lst=[]
        lst.append(ndname)
        for i in range(n,0,-1):
            lst1=[]
            for ndname in lst:
                print('ndname:',ndname)
                print('i:',i)
                lst2=getndnameparent(conn_params1,tablename,ndname)
                print('lst2:',lst2)
                lst1=lst1+lst2[1:]
                print('lst1:',lst1)
            lst=lst1
            print('lst:',lst)
        lst1.insert(0,len(lst1))
        print(lst1)
        return lst1

#获取一行的所有节点，供显示围棋树使用
def getrownodes(conn_params1,tablename,rownum):
    gt = GoTree(conn_params1)
    sql = 'select rw,cl,ovcl,frw,fcl,fovcl,ndname,fndname,nddata from ' + tablename + ' where rw=%s order by fndname'
    print(sql)
    params = (rownum)
    # print(params)
    result = gt.get_all(sql, params)
    print(result)

    if len(result) == 0:
        print('empty tree!')

    return result

#树形展示整颗围棋树图形，生成PDF文件
def graphtree(conn_params1,tablename,):
    height = getheight(conn_params1,tablename,)
    #height=8
    print('树的高度为：', height)
    tree = Tree('Go_Tree')
    #root = tree.root
    #print('root is:',root)

    for wk_rownum in range(1,height+1):
    #for wk_rownum in range(1, 3):
        result=getrownodes(conn_params1,tablename,wk_rownum)
        wk_last_item7=''
        for item in result:
            print('fndname is:', item[7])
            print('ndname is:', item[6])
            #node_root=Node(data=root)
            root=tree.root

            if item[7] == '':
                node_ndname = Node(data=item[6])
                tree.insert(tree.root,node_ndname)
            else:
                if wk_last_item7 != item[7]:
                    wk_last_item7 = item[7]
                    node_fndname = Node(data=item[7])
                p = tree.search(root, wk_last_item7)
                child = Node(data=item[6])
                tree.insert(p, child)
                #node_ndname = Node(data=item[6])
                #tree.insert(node_fndname, node_ndname)

    tree.show()

#树形展示围棋树子树图形，生成PDF文件
def graphsubtree(conn_params1,tablename,ndname):
    result = getnamedata(conn_params1,tablename,ndname)
    wk_rw = result[0]
    print('wk_rw:', wk_rw)

    height = getheight(conn_params1,tablename,)
    #height=8
    print('树的高度为：', height)

    tree = Tree('Go_Tree_Sub')
    root = tree.root
    print('root is:',root)

    node_ndname = Node(data=ndname)
    tree.insert(tree.root, node_ndname)

    if wk_rw != height:    #叶节点，直接显示，非叶节点，继续处理
        lst=[]
        lst.append(ndname)
        for wk_rownum in range(wk_rw,height):
            lst1 = []
            for father in lst:
                result=getndnamechildren(conn_params1,tablename,father)
                print('result is:',result)
                if len(result)==1:                #只返回个数0，没有子节点
                    continue

                for item in result[1:]:
                    p = tree.search(root, father)
                    child = Node(data=str(item))
                    tree.insert(p, child)

                    lst1.append(item)
            lst=lst1

    tree.show()
#公共函数--------------------*********************************---------------------------------
