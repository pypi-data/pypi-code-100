try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from . import files
import pickle
import numpy


def predict(duration_seconds: int, victory: bool) -> int:
    with pkg_resources.open_binary(files, 'model.pkl') as file:
        model = pickle.load(file)
    with pkg_resources.open_binary(files, 'scaler.pkl') as file:
        scaler = pickle.load(file)
    data = numpy.array([[duration_seconds, int(victory)]])
    scaled_data = scaler.transform(data)
    result = model.predict(scaled_data)
    return round(result[0])
