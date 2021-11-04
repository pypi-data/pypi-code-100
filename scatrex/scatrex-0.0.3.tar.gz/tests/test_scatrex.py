#!/usr/bin/env python

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np



scores = pd.read_csv('/Users/pedrof/projects/sc-dna/new_deltas_20_nodes.csv', index_col=0)


sns.set(style='ticks', font_scale=1., rc={'figure.figsize':(16,20)})

g = sns.FacetGrid(scores, col="n_regions", height=8.5, aspect=.85)
g.map_dataframe(sns.boxplot, x="method", y="delta", hue="n_reads", order=['hmm_copy', 'hclust', 'phenograph', 'ginkgo', 'scope', 'cluster_tree_sum', 'cluster_tree', 'full_tree_sum', 'full_tree'])
g.add_legend(bbox_to_anchor=[1., .8])
axes = g.axes.flatten()
for i, ax in enumerate(axes):
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout()



scores = pd.read_csv('/Users/pedrof/projects/sc-dna/new_deltas_20_nodes3.csv', index_col=0)


sns.set(style='ticks', font_scale=1., rc={'figure.figsize':(16,20)})

g = sns.FacetGrid(scores, col="n_regions", height=8.5, aspect=.85)
g.map_dataframe(sns.boxplot, x="method", y="delta", hue="n_reads", order=['hmm_copy', 'hclust', 'phenograph', 'ginkgo', 'scope', 'cluster_tree_sum', 'cluster_tree', 'full_tree_sum', 'full_tree'])
g.add_legend(bbox_to_anchor=[1., .8])
axes = g.axes.flatten()
for i, ax in enumerate(axes):
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout()



scores20 = pd.read_csv('~/20nodes_tree_distances.csv', index_col=0)
scores20

scores20 = scores20.replace({'medalt_tree_distance': 'SCOPE+MEDALT', 'cluster_tree_sum': 'SCICoNE cl. sum', 'full_tree_sum': 'SCICoNE sum'})
scores20
sns.set(style='ticks', font_scale=1., rc={'figure.figsize':(16,20)})
g = sns.FacetGrid(scores20, col="n_regions", height=4.5, aspect=.65)
g.map_dataframe(sns.boxplot, x="method", y="delta", hue="n_reads")
g.add_legend(bbox_to_anchor=[1., .8])
axes = g.axes.flatten()
for i, ax in enumerate(axes):
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig(f'tree_distances.pdf')

plt.figure(figsize=(6,4))
sns.boxplot(data=scores20, x='method', y='delta', hue='n_reads')
plt.savefig('/Users/pedrof/projects/sc-dna/scope_deltas_new.png')



scores20 = pd.read_csv('/Users/pedrof/projects/sc-dna/scope_20nodes_deltas.csv', index_col=0)
sns.boxplot(data=scores20, x='n_regions', y='delta', hue='n_reads')

scores20 = pd.read_csv('~/scope_20nodes_deltas_diploid_fixed.csv', index_col=0)
plt.figure(figsize=(6,4))
sns.boxplot(data=scores20, x='n_regions', y='delta', hue='n_reads')
plt.savefig('/Users/pedrof/projects/sc-dna/scope_deltas_new.png')


# scores10 = pd.read_csv('/Users/pedrof/projects/sc-dna/scope_10nodes_deltas.csv', index_col=0)
scores20 = pd.read_csv('/Users/pedrof/projects/sc-dna/scope_20nodes_deltas.csv', index_col=0)
fig, ax_list = plt.subplots(1,2, figsize=(12,4))
sns.boxplot(data=scores10, x='n_regions', y='delta', hue='n_reads', ax=ax_list[0],)
ax_list[0].set_title('10 nodes')
sns.boxplot(data=scores20, x='n_regions', y='delta', hue='n_reads', ax=ax_list[1],)
ax_list[1].set_title('20 nodes')
plt.savefig('/Users/pedrof/projects/sc-dna/scope_deltas.png')
plt.show()



"""Tests for `scatrex` package."""


import pytest

import scatrex
from scatrex import models
import numpy as np
import matplotlib.pyplot as plt
import jax

