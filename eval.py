import sys

import pandas as pd
import numpy as np


# https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/average_precision.py
def apk(actual, predicted, k=10):
    """
    Computes the average precision at k.

    This function computes the average prescision at k between two lists of
    items.

    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The average precision at k over the input lists

    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 0.0

    return score / min(len(actual), k)


def mapk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.

    This function computes the mean average prescision at k between two lists
    of lists of items.

    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The mean average precision at k over the input lists

    """
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])


def eval(true_csv, pred_csv):
    true_df = pd.read_csv(true_csv)
    pred_df = pd.read_csv(pred_csv).sort_values('topic')

    print(true_df)
    print(pred_df)

    true_doc = [list(np.array(e.split(), np.int64)) for e in true_df['doc'].to_list()]
    pred_doc = [list(np.array(e.split(), np.int64)) for e in pred_df['doc'].to_list()]

    score = mapk(true_doc, pred_doc, k=50)
    print(f'mapk score: {score:.4f}')


if __name__ == '__main__':
    eval(sys.argv[1], sys.argv[2])

