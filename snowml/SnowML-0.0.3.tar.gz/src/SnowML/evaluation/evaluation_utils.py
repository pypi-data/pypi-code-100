import numpy as np


def find_best_threshold(fpr, tpr, thresholds):
    """
    Find best threshold from results of `metrics.roc_curve`.
    Threshold is considered best when it is the closest to (0,0) of the ROC curve.
    :param fpr: np.array / pd.Series of false positive rate values
    :param tpr: np.array / pd.Series of true positive rate values
    :param thresholds: cut off threshold range for predict probabilities
    :return: the best threshold which trying to minimize fpr and maximize tpr
    """

    dist = np.power(fpr, 2) + np.power(tpr - 1, 2)
    return thresholds[dist.argmin()]


def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """
  Pretty print for confusion matrix
  :param cm:
  :param labels:
  :param hide_zeroes:
  :param hide_diagonal:
  :param hide_threshold:
  :return: pretty print for confusion matrix
  """

    colwidth = 6
    empty_cell = " " * colwidth
    # Begin CHANGES
    fst_empty_cell = (colwidth - 3) // 2 * " " + "T\P" + (colwidth - 3) // 2 * " "
    if len(fst_empty_cell) < len(empty_cell):
        fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
    # Print header
    print("    " + fst_empty_cell, end=" ")
    # End CHANGES
    for label in labels:
        print("%{0}s".format(colwidth) % label, end=" ")
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(colwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.0f".format(colwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()