#!/usr/bin/env python

"""Tests for `scatrex` package."""

import pytest

import scatrex
from scatrex import models
import numpy as np
import matplotlib.pyplot as plt
import jax

# Tests
G = 1000
N = 100
K = 2
s = N*G
fig, axs = plt.subplots(1, 5, figsize=(20,4))
for i, theta in enumerate([1, 5, 10, 50, 100]):
    plt.sca(axs[i])
    # Test compound distribution of unobserved factors
    omega = np.random.gamma(1/theta, 1, size=s)
    qsi = np.random.normal(0, omega)
    # Plot histograms of both
    # fig = plt.figure(figsize=(6,6))
    # plt.hist(qsi, bins=100)
    # plt.legend()
    # plt.show()
    # Test noise factor distribution
    w = np.random.normal(0, 1/np.sqrt(np.random.gamma(theta, 1., size=K)), size=[G, K])
    h = np.random.normal(0, 1, size=[N, K])
    n = h.dot(w.T).ravel()

    # fig = plt.figure(figsize=(6,6))
    # plt.hist(w)
    # plt.legend()
    # plt.show()

    # fig = plt.figure(figsize=(6,6))
    plt.hist(qsi, bins=100, label=r'$\xi$', density=True)
    plt.hist(n, bins=100, label=r'$h  w$', density=True, alpha=0.5)
    plt.legend()
    plt.yscale('log')
    plt.title(rf'$\theta$ = {theta}')
    if i == 0:
        plt.ylabel('log density')
    plt.xlabel('support')
plt.show()

K = 1
w = np.random.normal(0, np.sqrt(1/np.random.gamma(2, 1, size=K)), size=[G, K])
h = np.random.normal(0, 1, size=[N, K])
n = h.dot(w.T)
plt.pcolormesh(n); plt.ylabel('cells'); plt.xlabel('genes'); plt.title(r'$h w$, $K = 1$'); plt.colorbar(); plt.show()

K = 2
w = np.random.normal(0, np.sqrt(1/np.random.gamma(2, 1, size=K)), size=[G, K])
h = np.random.normal(0, 1, size=[N, K])
n = h.dot(w.T)
omega = np.random.gamma(0.01, 1, size=s)
qsi = np.random.normal(0, omega)
plt.hist(qsi, bins=100, label=r'$\xi$', density=True)
plt.hist(n.ravel(), bins=100, label=rf'$h  w$, $K = {K}$', density=True, alpha=0.5)
plt.legend()
plt.yscale('log')
plt.ylabel('log density')
plt.xlabel('support')
plt.show()



# Simulate a tree
theta = 100
sim_sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=dict(log_lib_size_mean=10, num_global_noise_factors=0,
                                                                            global_noise_factors_precisions_shape=10, unobserved_factors_kernel_concentration=1./theta))
sim_sca.simulate_tree(observed_tree=None, n_extra_per_observed=1, n_genes=100, seed=42)
sim_sca.ntssb.reset_node_parameters(node_hyperparams=sim_sca.model_args)
sim_sca.observed_tree.create_adata()
sim_sca.observed_tree.plot_heatmap(vmax=4, vmin=0)
sim_sca.simulate_data(n_cells=100)
sim_sca.normalize_data()
sim_sca.project_data()
sim_sca.ntssb.plot_tree(counts=True)
sim_sca.plot_tree_proj(s=50)
sim_sca.plot_unobserved_parameters()

plt.pcolormesh(sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False))
plt.colorbar()
plt.show()


nodes = sim_sca.ntssb.get_nodes()
for node in nodes:
    plt.plot(node.unobserved_factors)
    plt.show()

plt.hist(sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False).ravel())

import scanpy as sc
sc.pp.neighbors(sim_sca.adata)

noise = sim_sca.ntssb.root['node'].root['node'].cell_global_noise_factors_weights_caller().dot(sim_sca.ntssb.root['node'].root['node'].global_noise_factors_caller())
log_corrected_data = sim_sca.adata.raw.X - np.exp(noise)
corrected_data
sim_sca.adata.X = sim_sca.adata.raw.X
sc.pp.normalize_total(sim_sca.adata, target_sum=1e4)
sc.pp.log1p(sim_sca.adata)
sim_sca.adata.X = sim_sca.adata.X - noise
sim_sca.adata.X.max()
sc.pp.scale(sim_sca.adata, max_value=10)
sim_sca.adata.X.min()
sc.tl.pca(sim_sca.adata, svd_solver='arpack')
sc.pp.neighbors(sim_sca.adata, n_neighbors=10, n_pcs=40)
sc.tl.umap(sim_sca.adata)
sc.pl.umap(sim_sca.adata, color='node')

