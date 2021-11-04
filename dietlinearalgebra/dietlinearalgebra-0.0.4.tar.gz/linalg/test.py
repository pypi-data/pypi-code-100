from __init__ import *
ERR_CHECK = False #set True to run error checking code
TEST_MAT = [[1,2,3],[4,5,6],[7,8,9]]
###### CONSTRUCTOR TESTING ######
# init 
# m_by_n = Matrix(2,3)
# vec = Matrix([1,2,3])
# matrix = Matrix([[1,2,3],[4,5,6],[7,8,9]])

#test add,sub,mult
v1 = Matrix(2,3)
v2 = Matrix(2,3)


#test transpose
v_t = v1.T
#test determinent
det = Matrix([[3,6],[5,4]])
det_val = det.det
#test id mat
id = IdentityMatrix(5)
print(id)
#test zero matrix
z = ZerosMatrix(3,2)
print(z)
# error checking 
if ERR_CHECK:
    try:
        er = Matrix()
    except Exception as e:
        print(e)
    try:
        er = Matrix('error')
    except Exception as e:
        print(e)
    try:
        er = Matrix([[1],[1,2]])
    except Exception as e:
        print(e)
    try:
        er = Matrix([1,2],1)
    except Exception as e:
        print(e)
    try:
        er = Matrix(1,'error')
    except Exception as e:
        print(e)
    try:
        er = Matrix(1,2,3)
    except Exception as e:
        print(e)
