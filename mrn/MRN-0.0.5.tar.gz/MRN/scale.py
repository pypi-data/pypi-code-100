

import numpy as np


class Normalization:
    
    def __init__(self,array,memory_retention=0.5):
        self.__data=np.log(array)
        self.__memory_retention=memory_retention
        if memory_retention>1:
            self.__memory_retention=0
        elif memory_retention<0:
            self.__memory_retention=1
        else:
            self.__memory_retention=1-memory_retention
            
        self.__threshold=1/len(array)
        

    def __get_weight(self):
        w, k = [1.], 1
        ctr = 0
        while True:
            w_ = -w[-1] / k * (self.__memory_retention - k + 1)
            if abs(w_) < self.__threshold:
                break
            w.append(w_)
            k += 1
            ctr += 1
            if ctr == len(self.__data) - 1:
                break
        w = np.array(w[::-1]).reshape(-1, 1)
    
        return w
    
    def transform(self):
        w = self.__get_weight()
        width = len(w) - 1
        output = []
        output.extend([0] * width)
        print(width)
        for i in range(width, len(self.__data)):
            output.append(np.dot(w.T, self.__data[i - width:i + 1])[0])
        output=[(lambda x:x if x!=0 else float('nan'))(x) for x in output]
        return np.array(output)









    
    
    