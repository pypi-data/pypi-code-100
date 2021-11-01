import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ..metrics import *
from ..plots import *
from ..plots.express import *
from ..client.Session import TrojSession
import plotly.express as px
#import htmlmin

#TODO more plots
adver_plot_funcs = [SecurityCurveClassification, ClasswiseSecurityCurve, PertLossCorrelationClassification]
adver_plot_funcs_kwargs = [{}, {}, {}]
#Not clever, but works
def EZAdversarialClassification(df, session, plot_func_list = adver_plot_funcs,
                                plot_func_kwargs_list = adver_plot_funcs_kwargs):
    '''
    Makes basic plots for adversarial attacks on classifiers.
    :param df: Dataframe
    :param session: Troj session object.
    '''
    for idx in range(len(plot_func_list)):
        plot_func = plot_func_list[idx]
        plot_func_kwargs = plot_func_kwargs_list[idx]
        html_str = GraphMakerBase(plot_func, df, **plot_func_kwargs)
        #html_str = htmlmin.minify(html_str, remove_comments=True, remove_empty_space=True)
        session.log_graph(html_str)



def EZAdversarialObjectDetection(df, session, id_dictionary, model_name='model'):
    '''
    Makes basic plots for adversarial attacks on object detectors.
    :param df: Dataframe
    :param session: Troj session object.
    :param id_dictionary: A dictionary containing for each class the correspondence {class_id:class_name}.
    :param model_name: Name of model to be put in the displayed table.
    '''
    map_05, gt_df, preds_df, class_ap = mAP(df)
    adv_map_05, adv_gt_df, adv_preds_df, class_ap_adv = mAP(df, adversarial=True)
    od_adver_plot_funcs = [ODAdversarialTable, ODClassPrecisionGraph,ODClassRecallGraph,ODClassF1Graph, ODClassAPGraph]
    od_adver_plot_funcs_kwargs = [{'mean_ap':map_05, 'adv_mean_ap':adv_map_05, 'class_avp':class_ap, 'adv_class_avp':class_ap_adv, 'id_dictionary':id_dictionary, 'model_name':model_name},
                                  {'predictions_df':preds_df, 'adv_predictions_df':adv_preds_df, 'id_dictionary':id_dictionary},
                                  {'ground_truth_df':gt_df ,'predictions_df':preds_df, 'adv_predictions_df':adv_preds_df,
                                   'id_dictionary':id_dictionary}, {'ground_truth_df':gt_df ,'predictions_df':preds_df, 'adv_predictions_df':adv_preds_df,
                                   'id_dictionary':id_dictionary}, {'class_ap':class_ap, 'adv_class_ap':class_ap_adv, 'id_dictionary':id_dictionary}]


    for idx in range(len(od_adver_plot_funcs )):
        plot_func = od_adver_plot_funcs [idx]
        plot_func_kwargs = od_adver_plot_funcs_kwargs [idx]
        html_str = GraphMakerBase(plot_func, df, **plot_func_kwargs)
        #html_str = htmlmin.minify(html_str, remove_comments=True, remove_empty_space=True)
        session.log_graph(html_str)

def EZClassificationCorruptions(df, session):
    '''
    Makes basic plots for evluating the performance of classification models against different corruptions.
    :param df: Dataframe.
    :param session: Troj session.
    '''
    corrupt_plot_funcs = [MakeCorruptionsTable, Loss_ecdf, CorruptionAccuracyGraph, CorruptionRecallGraph, CorruptionPrecisionGraph,
                          CorruptionF1Graph]
    corrupt_plot_func_kwargs = [{}, {}, {}, {}, {}, {}]
    for idx in range(len(corrupt_plot_funcs)):
        plot_func = corrupt_plot_funcs[idx]
        plot_func_kwargs = corrupt_plot_func_kwargs[idx]
        html_str = GraphMakerBase(plot_func, df, **plot_func_kwargs)
        #html_str = htmlmin.minify(html_str, remove_comments=True, remove_empty_space=True)
        session.log_graph(html_str)