# Tests
s = 10000
fig, axs = plt.subplots(1, 5, figsize=(18,4))
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

    # Test another unobserved factors distribution
    xxi = np.random.standard_t(1, size=s)

    # Test noise factor distribution
    alpha = np.random.gamma(2, 1., size=2)
    w = np.random.normal(0, np.sqrt(1/alpha), size=[s,2])
    n = np.random.normal(0, size=[100, 2]).dot(w.T).ravel()

    # fig = plt.figure(figsize=(6,6))
    # plt.hist(w)
    # plt.legend()
    # plt.show()

    # fig = plt.figure(figsize=(6,6))
    plt.hist(qsi, bins=100, label='qsi', density=True)
    plt.hist(xxi, bins=100, label='xxi', density=True, alpha=0.5)
    # plt.hist(n, bins=100, label='w', density=True, alpha=0.5)
    plt.legend()
    plt.yscale('log')
    plt.title(f'{theta}')
plt.show()
np.max([4,3])
G = 1000
N = 100
K = 2
w = np.random.normal(0, np.sqrt(1/np.random.gamma(10, 1, size=K)), size=[G, K])
h = np.random.normal(0, 1, size=[N, K])
n = h.dot(w.T)
plt.pcolormesh(n); plt.colorbar(); plt.show()
plt.hist(n.ravel(), bins=100); plt.show()

np.arange(1,2)
np.arange(0, 50+1, int(50/5))[1:]
region_stops = np.sort(np.random.choice(np.arange(50), size=10, replace=False))
region_stops
# Simulate a tree
theta = 100
sim_sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=dict(log_lib_size_mean=6, log_lib_size_std=.8, num_global_noise_factors=4,
                                                                            global_noise_factors_precisions_shape=theta, unobserved_factors_kernel_concentration=1./theta,
                                                                            frac_dosage=0.0))
sim_sca.simulate_tree(observed_tree=None, n_extra_per_observed=1, n_genes=1000, seed=None, observed_tree_params=dict(n_regions=20))
sim_sca.ntssb.reset_node_parameters(node_hyperparams=sim_sca.model_args)
sim_sca.observed_tree.create_adata()
# sim_sca.observed_tree.plot_heatmap(vmax=4, vmin=0)
sim_sca.plot_tree(super_only=False, counts=False)

sim_sca.simulate_data(n_cells=2000)

lib_sizes = np.sum(sim_sca.adata.X, axis=1)
plt.hist(lib_sizes)
plt.show()

plt.hist(np.count_nonzero(sim_sca.adata.X, axis=0))

sim_sca.normalize_data()
sim_sca.project_data()
sim_sca.ntssb.plot_tree(counts=True)
sim_sca.plot_tree_proj(s=50)
sim_sca.plot_unobserved_parameters(step=5, estimated=False)


import scanpy as sc
sc.pl.heatmap(sim_sca.adata, sim_sca.adata.var_names, groupby='node', cmap=None, show=True, use_raw=True, show_gene_labels=False)
sc.tl.pca(sim_sca.adata, svd_solver='arpack', n_comps=100)
sc.pp.neighbors(sim_sca.adata, n_neighbors=15, n_pcs=100)
sc.tl.umap(sim_sca.adata)
sc.pl.umap(sim_sca.adata, color=['node'], alpha=0.8)


sc.pl.heatmap(sim_sca.adata, sim_sca.adata.var_names, groupby='node', cmap=None, show=True, use_raw=False, show_gene_labels=False, figsize=(16,4))

plt.plot(sim_sca.ntssb.root['node'].root['node'].baseline)

noise = sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False)
plt.pcolormesh(noise);plt.colorbar();plt.show()

plt.hist(noise.ravel());plt.show()


plt.plot(noise[0])

plt.plot(sim_sca.ntssb.root['children'][0]['children'][0]['node'].root['children'][0]['node'].unobserved_factors)
plt.plot(sim_sca.ntssb.root['children'][0]['children'][0]['node'].root['children'][0]['node'].unobserved_factors_kernel)

plt.plot(sim_sca.ntssb.root['node'].root['node'].baseline)
plt.plot(np.exp(sim_sca.ntssb.root['children'][0]['node'].root['node'].unobserved_factors) * sim_sca.ntssb.root['node'].root['node'].baseline, alpha=0.5)

plt.plot(sim_sca.ntssb.root['node'].root['node'].global_noise_factors[0])
plt.pcolormesh(sim_sca.ntssb.root['node'].root['node'].cell_global_noise_factors_weights)
plt.colorbar()
plt.show()

