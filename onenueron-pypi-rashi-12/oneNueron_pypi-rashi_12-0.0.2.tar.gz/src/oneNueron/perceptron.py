import numpy as np
import logging
from tqdm import tqdm

class Perceptron:
  def __init__(self,eta,epochs):
    np.random.seed(42)
    #small weights initialization
    self.weights=np.random.randn(3)*1e-4    
    logging.info(f"Weights before training :-\n{self.weights}")
    #assigning the learning rates 
    self.eta=eta
    #no of iterations 
    self.epochs=epochs
  def activationFunction(self,inputs,weights):
    #z=w*x
    z=np.dot(inputs,weights)
    # this is the base conditon of the funxtion if z>0 we return 1 else we return 0
    return np.where(z>0,1,0)
  def fit(self,X,y):
    self.X=X
    self.y=y
    # here we need to concatenate the x and y values with -1
    X_with_bias=np.c_[self.X,-np.ones((len(self.X),1))]
    logging.info(f"X with bias is :--\n{X_with_bias}")
    for epoch in tqdm(range(self.epochs),total=self.epochs,desc="training the model"):
      print("--"*10)
      print(f"for epoch:{epoch}")
      print("--"*10)
      #forward bias 
      y_hat=self.activationFunction(X_with_bias,self.weights)
      logging.info(f"Predicted value after the forward pass :--\n{y_hat}")
      self.error= self.y-y_hat
      #this would calcuate the error
      logging.info(f"Error :--{self.error}")
      #backward propagation
      self.weights=self.weights+self.eta*np.dot(X_with_bias.T,self.error)
      logging.info(f"Calculated weights after each epoch :-- \n {epoch}/{self.epochs}:\n{self.weights}")
      logging.info("#####"*10)  
  def predict(self, X):
    X_with_bias = np.c_[X,-np.ones((len(X),1))]
    return self.activationFunction(X_with_bias, self.weights)
  def loss(self):
    total_loss=np.sum(self.error)
    #total loss is siply the sum of all the losses in the epochs 
    print(f"Total loss:--\n {total_loss}")
    return total_loss  
    # using f string we dont have to convert it into string


    