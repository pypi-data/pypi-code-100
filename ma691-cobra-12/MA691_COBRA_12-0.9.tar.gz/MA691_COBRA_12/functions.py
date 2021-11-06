from sklearn.datasets import load_boston
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import warnings

warnings.filterwarnings('ignore', category = DeprecationWarning)
from warnings import filterwarnings
filterwarnings('ignore')

def lasso(X_b,y_b):
    
    """
    There are 14 attributes in each case of the dataset.It has two prototasks: nox, in which the nitrous oxide 
    level is to be predicted;and price, in which the median value of a home is to be predicted.
    """
#     df_b = load_boston()
#     data_b = pd.DataFrame(df_b.data,columns = df_b.feature_names)
#     data_b['PRICE'] = df_b.target
#     X_b = data_b.drop('PRICE',axis = 1)
#     y_b = data_b['PRICE']
    X_train,X_test,y_train,y_test = train_test_split(X_b,y_b,test_size = 0.2,random_state = 129)
    #Lasso Regression
    from sklearn.linear_model import Lasso
    from sklearn.model_selection import GridSearchCV
    lasso=Lasso()
    parameters={'alpha':[1e-20,1e-15,1e-10,1e-8,1e-3,1e-2,1,5,10,20,30,35,40,45,50,55,100]}
    lasso_regressor=GridSearchCV(lasso,parameters,scoring='neg_mean_squared_error',cv=5)

    lasso_regressor.fit(X_train,y_train)
    # Let's check out the best parameter and best score
    print("best parameters:\n\n")
    print(lasso_regressor.best_params_)
    print(lasso_regressor.best_score_)
    prediction_lasso=lasso_regressor.predict(X_test)
    # Prediction
    y_pred_train_lasso1 = lasso_regressor.predict(X_train)
    y_pred_test_lasso1 = lasso_regressor.predict(X_test)
    print('Training accuracy : {}\n'.format(r2_score(y_train, y_pred_train_lasso1).round(5)))
    print('Testing accuracy : {}'.format(r2_score(y_test, y_pred_test_lasso1).round(5)))

    mse1 = cross_val_score(lasso_regressor, X_b, y_b, scoring = 'neg_mean_squared_error',cv=5)
    mean_mse1 = np.mean(mse1)
    print("\nmean square error: ",-(mean_mse1).round(5))
    print("\n")

    import seaborn as sns
    sns.distplot(y_test-prediction_lasso)
    X=[]
    rng=int(max(y_b))+50
    for i in range(1,rng):
        X.append(i)
    X=np.array(X)
    plt.scatter(prediction_lasso,y_test)
    plt.xlabel("predicted")
    plt.ylabel("y_test")
    plt.plot(X,X,color="red")
    
def ridge(X_b,y_b):
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import GridSearchCV
    X_train,X_test,y_train,y_test = train_test_split(X_b,y_b,test_size = 0.2,random_state = 129)
    ridge=Ridge()
    parameters={'alpha':[1e-25,1e-20,1e-15,1e-10,1e-8,1e-3,1e-2,1,5,10,20,30,35,40,45,50,55,100]}
    ridge_regressor=GridSearchCV(ridge,parameters,scoring='neg_mean_squared_error',cv=5)
    ridge_regressor.fit(X_train,y_train)
    #checking out the best parameter and the score
    print("best parameter and the score:\n")
    print(ridge_regressor.best_params_)
    print(ridge_regressor.best_score_)
    print("\n")
    prediction_ridge=ridge_regressor.predict(X_test)
    # Prediction

    y_pred_train_ridge1 = ridge_regressor.predict(X_train)
    y_pred_test_ridge1 = ridge_regressor.predict(X_test)
    print('Training accuracy : {}\n'.format(r2_score(y_train, y_pred_train_ridge1).round(5)))
    print('Testing accuracy : {}'.format(r2_score(y_test, y_pred_test_ridge1).round(5)))

    mse1 = cross_val_score(ridge_regressor, X_b, y_b, scoring = 'neg_mean_squared_error',cv=5)
    mean_mse1 = np.mean(mse1)
    print("\nmean square error: ",-(mean_mse1).round(5))
    print("\n")

    import seaborn as sns
    sns.distplot(y_test-prediction_ridge)

    X=[]
    rng=int(max(y_b))+50
    for i in range(1,rng):
        X.append(i)
    X=np.array(X)
    plt.scatter(prediction_ridge,y_test)
    plt.xlabel("predicted")
    plt.ylabel("y_test")
    plt.plot(X,X,color="red")
    
