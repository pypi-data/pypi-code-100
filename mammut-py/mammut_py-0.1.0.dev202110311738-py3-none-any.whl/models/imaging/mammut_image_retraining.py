# coding=utf-8
import Augmentor
import logging
import numpy as np
import os
from PIL import Image
import shutil
import tensorflow as tf
from tensorflow_hub.tools.make_image_classifier import (
    make_image_classifier as retrain_script,
)

import mammut
from mammut import BASE_MODEL_VISON_DIR

log = logging.getLogger(__name__)


# retrain_script = make_image_classifier.make_image_classifier


def set_dir_as_category(directory):
    images = os.listdir(directory)
    for index, image in enumerate(images):
        image_category = ".".join(image.split(".")[:-1])
        new_path = directory + "/" + image_category
        if not os.path.isdir(new_path):
            src = directory + "/" + image
            dst = directory + "/" + image_category + "/" + image
            if not os.path.exists(new_path) and os.path.isfile(src):
                os.makedirs(new_path)
            if os.path.isfile(src):
                shutil.move(src, dst)


def augmentate_images(directory, samples):
    image_categories = os.listdir(directory)
    for category in image_categories:
        # print(directory + category + '/')
        p = Augmentor.Pipeline(directory + category + "/", "")
        p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
        p.zoom(probability=0.5, min_factor=1.1, max_factor=1.5)
        p.flip_left_right(probability=0.5)
        p.sample(samples)


def persist_retrained_model(retrained_graph_folder, labels):
    # obtener el current model name
    identifier = get_time_stamp_identifier(retrained_graph_folder, False)
    model_path, dir_base_name = (
        os.path.split(retrained_graph_folder)
        if os.path.split(retrained_graph_folder)[1] != ""
        else os.path.split(os.path.split(retrained_graph_folder)[0])
    )
    saved_model_dir = model_path + "/" + dir_base_name + identifier
    labels_output_file = saved_model_dir + "/" + "labels_output_file.txt"
    if os.path.exists(saved_model_dir):
        shutil.copy(labels, labels_output_file)
        shutil.move(saved_model_dir, retrained_graph_folder)


def retrain(
    image_dir,
    summaries_dir="/tmp/retrain_logs",
    tflite_output_file="/tmp/tflite_output_file.tflite",
    labels_output_file="/tmp/labels_output_file.txt",
    saved_model_dir="",
    train_epochs=10,
    should_create_new=True,
):
    # mod timestamp
    # si recibe crear_nuevo creamos uno nuevo
    # verificamos si hay mas que el maximo de modelos permitidos y borrmaos el mas viejo
    # sino devolvemos el mas nuevo/current
    identifier = get_time_stamp_identifier(saved_model_dir, should_create_new)
    model_path, dir_base_name = (
        os.path.split(saved_model_dir)
        if os.path.split(saved_model_dir)[1] != ""
        else os.path.split(os.path.split(saved_model_dir)[0])
    )
    saved_model_dir = model_path + "/" + dir_base_name + identifier
    print(saved_model_dir)

    if image_dir is not None:
        retrain_script.FLAGS.image_dir = image_dir
    # no available in tensorflow-hub 0.8 but looks like after it will (check master)
    # if summaries_dir is not None:
    #     retrain_script.FLAGS.summaries_dir = summaries_dir
    if tflite_output_file is not None:
        retrain_script.FLAGS.tflite_output_file = tflite_output_file
    if labels_output_file is not None:
        retrain_script.FLAGS.labels_output_file = labels_output_file
    if saved_model_dir is not None:
        retrain_script.FLAGS.saved_model_dir = saved_model_dir
    if train_epochs is not None:
        retrain_script.FLAGS.train_epochs = train_epochs
    for flag_key in retrain_script.FLAGS:
        flag = retrain_script.FLAGS[flag_key]
        flag.present += 1
    retrain_script.main(None)


MAX_MODELS_NUM = 3


