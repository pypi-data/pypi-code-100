# websites:
# https://pytorch.org/docs/stable/torchvision/transforms.html
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py
# https://pytorch.org/hub/pytorch_vision_resnet/
# https://discuss.pytorch.org/t/normalize-each-input-image-in-a-batch-independently-and-inverse-normalize-the-output/23739
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

from . import torch as pt
import numpy as np
import typing
import math
import os
import copy
from .. import txt as cp_txt
from .. import clock as cp_clock
from ..strings import format_float_to_str as cp_strings_format_float_to_str


pt.set_grad_enabled(False)


def classifier(
        model, loader, criterion, optimizer, scheduler, I=10, E=None, directory_outputs=None):

    cp_timer = cp_clock.Timer()

    for key_loader_k in loader.keys():
        if key_loader_k == 'training' or key_loader_k == 'validation':
            pass
        else:
            raise ValueError('Unknown keys in loader')

    headers = [
        'Epoch', 'Unsuccessful Epochs', 'Training Loss', 'Training Accuracy',
        'Validation Loss', 'Lowest Validation Loss', 'Is Lower Loss',
        'Validation Accuracy', 'Highest Validation Accuracy', 'Is Higher Accuracy']

    n_columns = len(headers)
    new_line_stats = [None for i in range(0, n_columns, 1)]   # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    if directory_outputs is None:
        directory_outputs = 'outputs'

    os.makedirs(directory_outputs, exist_ok=True)

    directory_best_model_state = os.path.join(directory_outputs, 'best_model_state.pth')
    directory_last_model_state = os.path.join(directory_outputs, 'last_model_state.pth')

    directory_best_model = os.path.join(directory_outputs, 'best_model.pth')
    directory_last_model = os.path.join(directory_outputs, 'last_model.pth')

    directory_stats = os.path.join(directory_outputs, 'stats.csv')

    n_decimals_for_printing = 6

    best_model_wts = copy.deepcopy(model.state_dict())

    lowest_loss = math.inf
    lowest_loss_str = str(lowest_loss)
    highest_accuracy = -math.inf
    highest_accuracy_str = str(highest_accuracy)

    if E is None:
        E = math.inf

    if I is None:
        I = math.inf

    i = 0
    e = 0

    n_dashes = 110
    dashes = '-' * n_dashes
    print(dashes)

    while (e < E) and (i < I):

        print('Epoch {e} ...'.format(e=e))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e

        # Each epoch has a training and a validation phase
        # training phase
        model.train()  # Set model to training mode
        criterion.train()

        running_loss_e = 0.0
        running_corrects_e = 0
        n_samples_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['training']:
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            # track history
            pt.set_grad_enabled(True)
            outputs = model(batch_eb)
            _, preds = pt.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            # backward + optimize
            loss_eb.backward()
            optimizer.step()

            pt.set_grad_enabled(False)

            running_loss_e += loss_eb.item() * batch_eb.shape[loader['training'].batch_axis_inputs]
            # noinspection PyTypeChecker
            running_corrects_e += pt.sum(preds == labels_eb).item()
            
            n_samples_e += batch_eb.shape[loader['training'].batch_axis_inputs]

            b += 1

        # scheduler.step()

        loss_e = running_loss_e / n_samples_e
        accuracy_e = running_corrects_e / n_samples_e

        loss_str_e = cp_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        print('Epoch: {:d}. Training.   Loss: {:s}. Accuracy: {:s}.'.format(e, loss_str_e, accuracy_str_e))

        stats['lines'][e][stats['headers']['Training Loss']] = loss_e
        stats['lines'][e][stats['headers']['Training Accuracy']] = accuracy_e

        # validation phase
        model.eval()  # Set model to evaluate mode

        criterion.eval()

        # zero the parameter gradients
        optimizer.zero_grad()

        pt.set_grad_enabled(False)

        running_loss_e = 0.0
        running_corrects_e = 0

        n_samples_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['validation']:

            # forward
            outputs = model(batch_eb)
            _, preds = pt.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            running_loss_e += loss_eb.item() * batch_eb.shape[loader['validation'].batch_axis_inputs]
            # noinspection PyTypeChecker
            running_corrects_e += pt.sum(preds == labels_eb).item()

            n_samples_e += batch_eb.shape[loader['validation'].batch_axis_inputs]

            b += 1

        loss_e = running_loss_e / n_samples_e
        accuracy_e = running_corrects_e / n_samples_e

        loss_str_e = cp_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        stats['lines'][e][stats['headers']['Validation Loss']] = loss_e
        stats['lines'][e][stats['headers']['Validation Accuracy']] = accuracy_e

        if accuracy_e > highest_accuracy:
            highest_accuracy = accuracy_e
            highest_accuracy_str = cp_strings_format_float_to_str(highest_accuracy, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 1
            stats['lines'][e][stats['headers']['Highest Validation Accuracy']] = highest_accuracy
        else:
            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 0
            stats['lines'][e][stats['headers']['Highest Validation Accuracy']] = highest_accuracy

        if loss_e < lowest_loss:

            lowest_loss = loss_e
            lowest_loss_str = cp_strings_format_float_to_str(lowest_loss, n_decimals=n_decimals_for_printing)
            i = 0
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 1
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Validation Loss']] = lowest_loss

            best_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
            for directory_i in [directory_best_model, directory_best_model_state]:
                if os.path.isfile(directory_i):
                    os.remove(directory_i)

            pt.save(model, directory_best_model)
            pt.save(best_model_wts, directory_best_model_state)

        else:
            i += 1
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 0
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Validation Loss']] = lowest_loss

        last_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
        for directory_i in [directory_last_model, directory_last_model_state, directory_stats]:
            if os.path.isfile(directory_i):
                os.remove(directory_i)

        pt.save(model, directory_last_model)
        pt.save(last_model_wts, directory_last_model_state)

        cp_txt.lines_to_csv_file(stats['lines'], directory_stats, stats['headers'])

        print('Epoch: {:d}. Validation. Loss: {:s}. Lowest Loss: {:s}. Accuracy: {:s}. Highest Accuracy: {:s}.'.format(
            e, loss_str_e, lowest_loss_str, accuracy_str_e, highest_accuracy_str))

        print('Epoch {e} - Unsuccessful Epochs {i}.'.format(e=e, i=i))

        e += 1
        print(dashes)

    print()
    E = e

    time_training = cp_timer.get_delta_time()

    print('Training completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_training.days, h=time_training.hours,
        m=time_training.minutes, s=time_training.seconds))
    print('Number of Epochs: {E:d}'.format(E=E))
    print('Lowest Validation Loss: {:s}'.format(lowest_loss_str))
    print('Highest Validation Accuracy: {:s}'.format(highest_accuracy_str))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, stats


