import numpy as np
class perceptron:
    def __init__(self,epoch,eta):
        self.w=np.random.randn(3)*1e-4
        self.eta=eta
        self.epoch=epoch
    def fit(self,x,y):
        self.x=x
        self.y=y
        xb=np.c_[self.x,-np.ones((len(x),1))]
        for _ in range(self.epoch):
            for d,y_ in zip(xb,self.y):
                yhat=self.activation(np.dot(d,self.w)) 
                error=y_-yhat
                dw=self.eta*error*np.array(d)
                self.w=self.w+dw

    def activation(self,x):
        if x>=0:
            return 1
        else:
            return 0
    def predict(self,x):
        x.append(-1)
        return self.activation(np.dot(self.w,x))

o1=perceptron(5,1)
o1.fit([[0,0],[0,1],[1,0],[1,1]],[0,0,0,1])
print(o1.predict([1,1]))
import logging

log_f='[%(asctime)s__%(levelname)s__%(module)s]:%(message)s'
logging.basicConfig(filename='loggggggg.log',filemode='a',level=10,format=log_f)
logging.info("this is info")
logging.debug('this is a debug warning')

    