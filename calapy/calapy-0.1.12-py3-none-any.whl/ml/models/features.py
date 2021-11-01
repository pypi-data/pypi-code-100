
from .. import torch as pt
from ...ml import devices as cp_device
from .model_tools import ModelMethods as cc_ModelMethods
from ...maths import prod as cp_prod
import numpy as np
import typing


class ProactiveFeatureSequenceClassifier(pt.nn.Module, cc_ModelMethods):

    def __init__(
            self, input_size_lstm: int, hidden_size_lstm: int,
            out_sizes_actors: typing.Union[int, list, tuple, np.ndarray, pt.Tensor],
            out_sizes_classifiers: typing.Union[int, list, tuple, np.ndarray, pt.Tensor],
            n_layers_lstm: int = 1, bias_lstm: typing.Union[bool, int] = True, batch_first_lstm: bool = False,
            dropout_lstm: typing.Union[int, float] = 0, bidirectional_lstm: bool = False,
            biases_actors: typing.Union[bool, int, list, tuple, np.ndarray, pt.Tensor] = True,
            biases_classifiers: typing.Union[bool, int, list, tuple, np.ndarray, pt.Tensor] = True,
            loss_weights_types: typing.Union[list, tuple, np.ndarray, pt.Tensor, None] = None,
            loss_weights_actors: typing.Union[int, float, list, tuple, np.ndarray, pt.Tensor, None] = None,
            loss_weights_classifiers: typing.Union[int, float, list, tuple, np.ndarray, pt.Tensor, None] = None,
            gamma=.999, condition='proactive', device: typing.Union[pt.device, str, None] = None) -> None:

        super(ProactiveFeatureSequenceClassifier, self).__init__()

        self.input_size_lstm = input_size_lstm
        self.hidden_size_lstm = hidden_size_lstm

        self.n_layers_lstm = n_layers_lstm

        if isinstance(bias_lstm, bool):
            self.bias_lstm = bias_lstm
        elif isinstance(bias_lstm, int):
            self.bias_lstm = bool(bias_lstm)
        else:
            raise TypeError('bias_lstm = ' + str(bias_lstm))

        self.batch_first_lstm = batch_first_lstm
        if self.batch_first_lstm:
            self.axis_batch_lstm = 0
            self.axis_sequence_lstm = 1
        else:
            self.axis_batch_lstm = 1
            self.axis_sequence_lstm = 0
        self.axis_features_lstm = 2

        self.dropout_lstm = dropout_lstm

        self.bidirectional_lstm = bidirectional_lstm
        if self.bidirectional_lstm:
            self.num_directions_lstm = 2
        else:
            self.num_directions_lstm = 1

        self.out_features_lstm = self.hidden_size_lstm * self.num_directions_lstm

        self.device = cp_device.define_device(device)

        # lstm tutorials at:
        # https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
        # https://pytorch.org/tutorials/beginner/nlp/sequence_models_tutorial.html

        self.lstm = pt.nn.LSTM(
            self.input_size_lstm, self.hidden_size_lstm,
            num_layers=self.n_layers_lstm, bias=self.bias_lstm,
            batch_first=self.batch_first_lstm, dropout=self.dropout_lstm,
            bidirectional=self.bidirectional_lstm, device=self.device)
        
        self.lstm.to(self.device)

        if isinstance(out_sizes_actors, int):
            self.out_sizes_actors = [out_sizes_actors]
        elif isinstance(out_sizes_actors, list):
            self.out_sizes_actors = out_sizes_actors
        elif isinstance(out_sizes_actors, tuple):
            self.out_sizes_actors = list(out_sizes_actors)
        elif isinstance(out_sizes_actors, (np.ndarray, pt.Tensor)):
            self.out_sizes_actors = out_sizes_actors.tolist()
        else:
            raise TypeError('out_sizes_actors')

        self.n_dimensions_actions = self.A = len(self.out_sizes_actors)

        if isinstance(out_sizes_classifiers, int):
            self.out_sizes_classifiers = [out_sizes_classifiers]
        elif isinstance(out_sizes_classifiers, list):
            self.out_sizes_classifiers = out_sizes_classifiers
        elif isinstance(out_sizes_classifiers, tuple):
            self.out_sizes_classifiers = list(out_sizes_classifiers)
        elif isinstance(out_sizes_classifiers, (np.ndarray, pt.Tensor)):
            self.out_sizes_classifiers = out_sizes_classifiers.tolist()
        else:
            raise TypeError('out_sizes_classifiers')

        self.n_dimensions_classes = self.C = len(self.out_sizes_classifiers)

        self.n_outputs = self.O = self.A + self.C

        if isinstance(biases_actors, bool):
            self.biases_actors = [biases_actors]
        elif isinstance(biases_actors, int):
            self.biases_actors = [bool(biases_actors)]
        elif isinstance(biases_actors, list):
            self.biases_actors = biases_actors
        elif isinstance(biases_actors, tuple):
            self.biases_actors = list(biases_actors)
        elif isinstance(biases_actors, (np.ndarray, pt.Tensor)):
            self.biases_actors = biases_actors.tolist()
        else:
            raise TypeError('biases_actors')

        if len(self.biases_actors) != self.A:
            if len(self.biases_actors) == 1:
                self.biases_actors = [self.biases_actors[0] for a in range(self.A)]
            else:
                raise ValueError('biases_actors = ' + str(biases_actors))

        if isinstance(biases_classifiers, bool):
            self.biases_classifiers = [biases_classifiers]
        elif isinstance(biases_classifiers, int):
            self.biases_classifiers = [bool(biases_classifiers)]
        elif isinstance(biases_classifiers, list):
            self.biases_classifiers = biases_classifiers
        elif isinstance(biases_classifiers, tuple):
            self.biases_classifiers = list(biases_classifiers)
        elif isinstance(biases_classifiers, (np.ndarray, pt.Tensor)):
            self.biases_classifiers = biases_classifiers.tolist()
        else:
            raise TypeError('biases_classifiers')

        if len(self.biases_classifiers) != self.C:
            if len(self.biases_classifiers) == 1:
                self.biases_classifiers = [self.biases_classifiers[0] for c in range(self.C)]
            else:
                raise ValueError('biases_classifiers = ' + str(biases_classifiers))

        self.n_out_types = 2

        if loss_weights_types is None:
            loss_weight_type_i = 1.0 / self.n_out_types
            self.loss_weights_types = [loss_weight_type_i for i in range(self.n_out_types)]
        elif isinstance(loss_weights_types, list):
            self.loss_weights_types = loss_weights_types
        elif isinstance(loss_weights_types, tuple):
            self.loss_weights_types = list(loss_weights_types)
        elif isinstance(loss_weights_types, (np.ndarray, pt.Tensor)):
            self.loss_weights_types = loss_weights_types.tolist()
        else:
            raise TypeError('loss_weights_types')

        if len(self.loss_weights_types) != self.n_out_types:
            raise ValueError('loss_weights_types = ' + str(loss_weights_types))

        sum_loss_weights_types = sum(self.loss_weights_types)
        self.loss_weights_types = [(self.loss_weights_types[i] / sum_loss_weights_types) for i in range(self.n_out_types)]
        self.sum_loss_weights_types = sum(self.loss_weights_types)

        if loss_weights_actors is None:
            loss_weight_actor_a = 1.0 / self.A
            self.loss_weights_actors = [loss_weight_actor_a for a in range(self.A)]
        elif isinstance(loss_weights_actors, int):
            self.loss_weights_actors = [float(loss_weights_actors)]
        elif isinstance(loss_weights_actors, float):
            self.loss_weights_actors = [loss_weights_actors]
        elif isinstance(loss_weights_actors, list):
            self.loss_weights_actors = loss_weights_actors
        elif isinstance(loss_weights_actors, tuple):
            self.loss_weights_actors = list(loss_weights_actors)
        elif isinstance(loss_weights_actors, (np.ndarray, pt.Tensor)):
            self.loss_weights_actors = loss_weights_actors.tolist()
        else:
            raise TypeError('loss_weights_actors')

        if len(self.loss_weights_actors) != self.A:
            if len(self.loss_weights_actors) == 1:
                self.loss_weights_actors = [self.loss_weights_actors[0] for a in range(self.A)]
            else:
                raise ValueError('loss_weights_actors = ' + str(loss_weights_actors))

        sum_loss_weights_actors = sum(self.loss_weights_actors)
        self.loss_weights_actors = [(self.loss_weights_actors[a] / sum_loss_weights_actors) for a in range(self.A)]
        self.sum_loss_weights_actors = sum(self.loss_weights_actors)

        if loss_weights_classifiers is None:
            loss_weight_classifier_c = 1.0 / self.C
            self.loss_weights_classifiers = [loss_weight_classifier_c for c in range(self.C)]
        elif isinstance(loss_weights_classifiers, int):
            self.loss_weights_classifiers = [float(loss_weights_classifiers)]
        elif isinstance(loss_weights_classifiers, float):
            self.loss_weights_classifiers = [loss_weights_classifiers]
        elif isinstance(loss_weights_classifiers, list):
            self.loss_weights_classifiers = loss_weights_classifiers
        elif isinstance(loss_weights_classifiers, tuple):
            self.loss_weights_classifiers = list(loss_weights_classifiers)
        elif isinstance(loss_weights_classifiers, (np.ndarray, pt.Tensor)):
            self.loss_weights_classifiers = loss_weights_classifiers.tolist()
        else:
            raise TypeError('loss_weights_classifiers')

        if len(self.loss_weights_classifiers) != self.C:
            if len(self.loss_weights_classifiers) == 1:
                self.loss_weights_classifiers = [self.loss_weights_classifiers[0] for c in range(self.C)]
            else:
                raise ValueError('loss_weights_classifiers = ' + str(loss_weights_classifiers))

        sum_loss_weights_classifiers = sum(self.loss_weights_classifiers)
        self.loss_weights_classifiers = [
            (self.loss_weights_classifiers[c] / sum_loss_weights_classifiers) for c in range(self.C)]
        self.sum_loss_weights_classifiers = sum(self.loss_weights_classifiers)

        self.in_features_actors = [self.out_features_lstm for a in range(self.A)]
        self.out_features_actors = self.out_sizes_actors

        self.actors = pt.nn.ModuleList([pt.nn.Linear(
            self.in_features_actors[a], self.out_features_actors[a],
            bias=self.biases_actors[a], device=self.device) for a in range(0, self.A, 1)])
        # self.actors = pt.nn.ModuleList([pt.nn.Linear(
        #     self.in_features_actors[a], self.out_features_actors[a],
        #     bias=self.biases_actors[a]) for a in range(0, self.A, 1)])
        # self.actors.to(self.device)

        self.in_features_classifiers = [self.out_features_lstm for c in range(self.C)]
        self.out_features_classifiers = self.out_sizes_classifiers

        self.classifiers = pt.nn.ModuleList([pt.nn.Linear(
            self.in_features_classifiers[c], self.out_features_classifiers[c],
            bias=self.biases_classifiers[c], device=self.device) for c in range(0, self.C, 1)])
        # self.classifiers = pt.nn.ModuleList([pt.nn.Linear(
        #     self.in_features_classifiers[c], self.out_features_classifiers[c],
        #     bias=self.biases_classifiers[c]) for c in range(0, self.C, 1)])
        # self.classifiers.to(self.device)

        self.criterion_values_actions = pt.nn.SmoothL1Loss(reduction='none')
        self.criterion_values_actions_reduction = pt.nn.SmoothL1Loss(reduction='mean')

        self.criterion_classifications = pt.nn.CrossEntropyLoss(reduction='none')
        self.criterion_classifications_reduction = pt.nn.CrossEntropyLoss(reduction='mean')

        self.condition = condition

        self.gamma = gamma

        self.to(self.device)

    def forward(self, x, h=None, c=None):

        x.to(self.device)

        if h is None:
            batch_size = x.shape[self.axis_batch_lstm]

            if c is None:
                h, c = self.init_hidden_state(batch_size)
            else:
                h = self.init_h(batch_size)

                c.to(self.device)

        elif c is None:

            h.to(self.device)

            batch_size = x.shape[self.axis_batch_lstm]
            c = self.init_c(batch_size)

        x, (h, c) = self.lstm(x, (h, c))

        values_actions = [self.actors[a](x) for a in range(0, self.A, 1)]
        # values_actions = [None for a in range(0, self.A, 1)]
        # for a in range(0, self.A, 1):
        #     values_actions[a] = self.actors[a](x)

        classifications = [self.classifiers[c](x) for c in range(0, self.C, 1)]
        # classifications = [None for c in range(0, self.C, 1)]
        # for c in range(0, self.C, 1):
        #     classifications[c] = self.classifiers[c](x)

        return values_actions, classifications, (h, c)


    def init_h(self, batch_size):

        h = pt.zeros(
            [self.num_directions_lstm * self.n_layers_lstm, batch_size, self.hidden_size_lstm],
            device=self.device)

        h.to(self.device)

        return h

    def init_c(self, batch_size):

        c = pt.zeros(
            [self.num_directions_lstm * self.n_layers_lstm, batch_size, self.hidden_size_lstm],
            device=self.device)

        return c

    def init_hidden_state(self, batch_size):

        h = self.init_h(batch_size)
        c = self.init_c(batch_size)

        return h, c

    def sample_action(self, x_t, h=None, c=None, epsilon=.1):

        # self.eval()
        # pt.set_grad_enabled(False)
        values_actions, classifications, (h, c) = self(x_t, h=h, c=c)

        # shape_actions = np.asarray(x_t.shape, dtype='i')
        # shape_actions = shape_actions[
        #     np.arange(0, len(shape_actions), 1, dtype='i') != self.axis_features_lstm].tolist()
        shape_actions = list(x_t.shape)
        shape_actions[self.axis_features_lstm] = 1

        mask_randoms = pt.rand(
            shape_actions, out=None, dtype=None, layout=pt.strided,
            device=self.device, requires_grad=False) < epsilon

        n_randoms = mask_randoms.sum(dtype=None).item()

        mask_greedy = pt.logical_not(mask_randoms, out=None)
        # n_greedy = batch_size - n_randoms

        actions = [None for a in range(0, self.A, 1)]  # type: list
        # actions = pt.empty([self.A] + shape_actions, dtype=pt.int64, device=self.device, requires_grad=False)

        for a in range(0, self.A, 1):

            actions[a] = pt.empty(shape_actions, dtype=pt.int64, device=self.device, requires_grad=False)

            random_action_a = pt.randint(
                low=0, high=self.actors[a].out_features, size=(n_randoms,),
                generator=None, dtype=pt.int64, device=self.device, requires_grad=False)

            actions[a][mask_randoms] = random_action_a

            actions[a][mask_greedy] = (
                values_actions[a].max(dim=self.axis_features_lstm, keepdim=True)[1][mask_greedy])

        return actions, classifications, (h, c)

    def compute_unweighted_value_action_losses_ABT(self, values_selected_actions, expected_values_actions):

        unweighted_value_action_losses_ABT = [self.criterion_values_actions(
            values_selected_actions[a], expected_values_actions[a]) for a in range(0, self.A, 1)]

        return unweighted_value_action_losses_ABT

    def compute_unweighted_value_action_losses_BT(self, values_selected_actions, expected_values_actions):

        if self.A > 0:
            weight = (1 / self.A)

            unweighted_value_action_losses_ABT = self.compute_unweighted_value_action_losses_ABT(
                values_selected_actions, expected_values_actions)

            unweighted_value_action_losses_BT = (unweighted_value_action_losses_ABT[0] * weight)
            for a in range(1, self.A, 1):
                unweighted_value_action_losses_BT += (unweighted_value_action_losses_ABT[a] * weight)
        else:
            unweighted_value_action_losses_BT = 0

        return unweighted_value_action_losses_BT

    def compute_unweighted_value_action_losses_AT(self, values_selected_actions, expected_values_actions):

        unweighted_value_action_losses_ABT = self.compute_unweighted_value_action_losses_ABT(
            values_selected_actions, expected_values_actions)

        unweighted_value_action_losses_AT = [
            unweighted_value_action_losses_ABT[a].mean(dim=self.axis_batch_lstm) for a in range(0, self.A, 1)]

        return unweighted_value_action_losses_AT

    def compute_unweighted_value_action_losses_T(self, values_selected_actions, expected_values_actions):
        if self.A > 0:
            weight = (1 / self.A)

            unweighted_value_action_losses_AT = self.compute_unweighted_value_action_losses_AT(
                values_selected_actions, expected_values_actions)

            unweighted_value_action_losses_T = (unweighted_value_action_losses_AT[0] * weight)
            for a in range(1, self.A, 1):
                unweighted_value_action_losses_T += (unweighted_value_action_losses_AT[a] * weight)
        else:
            unweighted_value_action_losses_T = 0

        return unweighted_value_action_losses_T

    def compute_unweighted_value_action_losses_A(self, values_selected_actions, expected_values_actions):

        unweighted_value_action_losses_A = [self.criterion_values_actions_reduction(
            values_selected_actions[a], expected_values_actions[a]) for a in range(0, self.A, 1)]

        return unweighted_value_action_losses_A

    def compute_unweighted_value_action_loss(self, values_selected_actions, expected_values_actions):
        if self.A > 0:
            weight = (1 / self.A)
            unweighted_value_action_losses_A = self.compute_unweighted_value_action_losses_A(
                values_selected_actions, expected_values_actions)

            unweighted_value_action_loss = unweighted_value_action_losses_A[0] * weight
            for a in range(1, self.A, 1):
                unweighted_value_action_loss += unweighted_value_action_losses_A[a] * weight
        else:
            unweighted_value_action_loss = 0

        return unweighted_value_action_loss

    def compute_weighted_value_action_losses_ABT(self, values_selected_actions, expected_values_actions):

        unweighted_value_action_losses_ABT = self.compute_unweighted_value_action_losses_ABT(
            values_selected_actions, expected_values_actions)

        weighted_value_action_losses_ABT = [
            (unweighted_value_action_losses_ABT[a] * self.loss_weights_actors[a]) for a in range(0, self.A, 1)]

        return weighted_value_action_losses_ABT

    def compute_weighted_value_action_losses_BT(self, values_selected_actions, expected_values_actions):

        if self.A > 0:
            unweighted_value_action_losses_ABT = self.compute_unweighted_value_action_losses_ABT(
                values_selected_actions, expected_values_actions)

            weighted_value_action_losses_BT = (unweighted_value_action_losses_ABT[0] * self.loss_weights_actors[0])
            for a in range(1, self.A, 1):
                weighted_value_action_losses_BT += (unweighted_value_action_losses_ABT[a] * self.loss_weights_actors[a])
        else:
            weighted_value_action_losses_BT = 0

        return weighted_value_action_losses_BT

    def compute_weighted_value_action_losses_AT(self, values_selected_actions, expected_values_actions):

        unweighted_value_action_losses_AT = self.compute_unweighted_value_action_losses_AT(
            values_selected_actions, expected_values_actions)

        weighted_value_action_losses_AT = [
            (unweighted_value_action_losses_AT[a] * self.loss_weights_actors[a]) for a in range(0, self.A, 1)]

        return weighted_value_action_losses_AT

    def compute_weighted_value_action_losses_T(self, values_selected_actions, expected_values_actions):

        if self.A > 0:

            unweighted_value_action_losses_AT = self.compute_unweighted_value_action_losses_AT(
                values_selected_actions, expected_values_actions)

            weighted_value_action_losses_T = (unweighted_value_action_losses_AT[0] * self.loss_weights_actors[0])
            for a in range(1, self.A, 1):
                weighted_value_action_losses_T += (unweighted_value_action_losses_AT[a] * self.loss_weights_actors[a])
        else:
            weighted_value_action_losses_T = 0

        return weighted_value_action_losses_T

    def compute_weighted_value_action_losses_A(self, values_selected_actions, expected_values_actions):

        unweighted_value_action_losses_A = self.compute_unweighted_value_action_losses_A(
            values_selected_actions, expected_values_actions)

        weighted_value_action_losses_A = [
            (unweighted_value_action_losses_A[a] * self.loss_weights_actors[a]) for a in range(0, self.A, 1)]

        return weighted_value_action_losses_A

    def compute_weighted_value_action_loss(self, values_selected_actions, expected_values_actions):
        if self.A > 0:

            unweighted_value_action_losses_A = self.compute_unweighted_value_action_losses_A(
                values_selected_actions, expected_values_actions)

            weighted_value_action_loss = (unweighted_value_action_losses_A[0] * self.loss_weights_actors[0])
            for a in range(1, self.A, 1):
                weighted_value_action_loss += (unweighted_value_action_losses_A[a] * self.loss_weights_actors[a])
        else:
            weighted_value_action_loss = 0

        return weighted_value_action_loss

    def compute_unweighted_classification_losses_CBT(self, classifications, labels):

        unweighted_classification_losses_CBT = [self.criterion_classifications(
            pt.movedim(classifications[c], self.axis_features_lstm, 1), labels[c]) for c in range(0, self.C, 1)]

        return unweighted_classification_losses_CBT

    def compute_unweighted_classification_losses_BT(self, classifications, labels):

        if self.C > 0:
            weight = (1 / self.C)

            unweighted_classification_losses_CBT = self.compute_unweighted_classification_losses_CBT(
                classifications, labels)

            unweighted_classification_losses_BT = (unweighted_classification_losses_CBT[0] * weight)
            for c in range(1, self.C, 1):
                unweighted_classification_losses_BT += (unweighted_classification_losses_CBT[c] * weight)
        else:
            unweighted_classification_losses_BT = 0

        return unweighted_classification_losses_BT

    def compute_unweighted_classification_losses_CT(self, classifications, labels):

        unweighted_classification_losses_CBT = self.compute_unweighted_classification_losses_CBT(
            classifications, labels)

        unweighted_classification_losses_CT = [
            unweighted_classification_losses_CBT[c].mean(dim=self.axis_batch_lstm) for c in range(0, self.C, 1)]

        return unweighted_classification_losses_CT

    def compute_unweighted_classification_losses_T(self, classifications, labels):
        if self.C > 0:
            weight = (1 / self.C)

            unweighted_classification_losses_CT = self.compute_unweighted_classification_losses_CT(
                classifications, labels)

            unweighted_classification_losses_T = (unweighted_classification_losses_CT[0] * weight)
            for c in range(1, self.C, 1):
                unweighted_classification_losses_T += (unweighted_classification_losses_CT[c] * weight)
        else:
            unweighted_classification_losses_T = 0

        return unweighted_classification_losses_T

    def compute_unweighted_classification_losses_C(self, classifications, labels):

        unweighted_classification_losses_C = [self.criterion_classifications_reduction(
            pt.movedim(classifications[c], self.axis_features_lstm, 1), labels[c]) for c in range(0, self.C, 1)]

        return unweighted_classification_losses_C

    def compute_unweighted_classification_loss(self, classifications, labels):
        if self.C > 0:
            weight = (1 / self.C)
            unweighted_classification_losses_C = self.compute_unweighted_classification_losses_C(
                classifications, labels)

            unweighted_classification_loss = unweighted_classification_losses_C[0] * weight
            for c in range(1, self.C, 1):
                unweighted_classification_loss += unweighted_classification_losses_C[c] * weight
        else:
            unweighted_classification_loss = 0

        return unweighted_classification_loss

    def compute_weighted_classification_losses_CBT(self, classifications, labels):

        unweighted_classification_losses_CBT = self.compute_unweighted_classification_losses_CBT(
            classifications, labels)

        weighted_classification_losses_CBT = [
            (unweighted_classification_losses_CBT[c] * self.loss_weights_classifiers[c]) for c in range(0, self.C, 1)]

        return weighted_classification_losses_CBT

    def compute_weighted_classification_losses_BT(self, classifications, labels):

        if self.C > 0:
            unweighted_classification_losses_CBT = self.compute_unweighted_classification_losses_CBT(
                classifications, labels)

            weighted_classification_losses_BT = (
                    unweighted_classification_losses_CBT[0] * self.loss_weights_classifiers[0])
            for c in range(1, self.C, 1):
                weighted_classification_losses_BT += (
                        unweighted_classification_losses_CBT[c] * self.loss_weights_classifiers[c])
        else:
            weighted_classification_losses_BT = 0

        return weighted_classification_losses_BT

    def compute_weighted_classification_losses_CT(self, classifications, labels):

        unweighted_classification_losses_CT = self.compute_unweighted_classification_losses_CT(
            classifications, labels)

        weighted_classification_losses_CT = [
            (unweighted_classification_losses_CT[c] * self.loss_weights_classifiers[c]) for c in range(0, self.C, 1)]

        return weighted_classification_losses_CT

    def compute_weighted_classification_losses_T(self, classifications, labels):

        if self.C > 0:

            unweighted_classification_losses_CT = self.compute_unweighted_classification_losses_CT(
                classifications, labels)

            weighted_classification_losses_T = (
                    unweighted_classification_losses_CT[0] * self.loss_weights_classifiers[0])
            for c in range(1, self.C, 1):
                weighted_classification_losses_T += (
                        unweighted_classification_losses_CT[c] * self.loss_weights_classifiers[c])
        else:
            weighted_classification_losses_T = 0

        return weighted_classification_losses_T

    def compute_weighted_classification_losses_C(self, classifications, labels):

        unweighted_classification_losses_C = self.compute_unweighted_classification_losses_C(
            classifications, labels)

        weighted_classification_losses_C = [
            (unweighted_classification_losses_C[c] * self.loss_weights_classifiers[c]) for c in range(0, self.C, 1)]

        return weighted_classification_losses_C

    def compute_weighted_classification_loss(self, classifications, labels):
        if self.C > 0:

            unweighted_classification_losses_C = self.compute_unweighted_classification_losses_C(
                classifications, labels)

            weighted_classification_loss = (
                    unweighted_classification_losses_C[0] * self.loss_weights_classifiers[0])
            for c in range(1, self.C, 1):
                weighted_classification_loss += (
                        unweighted_classification_losses_C[c] * self.loss_weights_classifiers[c])
        else:
            weighted_classification_loss = 0

        return weighted_classification_loss

    def get_previous_rewards(self, classifications, labels, reward_bias=0):

        weighted_classification_losses_BT = self.compute_weighted_classification_losses_BT(
            classifications, labels)

        previous_rewards = - weighted_classification_losses_BT + reward_bias

        return previous_rewards

    def compute_expected_values_actions(self, next_states, rewards):

        # samples = replay_memory.sample()
        # states = samples['states']
        # states_labels = samples['states_labels']
        # actions = samples['actions']
        # next_states = samples['next_states']
        # rewards = samples['rewards']
        # # non_final = samples['non_final']

        next_values_actions, next_classifications, (next_h, next_c) = self(next_states)

        max_next_values_actions = [
            next_values_actions_a.max(dim=self.axis_features_lstm, keepdim=False)[0].detach()
            for next_values_actions_a in next_values_actions]

        expected_values_actions = [
            (rewards + (self.gamma * max_next_values_actions_a))
            for max_next_values_actions_a in max_next_values_actions]

        return expected_values_actions

    def remove_last_values_actions(self, values_actions: list):

        values_actions_out = [None for a in range(0, self.A, 1)]
        for a in range(self.A):
            ind = tuple(
                [slice(0, values_actions[a].shape[d], 1) if d != self.axis_sequence_lstm
                 else slice(0, values_actions[a].shape[d] - 1, 1) for d in range(0, values_actions[a].ndim, 1)])

            values_actions_out[a] = values_actions[a][ind]

        return values_actions_out

    def gather_values_selected_actions(self, values_actions, actions):

        values_selected_actions = [values_actions[a].gather(self.axis_features_lstm, actions[a]).squeeze(
            dim=self.axis_features_lstm) for a in range(0, self.A, 1)]

        return values_selected_actions

    def compute_unweighted_losses(
            self,
            values_selected_actions, expected_values_actions,
            classifications, labels):

        unweighted_value_action_loss = self.compute_unweighted_value_action_loss(
            values_selected_actions=values_selected_actions, expected_values_actions=expected_values_actions)

        unweighted_classification_loss = self.compute_unweighted_classification_loss(
            classifications=classifications, labels=labels)

        weight = 1 / self.n_out_types

        unweighted_loss = ((unweighted_value_action_loss * weight) + (unweighted_classification_loss * weight))

        return unweighted_loss, unweighted_value_action_loss, unweighted_classification_loss

    def compute_weighted_losses(
            self,
            values_selected_actions, expected_values_actions,
            classifications, labels):

        weighted_value_action_loss = self.compute_weighted_value_action_loss(
            values_selected_actions=values_selected_actions, expected_values_actions=expected_values_actions)#.detach()

        weighted_classification_loss = self.compute_weighted_classification_loss(
            classifications=classifications, labels=labels)

        weighted_loss = ((weighted_value_action_loss * self.loss_weights_types[0]) +
                         (weighted_classification_loss * self.loss_weights_types[1]))

        # weighted_loss = weighted_classification_loss #* self.loss_weights_types[1]

        return weighted_loss, weighted_value_action_loss, weighted_classification_loss

    def compute_corrects_C(self, classifications, labels):

        predictions = [pt.max(classifications[c], self.axis_features_lstm)[1] for c in range(0, self.C, 1)]
        n_corrects_C = [pt.sum(predictions[c] == labels[c]).item() for c in range(0, self.C, 1)]

        n_classifications_C = [cp_prod(predictions[c].shape) for c in range(0, self.C, 1)]

        return n_corrects_C, n_classifications_C

    def compute_corrects(self, classifications, labels):

        n_corrects_C, n_classifications_C = self.compute_corrects_C(classifications, labels)

        n_corrects = sum(n_corrects_C)

        n_classifications = sum(n_classifications_C)

        return n_corrects, n_classifications
