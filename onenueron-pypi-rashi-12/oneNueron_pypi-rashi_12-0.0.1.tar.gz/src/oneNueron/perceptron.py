import numpy as np
import logging
from tqdm import tqdm

class Perecptron:
    def __init__(self,eta,epohcs):
        np.random.seed(42)
        # small weight initialization
        self.weights=np.random.randn(3)*1e-4
        logging.info(f"Weights before initialization are :--\n{self.weights}")
        self.eta=eta
        self.epochs=epohcs
    def activationFunction(self,inputs,weights):
        z=np.dot(inputs,weights)
        return np.where(z>0,1,0)
    def fit(self,X,y):
        self.X=X
        self.y=y
        X_with_bias=np.c_[self.X,-np.ones((len(self.X),1))]
        logging.info(f"X with bias is :--\n{X_with_bias}")
        for epoch in tqdm(range(len(self.epochs)),total=self.epochs,decs="training the model"):
            print("------"*10)
            print(f"for epoch :-{epoch}")
            print("------"*10)
            # forward propagation
            y_hat=self.activationFunction(X_with_bias,self.weights)
            logging.info(f"Predicted values after the forward pass:--{y_hat}")
            self.error=self.y-y_hat
            # This would calculate the error
            logging.info(f"Error :--{self.error}")
            #backward propagation
            self.weights=self.weights+self.eta*np.dot(X_with_bias.T,self.error)
            logging.info(f"Calculated weights after each ephoc:-\n{epoch/self.epoch}:\n{self.weights}")
            logging.info("#####"*10)
    def predict(self,X):
        X_with_bias=np.c_[X,-np.ones((len(X),1))] 
        return self.activationFunction(X_with_bias,self.weights) 
    def loss(self):
        total_loss=np.sum(self.error)    
        # total loss is simply the sum of all the losses in the epoch
        print(f"Total loss :-- \n{total_loss}")
        return total_loss



