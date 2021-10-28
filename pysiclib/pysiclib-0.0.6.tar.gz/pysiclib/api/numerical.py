from .._pysiclib import numerical as _impl_numerical
from .._pysiclib.numerical import *

#differentiation

#intial value
def initial_value_problem(
	system_of_eqs,
	inital_conditions,
	target_value,
	initial_value = 0.0):

	return _impl_numerical.initial_value_problem(
		system_of_eqs,
		inital_conditions,
		target_value,
		initial_value
	)

#integration
def integral_index_interval(
	input_array, start_index = 0, end_index = None):
	if end_index == None:
		end_index = len(input_array)
	return _impl_numerical.integral_index_interval(
		input_array, start_index, end_index)

#sol equations
def equation_solution(equation_as_function, target_val, precision = 6):
	output_val =\
		_impl_numerical.equation_solution(equation_as_function, target_val)
	if (output_val == None):
		 return None
	else:
		return round(output_val, precision)