plt.pcolormesh(sim_sca.ntssb.root['node'].root['node'].global_noise_factors)
plt.colorbar()
plt.show()


nodes = sim_sca.ntssb.get_nodes()
unobs_factors = np.concatenate([node.unobserved_factors for node in nodes])

plt.hist(unobs_factors.ravel(), density=True, alpha=0.5);
plt.yscale('log')
plt.hist(sim_sca.ntssb.root['node'].root['node'].global_noise_factors.ravel(), density=True, alpha=0.5);
plt.yscale('log'); plt.show()
from scatrex.util import gamma_sample
conc = 1/10.
alpha = 1/conc
print(alpha)
rate = conc
conc/rate
# plt.plot(gamma_sample(conc, rate, size=1000))
plt.plot(np.random.normal(0, 1/np.sqrt(alpha), size=1000))
plt.plot(np.random.normal(0, gamma_sample(conc, 1, size=1000)), alpha=0.5)


1/rate

sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors_kernel[np.argmax(sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors)] /= 10
plt.plot(sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors)
plt.plot(noise[3])
plt.plot(sim_sca.ntssb.root['node'].root['node'].global_noise_factors[0])
plt.plot(sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors + noise[0], alpha=0.5)
plt.plot(sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors)

plt.figure(figsize=(16,4))
plt.pcolormesh((sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors + noise));plt.colorbar()


plt.hist(noise.ravel())

plt.plot(sim_sca.ntssb.root['node'].root['children'][0]['node'].unobserved_factors)


sc.pl.pca_variance_ratio(sim_sca.adata, log=True)



import scanpy as sc
adata = sc.read_10x_mtx(
    'data/filtered_gene_bc_matrices/hg19/',  # the directory with the `.mtx` file
    var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
    cache=True)

-np.log10(0.00001)

adata.var_names_make_unique()  # this is unnecessary if using `var_names='gene_ids'` in `sc.read_10x_mtx`

sim_sca.adata.var_names = adata.var_names[:100]

sim_sca.compute_pathway_enrichments()
sim_sca.adata.var_names

sim_sca.ntssb.set_node_event_strings(estimated=False, var_names=sim_sca.adata.var_names, unobs_threshold=0.5)
sim_sca.ro
sim_sca.observed_tree.plot_tree(labels=True)
sim_sca.plot_tree(events=True)

gene_rankings[node]
enrichments[1]

from scipy import stats
mean = sim_sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean']
std = np.exp(sim_sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_log_std'])
np.arange(-5, 5, 0.01)
xx = np.arange(-5, 5, 0.001)
plt.scatter(xx, stats.norm.pdf(xx, mean[14], std[14]), c=np.abs(xx))

std
sim_sca.adata.var_names
sim_sca.plot_unobserved_parameters(estimated=True, gene='ATAD3C', title='Posterior densities of gene 14')


pivot_probabilities = dict()
pivot_probabilities['B'] = dict({'A':.3, 'A-0':.7})
pivot_probabilities['C'] = dict({'A':.3333, 'A-0':.6666})
g = sim_sca.plot_tree(pivot_probabilities=pivot_probabilities)
prob = .701
" " + f"{prob:.4g}".lstrip('0')
g
print(g.source)

a = 0.33333333
print(f'{a:0.3f}')


g.edge('A', 'B', penwidth='0.5')
g.edge('A', 'B', penwidth='4.', label=' .01', color='yellow', arrowsize='.5')
g

fig, ax_list = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(8,6))
sim_sca.plot_tree(gene='84', genemode='observed', title='Copy number state', cbtitle='', ax=ax_list[0])
sim_sca.plot_tree(gene='84', genemode='unobserved', title='Unobserved factor', cbtitle='', ax=ax_list[1])
plt.suptitle('Here is gene 84')
plt.show()

g.attr(dpi='200')
g.render('file', format='png')
im = plt.imread('file.png')
im.shape
plt.figure(figsize=(6,6))
plt.imshow(im, interpolation='bilinear')
plt.colorbar(sim_sca.ntssb.gene_node_colormaps['unobserved']['mapper'], label='Unobserved factors')
plt.axis('off')
# plt.show()
plt.savefig('ex.png', bbox_inches='tight')
help(plt.imshow)

