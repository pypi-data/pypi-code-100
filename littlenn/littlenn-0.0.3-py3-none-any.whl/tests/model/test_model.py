import unittest
from littlenn.model import Sequential
from littlenn.layers import Dense, Dropout

model = Sequential(input_size=100, optimizer_params={"name" : "sgd", "lr" : 1e-5, "ew" : 0.9})
model.add(Dense(256, "relu"))
model.add(Dropout(0.8))
model.add(Dense(128, "relu"))

model.summary()