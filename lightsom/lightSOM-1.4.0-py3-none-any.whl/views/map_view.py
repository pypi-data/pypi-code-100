import math

from matplotlib import colors
import os
from lightSOM.views.som_view import SOMView
from matplotlib import pyplot as plt
import numpy as np
from lightSOM.views.hexagons import plot_hex
from mpl_toolkits.axes_grid1 import make_axes_locatable

class MapView(SOMView):


    def show(self, som, which_dim='all', cmap = plt.get_cmap('viridis'),
             col_size=1, denormalize=False, save=True, path='.', show=False, colorEx=False):
        (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
         axis_num) = self._calculate_figure_params(som, which_dim, col_size)
        self.prepare()
        centers = [[node[0], node[1]] for node in som.nodes.coordinates]
        names = []
        colors = []
        if colorEx:
            colors.append([list(node) for node in som.nodes.matrix.reshape(-1, 3)])
            ax = plot_hex(self._fig, centers, colors, 'Node Grid w Color Features')
        else:
            if not denormalize:
                weights = som.nodes.matrix
            else:
                weights = som.normalizer.denormalize(som.data_raw, som.nodes.matrix)
            if which_dim == 'all':
                names = ["Feature_"+ f for f in som.features_names[0]]
                for which_dim in range(len(weights.reshape(-1, som.nodes.dim)[0])):
                    colors.append([[node[which_dim]] for node in weights.reshape(-1, 3)])
            elif type(which_dim) == int:
                names.append(["Feature_"+som.features_names[0][which_dim]])
                colors.append([[node[which_dim]] for node in weights.reshape(-1, 3)])
            elif type(which_dim) == list:
                for dim in which_dim:
                    names.append("Feature_" + som.features_names[0][dim])
                    colors.append([[node[dim]] for node in weights.reshape(-1, 3)])

            plot_hex(fig=self._fig, centers=centers, weights=colors, titles=names,
                         shape=[no_row_in_plot, no_col_in_plot], cmap=cmap)

        if save==True:
            if colorEx:
                printName = os.path.join(path, 'nodesColors.png')
            else:
                printName=os.path.join(path,'nodes_features.png')
            self.save(printName, bbox_inches='tight', dpi=300)
        if show==True:
            plt.show()
        if show!=False and save!=False:
            plt.clf()





class View2DPacked(MapView):

    def _set_axis(self, ax, msz0, msz1):
        plt.axis([0, msz0, 0, msz1])
        plt.axis('off')
        ax.axis('off')

    def show(self, som, what='codebook', which_dim='all', cmap=None,
             col_sz=None):
        if col_sz is None:
            col_sz = 6
        (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
         axis_num) = self._calculate_figure_params(som, which_dim, col_sz)
        codebook = som.nodes.matrix

        cmap = cmap or plt.cm.get_cmap('RdYlBu_r')
        msz0, msz1 = som.nodes.mapsize
        compname = som.component_names
        if what == 'codebook':
            h = .1
            w = .1
            self.width = no_col_in_plot*2.5*(1+w)
            self.height = no_row_in_plot*2.5*(1+h)
            self.prepare()

            while axis_num < len(indtoshow):
                axis_num += 1
                ax = self._fig.add_subplot(no_row_in_plot, no_col_in_plot,
                                           axis_num)
                ax.axis('off')
                ind = int(indtoshow[axis_num-1])
                mp = codebook[:, ind].reshape(msz0, msz1)
                plt.imshow(mp[::-1], norm=None, cmap=cmap)
                self._set_axis(ax, msz0, msz1)

                if self.show_text is True:
                    plt.title(compname[0][ind])
                    font = {'size': self.text_size}
                    plt.rc('font', **font)
        if what == 'cluster':
            try:
                codebook = getattr(som, 'cluster_labels')
            except:
                codebook = som.cluster()

            h = .2
            w = .001
            self.width = msz0/2
            self.height = msz1/2
            self.prepare()

            ax = self._fig.add_subplot(1, 1, 1)
            mp = codebook[:].reshape(msz0, msz1)
            plt.imshow(mp[::-1], cmap=cmap)

            self._set_axis(ax, msz0, msz1)

        plt.subplots_adjust(hspace=h, wspace=w)

        plt.show()
        
        
class View1D(MapView):

    def show(self, som, what='codebook', which_dim='all', cmap=None, col_sz=None):
        (self.width, self.height, indtoshow, no_row_in_plot, no_col_in_plot,
         axis_num) = self._calculate_figure_params(som, which_dim, col_sz)
        self.prepare()

        codebook = som.nodes.matrix

        while axis_num < len(indtoshow):
            axis_num += 1
            plt.subplot(no_row_in_plot, no_col_in_plot, axis_num)
            ind = int(indtoshow[axis_num-1])
            mp = codebook[:, ind]
            plt.plot(mp, '-k', linewidth=0.8)

        #plt.show()


