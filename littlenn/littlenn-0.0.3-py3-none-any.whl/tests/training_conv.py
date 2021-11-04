from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from littlenn.layers import Conv2D, Flatten, Dense
from littlenn.model import Sequential

digits = load_digits()

n_samples = len(digits.images)

data = digits.images.reshape((n_samples, 8, 8, 1))
target = (digits.target == 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    data, target, test_size=0.5, shuffle=False)

model = Sequential(input_size=(1, 8, 8))

conv1 = Conv2D(channels_out=16, kernel_size=(3, 3),
                padding=(0, 0), strides=(1, 1),
                activation='relu')

conv2 = Conv2D(channels_out=32, kernel_size=(3, 3),
                padding=(0, 0), strides=(1, 1),
                activation='relu')

flat = Flatten()

dense1 = Dense(64, activation='relu')
dense2 = Dense(1, activation='sigmoid')

model.add(conv1)
model.add(conv2)
model.add(flat)
model.add(dense1)
model.add(dense2)

model.compile(loss='binary_crossentropy',
              optimizer_params={"name" : "rmsprop", "lr" : 1e-2, "ew" : .99})

model.summary()

model.fit(data, target, epochs=10, batch_size=16)