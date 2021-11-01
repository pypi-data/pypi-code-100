# websites:
# https://pytorch.org/docs/stable/torchvision/transforms.html
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py
# https://pytorch.org/hub/pytorch_vision_resnet/
# https://discuss.pytorch.org/t/normalize-each-input-image-in-a-batch-independently-and-inverse-normalize-the-output/23739
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

from . import torch
import numpy as np
from .. import clock as cp_clock
from ..strings import format_float_to_str as cp_strings_format_float_to_str


def feature_classifier(model, loader, criterion):
    cp_timer = cp_clock.Timer()

    headers_stats = ['N_samples', *['C_' + str(g) for g in range(loader.G)], 'Loss', 'Accuracy']

    n_columns_stats = len(headers_stats)
    line_stats = [loader.n_samples, *loader.n_conditions_directories_inter, None, None]  # type: list

    stats = {
        'headers': {headers_stats[i]: i for i in range(n_columns_stats)},
        'lines': [line_stats]}

    headers_trials = [
        'ID_Trial',
        *['Condition_' + str(g) for g in range(loader.G)],
        'Label',
        *['Probability_' + str(k) for k in range(loader.K[0])],
        'Classification',
        'Correct_Classification'
    ]

    n_columns_trials = len(headers_trials)

    trials = {
        'headers': {headers_trials[i]: i for i in range(n_columns_trials)},
        'lines': None}

    n_decimals_for_printing = 6

    if model.training:
        model.eval()  # Set model to evaluate mode

    if criterion.training:
        criterion.eval()

    softmax = torch.nn.Softmax(dim=1)
    if softmax.training:
        softmax.eval()

    # Now set requires_grad to false
    for param_model in model.parameters():
        param_model.requires_grad = False

    for param_criterion in criterion.parameters():
        param_criterion.requires_grad = False

    for param_softmax in softmax.parameters():
        param_softmax.requires_grad = False

    torch.set_grad_enabled(False)

    running_loss_e = 0.0
    running_corrects_e = 0

    n_samples_e = 0

    start_index_samples = 0
    stop_index_samples = 0

    index_combinations_e = np.empty(2, dtype='O')
    index_combinations_e[1] = slice(0, loader.G, 1)
    combinations_e = np.empty([loader.n_samples_e, loader.G], dtype='O')

    index_probabilities_e = np.empty(2, dtype='O')
    index_probabilities_e[1] = slice(0, loader.K[0], 1)
    probabilities_e = np.empty([loader.n_samples_e, loader.K[0]], dtype='O')

    index_labels_e = np.empty(2, dtype='O')
    index_labels_e[1] = 0
    labels_e = np.empty([loader.n_samples_e, 1], dtype='O')

    classifications_e = labels_e.copy()

    correct_classifications_e = labels_e.copy()

    id_trials = np.arange(loader.n_samples_e, dtype='O')[:, None]

    # b = 0
    # Iterate over data.
    for data_eb in loader:
        samples_eb, labels_eb, combinations_eb = data_eb

        # forward
        outputs_eb = model(samples_eb)
        probabilities_eb = softmax(outputs_eb)
        _, classifications_eb = torch.max(outputs_eb, 1)
        correct_classifications_eb = (classifications_eb == labels_eb).long()
        loss_eb = criterion(outputs_eb, labels_eb)

        n_samples_eb = samples_eb.shape[loader.batch_axis_inputs]
        n_samples_e += n_samples_eb

        # stop_index_samples += n_samples_eb
        stop_index_samples = n_samples_e
        index_samples = slice(start_index_samples, stop_index_samples, 1)

        index_combinations_e[0] = index_samples
        combinations_e[tuple(index_combinations_e)] = combinations_eb.tolist()

        index_probabilities_e[0] = index_samples
        probabilities_e[tuple(index_probabilities_e)] = probabilities_eb.tolist()

        index_labels_e[0] = index_samples
        labels_e[tuple(index_labels_e)] = labels_eb.tolist()

        classifications_e[tuple(index_labels_e)] = classifications_eb.tolist()

        correct_classifications_e[tuple(index_labels_e)] = correct_classifications_eb.tolist()

        start_index_samples = stop_index_samples

        running_loss_e += loss_eb.item() * n_samples_eb
        # noinspection PyTypeChecker
        running_corrects_e += torch.sum(correct_classifications_eb).item()

        # b += 1

    loss_e = running_loss_e / n_samples_e
    accuracy_e = running_corrects_e / n_samples_e

    stats['lines'][0][stats['headers']['Loss']] = loss_e
    stats['lines'][0][stats['headers']['Accuracy']] = accuracy_e

    trials['lines'] = np.concatenate(
        (id_trials, combinations_e, labels_e, probabilities_e, classifications_e, correct_classifications_e),
        axis=1)

    loss_str_e = cp_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
    accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

    print('Test. Loss: {:s}. Accuracy: {:s}.'.format(loss_str_e, accuracy_str_e))
    print()

    time_test = cp_timer.get_delta_time()

    print('Test completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_test.days, h=time_test.hours,
        m=time_test.minutes, s=time_test.seconds))

    return stats, trials


