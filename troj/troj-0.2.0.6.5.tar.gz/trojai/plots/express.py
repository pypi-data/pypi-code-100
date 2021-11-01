import pandas as pd
import numpy as np
import plotly.graph_objects as go

import plotly.express as px
from ..plots import *
from ..data import *
from ..metrics import *
from ..metrics.metric_utils import *
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from collections import defaultdict

#TODO document

def SecurityCurveClassification(df, thresholds = None, classwise = False):
    '''
    Generates the security curve for a given class, or the average curve over all classes.
    :param df: dataframe.
    :param thresholds: Thresholds for calculating security curve. If None, all unique $L^\infty$ values in the dataframe are used.
    :param classwise: Whether or not we are using the function for classwise security curve or not.
    :return: Plotly figure.
    '''
    if thresholds is None:
        thresholds = sorted(df['Linf_perts'].unique().tolist())
    thresholds, accs = GetSCData(df, thresholds)
    if classwise:
        class_name = df['class_name'].unique().tolist()

        fig = go.Scatter(x=thresholds, y=accs,
                        mode='lines',
                        name=class_name[0])
    else:
        plot_data = {'Minimum Perturbation':thresholds, 'Accuracy at Perturbation Amount':accs}
        fig = px.line(plot_data, x="Minimum Perturbation", y="Accuracy at Perturbation Amount", title='Security Curve')
    return fig



def PertLossCorrelationClassification(df, thresholds=None):
    '''
    Generates a curve showing the correlation between the loss and the perturbation amount.
    :param df: Dataframe
    :param thresholds: $L^\infty$ Thresholds for calculating the perturbation-loss correlation curve. If None, all unique $L^\infty$ values in the dataframe are used.
    :return: plotly figure.
    '''
    if thresholds is None:
        thresholds = sorted(df['Linf_perts'].unique().tolist())
    thresholds, accs = GetLossPertCorrelationData(df, thresholds)
    plot_data = {'Minimum Perturbation': thresholds, 'Average Loss for Samples Requiring x Perturbation': accs}
    fig = px.line(plot_data, x="Minimum Perturbation",
                  y="Average Loss for Samples Requiring x Perturbation", title='Perturbation-Loss Curve')
    return fig


def ClasswiseSecurityCurve(df):
    '''
    Generates the classwise security curve.
    :param df: dataframe.
    :return: A plotly figure.
    '''
    lt = plotly.graph_objects.Layout(title='Classwise Security Curve',  xaxis_title="Minimum Perturbation",
        yaxis_title="Accuracy at Perturbation Amount")
    curve = ClasswisePlots(df, SecurityCurveClassification, go_kwargs={'layout':lt}, callback_kwargs={'classwise':True})
    return curve