sim_sca.ntssb.gene_node_colormaps['observed']['mapper']
plt.colorbar(sim_sca.ntssb.gene_node_colormaps['unobserved']['mapper'], label='Unobserved factors')


sim_sca.plot_tree(pathway='Hypoxia')
help(g)




networkx.nx_pydot.from_pydot(g)

sim_sca.ntssb.create_augmented_tree_dict()
dists = sim_sca.ntssb.get_pairwise_cell_distances()
plt.pcolormesh(dists)
plt.colorbar()
dists = dists + dists.T - np.diag(np.diag(dists))
plt.pcolormesh(dists)
plt.colorbar()

import matplotlib
cm = matplotlib.colors.ListedColormap([0, 1, 2])
cm.N

np.where(sim_sca.adata.var_names == '2')[0][0]

sim_sca.ntssb.gene_node_colormaps['unobserved']['vals']['C-0'][1]
sim_sca.ntssb.plot_tree(gene=90, genemode='unobserved')

import matplotlib
self = sim_sca.ntssb.root['node']
nodes, vals = self.ntssb.get_node_unobs()
vals = np.array(vals)
global_min, global_max = np.min(vals), np.max(vals)
node_labs = [node.label for node in nodes]
gene_vals = [val[1] for val in vals]
cmap = self.ntssb.exp_cmap
norm = matplotlib.colors.Normalize(vmin=global_min, vmax=global_max)

name_exp_dict = dict(zip(node_labs, gene_vals))
name_exp_dict
mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
name_color_dict = dict()
for name in name_exp_dict:
    color = matplotlib.colors.to_hex(mapper.to_rgba(name_exp_dict[name]))
    name_color_dict[name] = color

help(sim_sca.plot_tree)

plt.pcolormesh(sim_sca.ntssb.root['node'].root['node'].get_noise(variational=False))
plt.colorbar()
plt.show()


nodes = sim_sca.ntssb.get_nodes()
assignment_lls = []
for i, assignment in enumerate(sim_sca.ntssb.assignments):
    lls = []
    for node in nodes:
        lls.append(node.loglh(i, variational=False))
    assignment_lls.append(lls)
assignment_lls = np.array(assignment_lls)
plt.pcolormesh(assignment_lls)
mat = np.zeros((len(assignment_lls), len(assignment_lls)))
for i in range(len(assignment_lls)):
    for j in range(len(assignment_lls)):
        mat[i,j] = np.sum(np.sqrt((assignment_lls[i] - assignment_lls[j])**2))
plt.pcolormesh(mat)



assignment_lls = []
for i, assignment in enumerate(sim_sca.ntssb.assignments):
    assignment_lls.append(assignment.loglh(i, variational=False))
mat = np.zeros((len(assignment_lls), len(assignment_lls)))
for i in range(len(assignment_lls)):
    for j in range(len(assignment_lls)):
        mat[i,j] = (assignment_lls[i] - assignment_lls[j])**2
plt.pcolormesh(mat)
plt.plot(assignment_lls)

import scanpy as sc
sim_sca.adata
sc.tl.pca(sim_sca.adata, svd_solver='arpack')
sim_sca.adata
sc.pp.neighbors(sim_sca.adata, n_neighbors=10)
knn_indices, knn_dists, forest = sc.neighbors.compute_neighbors_umap( dists, n_neighbors=10, metric='precomputed' )
sim_sca.adata.obsp['distances'], sim_sca.adata.obsp['connectivities'] = sc.neighbors._compute_connectivities_umap(
    knn_indices,
    knn_dists,
    sim_sca.adata.shape[0],
    10, # change to neighbors you plan to use
)
sc.tl.umap(sim_sca.adata)
sim_sca.adata
sc.pl.umap(sim_sca.adata, color=['node'])


sim_sca.adata.obsm['lls2'] = np.array(assignment_lls)
sc.pp.neighbors(sim_sca.adata, use_rep='lls2', n_neighbors=10)
sc.tl.umap(sim_sca.adata)
sim_sca.adata
sc.pl.umap(sim_sca.adata, color=['obs_node'])

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


sim_sca.ntssb.merge_nodes('B-0', 'B')

sim_sca.plot_unobserved_parameters(estimated=False)