def passive_feature_sequence_classifier(model, loader, criterion):
    cp_timer = cp_clock.Timer()

    headers_stats = ['N_samples', *['C_' + str(g) for g in range(loader.G)], 'Loss', 'Accuracy']

    n_columns_stats = len(headers_stats)
    line_stats = [loader.n_samples, *loader.n_conditions_directories_inter, None, None]  # type: list

    stats = {
        'headers': {headers_stats[i]: i for i in range(n_columns_stats)},
        'lines': [line_stats]}

    headers_trials = [
        'ID_Trial',
        *['Condition_' + str(g) for g in range(loader.G)],
        'Label',
        *['Probability_' + str(k) for k in range(loader.K[0])],
        'Classification',
        'Correct_Classification'
    ]

    n_columns_trials = len(headers_trials)

    trials = {
        'headers': {headers_trials[i]: i for i in range(n_columns_trials)},
        'lines': None}

    n_decimals_for_printing = 6

    model.return_output_sequence = True

    if model.training:
        model.eval()  # Set model to evaluate mode

    if criterion.training:
        criterion.eval()

    softmax = torch.nn.Softmax(dim=2)
    if softmax.training:
        softmax.eval()

    # Now set requires_grad to false
    for param_model in model.parameters():
        param_model.requires_grad = False

    for param_criterion in criterion.parameters():
        param_criterion.requires_grad = False

    for param_softmax in softmax.parameters():
        param_softmax.requires_grad = False

    torch.set_grad_enabled(False)

    running_loss_e = 0.0
    running_corrects_e = 0

    n_samples_e = 0

    start_index_samples = 0
    stop_index_samples = 0

    index_combinations_e = np.empty(2, dtype='O')
    index_combinations_e[1] = slice(0, loader.G, 1)
    combinations_e = np.empty([loader.n_samples_e, loader.G], dtype='O')

    index_probabilities_e = np.empty(2, dtype='O')
    index_probabilities_e[1] = slice(0, loader.K[0], 1)
    probabilities_e = np.empty([loader.n_samples_e, loader.K[0]], dtype='O')

    index_labels_e = np.empty(2, dtype='O')
    index_labels_e[1] = 0
    labels_e = np.empty([loader.n_samples_e, 1], dtype='O')

    classifications_e = labels_e.copy()

    correct_classifications_e = labels_e.copy()

    id_trials = np.arange(loader.n_samples_e, dtype='O')[:, None]

    indexes_sequence_out_eb = [None, None, slice(0, model.K, 1)]  # type: list
    # shape_loss_eb = [None, None]  # type: list
    # indexes_loss_eb = [None, None]  # type: list

    indexes_probabilities_str_eb = [None, None, None]  # type: list

    indexes_classifications_str_eb = [None, None]  # type: list

    indexes_correct_classifications_eb = [None, None]  # type: list
    indexes_correct_classifications_eb[model.axis_lstm_sequence] = -1

    # b = 0
    # Iterate over data.
    for data_eb in loader:
        samples_eb, labels_eb, combinations_eb = data_eb

        # forward
        sequence_out_eb, out_eb = model(samples_eb)
        probabilities_eb = softmax(sequence_out_eb)
        _, classifications_eb = torch.max(sequence_out_eb, 2)
        correct_classifications_eb = (classifications_eb == labels_eb.unsqueeze(model.axis_lstm_sequence)).long()

        T = samples_eb.shape[model.axis_lstm_sequence]
        B = samples_eb.shape[model.axis_lstm_batch]

        # shape_loss_eb[model.axis_lstm_sequence] = T
        # shape_loss_eb[model.axis_lstm_batch] = B
        # loss_eb = torch.empty(shape_loss_eb, dtype=torch.float32, device=sequence_out_eb.device)
        loss_eb = torch.empty(T, dtype=torch.float32, device=sequence_out_eb.device)

        indexes_sequence_out_eb[model.axis_lstm_batch] = slice(0, B, 1)

        for t in range(0, T, 1):

            indexes_sequence_out_eb[model.axis_lstm_sequence] = t

            loss_eb[t] = criterion(sequence_out_eb[tuple(indexes_sequence_out_eb)], labels_eb)

        n_samples_eb = samples_eb.shape[loader.batch_axis_inputs]
        n_samples_e += n_samples_eb

        # stop_index_samples += n_samples_eb
        stop_index_samples = n_samples_e
        index_samples = slice(start_index_samples, stop_index_samples, 1)

        index_combinations_e[0] = index_samples
        combinations_e[tuple(index_combinations_e)] = combinations_eb.tolist()

        index_labels_e[0] = index_samples
        labels_e[tuple(index_labels_e)] = labels_eb.tolist()

        probabilities_formatted_eb = np.empty([B, model.K], dtype='O')
        probabilities_str_eb = probabilities_eb.cpu().numpy().astype('U')
        indexes_probabilities_str_eb[model.axis_lstm_sequence] = slice(0, T, 1)

        for s in range(0, B, 1):
            indexes_probabilities_str_eb[model.axis_lstm_batch] = s
            for k in range(0, model.K, 1):

                indexes_probabilities_str_eb[model.axis_lstm_features] = k

                probabilities_formatted_eb[s, k] = ' '.join(probabilities_str_eb[tuple(indexes_probabilities_str_eb)])

        index_probabilities_e[0] = index_samples
        probabilities_e[tuple(index_probabilities_e)] = probabilities_formatted_eb.tolist()
        # probabilities_e[tuple(index_probabilities_e)] = [probabilities_eb[indexes_sequence_out_eb].tolist()]

        classifications_formatted_eb = np.empty([B], dtype='O')
        classifications_str_eb = classifications_eb.cpu().numpy().astype('U')

        correct_classifications_formatted_eb = np.empty([B], dtype='O')
        correct_classifications_str_eb = correct_classifications_eb.cpu().numpy().astype('U')

        indexes_classifications_str_eb[model.axis_lstm_sequence] = slice(0, T, 1)

        for s in range(0, B, 1):
            indexes_classifications_str_eb[model.axis_lstm_batch] = s

            classifications_formatted_eb[s] = ' '.join(classifications_str_eb[tuple(indexes_classifications_str_eb)])

            correct_classifications_formatted_eb[s] = ' '.join(correct_classifications_str_eb[tuple(indexes_classifications_str_eb)])

        classifications_e[tuple(index_labels_e)] = classifications_formatted_eb.tolist()

        correct_classifications_e[tuple(index_labels_e)] = correct_classifications_formatted_eb.tolist()

        start_index_samples = stop_index_samples

        running_loss_e += loss_eb[-1].item() * n_samples_eb

        indexes_correct_classifications_eb[model.axis_lstm_batch] = slice(0, B, 1)
        running_corrects_e += torch.sum(correct_classifications_eb[tuple(indexes_correct_classifications_eb)]).item()

        # b += 1

    loss_e = running_loss_e / n_samples_e
    accuracy_e = running_corrects_e / n_samples_e

    stats['lines'][0][stats['headers']['Loss']] = loss_e
    stats['lines'][0][stats['headers']['Accuracy']] = accuracy_e

    trials['lines'] = np.concatenate(
        (id_trials, combinations_e, labels_e, probabilities_e, classifications_e, correct_classifications_e),
        axis=1)

    loss_str_e = cp_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
    accuracy_str_e = cp_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

    print('Test. Loss: {:s}. Accuracy: {:s}.'.format(loss_str_e, accuracy_str_e))
    print()

    time_test = cp_timer.get_delta_time()

    print('Test completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_test.days, h=time_test.hours,
        m=time_test.minutes, s=time_test.seconds))

    return stats, trials
