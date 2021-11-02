"""
Database of interaction models for classical molecular dynamics
and Monte Carlo simulations
"""

import os
import glob
import json


def _validate_model(model):
    assert 'potential' in model
    assert 'cutoff' in model
    assert isinstance(model.get("potential"), list)
    assert isinstance(model.get("cutoff"), list)

def _validate_sample(sample):
    assert 'path' in sample

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

def read(file_json):
    """Read a single json model file and return the entry as a dict"""
    with open(file_json) as fh:
        try:
            model = json.load(fh)
        except (ValueError, json.decoder.JSONDecodeError):
            print('Error with file {}'.format(file_json))
            raise

    # Guess paths from potential and cutoff types
    _validate_model(model)

    # Unless they are web links, sample paths are assumed relative to this file
    if "samples" in model:
        for sample in model.get("samples"):
            _validate_sample(sample)
            if not sample.get("path").startswith("http"):
                here = os.path.dirname(__file__)
                sample["path"] = os.path.join(here, sample.get("path"))

    return model

def available():
    """Pretty print the available models"""
    print('Available models:')
    for model in database:
        print('- {:20s} [{}]'.format(model, database[model].get("reference")))

def get(model):
    """Get a model from database"""
    if model in database:
        return database[model]
    else:
        raise KeyError('Model {} not present in database'.format(model))
        
def copy(sample, output_path=None):
    """Get a copy of `sample` configuration and return the path to it"""
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

def add(path):
    """
    Add all json files in `path` to the global `database`
    """    
    for _path in glob.glob('{}/*.json'.format(path)):
        # Be forgiving
        if not os.path.exists(_path):
            continue
        # Model name is file basename
        name = os.path.basename(_path)[:-5]
        model = read(_path)
        database[name] = model

# Singleton
database = {}

# By default, load all json files in module path
add(os.path.join(os.path.dirname(__file__)))
