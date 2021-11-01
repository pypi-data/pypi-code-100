import numpy as np
import trojai.data


class RobustnessEvaluatorBase:
    def __init__(self, model, callbacks, callback_kwargs):
        '''
        #TODO make all current evaluators use this base class.
        A base class for robustness evaluators.

        :param model: A placeholder used for the determining the structure of callbacks. If model != None, it is then the
        first argument passed to designated callback functions. Otherwise, the first argument to the callback is expected to be
        the input data.
        :param callbacks: A list of callback functions. If model != None, all functions must accept as the first 4 input arguments model,
        input data to the model, the target, indices and then any callback keyword arguments defined in the callback_kwargs argument.
        If model is None, then the callbacks all take in the data, the target, and indices as the first three arguments.
        Each callback function must return two values: a list of indices, and a dictionary of values to log to the
        dataframe at those indices.
        :param callback_kwargs: A list of keyword arguments for each callback function in callbacks.
        '''
        self.model = model
        self.callbacks = callbacks
        self.callback_kwargs = callback_kwargs

    def run(self, df, loader, num_batches=None, verbose=True):
        #TODO add verbose flag
        '''
        runs the evaluations defined in the callback functions.

        :param df: a dataframe to be logged to.
        :param loader: a troj batch iterator.
        :param num_batches: How many batches to evaluate. If none, all are evaluated.
        '''
        for idx in range(len(self.callbacks)):
            for batch_idx, (data, target, index) in enumerate(loader):
                if verbose:
                    verb_str = 'Batch {}/{} for callback {}/{}'
                    print(verb_str.format(batch_idx, len(loader), idx+1, len(self.callbacks)))
                if self.model != None:
                    log_index, log_dict, = self.callbacks[idx](self.model, data, target, index, **self.callback_kwargs[idx])
                else:
                    log_index, log_dict, = self.callbacks[idx](data, target, index, **self.callback_kwargs[idx])
                df = trojai.data.log_to_dataframe(df, log_index, log_dict)
                if num_batches is not None and batch_idx > num_batches:
                    break
        return df