jax.config.update("jax_debug_nans", False)
# jax.config.update("jax_debug_infs", True)

# Create a new object for the inference
args = dict(log_lib_size_mean=10, num_global_noise_factors=2)
sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=args)
sca.add_data(sim_sca.adata.raw.to_adata())
sca.set_observed_tree(sim_sca.observed_tree)
sca.normalize_data()
sca.project_data()

# Run clonealign
elbos = sca.learn_clonemap(n_iters=50, filter_genes=True, step_size=0.01)

gene = '602'
fig, ax_list = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(16,6))
sca.plot_tree(gene=gene, genemode='observed', title='Copy number state', cbtitle='', ax=ax_list[0])
sca.plot_tree(gene=gene, genemode='avg', title='Average expression', cbtitle='', ax=ax_list[1], counts=False)
plt.suptitle(gene, fontsize=16)
plt.show()


gene = '407'
fig, ax_list = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(16,6))
sca.plot_tree(gene=gene, genemode='observed', title='Copy number state', cbtitle='', ax=ax_list[0])
sca.plot_tree(gene=gene, genemode='avg', title='Average expression', cbtitle='', ax=ax_list[1], counts=False)
plt.suptitle(gene, fontsize=16)
plt.show()

node_obs = dict(zip([sca.observed_tree.tree_dict[node]['label'] for node in sca.observed_tree.tree_dict], [sca.observed_tree.tree_dict[node]['params'] for node in sca.observed_tree.tree_dict]))
nodes = sca.ntssb.get_nodes()
avgs = []
for node in nodes:
    idx = np.array(list(node.data))
    if len(idx) > 0:
        avgs.append(np.mean(sca.adata.X[idx], axis=0))
    else:
        avgs.append(np.nan*np.zeros(sca.adata.X.shape[1]))
node_avg_exp = dict(zip([node.label for node in nodes], avgs))
sca.ntssb.initialize_gene_node_colormaps(node_obs=node_obs, node_avg_exp=node_avg_exp)
node_avg_exp['B']
gene = '607'
fig, ax_list = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(16,6))
sca.plot_tree(gene=gene, genemode='observed', title='Copy number state', cbtitle='', ax=ax_list[0])
sca.plot_tree(gene=gene, genemode='avg', title='Average expression', cbtitle='', ax=ax_list[1], counts=False)
plt.suptitle(gene, fontsize=16)
plt.show()
import matplotlib
color = matplotlib.colors.to_hex(mapper.to_rgba(node_avg_exp['C'][902]))
color
cmap.set_bad('gray')
mapper.to_rgba(np.nan)
sca.plot_tree( counts=True)


nodes_labels = list(node_avg_exp.keys())
vals = list(node_avg_exp.values())
vals = np.array(vals)
np.nanmax(vals)
global_min, global_max = np.nanmin(vals), np.nanmax(vals)
cmap = sca.ntssb.exp_cmap
import matplotlib
norm = matplotlib.colors.Normalize(vmin=global_min, vmax=global_max)
mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
mapper.get_clim()
self.gene_node_colormaps['avg'] = dict()
self.gene_node_colormaps['avg']['vals'] = dict(zip(nodes_labels, vals))
self.gene_node_colormaps['avg']['mapper'] = mapper
]
color
color = matplotlib.colors.to_hex(mapper.to_rgba(vals[name][gene])) if not np.isnan(node_avg_exp['C'][902]) else 'gray'
global_min, global_max = np.nanmin(avgs), np.nanmax(avgs)
global_min, global_max

sca.ntssb.gene_node_colormaps['avg']['mapper'].get_clim()

plt.pcolormesh(sca.ntssb.root['node'].root['node'].get_noise(variational=True))
plt.colorbar()
plt.show()
sca.plot_tree_proj(project=True, s=50)
plt.plot(elbos[:])