def get_all_saved_models_timestamps(saved_models_dir):
    model_path, dir_base_name = (
        os.path.split(saved_models_dir)
        if os.path.split(saved_models_dir)[1] != ""
        else os.path.split(os.path.split(saved_models_dir)[0])
    )

    all_models = []
    for i in os.listdir(model_path):
        if dir_base_name in i:
            all_models.append(i)

    time_stamps = ["".join(i.split(dir_base_name + "-")) for i in all_models]

    datetime_objects = []
    for i in time_stamps:
        try:
            datetime_objects.append(mammut.str_parse_datetime(i))
        except Exception as ex:
            print(ex)

    return datetime_objects


def get_time_stamp_identifier(saved_model_dir, should_create_new):
    if should_create_new:
        # crea nuevo, obtiene todos elimina el mas viejo
        identifier = "-" + mammut.get_str_format_timezone_aware_datetime_now()
        all_timestamps = get_all_saved_models_timestamps(saved_model_dir)
        if len(all_timestamps) >= MAX_MODELS_NUM:
            older_model_identifier = "-" + mammut.str_format_datetime(
                min(all_timestamps)
            )
            model_path, dir_base_name = (
                os.path.split(saved_model_dir)
                if os.path.split(saved_model_dir)[1] != ""
                else os.path.split(os.path.split(saved_model_dir)[0])
            )
            older_model_name = model_path + "/" + dir_base_name + older_model_identifier
            print("delete model:", older_model_name)
            shutil.rmtree(older_model_name)
    else:
        # obtiene todos y retorna el mas nuevo
        all_timestamps = get_all_saved_models_timestamps(saved_model_dir)
        identifier = "-" + mammut.str_format_datetime(max(all_timestamps))

    return identifier


def load_labels(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_top_labels(
    tflite_output_file: str,
    image_file: str,
    label_file: str,
    top_count: int = 5,
    input_mean: float = 127.5,
    input_std: float = 127.5,
):
    interpreter = tf.lite.Interpreter(model_path=tflite_output_file)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # check the type of the input tensor
    floating_model = input_details[0]["dtype"] == np.float32

    # NxHxWxC, H:1, W:2
    height = input_details[0]["shape"][1]
    width = input_details[0]["shape"][2]
    img = Image.open(image_file).resize((width, height))

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_tensor(input_details[0]["index"], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]["index"])
    results = np.squeeze(output_data)

    labels = load_labels(label_file)
    if top_count > len(labels):
        top_count = len(labels)
    top_k = results.argsort()[-top_count:][::-1]
    top_labels = []
    for i in top_k:
        if floating_model:
            log.debug("{:08.6f}: {}".format(float(results[i]), labels[i]))
        else:
            log.debug("{:08.6f}: {}".format(float(results[i] / 255.0), labels[i]))
        top_labels.append((labels[i], results[i]))
    return top_labels


def label_image(
    tflite_output_file: str,
    image_file: str,
    label_file,
    top_count: int = 5,
    input_mean: float = 127.5,
    input_std: float = 127.5,
):
    top_labels = get_top_labels(
        tflite_output_file, image_file, label_file, top_count, input_mean, input_std
    )
    return top_labels[0][0]


def augmentate_and_retrain(directory: str, mammut_id: int, samples: int):
    base_dir_name = BASE_MODEL_VISON_DIR + "/" + str(mammut_id) + "/vision"
    augmentate_images(directory, samples)
    test_dir = directory
    training_sumaries_dir = base_dir_name + "/tf_summary"
    tflite_output_file = base_dir_name + "/saved_model.pb"
    labels_output_file = base_dir_name + "/labels_output_file.txt"
    retrianed_graph_folder = base_dir_name + "/models/place_recognition/"
    if not os.path.isdir(retrianed_graph_folder):
        os.makedirs(retrianed_graph_folder)
    retrain(
        test_dir,
        training_sumaries_dir,
        tflite_output_file,
        labels_output_file,
        retrianed_graph_folder,
    )
    return tflite_output_file, labels_output_file