sim_sca.ntssb.root['node'].root['node'].cell_global_noise_factors_weights_caller().dot(sim_sca.ntssb.root['node'].root['node'].global_noise_factors_caller()).shape
sim_sca.ntssb.root['node'].root['node'].variational_parameters['globals']['cell_noise_mean'].dot(sim_sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean']).shape
sc.tl.umap(sim_sca.adata)
sc.pl.umap(sim_sca.adata)
sim_sca.adata
sc.pl.umap(sim_sca.adata, color='node')


sim_sca.plot_tree()

import scanpy as sc
sim_sca.compute_smoothed_expression(window_size=10, clip=2)
sc.pl.heatmap(sim_sca.adata, sim_sca.adata.var_names, groupby='node', cmap=None, show=True, use_raw=False, show_gene_labels=False, layer='smoothed')

sc.pl.heatmap(sim_sca.adata, sim_sca.adata.var_names, groupby='node', cmap=None, show=True, use_raw=False, show_gene_labels=False)

sim_sca.plot_unobserved_parameters(estimated=False)

jax.config.update("jax_debug_nans", False)
# jax.config.update("jax_debug_infs", True)

# Create a new object for the inference
sca = scatrex.SCATrEx(model=models.cna, verbose=True)
sca.add_data(sim_sca.adata.raw.to_adata())
sca.set_observed_tree(sim_sca.observed_tree)
sca.normalize_data()
sca.project_data()

# Run clonealign
elbos = sca.learn_clonemap(n_iters=5000, filter_genes=False, step_size=0.01)

plt.pcolormesh(sca.ntssb.root['node'].root['node'].get_noise(variational=True))
plt.colorbar()
plt.show()

sca.ntssb.elbo

sca.plot_tree_proj(project=True, s=50)


args = dict(global_noise_factors_precisions_shape=2.,log_lib_size_mean=10, num_global_noise_factors=2, unobserved_factors_kernel_concentration=.01)
sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=args)
sca.add_data(sim_sca.adata.raw.to_adata())
sca.set_observed_tree(sim_sca.observed_tree)
sca.normalize_data()
sca.project_data()
sca.ntssb = scatrex.ntssb.NTSSB(sca.observed_tree, sca.model.Node, node_hyperparams=sca.model_args)
sca.ntssb.add_data(np.array(sca.adata.raw.X), to_root=True)
sca.ntssb.root['node'].root['node'].reset_data_parameters()
sca.ntssb.reset_variational_parameters()
init_baseline = np.mean(sca.ntssb.data / np.sum(sca.ntssb.data, axis=1).reshape(-1,1) * sca.ntssb.data.shape[1], axis=0)
init_baseline = init_baseline / init_baseline[0]
init_log_baseline = np.log(init_baseline[1:])
init_log_baseline = np.clip(init_log_baseline, -1, 1)
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'] = init_log_baseline
# sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'] = sim_sca.ntssb.root['node'].root['node'].global_noise_factors

sca.ntssb.elbo
sca.ntssb.root['node'].root['node'].num_global_noise_factors = 1
self = sca.ntssb.root['node'].root['node']
self.variational_parameters['globals']['cell_noise_mean'] = np.zeros((self.tssb.ntssb.num_data, self.num_global_noise_factors))
self.variational_parameters['globals']['cell_noise_log_std'] = -np.ones((self.tssb.ntssb.num_data, self.num_global_noise_factors))
self.variational_parameters['globals']['noise_factors_mean'] = np.zeros((self.num_global_noise_factors, self.n_genes))
self.variational_parameters['globals']['noise_factors_log_std'] = -np.ones((self.num_global_noise_factors, self.n_genes))
self.variational_parameters['globals']['factor_precision_log_means'] = np.log(self.global_noise_factors_precisions_shape)*np.ones((self.num_global_noise_factors))
self.variational_parameters['globals']['factor_precision_log_stds'] = -np.ones((self.num_global_noise_factors))
sca.ntssb.elbo
elbos = sca.ntssb.optimize_elbo(root_node=None, local_node=None, mb_size=100, step_size=0.01, sticks_only=False, num_samples=1, n_iters=5000, threshold=1e-3, max_nodes=5, run=True)
sca.ntssb.elbo
noise_factors = sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean']

