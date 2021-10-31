from matplotlib import pyplot as plt
import numpy as np
import math, os
from lightSOM.views.hexagons import plot_hex
from kdmt.matrix import euclidean_distance
from collections import Counter
import matplotlib

class SOMView():

    def __init__(self, som, width, height, show_axis=True, packed=True,
                 text_size=2.8, show_text=True, *args, **kwargs):

        self.width = width
        self.height = height

        self.show_axis = show_axis
        self.packed = packed
        self.text_size = text_size
        self.show_text = show_text
        self.som=som

        self._fig = None

    def __del__(self):
        self._close_fig()


    def build_diff_matrix(self, som, distance=1.01, denormalize=False):
        nodes_distances = np.array(som.nodes.node_distances)
        Diffmatrix = np.zeros((som.nodes.nnodes, 1))
        codebook = som.nodes.matrix.reshape(-1, som.data.shape[1])
        if denormalize:
            vector = som.normalizer.denormalize(som.data_raw, codebook)
        else:
            vector = codebook

        for i in range(som.nodes.nnodes):
            codebook_i = vector[i][np.newaxis, :]
            neighborbor_ind = nodes_distances[i][0:] <= distance
            neighborbor_weights = vector[neighborbor_ind]
            neighborbor_dists = euclidean_distance(
                codebook_i, neighborbor_weights)
            Diffmatrix[i] = np.float(np.sum(neighborbor_dists) / (neighborbor_dists.shape[1] - 1))

        return Diffmatrix.reshape(som.nodes.nnodes)

    def _set_labels(self, cents, ax, labels, onlyzeros, fontsize, hex=False):
        for i, txt in enumerate(labels):
            if onlyzeros == True:
                if txt > 0:
                    txt = ""
            c = cents[i] if hex else (cents[i, 1], cents[-(i + 1), 0])
            ax.annotate(txt, c, va="center", ha="center", size=fontsize)

    def _close_fig(self):
        if self._fig:
            plt.close(self._fig)

    def prepare(self, *args, **kwargs):
        self._close_fig()
        self._fig = plt.figure(figsize=(self.width, self.height))
        self._fig.patch.set_facecolor('white')
        plt.title(self.title, size=50)
        plt.axis('off')
        plt.rc('font', **{'size': self.text_size})

    def save(self, filename, transparent=False, bbox_inches='tight', dpi=400):
        self._fig.savefig(filename, transparent=transparent, dpi=dpi, bbox_inches=bbox_inches)
        return


    def _calculate_figure_params(self, which_dim, col_sz):

        indtoshow, sV, sH = None, None, None

        if which_dim == 'all':
            dim = self.som._dim
            row_sz = np.ceil(float(dim) / col_sz)
            msz_row, msz_col = self.som.nodes.mapsize
            ratio_hitmap = msz_row / float(msz_col)
            ratio_fig = row_sz / float(col_sz)
            indtoshow = np.arange(0, dim).T
            sH, sV = 16, 16*ratio_fig*ratio_hitmap

        elif type(which_dim) == int:
            dim = 1
            msz_row, msz_col = self.som.nodes.mapsize
            ratio_hitmap = msz_row / float(msz_col)
            indtoshow = np.zeros(1)
            indtoshow[0] = int(which_dim)
            sH, sV = 16, 16 * ratio_hitmap

        elif type(which_dim) == list:
            dim = len(which_dim)
            row_sz = np.ceil(float(dim) / col_sz)
            msz_row, msz_col = self.som.nodes.mapsize
            ratio_hitmap = msz_row / float(msz_col)
            ratio_fig = row_sz / float(col_sz)
            indtoshow = np.asarray(which_dim).T
            sH, sV = 16, 16*ratio_fig*ratio_hitmap
        elif which_dim == 'none':
            dim = 1
            row_sz = 1
            col_sz=1
            msz_row, msz_col = self.som.nodes.mapsize
            ratio_hitmap = msz_row / float(msz_col)
            ratio_fig = row_sz / float(col_sz)
            indtoshow = np.asarray(which_dim).T
            sH, sV = 16, 16*ratio_fig*ratio_hitmap
        no_row_in_plot = math.ceil(dim / col_sz)  # 6 is arbitrarily selected
        if no_row_in_plot <= 1:
            no_col_in_plot = dim
        else:
            no_col_in_plot = col_sz

        axis_num = 0

        width = sH
        height = sV

        return (width, height, indtoshow, no_row_in_plot, no_col_in_plot,
                axis_num)


    def show(self, matrix, file_name='nodesColors.png', which_dim='all', cmap = plt.get_cmap('viridis'),
             col_size=1, save=True, path='.', show=False, colorEx=False):
        (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
         axis_num) = self._calculate_figure_params(which_dim, col_size)
        self.prepare()
        centers = [[node[0], node[1]] for node in self.som.nodes.coordinates]
        names = []
        colors = []
        if colorEx:
            colors.append([list(node) for node in matrix.reshape(-1, 3)])
            ax = plot_hex(self._fig, centers, colors, 'Node Grid w Color Features')
        else:
            weights = matrix
            if which_dim == 'all':
                names = ["Feature_"+ f for f in self.som.features_names[0]]
                for which_dim in range(len(weights.reshape(-1, self.som.nodes.dim)[0])):
                    colors.append([[node[which_dim]] for node in weights.reshape(-1, 3)])
            elif type(which_dim) == int:
                names.append(["Feature_"+self.som.features_names[0][which_dim]])
                colors.append([[node[which_dim]] for node in weights.reshape(-1, 3)])
            elif type(which_dim) == list:
                for dim in which_dim:
                    names.append("Feature_" + self.som.features_names[0][dim])
                    colors.append([[node[dim]] for node in weights.reshape(-1, 3)])
            elif which_dim=='none':
                names=[]
                colors.append(matrix)

            plot_hex(fig=self._fig, centers=centers, weights=colors, titles=names,
                         shape=[no_row_in_plot, no_col_in_plot], cmap=cmap)

        if save==True:
            if colorEx:
                printName = os.path.join(path, 'nodesColors.png')
            else:
                printName=os.path.join(path, file_name)
            self.save(printName, bbox_inches='tight', dpi=300)
        if show==True:
            plt.show()
        if show!=False and save!=False:
            plt.clf()


    def plot_nodes_maps(self,  file_name='nodes_features.png',which_dim='all', cmap = plt.get_cmap('viridis'),
             col_size=1, denormalize=False, save=True, path='.', show=False, colorEx=False):
        self.title="Futures Map"
        weights=self.som.nodes.matrix
        if denormalize:
            weights=self.som.normalizer.denormalize(self.som.data_raw, weights)

        return self.show(weights, file_name,which_dim, cmap,
             col_size, save, path, show, colorEx)


    def plot_diffs(self, file_name='nodes_dofferences',cmap = plt.get_cmap('viridis'),
             col_size=1, denormalize=False, save=True, path='.', show=False, colorEx=False):

        diffs=self.build_diff_matrix(self.som, denormalize=denormalize)
        self.title="Difference Map"
        return self.show(diffs,file_name, "none", cmap,
             col_size, save, path, show, colorEx)


    def plot_cluster_map(self, data=None, anotate=False, onlyzeros=False, labelsize=7, cmap = plt.get_cmap('Pastel1')):
        org_w = self.width
        org_h = self.height
        self.title="Cluster Map"
        (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
         axis_num) = self._calculate_figure_params(1, 1)
        self.width /= (self.width / org_w) if self.width > self.height else (self.height / org_h)
        self.height /= (self.width / org_w) if self.width > self.height else (self.height / org_h)
        centers = [[node[0], node[1]] for node in self.som.nodes.coordinates]
        clusters=[]
        try:
            clusters.append(getattr(self.som, 'cluster_labels'))
        except:
            clusters.append(self.som.cluster())

        # codebook = getattr(som, 'cluster_labels', som.cluster())
        msz = self.som.nodes.mapsize

        self.prepare()
        if self.som.nodes.lattice == "rect":
            ax = self._fig.add_subplot(111)

            if data:
                proj = self.som.project(data)
                cents = self.som.bmu_ind_to_xy(proj)
                if anotate:
                    # TODO: Fix position of the labels
                    self._set_labels(cents, ax, clusters[proj], onlyzeros, labelsize, hex=False)

            else:
                cents = self.som.bmu_ind_to_xy(np.arange(0, msz[0]*msz[1]))
                if anotate:
                    # TODO: Fix position of the labels
                    self._set_labels(cents, ax, clusters, onlyzeros, labelsize, hex=False)

            plt.imshow(np.flip(clusters.reshape(msz[0], msz[1])[::],axis=0), alpha=0.5)

        elif self.som.nodes.lattice == "hexa":
            ax=plot_hex(self._fig, centers, clusters,   cmap=cmap, show_color_bar=False)
            if anotate:
                self._set_labels(centers, ax, clusters[0], onlyzeros, labelsize, hex=True)
            self.save("clusres.png", bbox_inches='tight', dpi=300)


    def plot_hits_map(self, anotate=True, onlyzeros=False, labelsize=7, cmap=plt.get_cmap("jet")):
        org_w = self.width
        org_h = self.height
        self.title="Hits Map"
        (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
         axis_num) = self._calculate_figure_params(1, 1)
        self.width /=  (self.width/org_w) if self.width > self.height else (self.height/org_h)
        self.height /=  (self.width / org_w) if self.width > self.height else (self.height / org_h)

        cnts = Counter(self.som.project(self.som.data))
        cnts = [cnts.get((x, y), 0) for x in range(self.som.nodes.mapsize[0]) for y in range(self.som.nodes.mapsize[1])]
        counts=[]
        counts.append(cnts)
        # mp = np.array(counts).reshape(self.som.nodes.mapsize[0],
        #                               self.som.nodes.mapsize[1])
        centers = [[node[0], node[1]] for node in self.som.nodes.coordinates]

        norm = matplotlib.colors.Normalize(
                vmin=0,
                vmax=np.max(np.array(counts).flatten()),
                clip=True)

        self.prepare()

        if self.som.nodes.lattice == "rect":

            ax = plt.gca()
            if anotate:
                self._set_labels(cents, ax, counts, onlyzeros, labelsize)

            pl = plt.pcolor(mp[::-1], norm=norm, cmap=cmap)

            plt.axis([0, self.som.codebook.mapsize[1], 0, self.som.codebook.mapsize[0]])
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            plt.colorbar(pl)

            #plt.show()
        elif self.som.nodes.lattice == "hexa":
            ax=plot_hex(self._fig, centers, counts,   cmap=cmap, show_color_bar=False)

#            ax, cents = plot_hex_map(mp[::-1], colormap=cmap, fig=self._fig)
            if anotate:
                self._set_labels(centers, ax, counts[0], onlyzeros, labelsize, hex=True)

#                self._set_labels(cents, ax, counts, onlyzeros, labelsize, hex=True)
            self.save("hitmap.png", bbox_inches='tight', dpi=300)