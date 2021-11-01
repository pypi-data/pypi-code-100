import numpy as np
from ..metrics.mAP_utils import MakePredAnnotBoxDataframes, box_ious, ClassAP
from ..metrics.metric_utils import *


def mAP(dataframe, iou_thresh=0.5, adversarial=False):
    '''
    Computes the mean average precision of an object detection algorithm from a dataframe, along with other related objects.
    :param dataframe: Dataframe.
    :param iou_thresh: Threshold to use for the mean average precision.
    :param adversarial: If True, the mean average precision will be computed on the adversarial predictions.
    :return: The mean average precision, and two special dataframes. One referred to as the ground_truth_df whose rows contain
    individual ground truth objects, along with their bounding box and what image they belong to. The other dataframe, called
    predictions_df does a similar thing for the predictions made by the model. We also return a dictionary which contains the average precision per class.
    '''
    ground_truth_df, predictions_df = MakePredAnnotBoxDataframes(dataframe, adversarial)
    ground_truth_df, predictions_df = box_ious(ground_truth_df, predictions_df)
    ap_dict = ClassAP(ground_truth_df, predictions_df)
    return np.mean(list(ap_dict.values())), ground_truth_df, predictions_df, ap_dict


def true_min_pert(labels, preds, original, perturbation, losses, norm=np.inf):
    """
    Finds the smallest perturbation which flips the label. If no perturbation is found, sets the minimum to 0.5 (since
    the image will become entirely grey at such a perturbation).

    :param original_ims: Original inputs
    :param outs_array: Adversarial examples
    :param losses: Adversarial losses
    :param preds: Predictions on Adversarial Examples
    :param norm: the L^p norm to use.
    :return: minimum perturbation, the loss for the perturbation, and the prediction
    """

    tile_list = [original for i in range(perturbation.shape[1])]
    tiled = np.stack(tile_list)
    # swap the first and second axis
    tiled = np.swapaxes(tiled, 0, 1)
    if tiled.shape[1] != 1:
        assert tiled[0, 0, 0, 0, 0] == tiled[0, 1, 0, 0, 0]

    # reshape outputs and original images to collection of vectors
    flattened_shape = (
        perturbation.shape[0],
        perturbation.shape[1],
        perturbation.shape[2] * perturbation.shape[3] * perturbation.shape[4],
    )
    flattened_outs = np.reshape(perturbation, flattened_shape)
    flattened_original = np.reshape(tiled, flattened_shape)

    # subtract the original from the perturbed to get the perturbation vector
    perturbations = flattened_outs - flattened_original
    perturbation_norms = np.linalg.norm(perturbations, norm, axis=2)

    tiled_labels = [labels for i in range(preds.shape[1])]
    tiled_labels = np.stack(tiled_labels)
    # swap the first and second axis
    tiled_labels = np.swapaxes(tiled_labels, 0, 1)
    # If the label isn't flipped, set min pert to 0.5
    perturbation_norms[tiled_labels == np.argmax(preds, axis=2)] = 0.5
    min_per_sample_idx = np.argmin(perturbation_norms, axis=1)

    min_pert_losses = []
    min_pert_preds = []
    min_pert_outs = []
    for idx in range(len(min_per_sample_idx)):
        min_pert_outs.append(perturbation[idx, min_per_sample_idx[idx]])
        min_pert_losses.append(losses[idx, min_per_sample_idx[idx]])
        min_pert_preds.append(preds[idx, min_per_sample_idx[idx]])

    min_pert_outs = np.asarray(min_pert_outs)
    min_pert_preds = np.asarray(min_pert_preds)
    min_pert_losses = np.asarray(min_pert_losses)
    return min_pert_outs, min_pert_preds, min_pert_losses


def ComputeAccuracy(df):
    cor_df = df[df['label'] == df['prediction']]
    accuracy = len(cor_df) / len(df)
    return accuracy

def GetSCData(df, thresholds, mode='classification'):
    '''
    Computes data for generating the security curve.
    :param df: Dataframe
    :param thresholds: Thresholds for computing the curve.
    :param mode:
    :return: The thresholds and accuracy at those thresholds as a list.
    '''
    metrics = []
    cor_df = df[df['label'] == df['prediction']]
    metrics.append(len(cor_df) / len(df))
    if mode == 'classification':
        for thresh in thresholds:
            sub_df = cor_df[cor_df['Linf_perts'] <= thresh]
            metrics.append((len(cor_df) - len(sub_df)) / len(df))
    thresholds.insert(0, 0)
    return thresholds, metrics

