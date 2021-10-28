from imblearn.over_sampling import SMOTE
from scipy.stats import sem
import numpy as np


def cv(x, y, model, metric, splitter,
       iters=20, probability=False, over=False, full=False, lower_bound=False):
    
    metric_list = []
    for i in range(iters):
        x_train, x_test, y_train, y_test = splitter(x, y)
        
        if over:
            oversample = SMOTE(n_jobs=-1)
            x_train, y_train = oversample.fit_resample(x_train, y_train)
            
        model.fit(x_train, y_train)
        predictions = model.predict_proba(x_test)[:, 1] if probability else model.predict(x_test)
        
        score = metric(y_test, predictions)
        metric_list.append(score)
    
    if full:
        return metric_list
    
    elif lower_bound:
        return np.mean(metric_list) - 1.96*sem(metric_list)
    
    else:
        return np.mean(metric_list)