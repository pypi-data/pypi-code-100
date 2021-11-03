from typing import Union

from instancelib.instances.base import InstanceProvider
from instancelib.environment.text import TextEnvironment
from instancelib.instances.text import TextInstanceProvider
from instancelib.labels.memory import MemoryLabelProvider
from instancelib.analysis.base import label_metrics

from text_sensitivity.perturbation.base import Perturbation


def apply_perturbation(dataset: Union[InstanceProvider, TextEnvironment],
                       perturbation: Perturbation):
    if isinstance(dataset, TextEnvironment):
        dataset = dataset.dataset
    if not isinstance(perturbation, Perturbation):
        perturbation = perturbation()

    new_data, attributes = [], []

    for key in dataset:
        for instances, labels in perturbation(dataset[key]):
            new_data.extend(instances) if isinstance(instances, list) else new_data.append(instances)
            attributes.extend(labels) if isinstance(labels, list) else attributes.append(labels)

    instanceprovider = TextInstanceProvider(new_data)
    instanceprovider.add_range(*dataset.dataset.get_all())
    labelprovider = MemoryLabelProvider.from_tuples(attributes)

    return instanceprovider, labelprovider


def equal_ground_truth(ground_truth, instances):
    # TODO: add ability to provide a different expectation of what will happen to the instance labels after perturbation
    for key in instances.keys():
        parent_key = key.split('|')[0] if isinstance(key, str) else str(key)
        parent_key = int(parent_key) if parent_key.isdigit() else parent_key
        yield (key, ground_truth._labeldict[parent_key])


def compare_metric(env, model, perturbation):
    """Get metrics for each ground-truth label and attribute."""
    instances, attributes = apply_perturbation(env, perturbation)
    model_predictions = MemoryLabelProvider.from_tuples(model.predict(instances))
    ground_truth = MemoryLabelProvider.from_tuples(equal_ground_truth(env.labels, instances))

    for label in list(model_predictions.labelset):
        for attribute in list(attributes.labelset):
            metrics = label_metrics(model_predictions,
                                    ground_truth,
                                    attributes.get_instances_by_label(attribute),
                                    label)
            yield label, attribute, metrics


def compare_accuracy(*args, **kwargs):
    """Compare accuracy scores for each ground-truth label and attribute."""
    import pandas as pd
    return pd.DataFrame([(label, attribute, metrics.accuracy)
                         for label, attribute, metrics in compare_metric(*args, **kwargs)],
                        columns=['label', 'attribute', 'accuracy'])


def compare_precision(*args, **kwargs):
    """Compare precision scores for each ground-truth label and attribute."""
    import pandas as pd
    return pd.DataFrame([(label, attribute, metrics.precision)
                         for label, attribute, metrics in compare_metric(*args, **kwargs)],
                        columns=['label', 'attribute', 'precision'])


def compare_recall(*args, **kwargs):
    """Compare recall scores for each ground-truth label and attribute."""
    import pandas as pd
    return pd.DataFrame([(label, attribute, metrics.recall)
                         for label, attribute, metrics in compare_metric(*args, **kwargs)],
                        columns=['label', 'attribute', 'recall'])