def GetLossPertCorrelationData(df, thresholds, mode='classification'):
    '''
    Computes data for generating the Perturbation-loss curve.
    :param df: Dataframe
    :param thresholds: Thresholds for computing the curve.
    :param mode:
    :return: The thresholds and loss at those thresholds as a list.
    '''
    metrics = []
    if mode == 'classification':
        for thresh in thresholds:
            sub_df = df[df['Linf_perts'] <= thresh]
            metrics.append(np.mean(sub_df['Loss'].tolist()))
    return thresholds, metrics



def GetFalseNegatives(ground_truth_df, predictions_df):
    '''
    Finds the false negatives from the results of an object detector.
    :param ground_truth_df: The ground truth dataframe (see trojai.metrics.mAP)
    :param predictions_df: The predictions dataframe (see trojai.metrics.mAP)
    :return: A dataframe containing the false negatives.
    '''
    # gets false negatives
    true_positives = predictions_df[predictions_df['gt_instance_idx'] != -1]
    tp_ids = true_positives['gt_instance_idx'].tolist()
    gt_index_list = ground_truth_df.index.tolist()
    false_negs = diff(gt_index_list, tp_ids)
    fn_df = ground_truth_df.loc[false_negs]
    return fn_df

def ClasswisePrecision(predictions_df, id_dictionary):
    '''
    Computes the classwise precision of the results of an object detector.
    :param predictions_df: The predictions dataframe (see trojai.metrics.mAP)
    :param id_dictionary: A dictionary containing for each class the correspondence {class_id:class_name}.
    :return: a dictionary containing the precision of each class.
    '''
    true_positives = predictions_df[predictions_df['gt_instance_idx']!=-1]
    total_preds_counts = SwapKeys(predictions_df['pred_label_id'].value_counts().to_dict(), id_dictionary)
    tp_counts = SwapKeys(true_positives['pred_label_id'].value_counts().to_dict(), id_dictionary)
    class_prec = sort_dict(normalize_dicts(tp_counts, total_preds_counts))
    return class_prec

def ClasswiseRecall(ground_truth_df, predictions_df, id_dictionary):
    '''
    Computes the recall of the results of an object detector.
    :param ground_truth_df: The ground truth dataframe (see trojai.metrics.mAP).
    :param predictions_df: The predictions dataframe (see trojai.metrics.mAP).
    :param id_dictionary: a dictionary containing the precision of each class.
    :return: Recall of each class.
    '''
    true_positives = predictions_df[predictions_df['gt_instance_idx']!=-1]
    tp_counts = SwapKeys(true_positives['pred_label_id'].value_counts().to_dict(), id_dictionary)
    false_n = GetFalseNegatives(ground_truth_df, predictions_df)
    false_negs_counts = false_n['label_id'].value_counts()
    fnc_dict = SwapKeys(false_negs_counts.to_dict(), id_dictionary)
    denom_dict = add_dicts(tp_counts, fnc_dict)
    recall_dict = normalize_dicts(tp_counts, denom_dict)
    return recall_dict

def ClasswiseF1(ground_truth_df, predictions_df, id_dictionary):
    '''
    Computes F1 scores for object detectors.
    :param ground_truth_df: The ground truth dataframe (see trojai.metrics.mAP).
    :param predictions_df: The predictions dataframe (see trojai.metrics.mAP).
    :param id_dictionary: a dictionary containing the precision of each class.
    :return: F1 score for each class.
    '''
    precisions = ClasswisePrecision(predictions_df, id_dictionary)
    recalls = ClasswiseRecall(ground_truth_df, predictions_df, id_dictionary)
    denom = add_dicts(precisions, recalls)
    nume = multiply_dicts(precisions, recalls)
    normed = normalize_dicts(nume, denom)
    f1 = scalar_mult_dict(2, normed)
    return f1


def APStats(ap_dict, id_dictionary, adv_ap_dict=None):
    '''
    Computes statistics related to the classwise average precision.
    :param ap_dict: Dictionary containing the avereage precisions per class.
    :param id_dictionary: a dictionary containing the precision of each class.
    :param adv_ap_dict: Dictionary containing the adversarial avereage precisions per class.
    :return: A dictionary.
    '''
    stats_dict = {}
    ap_dict = SwapKeys(ap_dict, id_dictionary)
    max_ap_class, max_ap = argmax_dict(ap_dict)
    min_ap_class, min_ap = argmin_dict(ap_dict)
    stats_dict['Highest AP Class'] = max_ap_class
    stats_dict['Lowest AP Class'] = min_ap_class
    stats_dict['Highest AP'] = round(max_ap, 4)
    stats_dict['Lowest AP'] = round(min_ap, 4)
    if adv_ap_dict != None:
        adv_ap_dict = SwapKeys(adv_ap_dict, id_dictionary)
        difference = sub_dicts(ap_dict, adv_ap_dict)
        max_ap_class_adv, max_ap_adv = argmax_dict(adv_ap_dict)
        min_ap_class_adv, min_ap_adv = argmin_dict(adv_ap_dict)
        largest_diff_class, big_diff = argmax_dict(difference)
        smallest_diff_class, small_diff = argmin_dict(difference)
        stats_dict['Highest Adversarial AP Class'] = max_ap_class_adv
        stats_dict['Lowest Adversarial AP Class'] = min_ap_class_adv
        stats_dict['Highest AP'] = round(max_ap_adv, 4)
        stats_dict['Lowest AP'] = round(min_ap_adv, 4)
        stats_dict['Highest Difference Class'] = largest_diff_class
        stats_dict['Lowest Difference Class'] = smallest_diff_class
        stats_dict['Highest Difference'] = round(big_diff, 4)
        stats_dict['Lowest Difference'] = round(small_diff, 4)
    return stats_dict