def knn(X_b,y_b):
    X_train, X_test, Y_train, Y_test = train_test_split(X_b, y_b, test_size = 0.20, random_state = 0)
    from sklearn.neighbors import KNeighborsRegressor
    import seaborn as sns
    knr = KNeighborsRegressor(n_neighbors=1)
    knr.fit(X_train, Y_train)

    Y_pred = knr.predict(X_test) # Prediction


    y_pred_train_knn1 = knr.predict(X_train)
    y_pred_test_knn1 = knr.predict(X_test)
    print('Training accuracy : {}\n'.format(r2_score(Y_train, y_pred_train_knn1).round(5)))
    print('Testing accuracy : {}\n'.format(r2_score(Y_test, y_pred_test_knn1).round(5)))

    mse1 = cross_val_score(knr, X_b, y_b, scoring = 'neg_mean_squared_error',cv=5)
    mean_mse1 = np.mean(mse1)
    print("\nmean square error(cross validation score): ",-(mean_mse1).round(5))
    print("\n")

    # Create Dataset with Testing values and Predicted Prices
    print("KNN Regresson Model")
    model_knn = pd.DataFrame(X_test)
    model_knn['MEDV'] = Y_test
    model_knn['Predicted MEDV'] = Y_pred
    print(model_knn.head(10))
    print("\n\n")

    # Measure Performance of the Model
    # Get Mean Squared Error (MSE)
    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(Y_test, Y_pred)
    # Get Mean Absolute Error (MAE)
    from sklearn.metrics import mean_absolute_error
    mae = mean_absolute_error(Y_test, Y_pred)

    err = "MSE(mean square error): " + str(round(mse, 2)) + "," + " MAE(mean absolute error): " + str(round(mae, 2))
    print("KNN Regresson Model Performance:-- ", err,"\n\n")

    # Create Regression Plot for Test and Prediction values
    fig = plt.figure(figsize=(12,9))
    ax = sns.regplot(Y_test, Y_pred, marker = 'o', color = 'red')
    ax.set_title('KNN Regression', fontsize=20)
    ax.set_xlabel('MEDV or Price', fontsize=20)
    ax.set_ylabel('Predicted Prices', fontsize=20)
    # Save the KNN Regrassion Plot along with Error value
    plt.text(35.0, 10.0, err, fontsize=20, bbox=dict(facecolor='yellow', alpha=0.5))
    plt.savefig("KNNRegression.png", dpi=70)
    plt.show()
    plt.close(fig)

    X=[]
    rng=int(max(y_b))+50
    for i in range(1,rng):
        X.append(i)
    X=np.array(X)
    plt.scatter(Y_pred,Y_test)
    plt.xlabel("predicted")
    plt.ylabel("y_test")
    plt.plot(X,X,color="red")
    
def mlr(X,Y):
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import load_boston
    from sklearn.metrics import mean_squared_error, r2_score
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state=9)
    from sklearn.linear_model import LinearRegression
    lin_reg_mod = LinearRegression()
    lin_reg_mod.fit(X_train, y_train)
    pred = lin_reg_mod.predict(X_test)

    y_pred_train_mlr1 = lin_reg_mod.predict(X_train)
    y_pred_test_mlr1 = lin_reg_mod.predict(X_test)


    print("MLR Model")
    model_mlr = pd.DataFrame(X_test)
    model_mlr['MEDV'] = y_test
    model_mlr['Predicted MEDV'] = pred
    print(model_mlr.head(10))
    print("\n\n")

    print('Training accuracy : {}\n'.format(r2_score(y_train, y_pred_train_mlr1).round(5)))
    print('Testing accuracy : {}'.format(r2_score(y_test, y_pred_test_mlr1).round(5)))
    print("\n")
    test_set_rmse = (np.sqrt(mean_squared_error(y_test, pred)))
    test_set_r2 = r2_score(y_test, pred)

    print("RMSE: ",test_set_rmse)
    print("r2 score: ",test_set_r2)
    X=[]
    rng=int(max(Y))+50
    for i in range(1,rng):
        X.append(i)
    X=np.array(X)
    plt.scatter(pred,y_test)
    plt.xlabel("predicted")
    plt.ylabel("y_test")
    plt.plot(X,X,color="red")
    
