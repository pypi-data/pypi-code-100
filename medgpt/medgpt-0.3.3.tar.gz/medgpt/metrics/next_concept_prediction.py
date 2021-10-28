import numpy as np
import pandas as pd


def precision(predictions, label_ids, id2tkn, token_type2tokens, type_data, select_token_types={'T-11'}, prediction_scope='one', shifted_labels=False,
        predictions_are_scores=True, old_data=None, topk=1, start=0, time_range=None, time_data=None):
    r''' Calculate precision for next concept prediction.

    Args:
        predictions:
            Expected shape <batch_size> x <sequence_length> x <vocabulary_size>
        label_ids:
            Expected shape <batch_size> x <sequence_length>
        token_type2tokens:
            Map from a token type to all tokens belonging to it
        type_data:
            token types for each label/example
        select_token_types (Set[str], optional, defaults to `{'cui'}`:
            On what token types to calculate the Precision. Leave empoty to include all token types.
        prediction_scope:
            How much into the future should we look to accept something as correct:
                - `one` has to be the next concept
                - `age` until the next age token
                - `any` whenever
        shifted_labels:
            Are labels == input_ids, or shifted by one to the left
        predictions_are_scores:
            Are predictions scores for each label_id or really label_ids already
        old_data:
            If set it will load old values for tp/fp/positives/negatives and continue ontop of those
        topk:
            How many predicted labels to consider when calculating precision
        start:
            At what point to start - we will look only at the precision of concepts at positions after start

    Return (Dict[str, ]):
        precision:
            Precision
        tp:
            Number of True positives
        fp:
            Number of False positives
        positives:
            For each label ID a count of positive examples
        negatives
            For each label ID a count of negative examples
    '''
    if predictions_are_scores:
        if type(predictions) == list:
            outputs = [np.argsort(-1 * x, axis=1) for x in predictions]
        else:
            # TODO: do some validation here, as this will let any type of predictions through
            outputs = np.argsort(-1 * predictions, axis=2)
    else:
        outputs = predictions
    tp = {'all': 0, 'new': 0, 'old': 0}
    fp = {'all': 0, 'new': 0, 'old': 0}
    positives = {'all': {}, 'new': {}, 'old': {}}
    negatives = {'all': {}, 'new': {}, 'old': {}}
    numerical_errors = []

    # Are the requested token types or numerical and can a numerical error be calculated
    calculate_numerical_error = all([tkn_type in ['age', 'ttd'] for tkn_type in select_token_types])

    # If not shifted_labels label = prediction - 1
    label_position_shift = 0 if shifted_labels else 1
    # If labels are not shifted move the start by one
    start += 0 if shifted_labels else 1

    if old_data:
        tp = old_data['tp']
        fp = old_data['fp']
        positives = old_data['positives']
        negatives = old_data['negatives']
        numerical_errors = old_data['numerical_errors']

    def prediction_end_index(i, lbl, ind):
        r''' Used below to get the end index for different
        prediction scopes
        '''
        if prediction_scope == 'one':
            return i + 1
        elif prediction_scope == 'any':
            return len(lbl)
        elif prediction_scope == 'age':
            end = len(lbl) # Set end to last token in the labels array (for one example)
            _token_types = type_data[ind]
            for j in range(i, len(lbl)):
                type_label = _token_types[j] if j < len(_token_types) else 'unk'
                if type_label == 'age':
                    end = j
                    break
            return end
        elif prediction_scope == 'sep':
            end = len(lbl) # Set end to last token in the labels array (for one example)
            _token_types = type_data[ind]
            for j in range(i, len(lbl)):
                type_label = _token_types[j] if j < len(_token_types) else 'unk'
                if type_label == 'sep':
                    end = j
                    break
            return end
        elif prediction_scope == 'time_range':
            end = len(lbl) # Set end to last token in the labels array (for one example)
            token_time = time_data[ind]
            for j in range(i, len(lbl)):
                if j < len(token_time): # It can be that time is not available for padding tokens
                    if token_time[j] > (token_time[i] + time_range):
                        end = j
                        break
            return end

    for ind, lbl in enumerate(label_ids):
        _token_types = type_data[ind]
        if start < len(lbl):
            for i in range(start, len(lbl)):
                tkn_label = str(id2tkn.get(lbl[i], lbl[i]))
                type_label = _token_types[i] if i < len(_token_types) else 'unk'
                if type_label in select_token_types:
                    candidates = []
                    select_tokens = token_type2tokens[type_label]
                    if predictions_are_scores:
                        # We only get the type of canidate we know we need at this position
                        for k in range(len(outputs[ind][i-label_position_shift])):
                            if id2tkn[outputs[ind][i-label_position_shift][k]] in select_tokens:
                                candidates.append(outputs[ind][i-label_position_shift][k])

                            if len(candidates) == topk:
                                break
                    else:
                        candidates.append(outputs[ind][i-label_position_shift])

                    is_tp = False
                    is_new = False
                    end = prediction_end_index(i, lbl, ind)
                    for candidate in candidates:
                        # Is it a new concept or an existing one, this only makes sense when there
                        #is just one candidate
                        if candidate not in lbl[0:i]:
                            is_new = True
                        else:
                            is_new = False

                        tkn_candidate = str(id2tkn.get(candidate, candidate))
                        if tkn_candidate in select_tokens:
                            # If predictions are scores we can do topk, if not just do simple label match
                            if candidate in lbl[i:end]:
                                positives['all'][tkn_candidate] = positives['all'].get(tkn_candidate, 0) + 1
                                is_tp = True
                            else:
                                negatives['all'][tkn_candidate] = negatives['all'].get(tkn_candidate, 0) + 1
                        else:
                            negatives['all'][tkn_candidate] = negatives['all'].get(tkn_candidate, 0) + 1
                    if is_tp:
                        tp['all'] += 1

                        temporality = 'new' if is_new else 'old'
                        tp[temporality] += 1
                        positives[temporality][tkn_candidate] = positives[temporality].get(tkn_candidate, 0) + 1
                    else:
                        fp['all'] += 1

                        temporality = 'new' if is_new else 'old'
                        fp[temporality] += 1
                        negatives[temporality][tkn_candidate] = negatives[temporality].get(tkn_candidate, 0) + 1

                    if calculate_numerical_error:
                        # Both have to be of the right type, that is how candidates are setup
                        num_label = int(tkn_label)
                        num_pred = int(tkn_candidate)
                        numerical_error = abs(num_label - num_pred)
                        numerical_errors.append([num_label, num_pred, numerical_error])


    precision = {}
    for temporality in tp.keys():
        if tp[temporality] > 0:
            precision[temporality] = tp[temporality] / (tp[temporality] + fp[temporality])
        else:
            precision[temporality] = 0

    return {
            'precision': precision,
            'tp': tp,
            'fp': fp,
            'positives': positives,
            'negatives': negatives,
            'numerical_errors': numerical_errors,
            }


