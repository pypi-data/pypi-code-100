import random
def guessno(num):
    a =[1,2,3]
    b =num
    c =random.choice(a)
    if b==c:
        d=print('correct number')
        return d
    else:
        d=print('wrong number')
        return d