def kernel_cobra(boston):
    from sklearn import datasets
    from sklearn.metrics import accuracy_score
    from kernelcobra import KernelCobra
    #from sklearn.datasets.samples_generator import make_regression
    #boston = datasets.load_boston()

    # boston_X_train = boston.data[:-40]
    # boston_X_test = boston.data[-40:]

    # boston_y_train = boston.target[:-40]
    # boston_y_test = boston.target[-40:]

    #boston_X_train, boston_X_test, boston_y_train, boston_y_test = train_test_split(X, Y, test_size = 0.2, random_state=9)
    boston_X_train = boston.data[:300]
    boston_X_test = boston.data[300:]

    boston_y_train = boston.target[:300]
    boston_y_test = boston.target[300:]

    from pycobra.cobra import Cobra
    from pycobra.kernelcobra import KernelCobra

    from pycobra.ewa import Ewa
    from pycobra.diagnostics import Diagnostics
    from pycobra.visualisation import Visualisation
    import numpy as np

    

    boston_kernelcobra = KernelCobra()
    boston_kernelcobra.fit(boston_X_train, boston_y_train)

    kernel = KernelCobra()

    kernel.fit(boston_X_train, boston_y_train)
    kernel.predict(boston_X_test)

    y_pred=kernel.predict(boston_X_test)
    import matplotlib.pyplot as plt
    import numpy as np

    X=[]
    rng=int(max(boston_y_test))+50
    for i in range(1,rng):
        X.append(i)
    X=np.array(X)


    from sklearn.metrics import r2_score
    from sklearn.model_selection import cross_val_score, GridSearchCV
    prediction_kernel=kernel.predict(boston_X_test)

    print("kernel cobra Model")
    model_mlr = pd.DataFrame(boston_X_test)
    model_mlr['MEDV'] = boston_y_test
    model_mlr['Predicted MEDV'] = prediction_kernel
    print(model_mlr.head(10))
    print("\n\n")

    # Prediction
    y_pred_train_kernel1 = kernel.predict(boston_X_train)
    y_pred_test_kernel1 = kernel.predict(boston_X_test)
    print('Training accuracy : {}\n'.format(r2_score(boston_y_train, y_pred_train_kernel1).round(5)))
    print('Testing accuracy : {}'.format(r2_score(boston_y_test, y_pred_test_kernel1).round(5)))

    mse1 = cross_val_score(kernel, boston.data, boston.target, scoring = 'neg_mean_squared_error',cv=5)
    mean_mse1 = np.mean(mse1)
    print("\nmean square error: ",-(mean_mse1).round(5))
    print("\n")

    plt.scatter(y_pred,boston_y_test)
    plt.xlabel("predicted")
    plt.ylabel("y_test")
    plt.plot(X,X,color="red")

    

def kernel_cobra_diabetes(X,y):
    from sklearn import datasets
    from sklearn.metrics import accuracy_score
    from kernelcobra import KernelCobra
    #from sklearn.datasets.samples_generator import make_regression
    #boston = datasets.load_boston()

    # boston_X_train = boston.data[:-40]
    # boston_X_test = boston.data[-40:]

    # boston_y_train = boston.target[:-40]
    # boston_y_test = boston.target[-40:]

    nn=len(X)
    nn1=nn/3
    lim=nn=nn1
    boston_X_train = X[:lim]
    boston_X_test = X[lim:]

    boston_y_train = y[:lim]
    boston_y_test = y[lim:]

    from pycobra.cobra import Cobra
    from pycobra.kernelcobra import KernelCobra

    from pycobra.ewa import Ewa
    from pycobra.diagnostics import Diagnostics
    from pycobra.visualisation import Visualisation
    import numpy as np

    

    boston_kernelcobra = KernelCobra()
    boston_kernelcobra.fit(boston_X_train, boston_y_train)

    kernel = KernelCobra()

    kernel.fit(boston_X_train, boston_y_train)
    kernel.predict(boston_X_test)

    y_pred=kernel.predict(boston_X_test)
    import matplotlib.pyplot as plt
    import numpy as np

    X=[]
    rng=int(max(y))+50
    for i in range(1,rng):
        X.append(i)
    X=np.array(X)


    from sklearn.metrics import r2_score
    from sklearn.model_selection import cross_val_score, GridSearchCV
    prediction_kernel=kernel.predict(boston_X_test)

    print("kernel cobra Model")
    model_mlr = pd.DataFrame(boston_X_test)
    model_mlr['MEDV'] = boston_y_test
    model_mlr['Predicted MEDV'] = prediction_kernel
    print(model_mlr.head(10))
    print("\n\n")

    # Prediction
    y_pred_train_kernel1 = kernel.predict(boston_X_train)
    y_pred_test_kernel1 = kernel.predict(boston_X_test)
    print('Training accuracy : {}\n'.format(r2_score(boston_y_train, y_pred_train_kernel1).round(5)))
    print('Testing accuracy : {}'.format(r2_score(boston_y_test, y_pred_test_kernel1).round(5)))

    mse1 = cross_val_score(kernel, boston.data, boston.target, scoring = 'neg_mean_squared_error',cv=5)
    mean_mse1 = np.mean(mse1)
    print("\nmean square error: ",-(mean_mse1).round(5))
    print("\n")

    plt.scatter(y_pred,boston_y_test)
    plt.xlabel("predicted")
    plt.ylabel("y_test")
    plt.plot(X,X,color="red")
