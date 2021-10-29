import pandas as pd
import plotly.express as px
import catboost
from scipy import optimize
import numpy as np
import math
import plotly.graph_objects as go
from sklearn import metrics
from scipy import special


def test_func():
    print("test func worked")


class DemandCurve:
    def __init__(self):
        self.model = None
        self.decision_variable = None
        self.x_observations = None
    
    def fit(self, x, y, monotone_constraints=None, decision_variable=None, **kwargs):
        self.decision_variable = decision_variable
        model = catboost.CatBoostRegressor(monotone_constraints=monotone_constraints, **kwargs)
        self.model = model.fit(x, y, verbose=False)
        self.x_observations = x[decision_variable]
        return model
    
    def s_curve(self, x, max_height, slope, inflection_point, asymmetry):
        return max_height * special.expit(slope * (x-inflection_point)) ** asymmetry
    
    def fit_s_curve(self, price, prd_volume):
        bounds = ([0, -prd_volume.max()/0.01, price.min(), 0],
                  [prd_volume.max(), 0, price.max(), 10])
        p0 = [prd_volume.max(), -0.5, price.median(), 2]
        try:
            popt, _ = optimize.curve_fit(self.s_curve, price, prd_volume, p0=p0, bounds=bounds)
        except:
            print('optimial value not found - using default guess')
            popt = p0
        return popt
    
    def predict_one_row(self, x):
        new_df = pd.DataFrame()
        new_df[self.decision_variable] = self.x_observations
        new_df[x.drop(self.decision_variable).index] = x.drop(self.decision_variable)
        popt = self.fit_s_curve(self.x_observations, self.model.predict(new_df))
        return self.s_curve(x[self.decision_variable], max_height=popt[0], slope=popt[1], inflection_point=popt[2], asymmetry=popt[3])
    
    def predict(self, x):
        return x.apply(self.predict_one_row, axis=1)
