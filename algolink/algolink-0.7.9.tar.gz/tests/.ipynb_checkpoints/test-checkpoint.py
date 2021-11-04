from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression

X, y = load_diabetes(True)

lr = LinearRegression()
lr.fit(X, y)
import algolink
model = algolink.create_model(lr, X, model_name='diabetes_model_11')
model
