import numpy as np
from .core import LayerType


class LayerStatistics():
    """Provides layer statistics:
        (average output sparsity, number of possible spikes, row_sparsity).
    """

    def __init__(self, layer, nb_samples=0, nb_activations=0):
        self._layer = layer
        self._nb_samples = nb_samples
        self._nb_activations = nb_activations

    def __repr__(self):
        data = "{layer: " + self._layer.name + ", layer_type: " + \
            str(self._layer.parameters.layer_type).split(".")[-1]
        data += ", output_sparsity: "
        if self.output_sparsity:
            data += format(self.output_sparsity, ".2f")
        else:
            data += "N/A"
        data += "}"
        return data

    def __str__(self):

        def str_column_data(data, col_width=20):
            if len(data) > col_width - 1:
                formatted_data = data[:col_width - 1] + ' '
            else:
                formatted_data = data + ' ' * (col_width - len(data))

            return formatted_data

        data = str_column_data("Layer (type)", 30)
        data += str_column_data("output sparsity")
        data += "\n"
        data += str_column_data(str(self._layer), 30)
        if self.output_sparsity:
            data += str_column_data(format(self.output_sparsity, ".2f"))
        else:
            data += "N/A"
        return data

    @property
    def possible_spikes(self):
        """Get possible spikes for the layer.

        Returns:
            int: the possible spike amount value.

        """
        return np.prod(self._layer.output_dims)

    @property
    def row_sparsity(self):
        """Get kernel row sparsity.

        Compute row sparsity for kernel weights.

        Returns:
          float: the kernel row sparsity value.

        """
        if (self._layer.parameters.layer_type == LayerType.Convolutional or
                self._layer.parameters.layer_type
                == LayerType.SeparableConvolutional):
            row_sparsity = 0.0
            weights = self._layer.get_variable("weights")
            wshape = weights.shape
            if np.prod(wshape) == 0:
                raise ValueError("Exception in LayerStatistics: weights shape "
                                 "have null dimension: " + str(wshape))

            # Going through all line blocks
            for f in range(wshape[3]):
                for c in range(wshape[2]):
                    for y in range(wshape[1]):
                        if np.array_equal(weights[:, y, c, f],
                                          np.zeros((wshape[0]))):
                            # Counting when line block is full of zero.
                            row_sparsity += 1
            return row_sparsity / (wshape[1] * wshape[2] * wshape[3])

        return None

    @property
    def output_sparsity(self):
        """Get average output sparsity for the layer.

        Returns:
            float: the average output sparsity value.

        """
        if self._nb_samples == 0:
            return None
        activations_per_sample = self._nb_activations / self._nb_samples
        return 1 - activations_per_sample / self.possible_spikes

    @property
    def layer_name(self):
        """Get the name of the corresponding layer.

        Returns:
            str: the layer name.

        """
        return self._layer.name