sca.ntssb.elbo
sca.ntssb.ll
sca.ntssb.kl

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
theta = 100
args = dict(global_noise_factors_precisions_shape=theta,log_lib_size_mean=10, num_global_noise_factors=0, unobserved_factors_kernel_concentration=1./theta, unobserved_factors_root_kernel=0.01)
sca = scatrex.SCATrEx(model=models.cna, verbose=True, model_args=args)
sca.add_data(sim_sca.adata.raw.to_adata())
sca.set_observed_tree(sim_sca.observed_tree)
sca.normalize_data()
sca.project_data()
sca.ntssb = scatrex.ntssb.NTSSB(sca.observed_tree, sca.model.Node, node_hyperparams=sca.model_args)
sca.ntssb.add_data(np.array(sca.adata.raw.X), to_root=True)
sca.ntssb.root['node'].root['node'].reset_data_parameters()
sca.ntssb.reset_variational_parameters()
# sca.ntssb.add_node_to('')
# sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'] = sim_sca.ntssb.root['node'].root['node'].log_baseline_caller()
init_baseline = np.mean(sca.ntssb.data / np.sum(sca.ntssb.data, axis=1).reshape(-1,1) * sca.ntssb.data.shape[1], axis=0)
init_baseline = init_baseline / init_baseline[0]
init_log_baseline = np.log(init_baseline[1:])
init_log_baseline = np.clip(init_log_baseline, -1, 1)
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['log_baseline_mean'] = init_log_baseline
sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sim_sca.ntssb.root['node'].root['node'].unobserved_factors
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'] = sim_sca.ntssb.root['node'].root['node'].global_noise_factors

sca.ntssb.elbo
sca.ntssb.pivot_reattach_to('B', 'A-0')
new_node = sca.ntssb.add_node_to('A')
elbos = sca.ntssb.optimize_elbo(root_node=None, local_node=None, step_size=0.01, sticks_only=True, num_samples=1, n_iters=20000, threshold=1e-3, max_nodes=5)
elbos = sca.ntssb.optimize_elbo(root_node=sca.ntssb.root['children'][0]['node'].root['node'], local_node=None, step_size=0.01, sticks_only=False, num_samples=1, n_iters=2000, threshold=1e-3, max_nodes=5)
sca.ntssb.elbo

sca.ntssb.plot_tree(counts=True)
sca.plot_tree_proj(project=True, s=50)

plt.plot(sca.ntssb.root['children'][0]['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'])
plt.plot(sca.ntssb.root['children'][0]['node'].root['node'].variational_parameters['locals']['unobserved_factors_kernel_log_mean'])
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors')
sim_sca.plot_unobserved_parameters(estimated=False, name='unobserved_factors_kernel')
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors_kernel', figsize=(8,8))

sca.ntssb.ll, sca.ntssb.kl

sca.ntssb.ll, sca.ntssb.kl

sca.ntssb.ll, sca.ntssb.kl

theta = 100
args = dict(global_noise_factors_precisions_shape=theta, log_lib_size_mean=10, num_global_noise_factors=3, unobserved_factors_kernel_concentration=1/theta, unobserved_factors_root_kernel=0.01)
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
search_kwargs = {'n_iters': 100, 'n_iters_elbo': 2000,
                'moves':        ['add', 'merge', 'pivot_reattach', 'swap', 'subtree_reattach', 'push_subtree', 'perturb_node', 'reset_globals'],
                'move_weights': [1,         3,         1,            1,        .5,                  .5,              1,                       .5],
                'local': True,
                'factor_delay': 0,
                'step_size': 0.01}
sca.learn_tree(reset=True, search_kwargs=search_kwargs)

n_nodes = len(sca.search.tree.get_nodes())
n_nodes
sca.search.tree.n_nodes
sim_sca.ntssb.plot_tree(counts=True)

sca.ntssb = sca.search.best_tree
sca.ntssb.plot_tree(counts=True)



sca.ntssb.elbo

sim_sca.plot_tree_proj(s=50)
sca.ntssb = sca.search.tree
sca.plot_tree_proj(s=50)

plt.plot(sca.search.traces['times'][:])
plt.plot(sca.search.traces['score'][:])
len(sca.ntssb.root['node'].root['node'].data)

sca.ntssb.merge_nodes('C', 'C-0')

sca.ntssb = sca.search.tree
sim_sca.plot_tree_proj(s=50)
sca.plot_tree_proj(s=50)
sca.plot_tree_proj(s=50)
sim_sca.plot_unobserved_parameters(estimated=False)
sca.plot_unobserved_parameters(estimated=True)
np.argmax(sca.ntssb.root['children'][1]['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'])
sca.plot_unobserved_parameters(estimated=True, gene='54')