sca.ntssb.merge_nodes('C-0', 'C')
new_node = sca.ntssb.pivot_reattach_to('C', 'A-0')
sca.ntssb.plot_tree(counts=True)

np.array([n.label for n in sim_sca.ntssb.assignments])[np.argsort(sca.ntssb.root['children'][1]['node'].root['node'].data_ass_logits)][65:]

sca.plot_tree_proj(s=50)

sim_sca.plot_tree_proj(s=50)

n = sca.ntssb.root['children'][1]['node'].root['children'][0]['node']
sca.ntssb.root['children'][1]['node'].root['children'][0]['node'].variational_parameters['locals']['unobserved_factors_mean'] = sim_sca.ntssb.root['children'][1]['node'].root['children'][0]['node'].unobserved_factors
sca.ntssb.root['children'][1]['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sim_sca.ntssb.root['children'][1]['node'].root['node'].unobserved_factors
sca.ntssb.root['children'][0]['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sim_sca.ntssb.root['children'][0]['node'].root['node'].unobserved_factors
sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sim_sca.ntssb.root['node'].root['node'].unobserved_factors
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'] = np.log(sim_sca.ntssb.root['children'][1]['node'].root['children'][0]['node'].baseline_caller()[1:])
sca.ntssb.root['children'][1]['node'].root['children'][0]['node'].set_mean(variational=True)
sca.ntssb.root['children'][0]['node'].root['node'].set_mean(variational=True)
sca.ntssb.root['node'].root['node'].set_mean(variational=True)
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'] *= 0.
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['cell_noise_mean'] *= 0.

sim_sca.plot_unobserved_parameters(estimated=False)
sca.plot_unobserved_parameters(estimated=True)

plt.pcolormesh(sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False))
plt.colorbar()

plt.pcolormesh(sca.ntssb.root['node'].root['node'].get_noise(variational=True))
plt.colorbar()
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['factor_precision_log_means']
plt.pcolormesh(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['cell_noise_mean']);plt.colorbar()

plt.pcolormesh(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean']);plt.colorbar()

plt.hist(sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False).ravel(), bins=100); plt.show()
plt.hist(sca.ntssb.root['node'].root['node'].get_noise(variational=True).ravel(), bins=100); plt.show()

sca.ntssb.elbo

plt.plot(elbos[:])

sim_sca.ntssb.plot_tree(counts=True)
sca.ntssb.plot_tree(counts=True)
sim_sca.plot_tree_proj(s=50)

sca.plot_tree_proj(project=False, s=50)


# Evaluate with true parameters
args = dict(global_noise_factors_precisions_shape=20.,log_lib_size_mean=10, num_global_noise_factors=0, unobserved_factors_kernel_concentration=.01)
sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=args)
sca.add_data(sim_sca.adata.raw.to_adata())
sca.set_observed_tree(sim_sca.observed_tree)
sca.normalize_data()
sca.project_data()
sca.ntssb = scatrex.ntssb.NTSSB(sca.observed_tree, sca.model.Node, node_hyperparams=sca.model_args)
sca.ntssb.add_data(np.array(sca.adata.raw.X), to_root=True)
sca.ntssb.root['node'].root['node'].reset_data_parameters()
sca.ntssb.reset_variational_parameters()
sca.ntssb.add_node_to('')
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'] = sim_sca.ntssb.root['node'].root['node'].log_baseline_caller()
sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sim_sca.ntssb.root['node'].root['node'].unobserved_factors
sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sim_sca.ntssb.root['node'].root['node'].unobserved_factors
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'] = sim_sca.ntssb.root['node'].root['node'].global_noise_factors

elbos = sca.ntssb.optimize_elbo(root_node=None, local_node=None,  step_size=0.01, sticks_only=True, num_samples=1, n_iters=5000, threshold=1e-3, max_nodes=1)


theta = 100
args = dict(global_noise_factors_precisions_shape=10, log_lib_size_mean=10, num_global_noise_factors=2, unobserved_factors_kernel_concentration=0.01)
sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=args)
sca.add_data(sim_sca.adata.raw.to_adata())
sca.set_observed_tree(sim_sca.observed_tree)
sca.normalize_data()
sca.project_data()