def metrics_data2df(metrics_data, tkn2name, main='positives', temporality='all'):
    d = metrics_data
    if main == 'positives':
        other = 'negatives'
    else:
        other = 'positives'

    out = sorted([(
        "{:.2f}".format(tp / (tp + d[other][temporality].get(cui, 0))),
        tkn2name.get(cui, cui),
        cui,
        tp,
        d[other][temporality].get(cui, 0),
        cui) for cui, tp in sorted(d[main][temporality].items(), key=lambda x: x[1], reverse=True)],
        key=lambda x: x[0], reverse=True)

    out = pd.DataFrame(out, columns=['precision', 'name', 'cui', main, other, 'cui'])

    return out


class ComputePrecisionHF(object):
    r''' Used for computing precison when working with HF trainer
    '''

    def __init__(self, id2tkn, type_data, token_type2tokens, batch_size=1000, topk=1, return_all_metrics=False, time_range=None, time_data=None, **kwargs):
        self.id2tkn = id2tkn
        self.batch_size = batch_size
        self.kwargs = kwargs
        self.topk = topk
        self.return_all_metrics = return_all_metrics
        self.type_data = type_data
        self.token_type2tokens = token_type2tokens
        self.time_range = time_range
        self.time_data = time_data

    def __call__(self, p):
        # We will do this in batches, because it can be very memory demanding
        metrics_data = None
        start = 0
        while start < len(p.predictions):
            predictions = p.predictions[start:start+self.batch_size]
            label_ids = p.label_ids[start:start+self.batch_size]
            if self.time_data is not None:
                time_data_batch = self.time_data[start:start+self.batch_size]
            else:
                time_data_batch = None
            type_data_batch = self.type_data[start:start+self.batch_size]

            metrics_data = precision(predictions, label_ids=label_ids, token_type2tokens=self.token_type2tokens,
                                     id2tkn=self.id2tkn, type_data=type_data_batch, old_data=metrics_data,
                                     predictions_are_scores=True, topk=self.topk, time_range=self.time_range,
                                     time_data=time_data_batch, **self.kwargs)
            start += self.batch_size

        if self.return_all_metrics:
            return {
                'metrics_data': metrics_data, # Return all the metrics data too
            }
        else:
            return {
                'precision': metrics_data['precision']['all'], # Return only the overall precision
            }