sca.plot_unobserved_parameters(estimated=True)

sim_sca.plot_unobserved_parameters(estimated=False, name='unobserved_factors_kernel')
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors_kernel')
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors_kernel')



from copy import deepcopy
sca.search.tree = deepcopy(sca.search.best_tree)
sca.search.tree.elbo
sca.search.tree.pivot_reattach_to('B', 'A-0')
sca.search.tree.merge_nodes('B-0', 'B')
sca.search.tree.root['node'].root['node'].set_mean(variational=True)
sca.search.tree.update_ass_logits(variational=True)
sca.search.tree.assign_to_best()
sca.ntssb = sca.search.tree
sca.ntssb.plot_tree(counts=True)
sca.plot_tree_proj(s=50)

sca.ntssb = sca.search.best_tree
sca.plot_unobserved_parameters(estimated=True)
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors_kernel')

sca.ntssb = sca.search.tree
sca.plot_unobserved_parameters(estimated=True)
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors_kernel')

sca.search.best_tree.root['children'][0]['node'].root['node'].variational_parameters['locals']['nu_log_mean']
sca.search.best_tree.root['children'][0]['node'].root['node'].variational_parameters['locals']['nu_log_std']
sca.search.tree.root['children'][0]['node'].root['node'].variational_parameters['locals']['nu_log_mean']
sca.search.tree.root['children'][0]['node'].root['node'].variational_parameters['locals']['nu_log_std']

sca.search.tree.elbo, sca.search.tree.ll, sca.search.tree.kl

import time
start = time.time()
print("hey")
end = time.time()
print(end-start)

sca.search.tree.plot_tree(counts=True)
new_node = sca.search.tree.merge_nodes('A-0', 'A')
start = time.time()
elbos = sca.ntssb.optimize_elbo(root_node=sca.ntssb.root['node'].root['node'], local_node=None, step_size=0.01, sticks_only=True, num_samples=1, n_iters=2000, threshold=1e-5, max_nodes=1)
end = time.time()
print(end-start)
plt.plot(elbos)
sca.search.tree.elbo, sca.search.tree.ll, sca.search.tree.kl

n, m = sca.search.tree.get_node_mixture()
dict(zip([node.label for node in n], [(w, len(n[i].data)) for i, w in enumerate(m)]))

sca.search.tree.merge_nodes('B-0', 'B')
elbos = sca.search.tree.optimize_elbo(root_node=sca.search.tree.root['children'][0]['node'].root['node'], local_node=None, step_size=0.01, sticks_only=False, num_samples=1, n_iters=2000, threshold=1e-3, max_nodes=5)
sca.search.tree.elbo, sca.search.tree.ll, sca.search.tree.kl

sca.search.tree.elbo, sca.search.tree.ll, sca.search.tree.kl

n, m = sca.search.tree.get_node_mixture()
dict(zip([node.label for node in n], [(w, len(n[i].data)) for i, w in enumerate(m)]))


n, m = sca.search.tree.get_node_mixture()
dict(zip([node.label for node in n], [(w, len(n[i].data)) for i, w in enumerate(m)]))

np.exp(-4.0226254) * 0.3
plt.plot(np.random.normal(np.exp(-4.0226254), np.exp(1.4086884), size=100))
n[0].variational_parameters['locals']['nu_log_mean'], n[0].variational_parameters['locals']['nu_log_std']

n, m = sca.search.tree.get_node_mixture()
dict(zip([node.label for node in n], [w for w in m]))

plt.plot(elbos)

sca.ntssb = sca.search.tree
sim_sca.plot_unobserved_parameters(estimated=False)
sca.plot_unobserved_parameters(estimated=True)
sca.plot_unobserved_parameters(estimated=True, name='unobserved_factors_kernel')

sca.search.best_tree.elbo


plt.plot(np.cumsum(np.array(sca.search.traces['move'])=='add'))
plt.plot(sca.search.traces['move'][:])
plt.xticks(np.arange(len(sca.search.traces['score'][:])))
plt.grid('on')
plt.plot(sca.search.traces['score'][:])
plt.ylim([-160000, -50000])
# plt.xticks(np.arange(len(sca.search.traces['score'][:])))
# plt.grid('on')

plt.plot(sca.search.traces['accepted'][:])
plt.xticks(np.arange(len(sca.search.traces['accepted'][:])))
plt.grid('on')