class SequenceStatistics():
    """Provides layer sequence statistics.
    """

    def __init__(self, sequence, inference, nb_activations, hw_interactions,
                 power_events):
        self._sequence = sequence
        self._inference = inference
        layers = [
            layer for layer in list(sequence.layers)
            if layer.parameters.layer_type != LayerType.InputData
        ]
        # Initialize empty statistics per layer
        self._layer_stats = {
            layer.name: LayerStatistics(layer) for layer in layers
        }
        if inference is not None and nb_activations is not None:
            # Get the number of samples evaluated for that sequence
            nb_samples = inference[0]
            if nb_activations.shape[0] == 1:
                # A single activations value corresponds to the last layer
                layer = sequence.layers[-1]
                layer_activations = nb_activations[0]
                self._layer_stats[layer.name] = LayerStatistics(
                    layer, nb_samples, layer_activations)
            else:
                # Each activations value correspond to a sequence layer
                for i, layer in enumerate(sequence.layers):
                    layer_activations = nb_activations[i]
                    self._layer_stats[layer.name] = LayerStatistics(
                        layer, nb_samples, layer_activations)
        self._powers = {}
        if hw_interactions is not None:
            if power_events:

                def get_power_events(time_range):
                    result = []
                    for event in power_events:
                        if event.ts >= time_range[0] and event.ts <= time_range[
                                1]:
                            result.append(event)
                    return result

                # get power measure between program start & end
                self.powers['program'] = get_power_events(hw_interactions[:2])
                # get power mesures between inference start & end
                self.powers['inference'] = get_power_events(hw_interactions[2:])

    def __repr__(self):
        data = "{sequence: " + self._sequence.name
        fps = "N/A" if self.fps is None else "%.2f" % self.fps
        data += ", fps: " + fps
        if self._powers:
            data += ", powers: " + str(self._powers)
        data += ", layer_stats: " + self.layer_stats.__repr__() + "}"
        return data

    def __str__(self):
        data = "Sequence " + self._sequence.name
        fps = "N/A" if self.fps is None else "%.2f" % self.fps + " fps"
        data += "\nAverage framerate = " + fps
        if self._powers:

            def power(event):
                # voltage is in µV, current in mA, power is in mW.
                return event.voltage * event.current / 1000000

            # get all inference powers value
            all_powers = [power(event) for event in self.powers['inference']]
            # get avg/min/max
            avg_power = sum(all_powers) / len(all_powers)
            min_power = min(all_powers)
            max_power = max(all_powers)

            data += "\nLast inference power usage (mW): "
            data += f"Avg {avg_power:.2f} / Min {min_power:.2f} / Max {max_power:.2f}"
        for layer in self._sequence.layers:
            layer_stats = self._layer_stats[layer.name]
            if layer_stats.output_sparsity is not None:
                data += "\n"
                data += layer_stats.__str__()
        return data

    @property
    def layer_stats(self):
        """Get statistics by layer for this sequence.

        Returns:
            a dictionary of obj:`LayerStatistics` indexed by layer_name.

        """
        return self._layer_stats

    @property
    def fps(self):
        if self._inference is not None:
            return 1000 * self._inference[0] / self._inference[1]
        return None

    @property
    def powers(self):
        return self._powers


def _get_metrics(model, sequence, metrics):
    """Return the metrics for a specific sequence
    """
    if len(model.metrics.names) == 0:
        return None
    # Sequence metrics are identified by the first and last layers
    prefix = sequence.name
    # Filter-out metrics not corresponding to that sequence
    seq_metrics_names = [name for name in model.metrics.names if prefix in name]
    # Get the metrics matching the specified name for the sequence
    metrics_names = [name for name in seq_metrics_names if metrics in name]
    if len(metrics_names) > 0:
        return model.metrics[metrics_names[0]]
    return None


class Statistics:
    """Provides statistics for all Model layer sequences.
    """

    def __init__(self, model):
        self._stats = {}
        # Iterate through model layer sequences
        for sequence in model.sequences:
            # Get activations and inference metrics for the sequence
            inference = _get_metrics(model, sequence, "inference")
            nb_activations = _get_metrics(model, sequence, "activations")
            hw_interactions = _get_metrics(model, sequence,
                                           "hardware_interactions")
            self._stats[sequence.name] = SequenceStatistics(
                sequence, inference, nb_activations, hw_interactions,
                model.power_events)

    def __str__(self):
        data = ""
        for _, stat in self._stats.items():
            if stat.fps is not None:
                data += "\n" + stat.__str__()
        if not data:
            data = "N/A"
        return data

    def __repr__(self):
        return self._stats.__repr__()

    def __getitem__(self, key):
        # Look first for a Sequence statistics
        if key in self._stats:
            return self._stats[key]
        # Look for a Layer statistics in each sequence statistics
        for _, seq_stat in self._stats.items():
            if key in seq_stat.layer_stats:
                return seq_stat.layer_stats[key]
        raise KeyError

    def __len__(self):
        return len(self._stats)

    def __iter__(self):
        return iter(self._stats.items())

    def keys(self):
        return self._stats.keys()

    def items(self):
        return self._stats.items()