def proactive_classifier(
        model, loader, preprocess, criterion, optimizer, scheduler, epsilon=0, I=10, E=None, T=None,
        directory_outputs=None):

    cp_timer = cp_clock.Timer()

    for key_loader_k in loader.keys():
        if key_loader_k == 'training' or key_loader_k == 'validation':
            pass
        else:
            raise ValueError('Unknown keys in loader')

    headers = [
        'Epoch', 'Unsuccessful Epochs', 'Training Loss', 'Training Accuracy',
        'Validation Loss', 'Lowest Validation Loss', 'Is Lower Loss',
        'Validation Accuracy', 'Highest Validation Accuracy', 'Is Higher Accuracy']

    n_columns = len(headers)
    new_line_stats = [None for i in range(0, n_columns, 1)]  # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    if directory_outputs is None:
        directory_outputs = 'outputs'

    os.makedirs(directory_outputs, exist_ok=True)

    directory_best_model_state = os.path.join(directory_outputs, 'best_model_state.pth')
    directory_last_model_state = os.path.join(directory_outputs, 'last_model_state.pth')

    directory_best_model = os.path.join(directory_outputs, 'best_model.pth')
    directory_last_model = os.path.join(directory_outputs, 'last_model.pth')

    directory_stats = os.path.join(directory_outputs, 'stats.csv')

    n_decimals_for_printing = 6

    best_model_wts = copy.deepcopy(model.state_dict())

    lowest_loss = math.inf
    lowest_loss_str = str(lowest_loss)
    highest_accuracy = -math.inf
    highest_accuracy_str = str(highest_accuracy)

    if E is None:
        E = math.inf

    if I is None:
        I = math.inf

    if T is None:
        T = math.inf

    i = 0
    e = 0

    n_dashes = 110
    dashes = '-' * n_dashes
    print(dashes)

    while (e < E) and (i < I):

        print('Epoch {e} ...'.format(e=e))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e

        # Each epoch has a training and a validation phase
        # training phase
        model.train()  # Set model to training mode

        running_loss_e = 0.0
        running_corrects_e = 0
        n_samples_e = 0

        b = 0
        # Iterate over data.
        for environments_eb in loader['training']:

            replay_memory = ReplayMemory(axis_time=model.axis_sequence_lstm, axis_features=model.axis_features_lstm)

            state_ebt, labels_ebt = environments_eb()

            labels_ebt = [pt.unsqueeze(labels_ebtc, dim=1) for labels_ebtc in labels_ebt]

            batch_size = state_ebt.shape[loader['training'].batch_axis_inputs]
            # device = state_ebt.device

            (h_ebt, c_ebt) = model.init_hidden_state(batch_size)

            t = 0
            while t < T:

                action_ebt, classifications_ebt, (h_ebt, c_ebt) = model.sample_action(
                    state_ebt, h=h_ebt, c=c_ebt, epsilon=epsilon)

                if preprocess is None:
                    delta_ebt = action_ebt
                else:
                    delta_ebt = preprocess(action_ebt)

                if t == (T - 1):

                    action_ebt = None
                    next_state_ebt = None
                    next_labels_ebt = None
                    rewards_ebt = None

                else:
                    next_state_ebt, next_labels_ebt = environments_eb.step(delta_ebt)
                    next_labels_ebt = [pt.unsqueeze(next_labels_ebtc, dim=1) for next_labels_ebtc in next_labels_ebt]

                    rewards_ebt = None

                replay_memory.put(states=state_ebt, states_labels=labels_ebt, actions=action_ebt,
                                  next_states=next_state_ebt, rewards=rewards_ebt)

                if t > 0:

                    previous_rewards_ebt = model.get_previous_rewards(
                        classifications=classifications_ebt, labels=labels_ebt)

                    replay_memory.rewards[t-1] = previous_rewards_ebt

                t += 1

                state_ebt, labels_ebt = next_state_ebt, next_labels_ebt

                # todo: store done?

            samples_eb = replay_memory.sample()
            states_eb = samples_eb['states']
            states_labels_eb = samples_eb['states_labels']
            actions_eb = samples_eb['actions']
            next_states_eb = samples_eb['next_states']
            rewards_eb = samples_eb['rewards']
            # non_final_eb = samples_eb['non_final']

            optimizer.zero_grad()
            pt.set_grad_enabled(True)

            expected_values_actions = model.compute_expected_values_actions(
                next_states=next_states_eb, rewards=rewards_eb)

            values_actions, classifications, (h, c) = model(states_eb)

            values_selected_actions = model.gather_values_selected_actions(
                values_actions=values_actions, actions=actions_eb)

            weighted_loss, weighted_value_action_loss, weighted_classification_loss = model.compute_losses(
                values_selected_actions, expected_values_actions, classifications, states_labels_eb)

            weighted_loss.backward()
            optimizer.step()

            pt.set_grad_enabled(False)
            print(weighted_loss.item(), weighted_value_action_loss.item(), weighted_classification_loss.item())

        # scheduler.step()

        loss_e = running_loss_e / n_samples_e
        accuracy_e = running_corrects_e / n_samples_e

        loss_str_e = cp_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        print('Epoch: {:d}. Training.   Loss: {:s}. Accuracy: {:s}.'.format(e, loss_str_e, accuracy_str_e))

        stats['lines'][e][stats['headers']['Training Loss']] = loss_e
        stats['lines'][e][stats['headers']['Training Accuracy']] = accuracy_e

        # validation phase
        model.eval()  # Set model to evaluate mode

        criterion.eval()

        # zero the parameter gradients
        optimizer.zero_grad()

        pt.set_grad_enabled(False)

        running_loss_e = 0.0
        running_corrects_e = 0

        n_samples_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['validation']:
            # forward
            outputs = model(batch_eb)
            _, preds = pt.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            running_loss_e += loss_eb.item() * batch_eb.shape[loader['validation'].batch_axis_inputs]
            # noinspection PyTypeChecker
            running_corrects_e += pt.sum(preds == labels_eb).item()

            n_samples_e += batch_eb.shape[loader['validation'].batch_axis_inputs]

            b += 1

        loss_e = running_loss_e / n_samples_e
        accuracy_e = running_corrects_e / n_samples_e

        loss_str_e = cp_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        stats['lines'][e][stats['headers']['Validation Loss']] = loss_e
        stats['lines'][e][stats['headers']['Validation Accuracy']] = accuracy_e

        if accuracy_e > highest_accuracy:
            highest_accuracy = accuracy_e
            highest_accuracy_str = cp_strings_format_float_to_str(highest_accuracy, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 1
            stats['lines'][e][stats['headers']['Highest Validation Accuracy']] = highest_accuracy
        else:
            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 0
            stats['lines'][e][stats['headers']['Highest Validation Accuracy']] = highest_accuracy

        if loss_e < lowest_loss:

            lowest_loss = loss_e
            lowest_loss_str = cp_strings_format_float_to_str(lowest_loss, n_decimals=n_decimals_for_printing)
            i = 0
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 1
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Validation Loss']] = lowest_loss

            best_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
            for directory_i in [directory_best_model, directory_best_model_state]:
                if os.path.isfile(directory_i):
                    os.remove(directory_i)

            pt.save(model, directory_best_model)
            pt.save(best_model_wts, directory_best_model_state)

        else:
            i += 1
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 0
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Validation Loss']] = lowest_loss

        last_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
        for directory_i in [directory_last_model, directory_last_model_state, directory_stats]:
            if os.path.isfile(directory_i):
                os.remove(directory_i)

        pt.save(model, directory_last_model)
        pt.save(last_model_wts, directory_last_model_state)

        cp_txt.lines_to_csv_file(stats['lines'], directory_stats, stats['headers'])

        print('Epoch: {:d}. Validation. Loss: {:s}. Lowest Loss: {:s}. Accuracy: {:s}. Highest Accuracy: {:s}.'.format(
            e, loss_str_e, lowest_loss_str, accuracy_str_e, highest_accuracy_str))

        print('Epoch {e} - Unsuccessful Epochs {i}.'.format(e=e, i=i))

        e += 1
        print(dashes)

    print()
    E = e

    time_training = cp_timer.get_delta_time()

    print('Training completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_training.days, h=time_training.hours,
        m=time_training.minutes, s=time_training.seconds))
    print('Number of Epochs: {E:d}'.format(E=E))
    print('Lowest Validation Loss: {:s}'.format(lowest_loss_str))
    print('Highest Validation Accuracy: {:s}'.format(highest_accuracy_str))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model


