def fun(a,n,k):             #数组a共有n个元素
    if k==n-1:
        for i in range(n):  
            print(a[i],end=' ')
    else:
        for i in range(k,n):
            a[i]+=i*i
        fun(a,n,k+1)

a=[1,2,3]
fun(a,3,0)