def ODNormalizedFNGraph(df, ground_truth_df, predictions_df, adv_predictions_df, id_dictionary):
    '''
    A bar chart displaying the false negatives per class, normalized between [0,1] (normal and adversarial).
    :param df: Dataframe
    :param ground_truth_df: Dataframe containing the ground truth objects (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param predictions_df: Dataframe containing the predicted objects (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param adv_predictions_df: Dataframe containing the predicted objects under adversarial perturbations
     (can be obtained by computing the mAP score using trojai.metrics.mAP after the adversarial evaluation by setting the adversarial argument in the mAP function to True).
    :param id_dictionary: A dictionary containing for each class the correspondence {class_id:class_name}.
    :return: A plotly figure.
    '''
    false_n = GetFalseNegatives(ground_truth_df, predictions_df)
    label_occurance_counts = ground_truth_df['label_id'].value_counts()
    loc_dict = SwapKeys(label_occurance_counts.to_dict(), id_dictionary)
    false_negs_counts = false_n['label_id'].value_counts()
    fnc_dict = SwapKeys(false_negs_counts.to_dict(), id_dictionary)
    adv_false_n = GetFalseNegatives(ground_truth_df, adv_predictions_df)
    adv_false_negs_counts = adv_false_n['label_id'].value_counts()
    adv_fnc_dict = SwapKeys(adv_false_negs_counts.to_dict(), id_dictionary)
    adv_normed = sort_dict(normalize_dicts(adv_fnc_dict, loc_dict))
    plot_data = []
    plot_data.append(go.Bar(x=list(normed.keys()), y=list(normed.values()), name="Normal"))
    plot_data.append(go.Bar(x=list(adv_normed.keys()), y=list(adv_normed.values()), name="Adversarial"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Normalized False Negative Counts By Class"))
    )
    return fig



def ODClassPrecisionGraph(df, predictions_df, adv_predictions_df, id_dictionary):
    '''
    Makes a barchart displaying the classwise precision (normal and adversarial).
    :param df: Dataframe.
    :param predictions_df: Dataframe containing the predicted objects (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param adv_predictions_df: Dataframe containing the predicted objects under adversarial perturbations
     (can be obtained by computing the mAP score using trojai.metrics.mAP after the adversarial evaluation by setting the adversarial argument in the mAP function to True).
    :param id_dictionary: A dictionary containing for each class the correspondence {class_id:class_name}.
    :return: A plotly figure.
    '''
    class_prec = ClasswisePrecision(predictions_df, id_dictionary)
    adv_class_prec = ClasswisePrecision(adv_predictions_df, id_dictionary)
    plot_data = []
    plot_data.append(go.Bar(x=list(class_prec.keys()), y=list(class_prec.values()), name="Normal Precision"))
    plot_data.append(go.Bar(x=list(adv_class_prec.keys()), y=list(adv_class_prec.values()), name="Adversarial Precision"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Classwise Precision"))
    )
    return fig

#TODO move to metrics


def ODClassRecallGraph(df, ground_truth_df, predictions_df, adv_predictions_df, id_dictionary):
    '''
    Makes a barchart for the classwise recall (normal and adversarial).
    :param df: Dataframe.
    :param ground_truth_df: Dataframe containing the ground truth objects (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param predictions_df:  Dataframe containing the predicted objects (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param adv_predictions_df: Dataframe containing the predicted objects under adversarial perturbations.
    :param id_dictionary: id_dictionary: A dictionary containing for each class the correspondence {class_id:class_name}.
    :return: a plotly figure.
    '''
    class_rec = ClasswiseRecall(ground_truth_df, predictions_df, id_dictionary)
    adv_class_rec = ClasswiseRecall(ground_truth_df, adv_predictions_df, id_dictionary)
    plot_data = []
    plot_data.append(go.Bar(x=list(class_rec.keys()), y=list(class_rec.values()), name="Normal Recall"))
    plot_data.append(go.Bar(x=list(adv_class_rec.keys()), y=list(adv_class_rec.values()), name="Adversarial Recall"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Classwise Recall"))
    )
    return fig


def ODClassF1Graph(df, ground_truth_df, predictions_df, adv_predictions_df, id_dictionary):
    '''
    Makes a barchart for the classwise F1 (normal and adversarial).
    :param df: Dataframe.
    :param ground_truth_df: Dataframe containing the ground truth objects (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param predictions_df:  Dataframe containing the predicted objects (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param adv_predictions_df: Dataframe containing the predicted objects under adversarial perturbations.
    :param id_dictionary: id_dictionary: A dictionary containing for each class the correspondence {class_id:class_name}.
    :return: a plotly figure.
    '''
    class_f1 = ClasswiseF1(ground_truth_df, predictions_df, id_dictionary)
    adv_class_f1 = ClasswiseF1(ground_truth_df, adv_predictions_df, id_dictionary)
    plot_data = []
    plot_data.append(go.Bar(x=list(class_f1.keys()), y=list(class_f1.values()), name="Normal F1"))
    plot_data.append(go.Bar(x=list(adv_class_f1.keys()), y=list(adv_class_f1.values()), name="Adversarial F1"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Classwise F1"))
    )
    return fig

def ODClassAPGraph(df, class_ap, adv_class_ap, id_dictionary):
    '''
    Makes a barchart for the classwise average precision (normal and adversarial).
    :param df: Dataframe
    :param class_ap: The average precision dictionary (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param adv_class_ap: The adversarial average precision dictionary (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param id_dictionary: A dictionary containing for each class the correspondence {class_id:class_name}.
    :return: a plotly figure.
    '''
    class_ap = SwapKeys(class_ap, id_dictionary)
    adv_class_ap = SwapKeys(adv_class_ap, id_dictionary)

    plot_data = []
    plot_data.append(go.Bar(x=list(class_ap.keys()), y=list(class_ap.values()), name="Normal AP"))
    plot_data.append(go.Bar(x=list(adv_class_ap.keys()), y=list(adv_class_ap.values()), name="Adversarial AP"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Classwise AP"))
    )
    return fig


def MakeTableFigure(row_names, column_names, vals):
    '''
    Makes a table which can be displayed as a plotly figure goven the appropraie inputs. For example, this function would normally take in data like

    fake_rows = ['row_1', 'row_2']
    fake_columns = [['column_1'], ['column_2'], ['column_3'], ['column_3']]
    fake_values = [[1,2], [3,4], [5,6]]

    :param row_names: list of names of the rows in the table.
    :param column_names: A list containing the names of columns (each must be contained itself in a list)
    :param vals: The values for the table given as a list where each entry in the list is itself a list containing the values
    for each row.
    :return: A plotly figure.
    '''
    header_dict = dict(
        values=column_names,
        line_color='darkslategray',
        fill_color='royalblue',
        align=['left', 'center'],
        font=dict(color='black', size=15),
        height=40)

    row_data = vals.insert(0, row_names)

    cell_data = dict(
        values=vals,
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        align=['left', 'center'],
        font_size=12,
        height=30)

    plot_data = [go.Table(
        header=header_dict,
        cells=cell_data)]

    fig = go.Figure(plot_data)
    return fig


def ODAdversarialTable(df, mean_ap, adv_mean_ap, class_avp, adv_class_avp, id_dictionary, model_name='model'):
    '''
    Generates a table from data obtained via the adversarial evaluation for object detection.
    :param df: Dataframe
    :param mean_ap: Mean average precision score (at 0.5).
    :param adv_mean_ap: Adversarial mean average precision (at 0.5).
    :param class_avp: The average precision dictionary (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param adv_class_avp: The adversarial average precision dictionary (can be obtained by computing the mAP score using trojai.metrics.mAP).
    :param id_dictionary:  A dictionary containing for each class the correspondence {class_id:class_name}.
    :param model_name: Name of the model to be displayed in the table.
    :return: A plotly figure.
    '''
    stats_dict = APStats(class_avp, id_dictionary, adv_class_avp)
    stats_dict['mAP@0.5'] = round(mean_ap, 2)
    stats_dict['Adversarial mAP@0.5'] = round(adv_mean_ap,2)
    column_names = list(stats_dict.keys())
    column_names.insert(0, 'Model Name')
    row_name = [model_name]
    values = list(stats_dict.values())
    fig = MakeTableFigure(row_name, column_names, values)
    return fig

def CorruptionAccuracyGraph(df):
    '''
    Makes a barchart for the different corruption accuracy scores.
    :param df: Dataframe.
    :return: A barchart displaying the accuracy on different corruptions.
    '''
    corrupt_acc_dict, diff_dict, clean = PerCorruptionMetric(df, accuracy_score)
    corrupt_acc_dict['none'] = clean
    plot_data = []
    plot_data.append(go.Bar(x=list(corrupt_acc_dict.keys()), y=list(corrupt_acc_dict.values()), name="Accuracy per Corruption"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Accuracy per Corruption"))
    )
    return fig

def CorruptionRecallGraph(df):
    '''
    Makes a barchart for the different corruption recalls.
    :param df: Dataframe.
    :return: A barchart displaying the recall on different corruptions.
    '''
    corrupt_acc_dict, diff_dict, clean = PerCorruptionMetric(df, recall_score,  **{'average':'macro'})
    corrupt_acc_dict['none'] = clean
    plot_data = []
    plot_data.append(go.Bar(x=list(corrupt_acc_dict.keys()), y=list(corrupt_acc_dict.values()), name="Recall per Corruption"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Recall per Corruption"))
    )
    return fig


def CorruptionPrecisionGraph(df):
    '''
    Makes a barchart for the different corruption precisions.
    :param df: Dataframe.
    :return: A barchart displaying the precision on different corruptions.
    '''
    corrupt_acc_dict, diff_dict, clean = PerCorruptionMetric(df, precision_score,  **{'average':'macro'})
    corrupt_acc_dict['none'] = clean
    plot_data = []
    plot_data.append(go.Bar(x=list(corrupt_acc_dict.keys()), y=list(corrupt_acc_dict.values()), name="Precision per Corruption"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="Precision per Corruption"))
    )
    return fig



def CorruptionF1Graph(df):
    '''
    Makes a barchart for the different corruption F1 scores.
    :param df: Dataframe.
    :return: A barchart displaying the F1 scors on different corruptions.
    '''
    corrupt_acc_dict, diff_dict, clean = PerCorruptionMetric(df, f1_score,  **{'average':'macro'})
    corrupt_acc_dict['none'] = clean
    plot_data = []
    plot_data.append(go.Bar(x=list(corrupt_acc_dict.keys()), y=list(corrupt_acc_dict.values()), name="F1 per Corruption"))
    fig = go.Figure(
        data=plot_data,
        layout=dict(title=dict(text="F1 per Corruption"))
    )
    return fig

def Loss_ecdf(df):
    '''
    Generates the empirical cumulative distribution of the loss for each corruption.
    :param df: Dataframe
    :return: The loss eCDF.
    '''
    fig = px.ecdf(df, x="Loss", color="corruption_type", title='Empirical Cumulative Distribution of the Loss for Each Corruption')
    return fig


def MakeCorruptionsTable(df):
    '''
    Makes a table containing information about performance on different corruptions.
    :param df: Dataframe.
    :return: Table of information.
    '''
    corruptions = df['corruption_type'].unique()
    column_names = [['Corruption'], ['Loss'], ['Accuracy'], ['Precision'], ['Recall'], ['F1']]
    stats_dict = defaultdict(list)
    for corrupt in corruptions:
        corrupt_df = df[df['corruption_type'] == corrupt]
        loss_str = '{}+/-{}'
        loss_mean, loss_std = ColumnMeanStd(corrupt_df, 'Loss')
        stats_dict['Loss'].append(loss_str.format(loss_mean, loss_std))
        stats_dict['Accuracy'].append(round(ComputeMetric(corrupt_df, accuracy_score), 3))
        stats_dict['Precision'].append(round(ComputeMetric(corrupt_df, precision_score, **{'average': 'macro'}), 3))
        stats_dict['Recall'].append(round(ComputeMetric(corrupt_df, recall_score, **{'average': 'macro'}), 3))
        stats_dict['F1'].append(round(ComputeMetric(corrupt_df, f1_score, **{'average': 'macro'}), 3))
    vals = list(stats_dict.values())
    fig = MakeTableFigure(corruptions, column_names, vals)
    return fig