sca.ntssb.root['node'].root['node'].num_global_noise_factors
sca.search.tree.root['node'].root['node'].num_global_noise_factors = 1
sca.search.tree.root['node'].root['node'].global_noise_factors_precisions_shape = theta
sca.search.tree.root['node'].root['node'].init_noise_factors()
sca.search.tree.root['node'].root['node'].variational_parameters['globals']
sca.search.tree.elbo
sca.search.tree.merge_nodes('A-0-0-0-0-0', 'A-0-0-0-0')
elbos = sca.search.tree.optimize_elbo(root_node=None, local_node=None,  step_size=0.01, sticks_only=False, num_samples=1, n_iters=5000, threshold=1e-3, max_nodes=5)
sca.search.tree.elbo
plt.plot(elbos)
search_kwargs = {'n_iters': 200, 'n_iters_elbo': 2000,
                'moves':        ['add', 'merge', 'pivot_reattach', 'swap', 'subtree_reattach', 'push_subtree', 'perturb_node', 'reset_globals'],
                'move_weights': [1,         3,         1,            1,        1,                  1,              1,                       1],
                'local': True,
                'factor_delay': 100}
sca.learn_tree(reset=True, search_kwargs=search_kwargs)

sca.n

sca.ntssb.

sca.ntssb.elbo

sca.ntssb = sca.search.tree
sca.ntssb.elbo

sim_sca.ntssb.plot_tree(counts=True)

sca.ntssb = sca.search.tree
sca.ntssb.plot_tree(counts=True)

sca.search.tree.elbo
sca.search.tree.merge_nodes('')

plt.plot(sca.search.traces['score'][:])


plt.pcolormesh(sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False))
plt.colorbar()

sim_sca.plot_unobserved_parameters(estimated=False, figsize=(8,8))
sca.ntssb = sca.search.best_tree

sca.plot_unobserved_parameters(estimated=True, figsize=(8,8))


plt.plot(sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors)
plt.plot(sca.ntssb.root['node'].root['children'][0]['node'].variational_parameters['locals']['unobserved_factors_mean'])

sca.ntssb.root['node'].root['node'].variational_parameters['globals']['factor_precision_log_means']
sca.ntssb.root['node'].root['node'].global_noise_factors_precisions_shape
plt.figure(figsize=(6,4))
plt.pcolormesh(sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False))
plt.colorbar()

sca.ntssb = sca.search.best_tree
plt.figure(figsize=(6,4))
plt.pcolormesh(sca.ntssb.root['node'].root['node'].get_noise(variational=True))
plt.colorbar()

