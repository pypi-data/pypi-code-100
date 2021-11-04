from littlenn.model import Sequential
from littlenn.layers import Dense, Dropout, BatchNorm
import numpy as np
from sklearn.datasets import make_classification

X, y = make_classification(1000, 30, random_state=42)

X /= np.max(X)
N = X.shape[1]
T = int(X.shape[0] * 0.95)

model = Sequential(input_size=N)

model.add(Dense(128, activation='relu'))
model.add(BatchNorm(activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dropout(keep_prob=0.9))
model.add(Dense(64, activation='relu'))
model.add(BatchNorm())
model.add(Dense(32, activation='relu'))
model.add(Dropout(keep_prob=0.9))
model.add(Dense(1, activation='sigmoid'))

X, y = X.reshape(X.shape[0], N), y.reshape(X.shape[0], 1)

X_val, y_val = X[T:].T, y[T:].T
X, y = X[:T], y[:T]

epochs = 500
batch_size = 50

model.compile(loss='binary_crossentropy',
              optimizer_params={"name" : "rmsprop", "lr" : 1e-3, "ew" : .99})

model.fit(X, y, epochs=epochs, batch_size=batch_size)