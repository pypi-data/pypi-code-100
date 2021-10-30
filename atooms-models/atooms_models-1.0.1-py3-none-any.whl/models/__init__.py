import os
import glob
import json


def validate_model(model):
    assert 'potential' in model
    assert 'cutoff' in model
    assert isinstance(model.get("potential"), list)
    assert isinstance(model.get("cutoff"), list)

def validate_sample(sample):
    assert 'path' in sample

def read_json(file_json):
    """Read a single json model file and return the entry as a dict"""
    with open(file_json) as fh:
        try:
            model = json.load(fh)
        except (ValueError, json.decoder.JSONDecodeError):
            print('Error with file {}'.format(file_json))
            raise

    # Guess paths from potential and cutoff types
    validate_model(model)

    # Unless they are web links, sample paths are assumed relative to this file
    if "samples" in model:
        for sample in model.get("samples"):
            validate_sample(sample)
            if not sample.get("path").startswith("http"):
                here = os.path.dirname(__file__)
                sample["path"] = os.path.join(here, sample.get("path"))

    return model

def load(layout="atooms", path='atooms_models'):
    """
    Load all json files in this package and in `path`
    """
    db_paths = glob.glob(os.path.join(os.path.dirname(__file__), '*.json'))
    included_paths = glob.glob('{}/*.json'.format(path))
    database = {}
    for path in db_paths + included_paths:
        # Be forgiving
        if not os.path.exists(path):
            continue
        # Model name is file basename
        name = os.path.basename(path)[:-5]
        model = read_json(path)
        database[name] = model
    return database

def show():
    db = load()
    for model in db:
        print('- {:20s} [{}]'.format(model, db[model].get("reference")))

def _wget(url, output_dir):
    import sys
    import os
    import shutil
    try:
        from urllib.request import urlopen  # Python 3
    except ImportError:
        from urllib2 import urlopen  # Python 2

    basename = os.path.basename(url)
    output_file = os.path.join(output_dir, basename)
    response = urlopen(url)
    length = 16*1024
    with open(output_file, 'wb') as fh:
        shutil.copyfileobj(response, fh, length)

def copy(sample, output_path=None):
    import tempfile
    import shutil
    input_path = sample.get("path")

    if output_path is None:
        tmpdir = tempfile.mkdtemp()
        basename = os.path.basename(input_path)
        output_path = os.path.join(tmpdir, basename)

    if input_path.startswith('http'):
        _wget(input_path, tmpdir)
    else:
        # Assume it is relative
        shutil.copy(input_path, output_path)
    return output_path


# Singleton
database = load()
