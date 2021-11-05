import tensorflow as tf
from tensorflow.python.framework import load_library
lib = load_library.load_op_library("./_reco_ops.so")
print(dir(lib))