plt.pcolormesh(sca.ntssb.root['node'].root['node'].get_noise(variational=True))
plt.colorbar()

sim_sca.plot_unobserved_parameters(estimated=False, figsize=(8,8))

import numpy as np
np.log(0.00995)
sca.ntssb = sca.search.best_tree
sca.ntssb.root['node'].root['node'].unobserved_factors_kernel_concentration
sca.ntssb = sca.search.best_tree
plt.plot(sim_sca.ntssb.root['node'].root['node'].unobserved_factors)
plt.plot(sca.ntssb.root['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'])
plt.plot(sca.ntssb.root['children'][0]['node'].root['node'].variational_parameters['locals']['unobserved_factors_kernel_log_mean'])
plt.plot(sca.ntssb.root['children'][0]['node'].root['children'][0]['children'][0]['node'].variational_parameters['locals']['unobserved_factors_kernel_log_mean'])
sca.plot_unobserved_parameters(estimated=True, figsize=(8,8), name='unobserved_factors_kernel')
sca.plot_unobserved_parameters(estimated=True, figsize=(8,8), name='unobserved_factors')

sim_sca.plot_tree_proj(s=50)
sca.plot_tree_proj(s=50)

[node.label for node in sca.ntssb.get_node_mixture()[0]]
plt.plot(sca.ntssb.get_node_mixture()[1])
plt.yscale('log')

sca.ntssb.subtree_reattach_to('A-0-0', 'B')

sca.ntssb.elbo
sca.ntssb.ll
sca.ntssb.kl

sca.ntssb.merge_nodes('C-1', 'C')
sca.ntssb.push_subtree('C')
sca.ntssb.elbo
sca.ntssb = sca.search.best_tree
sca.plot_tree_proj(s=50)


sca.plot_tree_proj(s=50)

sca.ntssb = sca.search.tree
sca.plot_unobserved_parameters(estimated=True, figsize=(8,8))
sim_sca.plot_unobserved_parameters(estimated=False, figsize=(8,8))

plt.plot(np.exp(sca.ntssb.root['node'].root['children'][0]['node'].variational_parameters['locals']['unobserved_factors_kernel_log_mean']))
plt.plot(sca.ntssb.root['node'].root['children'][0]['node'].variational_parameters['locals']['unobserved_factors_log_std'])

sca.plot_unobserved_parameters(estimated=True, figsize=(8,8))
sca.plot_tree_proj(s=50)


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

new_node = sca.search.tree.add_node_to('B')
sca.ntssb.swap_nodes('A', 'A-0')
sca.search.tree.merge_nodes('B-0', 'B')
new_node.variational_parameters['locals']['unobserved_factors_mean'] = sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'][0]
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['factor_precision_log_means']
fidx = np.argmin(np.var(sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'], axis=1))
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'].shape
sca.ntssb.root['children'][1]['node'].root['node'].variational_parameters['locals']['unobserved_factors_mean'] = sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'][fidx]
sca.ntssb.root['node'].root['node'].variational_parameters['globals']['noise_factors_mean'] *= 0.01

sca.ntssb.elbo, sca.ntssb.ll, sca.ntssb.kl
elbos = sca.ntssb.optimize_elbo(root_node=sca.ntssb.root['children'][1]['node'].root['node'], local_node=None,  step_size=0.01, sticks_only=False, num_samples=1, n_iters=5000, threshold=1e-3, max_nodes=5)
sca.ntssb.elbo, sca.ntssb.ll, sca.ntssb.kl



nodes, parent_vector = sca.ntssb.get_nodes(parent_vector=True)
tssbs = [node.tssb.label for node in nodes]
tssb_indices = sca.ntssb.get_tssb_indices(nodes, tssbs)
import jax.numpy as jnp
[node.label for node in nodes]
parent_vector
tssb_indices[1]
tssb_indices[parent_vector[1]]
jnp.all(tssb_indices[parent_vector[1]] == tssb_indices[1])
jnp.concatenate([tssb_indices, -1*jnp.ones((4, tssb_indices.shape[1]))], axis=0).astype(int)

plt.plot(elbos)
sca.ntssb = sca.search.tree
sca.plot_tree_proj(s=100, figsize=(6,6))

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
