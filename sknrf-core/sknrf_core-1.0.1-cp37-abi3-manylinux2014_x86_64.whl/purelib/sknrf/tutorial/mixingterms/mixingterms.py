# __author__ = 'dtbespal'
#
# import time
# import itertools
#
# import numpy as np
# from numba.decorators import jit
#
#
# """Nomenclature:
#    p...P input port
#    l...L input harmonic
#    r...R output port
#    s...S output harmonic
#    k...K nonlinear order
#    m...M memory depth
#    n...N time sample index
# """
#
#
# def calculate_siso_mixing_terms(num_outputs, num_inputs, max_order, timeout=3600):
# # def calculate_siso_mixing_terms(num_outputs, num_inputs, max_order, mixing_terms=None, timeout=3600):
#     """Calucaltes siso Mixing terms uisng exhaustive search algorithm based on the number of inputs, outputs, and
#     maximum order
#
#     :param num_inputs: The number of harmonic inputs
#     :param num_outputs: The number of harmonic outputs
#     :param max_order: The maximum order of a mixing product during this iteration
#     :param mixing_terms: Then mixing terms from a previous iteration
#     :param timeout: Time limit in min
#     :return: mixing_terms
#
#     calculate_SISO_mixing_terms(num_inputs,num_outputs,max_order): calculates the mixing terms based on the number of
#     harmonic inputs and outputs that are less than or equal to the max_order.
#
#     calculateSISOMixingTerms(num_inputs,num_outputs,max_order):appends higher order mixing terms up to max_order to
#     an existing mixing_terms. Note mixing_terms[num_inputs,0] must be re-calculated.
#
#     f_input = companion rfvector [-num_inputs,...-k,...,-2,-1,0,1,2,...k,...num_inputs] used to calculate the output
#     frequency of the mixing product
#
#     mixing_terms[num_inputs][output_index] is a 2*num_inputs+1 by i matrix of unique mixing product basis vectors that
#     generate a response at the "output_index" harmonic using "num_inputs" incident tones
#
#     mixing_terms[num_inputs, 0] is the unique DC mixing product exponents
#     mixing_terms[num_inputs, output_index>0] is the unique AC mixing product exponents
#
#     mixing_terms[num_inputs, 0] are the BB terms
#     mixing_terms[num_inputs][output] are the AC terms
#     """
#
#     min_order = 1
#     # if mixing_terms is None:
#     mixing_terms = [[None]*(num_outputs+1)]*(num_inputs+1)
#     # else:
#     #     assert len(mixing_terms[num_inputs]) == num_outputs+1,\
#     #         "The number of outputs: " + str(num_outputs) + "does not impedance length of mixing products: "\
#     #         + str(len(mixing_terms[num_inputs]))
#     #     for mixing_term_in_out in mixing_terms[num_inputs]:
#     #         min_order = max([max(sum(mixing_term_in_out, 1)), min_order])
#     #     min_order += 1
#
#     f_input = np.matrix(np.arange(-1*num_inputs, num_inputs+1, 1))
#     max_exponent = max_order
#     max_time = time.time() + timeout
#
#     for output_index in range(0, num_outputs+1):
#         if output_index:
#             mixing_terms[num_inputs][output_index] = np.matrix(np.zeros((2*num_inputs+1, 0), dtype=np.int))
#         else:
#             # Append a pre-determined DC mixing exponent (a_00)
#             mixing_terms[num_inputs][output_index] = np.matrix(np.zeros((2*num_inputs+1, 1), dtype=np.int))
#             mixing_terms[num_inputs][output_index][num_inputs, output_index] = 1
#
#         for order in range(1, 2*num_inputs+1):
#             y_out = np.matrix(np.zeros((2*num_inputs+1, 1), dtype=np.int))
#             while True:
#                 # if(timeout)
#                 #     %Timeout
#                 #     obj.BBTerms = [];
#                 #     obj.RFTerms = cell(num_outputs,1);
#                 #     obj.saveMixingTerms();
#                 #     return;
#                 # end
#                 # Determine output harmonic, by calculating output_index = f_input*y_out
#                 if output_index == f_input*y_out and np.sum(y_out) == order:
#                     # Solve for X_p = y_out/mixing_terms[num_inputs][0]
#                     [multiple, new_basis] = factor_vector(y_out, mixing_terms[num_inputs][0])
#                     # if X_0 is not an integer array, it cannot be factored
#                     if not multiple and output_index:
#                         # Solve for X_p = y_out-X_p*mixing_terms[num_inputs, 0]
#                         [multiple, new_basis] = factor_vector(new_basis, mixing_terms[num_inputs][output_index])
#                         # if X_p is not an integer array, it cannot be factored
#                         if ~multiple:
#                             # Append to mixing term
#                             mixing_terms[num_inputs][output_index] = np.append(mixing_terms[num_inputs][output_index],
#                                                                                new_basis, axis=1)
#                     elif not multiple and not output_index:
#                         # Append new_basis to mixing_terms[num_inputs][0][:,end+1]
#                         mixing_terms[num_inputs][output_index] = np.append(mixing_terms[num_inputs][output_index],
#                                                                            new_basis, axis=1)
#                         # Add the conjugate bias if it is unique
#                         if np.any(new_basis != new_basis[::-1]):
#                             mixing_terms[num_inputs][output_index] = np.append(mixing_terms[num_inputs][output_index],
#                                                                                new_basis[::-1], axis=1)
#
#                 # Check for end of y_out loop
#                 if np.all(y_out == max_exponent):
#                     break
#
#                 # Check for time-out
#                 if time.time() > max_time:
#                     return
#
#                 # Generate a new y_out
#                 for idx in range(len(y_out)):
#                     if y_out[idx] < max_exponent:
#                         y_out[idx] += 1
#                         if idx > 0:
#                             y_out[0:idx] = 0
#                         break
#
#     # Remove the higher order bases from mixing_terms[num_inputs][0]
#     for idx in reversed(range(np.size(mixing_terms[num_inputs][0], 1))):
#         if np.sum(mixing_terms[num_inputs][0][:, idx]) > max_order:
#             np.delete(mixing_terms[num_inputs][0], idx, 1)
#
#     return mixing_terms
#
#
# @jit
# def factor_vector(y, d):
#     """Factors mixing term to determine if it is linearly independent
#
#     :param y: non-unique rfvector representing a mixing term
#     :param d: list of unique basis vectors
#     :return: multiple, new_basis
#
#     [multiple,new_basis] = factor_vector(y,d) Empirically factors rfvector y as multiple of the basis vectors
#     represented by each column of d
#
#     x is a multiplier rfvector that creates y from unique basis vectors in d
#     """
#
#     # Assume new basis if d is empty
#     if not d.size:
#         multiple = np.zeros(np.size(y, 1), dtype=bool)
#         new_basis = y.copy()
#         return multiple, new_basis
#
#     new_basis = y.copy()
#     multiple = np.zeros(np.size(y, 1), dtype=bool)
#     for col in range(0, np.size(y, 1)):
#         x = np.matrix(np.zeros((np.size(d, 1), 1), dtype=int))
#         x_old = np.matrix(np.zeros((np.size(d, 1), 1), dtype=int))
#
#         while True:
#             y_iter = d*x
#             # Check for solution y == d*x
#             if np.all(y[:, col] == y_iter):
#                 multiple[col] = True
#                 break
#
#             # Check that y_new does not exceed any of y
#             if np.any(y_iter > y[:, col]):
#                 # Record the remainder
#                 remainder = y[:, col] - d*x_old
#                 order = np.sum(remainder)
#                 # Check for lowest remainder
#                 if order < np.sum(new_basis[:, col]):
#                     new_basis[:, col] = remainder
#
#                 # Optimization: skip over useless iterations in the nested loop
#                 changed = x > x_old
#                 changed_indexes = np.where(np.squeeze(np.asarray(changed)))
#                 if changed_indexes[-1]+1 < len(x):
#                     x[:changed_indexes[-1]+1] = 0
#                     x[changed_indexes[-1]+1] += 1
#                 else:
#                     multiple[col] = False
#                     break
#             else:
#                 # Normal incrementing of x
#                 x_old = x.copy()
#                 x[0] += 1
#
#     return multiple, new_basis
#
#
# def calculate_multi_tone_mixing_terms(num_outputs, num_inputs, max_order, num_tones, mixing_terms=None, timeout=3600):
#     """Calucaltes multi-tone frequencies list based on the SISO mixing terms
#
#     :param num_inputs: The number of harmonic inputs
#     :param num_outputs: The number of harmonic outputs
#     :param max_order: The maximum order of a mixing product during this iteration
#     :param num_tones: The initial number of incident tones applied applied at the fundamental frequency
#     :param mixing_terms: Then mixing terms from a SISO system
#     :param timeout: Time limit in min
#     :return: freq_list: A list of frequencies uniquely defined by num_outputs, num_inputs, max_order, num_tones
#     """
#     mixing_terms = calculate_siso_mixing_terms(num_outputs, num_inputs, max_order, timeout=timeout)
#     tones = np.arange(0, num_tones)-(num_tones-1)/2
#     f_input = np.matrix(np.arange(-1*num_inputs, num_inputs+1, 1))
#     freq_list = [[None]*(num_outputs+1)]*(num_inputs+1)
#     for output_index in range(0, num_outputs+1):
#         freq_list_in_out = []
#         for mixing_term in mixing_terms[num_inputs][output_index].T:
#             # Generate all possible tone products for the number of non-zero mixing terms
#             scaled_mixing_term = mixing_term[np.nonzero(np.multiply(f_input, mixing_term))]
#             tone_products = itertools.product(tones, repeat=np.count_nonzero(mixing_term > 0))
#             for tone_product in tone_products:
#                 freq_list_in_out.append(np.sum(np.multiply(tone_product, scaled_mixing_term)))
#         freq_list[num_inputs][output_index] = np.unique(np.array(freq_list_in_out))
#     return freq_list
#
#
# if __name__ == "__main__":
#     inputs_idx = 2
#     outputs_idx = 5
#     order_idx = 5
#     tones_idx = 2
#     mixing_terms_list = calculate_siso_mixing_terms(outputs_idx, inputs_idx, order_idx)
#     print(mixing_terms_list)
#     # frequency_list = calculate_multi_tone_mixing_terms(outputs_idx, inputs_idx, order_idx, tones_idx)
#     # print(frequency_list[inputs_idx])