plt.figure(figsize=(6,4))
plt.pcolormesh(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'])
plt.colorbar();

plt.figure(figsize=(6,4))
plt.pcolormesh(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'])
plt.colorbar();

plt.pcolormesh(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'])
plt.colorbar()
plt.savefig('')
plt.pcolormesh(sca.search.tree.root['node'].root['node'].variational_parameters['globals']['cell_noise_mean']);plt.colorbar()

sca.ntssb.plot_tree(counts=True)


plt.plot(errs)
plt.yscale('log')

plt.plot(sca.search.traces['move'])
plt.plot(sca.search.traces['n_nodes'])
plt.plot(sca.search.traces['accepted'][:])
plt.plot(sca.search.traces['score'][:])
plt.plot(sca.search.traces['accepted'][:])

sim_sca.plot_tree_proj(s=50)
sca.ntssb = sca.search.best_tree

sca.plot_tree_proj(s=50, figsize=(8,8))
sca.ntssb = sca.search.tree
sca.plot_tree_proj(s=50, figsize=(8,8))
sca.ntssb.elbo

new_node = sca.ntssb.add_node_to('C')
sca.ntssb.swap_nodes('A', 'A-0')
sca.search.tree.merge_nodes('A-0', 'A')
new_node.variational_parameters['locals']['unobserved_factors_mean'] = sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'][0]
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['factor_precision_log_means']
fidx = np.argmin(np.var(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'], axis=1))
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'].shape
sca.ntssb.root['children'][1]['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'][fidx]
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'] *= 0.01
elbos = sca.ntssb.optimize_elbo(root_node=new_node.parent(), local_node=None,  step_size=0.01, sticks_only=False, num_samples=1, n_iters=5000, threshold=1e-3, max_nodes=5)

plt.plot(elbos)
sca.ntssb.elbo
sca.plot_tree_proj(s=100, save='est_pca.pdf', figsize=(6,6))

sca.plot_tree_proj(s=50)

plt.plot(sca.search.traces['score'])

sca.ntssb.plot_tree(counts=True)

create_augmented_tree_dict(sca.ntssb)
mat = get_pairwise_cell_distances(sca.ntssb)

plt.pcolormesh(mat);plt.colorbar()

create_augmented_tree_dict(sca.ntssb)
sca.ntssb.node_dict

sca.ntssb.elbo
sca.ntssb.subtree_reattach_to('A-0-0', 'B')
sca.ntssb.plot_tree(counts=True)


sca.plot_tree_proj(s=50, figsize=(16,8))



nodes = sca.ntssb.get_nodes()
print([(i, node.label) for i, node in enumerate(nodes)])
sca.ntssb.elbo
sca.ntssb.perturb_node(nodes[5], nodes[6])

sca.plot_tree_proj(s=50)

from scatrex.plotting import scatterplot
sca.ntssb.
scatterplot.plot_tree_proj(sca.pca, sca.ntssb, pca_obj=sca.pca_obj, node_logit='B', s=200)
plot_tree_proj(s=50, node_logit='B')
sca.ntssb.elbo


sca.ntssb.elbo

sca.search.tree.root['children'][0]['node'].root

sca.search.tree.root['children'][0]['children'][0]['node'].root

subtrees = sca.search.tree.get_mixture()[1][1:]
for subtree in subtrees:
    print(subtree.root)

plt.plot(sca.search.traces['n_nodes'])
plt.plot(sca.search.traces['score'])

sim_sca.plot_unobserved_parameters(estimated=False)
sca.plot_unobserved_parameters(estimated=True)

sca.search.best_tree.get_mixture()
sim_sca.ntssb.plot_tree(counts=True)
sca.ntssb.plot_tree(counts=True)

sca.ntssb.elbo
sca.ntssb.swap_nodes('B', 'B-0')
sca.plot_tree_proj(s=50)
sca.ntssb.elbo
sca.ntssb.elbo

elbos = sca.ntssb.optimize_elbo(root_node=sca.ntssb.root['children'][0]['node'].root['node'], local_node=None, step_size=0.01, sticks_only=False, num_samples=1, n_iters=2000)
plt.plot(elbos[0])
sca.ntssb.elbo

sca.ntssb.plot_tree(counts=True)

sca.plot_tree_proj(s=50)

plt.plot(sca.search.traces['score'])

plt.plot(init_log_baseline)
plt.plot(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'])
plt.plot(sim_sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'])

sim_sca.plot_tree_proj(s=50)

sca.ntssb.elbo
sca.ntssb.push_subtree('C')
sca.plot_tree_proj(s=50)
sca.ntssb.elbo
elbos = sca.ntssb.optimize_elbo(root_node=sca.ntssb.root['node'].root['node'], step_size=0.01, sticks_only=False, num_samples=1, n_iters=5000)

plt.plot(elbos)

plt.plot(sca.search.traces['accepted'])
plt.plot(sca.search.traces['move'])

# Fit variational parameters to data
sim_sca.ntssb.root['node'].root['node'].reset_data_parameters()
sim_sca.ntssb.reset_variational_parameters()
# Initialize with real parameters
sim_sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'] = np.log(sim_sca.ntssb.root['node'].root['node'].baseline[1:])
nodes = sim_sca.ntssb.get_nodes()
for node in nodes:
    node.variational_parameters['locals']['unobserved_factors_mean'] = node.unobserved_factors

sim_sca.ntssb.root['node'].dp_alpha = 1e-30
sim_sca.ntssb.root['node'].dp_gamma = 1e-30
sim_sca.ntssb.root['node'].alpha_decay = 1e-3

# Tune
elbos = sca.ntssb.optimize_elbo(n_iters=2000)
import matplotlib.pyplot as plt
plt.plot(elbos)
sim_sca.ntssb.elbo
print(f'ELBO of initial tree: {sim_sca.ntssb.elbo}')

sca.ntssb = sca.search.tree
sca.plot_tree_proj(s=50)

# Add node below A with equal unobserved factors
sim_sca.ntssb.add_node_to('A-0')
sim_sca.ntssb.plot_tree(counts=True)
sim_sca.plot_tree_proj(s=50)

sim_sca.plot_unobserved_parameters(estimated=False, name='unobserved_factors')
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors')

# Get scores
elbos = sim_sca.ntssb.optimize_elbo(root_node=sim_sca.ntssb.root['node'].root['node'], n_iters=2000)
plt.plot(elbos)
initial_score = sim_sca.ntssb.elbo
initial_score

sim_sca.ntssb.plot_tree(counts=True)
sim_sca.ntssb.root['node'].root['node'].unobserved_factors_kernel_concentration

np.abs(sim_sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'])
from scatrex import util
util.diag_gamma_logpdf(np.exp(sim_sca.ntssb.root['node'].root['children'][1]['node'].variational_parameters['locals']['unobserved_factors_kernel_log_mean']),
                    np.log(0.001 * np.ones((50,))), np.log(0.001) + 1.*np.abs(sim_sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean']))
util.diag_gaussian_logpdf(sim_sca.ntssb.root['node'].root['children'][1]['node'].variational_parameters['locals']['unobserved_factors_mean'],
                    sim_sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'],
                    sim_sca.ntssb.root['node'].root['children'][1]['node'].variational_parameters['locals']['unobserved_factors_kernel_log_mean'])


nodes, mix = sim_sca.ntssb.get_node_mixture()
for i, node in enumerate(nodes):
    print(f'{node.label}\t{mix[i]}')


# Merge nodes
sim_sca.ntssb.merge_nodes('A-0-0', 'A-0')

# Get scores
sim_sca.ntssb.optimize_elbo(root_node=sim_sca.ntssb.root['node'].root['node'], n_iters=2000)
merged_score = sim_sca.ntssb.elbo
merged_score

nodes, mix = sim_sca.ntssb.get_node_mixture()
for i, node in enumerate(nodes):
    print(f'{node.label}\t{mix[i]}')


def test_add():
    pass

def test_merge():
    # Add node below A with equal unobserved factors
    sim_sca.add_node_to('A')
    sim_sca.plot_tree();

    # Get scores
    initial_score = sim_sca.ntssb.elbo

    # Merge nodes
    sim_sca.merge_nodes('A-1', 'A')

    # Get scores
    sim_sca.ntssb.optimize_elbo(unique_node=sim_sca.ntssb.root['node'].root['node'], sticks_only=True)
    merged_score = sim_sca.ntssb.elbo

    # Both initial tree and merged must be larger than larger tree
    # because new node is redundant
    assert merged_score > initial_score

def test_pivot_reattach():
    pass

def test_swap():
    pass

def test_push_subtree():
    pass

def test_add_reattach_pivot():
    pass

def test_simulation():
    """Run a complete simulation test"""
    model_args = dict(log_lib_size_mean=10, num_global_noise_factors=0)

    # Simulate
    sim_sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=model_args)
    sim_sca.simulate_tree(observed_tree=None, n_extra_per_observed=1, seed=40)
    sim_sca.ntssb.reset_node_parameters(node_hyperparams=sim_sca.model_args)
    sim_sca.observed_tree.create_adata()
    sim_sca.simulate_data()
    sim_sca.normalize_data()
    sim_sca.project_data()

    # Create a new object for the inference
    sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=model_args)
    sca.add_data(sim_sca.adata.raw.to_adata())
    sca.set_observed_tree(sim_sca.observed_tree)
    sca.normalize_data()
    sca.project_data()
    search_kwargs = {'n_iters': 100, 'n_iters_elbo': 100,
                    'local': True,
                    'moves': ['add', 'merge', 'pivot_reattach', 'swap', 'subtree_reattach', 'full']}
    sca.learn_tree(reset=True, search_kwargs=search_kwargs)

    import numpy as np
    from sklearn.metrics import accuracy_score, adjusted_rand_score
    true_hnode = np.array([assignment['subtree'].label for assignment in sim_sca.ntssb.assignments])
    inf_hnode = np.array([assignment['subtree'].label for assignment in sca.ntssb.assignments])
    assert accuracy_score(inf_hnode, true_hnode) > 1/3 # better than random