class ReplayMemory:
    """A simple numpy replay buffer."""

    def __init__(self, axis_time, axis_features):
        self.states = []
        self.states_labels = []
        self.actions = []
        self.next_states = []
        self.rewards = []
        # self.non_final = []

        self.axis_time = axis_time
        self.axis_features = axis_features

    def put(self, states=None, states_labels=None, actions=None, next_states=None, rewards=None):#, non_final):

        self.states.append(states)
        self.states_labels.append(states_labels)

        if next_states is not None:
            self.actions.append(actions)
            self.next_states.append(next_states)
            self.rewards.append(rewards)
        # if transition[5] is not None:
            # self.non_final.append(transition[5])

    def sample(self):

        T = len(self.states)

        states = pt.cat(self.states, dim=self.axis_time)

        C = len(self.states_labels[0])
        states_labels = [[None for t in range(0, T, 1)] for c in range(0, C, 1)]  # type: list
        for c in range(0, C, 1):
            for t in range(0, T, 1):
                states_labels[c][t] = self.states_labels[t][c]
            states_labels[c] = pt.cat(states_labels[c], dim=self.axis_time)

        T = len(self.next_states)
        A = len(self.actions[0])
        actions = [[None for t in range(0, T, 1)] for a in range(0, A, 1)]  # type: list
        for a in range(0, A, 1):
            for t in range(0, T, 1):
                if self.actions[t][a] is not None:
                    actions[a][t] = self.actions[t][a]
            actions[a] = pt.cat(actions[a], dim=self.axis_time)#.unsqueeze(dim=self.axis_features)

        next_states = pt.cat(self.next_states, dim=self.axis_time)

        rewards = pt.cat(self.rewards, dim=self.axis_time)#.unsqueeze(dim=self.axis_features)

        # non_final = pt.cat(self.non_final, dim=self.axis_time)#.unsqueeze(dim=self.axis_features)

        return dict(
            states=states, states_labels=states_labels, actions=actions,
            next_states=next_states, rewards=rewards)  #, non_final=non_final)

    def __len__(self) -> int:
        return len(self.states)
