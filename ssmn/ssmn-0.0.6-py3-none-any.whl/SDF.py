#ord() = example : ord("A") - 65
#chr() = example : chr("65") - "A"

def mkl(name, key, information):
    confirm1 = name.find("\\")
    confirm2 = name.find(" ")
    confirm3 = name.find("	")
    confirm4 = key.find("\\")
    confirm5 = key.find(" ")
    confirm6 = key.find("	")
    confirm7 = information.find("\\")
    confirm8 = information.find(" ")
    confirm9 = information.find("	")
    confirm10 = name.find("\n")
    confirm11 = key.find("\n")
    confirm12 = information.find("\n")
    if confirm1 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm2 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm3 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm4 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm5 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm6 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm7 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm8 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm9 > 0: #만약 confirm1의 값이 0보다 작다면
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm10 > 0:
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm11 > 0:
        raise Exception("There are characters that cannot be used (\,  ,	)")
    if confirm12 > 0:
        raise Exception("There are characters that cannot be used (\,  ,	)")
    line = name + " " + key + " " + information
    return line

def mkf(*args):
    last = ""
    for d in args:
        last += d
        last += "\n"

    return last

def getall(mkflast):
    #mklast는
    #name key information
    #name2 key2 information2
    #형태를 지니고 있다.
    getallv1 = mkflast.split("\n")
    #예를 들어서 만약 a가 2개로 측정이 됬다면
    #리스트에서는 0부터 숫자를 세니깐 -1한 값을 제외 시키면 된다.
    #
    a = len(getallv1) #개수
    a = a - 1
    del getallv1[a] #마지막 요소를 삭제한다.
    getallv2 = getallv1
    return getallv2

if __name__ == "__main__":
    t1 = mkl("testname", "testkey", "testinfo")
    t2 = mkl("testname2", "testkey2", "testinfo2")
    print(t1)
    print("\n")
    print(t2)
    print("\n")
    t3 = mkf(t1, t2)
    print(t3)
    print("\n")
    t4 = getall(t3)
    print(t4)
    print("\n")

#This file format is very weak