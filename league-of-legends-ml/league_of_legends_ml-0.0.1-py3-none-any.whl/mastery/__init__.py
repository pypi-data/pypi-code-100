try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from . import files
import pickle
import numpy


def predict(duration_seconds: int, victory: bool) -> int:
    print('opening model')
    with pkg_resources.open_binary(files, 'model.pkl') as file:
        model = pickle.load(file)
    print('opening scaler')
    with pkg_resources.open_binary(files, 'scaler.pkl') as file:
        scaler = pickle.load(file)
    print('creating input')
    data = numpy.array([[duration_seconds, int(victory)]])
    print('scaling input')
    scaled_data = scaler.transform(data)
    print('computiong input')
    result = model.predict(scaled_data)
    print('returning')
    return round(result[0])