def ComputeMetric(df, callback, method='predictions', **cb_kwargs):
    '''
    Given a dataframe and a function which takes in one of either (labels, predictions) or (labels, probabilities),
    compute the value of the function on the corresponding dataframe columns.

    :param df: Dataframe
    :param callback: The function to compute.
    :param method: Either 'predictions' or 'probabilities'. If predictions, the hard predictions are passed to the
    callback function. If 'probabilites', it is assumed that the 'pred_probs' column in the dataframe contains logits,
    so we compute the softmax for each row in the 'pred_probs' column, which are the values that are then passed to the callback function.
    :param cb_kwargs: Any extra keyword arguments for the callback.
    :return:
    '''
    #if callback expects class probabilites, set method=probabilites
    labels = df['label'].tolist()
    if method=='predictions':
        preds = df['Preds'].tolist()
    elif method=='probabilities':
        #assumes that pred_probs is logits
        preds = scipy.special.softmax(np.asarray(df['pred_probs'].tolist()), 1)
    outs = callback(labels, preds, **cb_kwargs)
    return outs

def ComputeCorruptionMetricDifference(df, callback, corruption_type=None, severity_level=None, method='predictions', **cb_kwargs):
    '''
    Computes the difference in value of the output of a callback function between corrupted and non-corrupted samples.

    :param df: Dataframe.
    :param callback: The function to be computed.
    :param corruption_type: Corruption type. If None, all corruptions are used.
    :param severity_level: Severity level. If None, value is computed over all severity levels.
    :param method: Either 'predictions' or 'probabilities'. If predictions, the hard predictions are passed to the
    callback function. If 'probabilites', it is assumed that the 'pred_probs' column in the dataframe contains logits,
    so we compute the softmax for each row in the 'pred_probs' column, which are the values that are then passed to the callback function.
    :param cb_kwargs: Keyword arguments to the callback function.
    :return: The score on the clean images, the score on the corrupted images, and the difference between the two.
    '''
    clean_df = df[df['corruption_type']=='none']
    if corruption_type==None:
        corrupt_df = df[df['corruption_type']!='none']
    else:
        corrupt_df = df[df['corruption_type']==corruption_type]
    if severity_level != None:
        corrupt_df = corrupt_df[corrupt_df['severity']==severity_level]
    clean_score = ComputeMetric(clean_df, callback, method=method, **cb_kwargs)
    corrupt_score = ComputeMetric(corrupt_df, callback, method=method, **cb_kwargs)
    diff = clean_score - corrupt_score
    return clean_score, corrupt_score, diff

def PerCorruptionMetric(df, callback, method='predictions', **cb_kwargs):
    '''
    Gets difference in corruption callback per corruption.
    :param df: Dataframe.
    :param callback: The function to be computed.
    :param method: Either 'predictions' or 'probabilities'. If predictions, the hard predictions are passed to the
    callback function. If 'probabilites', it is assumed that the 'pred_probs' column in the dataframe contains logits,
    so we compute the softmax for each row in the 'pred_probs' column, which are the values that are then passed to the callback function.
    :param cb_kwargs: Keyword arguments to the callback function.
    :return: Accuracy on corruptions dictionary, difference dictionary, clean accuracy.
    '''
    #Gets difference in corruption callback per corruption
    corruptions = df[df['corruption_type']!='none']['corruption_type'].unique()
    corr_act_dict = {}
    diff_dict = {}
    for corrupt in corruptions:
        clean, corr, differ = ComputeCorruptionMetricDifference(df, callback, corrupt, method=method, **cb_kwargs)
        corr_act_dict[corrupt] = corr
        diff_dict[corrupt] = differ
    return corr_act_dict, diff_dict, clean