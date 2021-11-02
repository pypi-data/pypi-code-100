# import libsbn
# import libsbn.beagle_flags as beagle_flags
# import numpy as np
#
# inst = libsbn.rooted_instance('cheese')
# inst.read_newick_file('data/fluA.tree')
# inst.read_fasta_file('data/fluA.fasta')
# inst.parse_dates_from_taxon_names(True)
# spec = libsbn.PhyloModelSpecification(
#     substitution='GTR', site='weibull+4', clock='strict'
# )
# inst.prepare_for_phylo_likelihood(spec, 1, [beagle_flags.VECTOR_SSE], False)
#
# # initialize model parameters
# phylo_model_param_block_map = inst.get_phylo_model_param_block_map()
# phylo_model_param_block_map["substitution model rates"][:] = np.repeat(1 / 6, 6)
# phylo_model_param_block_map["substitution model frequencies"][:] = np.repeat(1 / 4, 4)
# phylo_model_param_block_map["Weibull shape"][:] = np.array([0.5])
# phylo_model_param_block_map["clock rate"][:] = np.array([0.001])
#
# log_prob = np.array(inst.log_likelihoods())[0]
# print('log_prob', log_prob)  # log likliehood + log determinant of node height transform
#
# brito_grad = inst.phylo_gradients()[0]
# ratios_root_height_grad = np.array(brito_grad.gradient['ratios_root_height'])
# gtr_grad = np.array(brito_grad.gradient['substitution_model'])
# # not interested in the strict clock and weibull gradients but it is calculated
# print('GTR rates gradient', gtr_grad[:5])
# print('GTR freqs gradient', gtr_grad[5:])
# print(
#     'root height gradient', ratios_root_height_grad[-1]
# )  # log determinant of node height transform NOT included
#
# # log det jacobian of node height transform is coming from here:
# det_jacobian_grad = libsbn.ratio_gradient_of_height_gradient(
#     inst.tree_collection.trees[0],
#     ratios_root_height_grad,
# )
# print('Log det Jacobian gradient', det_jacobian_grad)
#
# exit(0)
#
# # instead we could have something like:
# from libsbn.flags import (
#     CLOCK_MODEL_RATES,
#     RATIOS_ROOT_HEIGHT,
#     SITE_MODEL_PARAMETERS,
#     SUBSTITUTION_MODEL_FREQUENCIES,
#     SUBSTITUTION_MODEL_RATES,
# )
#
# # initialize with enums
# phylo_model_param_block_map[SUBSTITUTION_MODEL_RATES][:] = np.repeat(1 / 6, 6)
# phylo_model_param_block_map[SUBSTITUTION_MODEL_FREQUENCIES][:] = np.repeat(1 / 4, 4)
# phylo_model_param_block_map[SITE_MODEL_PARAMETERS][:] = np.array([0.5])
# phylo_model_param_block_map[CLOCK_MODEL_RATES][:] = np.array([0.001])
#
# # provide a separate method to calculate the log det jacobian of the node height
# # transform  so it is not included in inst.log_likelihoods. This would be the
# # equivalent of ratio_gradient_of_height_gradient for gradient
# log_det_jacobian = libsbn.log_det_jacobian_height_transform(
#     inst.tree_collection.trees[0]
# )
#
# # request and calculate gradients for RATIOS_ROOT_HEIGHT,
# # SUBSTITUTION_MODEL_FREQUENCIES, SUBSTITUTION_MODEL_RATES
# brito_grad = inst.phylo_gradients(
#     {RATIOS_ROOT_HEIGHT, SUBSTITUTION_MODEL_FREQUENCIES, SUBSTITUTION_MODEL_RATES}
# )[0]
# ratios_root_height = np.array(brito_grad.gradient[RATIOS_ROOT_HEIGHT])
# gtr_rates_grad = np.array(brito_grad.gradient[SUBSTITUTION_MODEL_RATES])
# gtr_freqs_grad = np.array(brito_grad.gradient[SUBSTITUTION_MODEL_FREQUENCIES])
# try:
#     clock_grad = np.array(brito_grad.gradient[CLOCK_MODEL_RATES])
# except RuntimeError:
#     exit(1)
