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
        model, loader, preprocess, optimizer, scheduler, I=10, E=None, T=None, reward_bias=0, epsilon=0,
        directory_outputs=None):

    cp_timer = cp_clock.Timer()

    for key_loader_k in loader.keys():
        if key_loader_k == 'training' or key_loader_k == 'validation':
            pass
        else:
            raise ValueError('Unknown keys in loader')

    headers = [
        'Epoch', 'Unsuccessful_Epochs',

        'Training_Unweighted_Loss', 'Training_Weighted_Loss',
        'Training_Unweighted_Value_Action_Loss', 'Training_Weighted_Value_Action_Loss',
        'Training_Unweighted_Classification_Loss', 'Training_Weighted_Classification_Loss',
        'Training_Accuracy',

        'Validation_Unweighted_Loss', 'Validation_Weighted_Loss',
        'Validation_Unweighted_Value_Action_Loss', 'Validation_Weighted_Value_Action_Loss',

        'Validation_Unweighted_Classification_Loss',
        'Lowest_Validation_Unweighted_Classification_Loss',
        'Is_Lower_Validation_Unweighted_Classification_Loss',

        'Validation_Weighted_Classification_Loss',
        'Lowest_Validation_Weighted_Classification_Loss',
        'Is_Lower_Validation_Weighted_Classification_Loss',

        'Validation_Accuracy', 'Highest_Validation_Accuracy', 'Is_Higher_Accuracy']

    n_columns = len(headers)
    new_line_stats = [None for i in range(0, n_columns, 1)]  # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    if directory_outputs is None:
        directory_outputs = 'outputs'

    os.makedirs(directory_outputs, exist_ok=True)

    directory_model_at_last_epoch = os.path.join(directory_outputs, 'model_at_last_epoch.pth')

    directory_model_with_lowest_unweighted_classification_loss = os.path.join(
        directory_outputs, 'model_with_lowest_unweighted_classification_loss.pth')

    directory_model_with_lowest_weighted_classification_loss = os.path.join(
        directory_outputs, 'model_with_lowest_weighted_classification_loss.pth')

    directory_model_with_highest_accuracy = os.path.join(
        directory_outputs, 'model_with_highest_accuracy.pth')

    directory_stats = os.path.join(directory_outputs, 'stats.csv')

    n_decimals_for_printing = 6

    best_model_wts = copy.deepcopy(model.state_dict())

    lowest_unweighted_classification_loss = math.inf
    lowest_unweighted_classification_loss_str = str(lowest_unweighted_classification_loss)

    lowest_weighted_classification_loss = math.inf
    lowest_weighted_classification_loss_str = str(lowest_unweighted_classification_loss)

    highest_accuracy = -math.inf
    highest_accuracy_str = str(highest_accuracy)

    if E is None:
        E = math.inf

    if I is None:
        I = math.inf

    if T is None:
        T = math.inf

    model.eval()
    model.freeze()
    pt.set_grad_enabled(False)

    i = 0
    e = 0

    n_dashes = 130
    dashes = '-' * n_dashes
    print(dashes)

    while (e < E) and (i < I):

        print('Epoch {e} ...'.format(e=e))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e

        # Each epoch has a training and a validation phase
        # training phase

        running_unweighted_loss_e = 0
        running_unweighted_value_action_loss_e = 0
        running_unweighted_classification_loss_e = 0

        running_weighted_loss_e = 0
        running_weighted_value_action_loss_e = 0
        running_weighted_classification_loss_e = 0

        running_n_corrects_e = 0
        n_classifications_e = 0

        n_samples_e = 0

        b = 0
        # Iterate over data.
        for environments_eb in loader['training']:

            replay_memory = ReplayMemory(axis_time=model.axis_sequence_lstm, axis_features=model.axis_features_lstm)

            h_ebt, c_ebt = None, None

            t = 0
            for state_ebt, labels_ebt in environments_eb:

                labels_ebt = [pt.unsqueeze(labels_ebtc, dim=model.axis_sequence_lstm) for labels_ebtc in labels_ebt]

                action_ebt, classifications_ebt, (h_ebt, c_ebt) = model.sample_action(
                    state_ebt, h=h_ebt, c=c_ebt, epsilon=epsilon)

                rewards_ebt = None

                replay_memory.put(
                    states=state_ebt, states_labels=labels_ebt, actions=action_ebt,
                    next_states=None, rewards=rewards_ebt)

                if t > 0:
                    replay_memory.rewards[t - 1] = model.get_previous_rewards(
                        classifications=classifications_ebt, labels=labels_ebt, reward_bias=reward_bias)

                if preprocess is None:
                    delta_ebt = action_ebt
                else:
                    delta_ebt = preprocess(action_ebt)

                environments_eb.step(delta_ebt)

                t += 1

                if t >= T:
                    break

            replay_memory.actions[-1] = None
            # replay_memory.actions.pop()
            # replay_memory.rewards.pop()

            samples_eb = replay_memory.sample()
            states_eb = samples_eb['states']
            states_labels_eb = samples_eb['states_labels']
            actions_eb = samples_eb['actions']
            next_states_eb = samples_eb['next_states']
            rewards_eb = samples_eb['rewards']
            # non_final_eb = samples_eb['non_final']

            expected_values_actions = model.compute_expected_values_actions(
                next_states=next_states_eb, rewards=rewards_eb)

            pt.set_grad_enabled(True)
            model.unfreeze()
            model.train()

            optimizer.zero_grad()

            values_actions, classifications, (h, c) = model(states_eb)

            values_actions = model.remove_last_values_actions(values_actions)

            values_selected_actions = model.gather_values_selected_actions(
                values_actions=values_actions, actions=actions_eb)

            weighted_loss_eb, weighted_value_action_loss_eb, weighted_classification_loss_eb = (
                model.compute_weighted_losses(
                    values_selected_actions=values_selected_actions, expected_values_actions=expected_values_actions,
                    classifications=classifications, labels=states_labels_eb))

            weighted_loss_eb.backward()
            optimizer.step()

            model.eval()
            model.freeze()
            pt.set_grad_enabled(False)

            unweighted_loss_eb, unweighted_value_action_loss_eb, unweighted_classification_loss_eb = (
                model.compute_unweighted_losses(
                    values_selected_actions=values_selected_actions, expected_values_actions=expected_values_actions,
                    classifications=classifications, labels=states_labels_eb))

            n_samples_eb = states_eb.shape[loader['training'].batch_axis_inputs]

            running_unweighted_loss_e += unweighted_loss_eb.item() * n_samples_eb
            running_unweighted_value_action_loss_e += unweighted_value_action_loss_eb.item() * n_samples_eb
            running_unweighted_classification_loss_e += unweighted_classification_loss_eb.item() * n_samples_eb

            running_weighted_loss_e += weighted_loss_eb.item() * n_samples_eb
            running_weighted_value_action_loss_e += weighted_value_action_loss_eb.item() * n_samples_eb
            running_weighted_classification_loss_e += weighted_classification_loss_eb.item() * n_samples_eb

            n_corrects_eb, n_classifications_eb = model.compute_corrects(
                classifications=classifications, labels=states_labels_eb)

            running_n_corrects_e += n_corrects_eb
            n_classifications_e += n_classifications_eb

            n_samples_e += n_samples_eb

            b += 1

        # scheduler.step()

        unweighted_loss_e = running_unweighted_loss_e / n_samples_e
        unweighted_value_action_loss_e = running_unweighted_value_action_loss_e / n_samples_e
        unweighted_classification_loss_e = running_unweighted_classification_loss_e / n_samples_e

        weighted_loss_e = running_weighted_loss_e / n_samples_e
        weighted_value_action_loss_e = running_weighted_value_action_loss_e / n_samples_e
        weighted_classification_loss_e = running_weighted_classification_loss_e / n_samples_e

        accuracy_e = running_n_corrects_e / n_classifications_e

        unweighted_loss_str_e = cp_strings_format_float_to_str(
            unweighted_loss_e, n_decimals=n_decimals_for_printing)
        unweighted_value_action_loss_str_e = cp_strings_format_float_to_str(
            unweighted_value_action_loss_e, n_decimals=n_decimals_for_printing)
        unweighted_classification_loss_str_e = cp_strings_format_float_to_str(
            unweighted_classification_loss_e, n_decimals=n_decimals_for_printing)

        weighted_loss_str_e = cp_strings_format_float_to_str(
            weighted_loss_e, n_decimals=n_decimals_for_printing)
        weighted_value_action_loss_str_e = cp_strings_format_float_to_str(
            weighted_value_action_loss_e, n_decimals=n_decimals_for_printing)
        weighted_classification_loss_str_e = cp_strings_format_float_to_str(
            weighted_classification_loss_e, n_decimals=n_decimals_for_printing)

        accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        stats['lines'][e][stats['headers']['Training_Unweighted_Loss']] = unweighted_loss_e
        stats['lines'][e][stats['headers']['Training_Unweighted_Value_Action_Loss']] = unweighted_value_action_loss_e
        stats['lines'][e][stats['headers']['Training_Unweighted_Classification_Loss']] = \
            unweighted_classification_loss_e

        stats['lines'][e][stats['headers']['Training_Weighted_Loss']] = weighted_loss_e
        stats['lines'][e][stats['headers']['Training_Weighted_Value_Action_Loss']] = weighted_value_action_loss_e
        stats['lines'][e][stats['headers']['Training_Weighted_Classification_Loss']] = weighted_classification_loss_e

        stats['lines'][e][stats['headers']['Training_Accuracy']] = accuracy_e

        print('Epoch: {:d}. Training.  Unweighted Value Action Loss: {:s}. Unweighted Classification Loss: {:s}. '
            'Accuracy: {:s}.'.format(
                e, unweighted_value_action_loss_str_e, unweighted_classification_loss_str_e, accuracy_str_e))

        # validation phase

        running_unweighted_loss_e = 0
        running_unweighted_value_action_loss_e = 0
        running_unweighted_classification_loss_e = 0

        running_weighted_loss_e = 0
        running_weighted_value_action_loss_e = 0
        running_weighted_classification_loss_e = 0

        running_n_corrects_e = 0
        n_classifications_e = 0

        n_samples_e = 0

        b = 0
        # Iterate over data.
        for environments_eb in loader['validation']:

            replay_memory = ReplayMemory(axis_time=model.axis_sequence_lstm, axis_features=model.axis_features_lstm)

            h_ebt, c_ebt = None, None

            t = 0
            for state_ebt, labels_ebt in environments_eb:

                labels_ebt = [pt.unsqueeze(labels_ebtc, dim=model.axis_sequence_lstm) for labels_ebtc in labels_ebt]

                action_ebt, classifications_ebt, (h_ebt, c_ebt) = model.sample_action(
                    state_ebt, h=h_ebt, c=c_ebt, epsilon=0)

                rewards_ebt = None

                replay_memory.put(
                    states=state_ebt, states_labels=labels_ebt, actions=action_ebt,
                    next_states=None, rewards=rewards_ebt)

                if t > 0:
                    replay_memory.rewards[t - 1] = model.get_previous_rewards(
                        classifications=classifications_ebt, labels=labels_ebt, reward_bias=reward_bias)

                if preprocess is None:
                    delta_ebt = action_ebt
                else:
                    delta_ebt = preprocess(action_ebt)

                environments_eb.step(delta_ebt)

                t += 1

                if t >= T:
                    break

            replay_memory.actions[-1] = None
            # replay_memory.actions.pop()
            # replay_memory.rewards.pop()

            samples_eb = replay_memory.sample()
            states_eb = samples_eb['states']
            states_labels_eb = samples_eb['states_labels']
            actions_eb = samples_eb['actions']
            next_states_eb = samples_eb['next_states']
            rewards_eb = samples_eb['rewards']
            # non_final_eb = samples_eb['non_final']

            expected_values_actions = model.compute_expected_values_actions(
                next_states=next_states_eb, rewards=rewards_eb)

            values_actions, classifications, (h, c) = model(states_eb)

            values_actions = model.remove_last_values_actions(values_actions)

            values_selected_actions = model.gather_values_selected_actions(
                values_actions=values_actions, actions=actions_eb)

            weighted_loss_eb, weighted_value_action_loss_eb, weighted_classification_loss_eb = (
                model.compute_weighted_losses(
                    values_selected_actions=values_selected_actions, expected_values_actions=expected_values_actions,
                    classifications=classifications, labels=states_labels_eb))

            unweighted_loss_eb, unweighted_value_action_loss_eb, unweighted_classification_loss_eb = (
                model.compute_unweighted_losses(
                    values_selected_actions=values_selected_actions, expected_values_actions=expected_values_actions,
                    classifications=classifications, labels=states_labels_eb))

            n_samples_eb = states_eb.shape[loader['validation'].batch_axis_inputs]

            running_unweighted_loss_e += unweighted_loss_eb.item() * n_samples_eb
            running_unweighted_value_action_loss_e += unweighted_value_action_loss_eb.item() * n_samples_eb
            running_unweighted_classification_loss_e += unweighted_classification_loss_eb.item() * n_samples_eb

            running_weighted_loss_e += weighted_loss_eb.item() * n_samples_eb
            running_weighted_value_action_loss_e += weighted_value_action_loss_eb.item() * n_samples_eb
            running_weighted_classification_loss_e += weighted_classification_loss_eb.item() * n_samples_eb

            n_corrects_eb, n_classifications_eb = model.compute_corrects(
                classifications=classifications, labels=states_labels_eb)

            running_n_corrects_e += n_corrects_eb
            n_classifications_e += n_classifications_eb

            n_samples_e += n_samples_eb

            b += 1

        # scheduler.step()

        unweighted_loss_e = running_unweighted_loss_e / n_samples_e
        unweighted_value_action_loss_e = running_unweighted_value_action_loss_e / n_samples_e
        unweighted_classification_loss_e = running_unweighted_classification_loss_e / n_samples_e

        weighted_loss_e = running_weighted_loss_e / n_samples_e
        weighted_value_action_loss_e = running_weighted_value_action_loss_e / n_samples_e
        weighted_classification_loss_e = running_weighted_classification_loss_e / n_samples_e

        accuracy_e = running_n_corrects_e / n_classifications_e

        unweighted_loss_str_e = cp_strings_format_float_to_str(
            unweighted_loss_e, n_decimals=n_decimals_for_printing)
        unweighted_value_action_loss_str_e = cp_strings_format_float_to_str(
            unweighted_value_action_loss_e, n_decimals=n_decimals_for_printing)
        unweighted_classification_loss_str_e = cp_strings_format_float_to_str(
            unweighted_classification_loss_e, n_decimals=n_decimals_for_printing)

        weighted_loss_str_e = cp_strings_format_float_to_str(
            weighted_loss_e, n_decimals=n_decimals_for_printing)
        weighted_value_action_loss_str_e = cp_strings_format_float_to_str(
            weighted_value_action_loss_e, n_decimals=n_decimals_for_printing)
        weighted_classification_loss_str_e = cp_strings_format_float_to_str(
            weighted_classification_loss_e, n_decimals=n_decimals_for_printing)

        accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        stats['lines'][e][stats['headers']['Validation_Unweighted_Loss']] = unweighted_loss_e
        stats['lines'][e][stats['headers']['Validation_Unweighted_Value_Action_Loss']] = unweighted_value_action_loss_e
        stats['lines'][e][stats['headers']['Validation_Unweighted_Classification_Loss']] = \
            unweighted_classification_loss_e

        stats['lines'][e][stats['headers']['Validation_Weighted_Loss']] = weighted_loss_e
        stats['lines'][e][stats['headers']['Validation_Weighted_Value_Action_Loss']] = weighted_value_action_loss_e
        stats['lines'][e][stats['headers']['Validation_Weighted_Classification_Loss']] = weighted_classification_loss_e

        stats['lines'][e][stats['headers']['Validation_Accuracy']] = accuracy_e

        model_dict = copy.deepcopy(model.state_dict())
        if os.path.isfile(directory_model_at_last_epoch):
            os.remove(directory_model_at_last_epoch)
        pt.save(model_dict, directory_model_at_last_epoch)

        is_successful_epoch = False

        if unweighted_classification_loss_e < lowest_unweighted_classification_loss:

            lowest_unweighted_classification_loss = unweighted_classification_loss_e
            lowest_unweighted_classification_loss_str = cp_strings_format_float_to_str(
                lowest_unweighted_classification_loss, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is_Lower_Validation_Unweighted_Classification_Loss']] = 1
            is_successful_epoch = True

            if os.path.isfile(directory_model_with_lowest_unweighted_classification_loss):
                os.remove(directory_model_with_lowest_unweighted_classification_loss)
            pt.save(model_dict, directory_model_with_lowest_unweighted_classification_loss)
        else:
            stats['lines'][e][stats['headers']['Is_Lower_Validation_Unweighted_Classification_Loss']] = 0

        stats['lines'][e][stats['headers']['Lowest_Validation_Unweighted_Classification_Loss']] = \
            lowest_unweighted_classification_loss


        if weighted_classification_loss_e < lowest_weighted_classification_loss:

            lowest_weighted_classification_loss = weighted_classification_loss_e
            lowest_weighted_classification_loss_str = cp_strings_format_float_to_str(
                lowest_weighted_classification_loss, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is_Lower_Validation_Weighted_Classification_Loss']] = 1
            is_successful_epoch = True

            if os.path.isfile(directory_model_with_lowest_weighted_classification_loss):
                os.remove(directory_model_with_lowest_weighted_classification_loss)
            pt.save(model_dict, directory_model_with_lowest_weighted_classification_loss)
        else:
            stats['lines'][e][stats['headers']['Is_Lower_Validation_Weighted_Classification_Loss']] = 0

        stats['lines'][e][stats['headers']['Lowest_Validation_Weighted_Classification_Loss']] = \
            lowest_weighted_classification_loss


        if accuracy_e > highest_accuracy:
            highest_accuracy = accuracy_e
            highest_accuracy_str = cp_strings_format_float_to_str(
                highest_accuracy, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is_Higher_Accuracy']] = 1
            is_successful_epoch = True

            if os.path.isfile(directory_model_with_highest_accuracy):
                os.remove(directory_model_with_highest_accuracy)
            pt.save(model_dict, directory_model_with_highest_accuracy)
        else:
            stats['lines'][e][stats['headers']['Is_Higher_Accuracy']] = 0

        stats['lines'][e][stats['headers']['Highest_Validation_Accuracy']] = highest_accuracy

        if is_successful_epoch:
            i = 0
        else:
            i += 1
        stats['lines'][e][stats['headers']['Unsuccessful_Epochs']] = i

        if os.path.isfile(directory_stats):
            os.remove(directory_stats)

        cp_txt.lines_to_csv_file(stats['lines'], directory_stats, stats['headers'])

        print(
            'Epoch: {:d}. Validation.  Unweighted Value Action Loss: {:s}. Unweighted Classification Loss: {:s}. '
            'Accuracy: {:s}.'.format(
                e, unweighted_value_action_loss_str_e, unweighted_classification_loss_str_e, accuracy_str_e))

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
    print('Lowest Unweighted_Classification Loss: {:s}'.format(lowest_unweighted_classification_loss_str))
    print('Lowest Weighted_Classification Loss: {:s}'.format(lowest_weighted_classification_loss_str))
    print('Highest Accuracy: {:s}'.format(highest_accuracy_str))

    return None


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
        self.actions.append(actions)

        self.next_states.append(next_states)

        self.rewards.append(rewards)

        # if non_final is not None:
            # self.non_final.append(non_final)

    def sample(self):

        T = len(self.states)

        states = pt.cat([s for s in self.states if s is not None], dim=self.axis_time)

        C = len(self.states_labels[0])
        states_labels = [pt.cat(
            [self.states_labels[t][c] for t in range(0, T, 1) if self.states_labels[c] is not None],
            dim=self.axis_time) for c in range(0, C, 1)]

        A = len(self.actions[0])
        actions = [pt.cat(
            [self.actions[t][a] for t in range(0, T, 1) if self.actions[t] is not None],
            dim=self.axis_time) for a in range(0, A, 1)]

        next_states = [n for n in self.next_states if n is not None]
        if len(next_states) == 0:
            ind = tuple(
                [slice(0, states.shape[d], 1) if d != self.axis_time else slice(1, T, 1)
                 for d in range(0, states.ndim, 1)])
            next_states = states[ind]
        else:
            next_states = pt.cat(next_states, dim=self.axis_time)

        rewards = pt.cat([r for r in self.rewards if r is not None], dim=self.axis_time)

        # non_final = pt.cat(self.non_final, dim=self.axis_time)

        return dict(
            states=states, states_labels=states_labels, actions=actions,
            next_states=next_states, rewards=rewards)  #, non_final=non_final)

    def __len__(self) -> int:
        return len(self.states)
