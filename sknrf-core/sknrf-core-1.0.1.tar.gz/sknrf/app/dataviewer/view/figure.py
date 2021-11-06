import os
from enum import Flag, auto, unique
import logging
from itertools import cycle

import math as mt
import cmath as cmt
import numpy as np
import torch as th
import matplotlib as mpl
from PySide2 import QtCore
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QMenu, QFrame, QAction
from PySide2.QtWidgets import QVBoxLayout
from matplotlib.colors import to_rgba
from matplotlib.gridspec import GridSpec
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.interpolate import griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable
from skrf.plotting import smith

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.settings import Settings
from sknrf.app.dataviewer.model.figure import AxesType, AxisType, PlotType, FormatType, options_map
from sknrf.utilities.rf import rU2dBU, g2z

from sknrf.icons import black_32_rc

logger = logging.getLogger(__name__)
plot_pad = {"pad": 1.5, "w_pad": 0.6, "h_pad": 1.0}

@unique
class ToolbarMenus(Flag):
    STATE = auto()
    SCALE = auto()
    MARKUP = auto()
    AXES = auto()
    SUBPLOT = auto()
    ALL = STATE | SCALE | MARKUP | AXES | SUBPLOT


def do_nothing(*args):
    return args


def contour_plot(fig, ax, x, y, xi, yi, z, **kwargs):
    if ax._plot_type == PlotType.Contour:
        for index in range(x.shape[-1]):
            zi = griddata((x, y), z[..., index], (xi[None, :], yi[:, None]),
                          method='cubic')
            cs = ax.contour(xi, xi, zi, **kwargs)
    elif ax._plot_type == PlotType.Contourf:
        for index in range(x.shape[-1]):
            zi = griddata((x, y), z[..., index], (xi[None, :], yi[:, None]),
                          method='cubic')
            cs = ax.contourf(xi, xi, zi, **kwargs)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cb = fig.colorbar(cs, cax=cax, ax=ax)
    cb.ax.tick_params(labelsize=22)
    cb.ax.set_ylabel(ax.get_ylabel(), fontsize=22)
    return cs


class Cursor(object):
    def __init__(self, ax):
        self.axes = ax
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        self.lx = ax.axhline(y=ylim[0], color='k')  # the horiz line
        self.ly = ax.axvline(x=xlim[0], color='k')  # the vert line

    def __del__(self):
        try:
            self.axes.lines.remove(self.lx)
            self.axes.lines.remove(self.ly)
        except Exception:
            logger.error("Plot cursor could not be deleted", exc_info=True)

    def mouse_move(self, event):
        if not event.inaxes: return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)
        event.canvas.draw()


class NavigationToolbar(NavigationToolbar2QT):
    """A Custom Matplotlib Navigation Toolbar
    """

    # (text, tooltip_text, image_file, callback)
    toolbar_menu_map = {
        ToolbarMenus.STATE:
            (('Save', 'Save\nFigure', 'download', 'save_figure'),
             ('Back', 'Undo', 'circled_undo', 'back'),
             ('Forward', 'Redo', 'circled_redo', 'forward')),
        ToolbarMenus.SCALE:
            (('Zoom', 'Rectangle\nZoom', 'zoom-in', 'zoom'),
             ('Auto-scale', 'Auto\nScale', 'zoom-out', 'home'),
             ('Pan', 'Pan Left\nZoom Right\nMouse', 'arrow_left_right', 'pan')),
        ToolbarMenus.MARKUP:
            (('Cursor', 'Crosshair', 'eye', 'crosshair'),
             ('Hide Markers', 'Show/Hide\nmarkers', 'pin', 'toggle_markers')),
        ToolbarMenus.AXES:
            (('Clear Axes', 'Clear the\nAxes', 'cancel', 'clear_axes'),),
        ToolbarMenus.SUBPLOT:
            (('Refresh', 'Refresh', 'circled_sync', 'refresh'),
             ('Subplots', 'Configure\nSubplots', 'equalizer', 'configure_subplots'),
             ('Clear Figure', 'Clear\nFigure', 'cancel-circle', 'clear_figure')),
    }

    def __init__(self, canvas, parent, coordinates=True, toolbar_menus=ToolbarMenus.ALL):
        self.toolitems = ()
        if toolbar_menus & ToolbarMenus.STATE:
            self.toolitems += NavigationToolbar.toolbar_menu_map[ToolbarMenus.STATE]
            self.toolitems += ((None, None, None, None),)
        if toolbar_menus & ToolbarMenus.SCALE:
            self.toolitems += NavigationToolbar.toolbar_menu_map[ToolbarMenus.SCALE]
            self.toolitems += ((None, None, None, None),)
        if toolbar_menus & ToolbarMenus.MARKUP:
            self.toolitems += NavigationToolbar.toolbar_menu_map[ToolbarMenus.MARKUP]
            self.toolitems += ((None, None, None, None),)
        if toolbar_menus & ToolbarMenus.AXES:
            self.toolitems += NavigationToolbar.toolbar_menu_map[ToolbarMenus.AXES]
            self.toolitems += ((None, None, None, None),)
        if toolbar_menus & ToolbarMenus.SUBPLOT:
            self.toolitems += NavigationToolbar.toolbar_menu_map[ToolbarMenus.SUBPLOT]
            self.toolitems += ((None, None, None, None),)
        os.path.join(mpl.get_data_path(), os.sep.join((Settings().root, "icons", "PNG", "black", "32")))
        super(NavigationToolbar, self).__init__(canvas, parent, coordinates=coordinates)
        font = QFont("Courier")
        font.setPixelSize(10)
        self.locLabel.setFont(font)
        self.locLabel.setMargin(0)
        self.locLabel.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        for a in self.actions():
            if a.text() == "Customize":
                a.setIcon(self._icon("cog" + '.png'))
        for text, tooltip_text, image_file, callback in self.toolitems:
            if callback is not None:
                a = self._actions[callback]
                if callback in ['crosshair']:
                    a.setCheckable(True)
                if callback in ['toggle_markers']:
                    a.setCheckable(True)

    def set_message(self, message):
        message = message.replace("−", "-")
        self.message.emit(message)
        x_start = message.find("x=") + 2
        y_start = message.find("y=") + 2
        if self.coordinates and x_start > 1 and y_start > 1:
            axes = self.canvas.figure.gca()
            x = float(message[x_start:y_start-2])
            y = float(message[y_start::])
            mag = abs(x + y*1j)
            mag_dbm = 20*mt.log10(mag)+30
            phase = mt.degrees(cmt.phase(x + y*1j))
            if len(axes.lines) and AxesType(axes.type) == AxesType.Smith:
                z = g2z(x + 1j * y, z0=Settings().z0)[0]
                lin_deg_test = u'%*.*e \u2220 %*.*e\u00B0' % (Settings().precision + 2, Settings().precision, mag,
                                                              Settings().precision + 2, Settings().precision, phase)
                log_deg_test = u'%*.*e \u2220 %*.*e\u00B0' % (Settings().precision + 2, Settings().precision, mag_dbm,
                                                              Settings().precision + 2, Settings().precision, phase)
                z_text = '%*.*e + %*.*ej' % (Settings().precision + 2, Settings().precision, z.real,
                                             Settings().precision + 2, Settings().precision, z.imag)
                self.locLabel.setText(u"Z:%s \n\u0393:%s\n\u0393:%s" % (z_text, lin_deg_test, log_deg_test, ))
            else:
                xy_text = '%*.*e + %-*.*ej' % (Settings().precision + 2, Settings().precision, x,
                                                Settings().precision + 2, Settings().precision, y)
                lin_deg_test = u'%*.*e \u2220 %*.*e\u00B0' % (Settings().precision + 2, Settings().precision, mag,
                                                              Settings().precision + 2, Settings().precision, phase)
                log_deg_test = u'%*.*e \u2220 %*.*e\u00B0' % (Settings().precision + 2, Settings().precision, mag_dbm,
                                                              Settings().precision + 2, Settings().precision, phase)
                self.locLabel.setText("  %s \n  %s\n  %s" % (xy_text, lin_deg_test, log_deg_test))
        else:
            self.locLabel.setText(message)

    def _icon(self, name, color=None):
        file_path = os.sep.join((":", "PNG", "black", "32"))
        return QIcon(os.path.join(file_path, name))

    def save_figure(self, *args):
        super().save_figure(*args)
        self.set_message("Saved\nFigure")

    def back(self, *args):
        super().back(*args)
        a = self._actions["back"]
        self.set_message(a.toolTip())

    def forward(self, *args):
        super().forward(*args)
        a = self._actions["forward"]
        self.set_message(a.toolTip())

    def refresh(self):
        self.parent.update()
        self.set_message("Refreshed")

    def configure_subplots(self):
        super().configure_subplots()
        self.set_message("Configured\nSubplots")

    def edit_parameters(self):
        super().edit_parameters()
        self.set_message("Updated\nFigure\nOptions")

    def clear_figure(self):
        fig = self.canvas.figure
        fig.clear()
        self.parent.update()
        self.set_message("Cleared\nFigure")

    def zoom(self, *args):
        super().zoom(*args)
        a = self._actions["zoom"]
        self.set_message(a.toolTip())

    def home(self, *args):
        super().home(*args)
        a = self._actions["home"]
        self.set_message(a.toolTip())

    def pan(self, *args):
        super().pan(*args)
        a = self._actions["pan"]
        self.set_message(a.toolTip())

    def crosshair(self, *args):
        a = self._actions["crosshair"]
        if a.isChecked():
            self.canvas.cursor = Cursor(self.parent.gca())
            self.canvas.callbacks.connect('motion_notify_event', self.canvas.cursor.mouse_move)
            state = "On"
        else:
            self.canvas.callbacks.connect('motion_notify_event', self.canvas.cursor.mouse_move)
            self.canvas.cursor = None
            state = "Off"
        self.canvas.draw()
        self.set_message("Crosshair %s" % (state,))

    def toggle_markers(self, *args):
        a = self._actions['toggle_markers']
        ax = self.parent.gca()
        size = 0.0 if a.isChecked() else mpl.rcParams['lines.markersize']
        for ln in ax.lines:
            ln.set_markersize(size)
        self.canvas.draw()
        state = "On" if a.isChecked() else "Off"
        self.set_message("Markers %s" % (state,))

    def clear_axes(self, *args):
        ax = self.parent.gca()
        ax.clear()
        self.parent.update()
        self.set_message("Cleared\nAxes")


class ContentCanvas(FigureCanvas):

    def __init__(self, figure):
        super(ContentCanvas, self).__init__(figure)
        self.cursor = None

    def get_default_filename(self):
        filename = super(ContentCanvas, self).get_default_filename()
        try:
            tab_widget = self.parentWidget().parentWidget().parentWidget()
            tab_name = tab_widget.tabText(tab_widget.currentIndex())
            filename = os.sep.join((Settings().data_root, "temp", tab_name + "." + self.get_default_filetype()))
        except AttributeError:
            pass
        return filename


class ContentFigure(QFrame):
    """The content frame.

        Parameters
        ----------
        parent : QtGui.QWidget
               The tables parent widget.

        Attributes
        ----------
        figure : matplotlib.figure
            The matplotlib figure.
        canvas : matplotlib.canvas
            The rendering canvas of the figure.
        toolbar : matplotlib.toolbar
            The figure toolbar.
    """

    axesSelected = QtCore.Signal(int)
    addLegend = QtCore.Signal(object, object)
    removeLegend = QtCore.Signal(object)

    def __init__(self, parent=None, figure=None, gridspec=GridSpec(1, 1), interactive=False):
        super(ContentFigure, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self._context_artist = None
        self._context_menu = QMenu(self)
        self._artist_submenu = self._context_menu.addMenu("Artist")
        self._artist_submenu.addAction(QAction("Send to Front", self._artist_submenu))
        self._artist_submenu.addAction(QAction("Send Forward", self._artist_submenu))
        self._artist_submenu.addAction(QAction("Send Backward", self._artist_submenu))
        self._artist_submenu.addAction(QAction("Send to Back", self._artist_submenu))
        self._artist_submenu.addSeparator()
        self._artist_submenu.addAction(QAction("Hide", self._artist_submenu))
        self._legend_submenu = self._context_menu.addMenu("Legend")
        self._legend_submenu.addAction(QAction("Add Legend", self._legend_submenu))
        self._legend_submenu.addAction(QAction("Add Legend Here", self._legend_submenu))
        self._legend_submenu.addSeparator()
        self._legend_submenu.addAction(QAction("Shift Left", self._legend_submenu))
        self._legend_submenu.addAction(QAction("Shift Right", self._legend_submenu))
        self._legend_submenu.addAction(QAction("Shift Up", self._legend_submenu))
        self._legend_submenu.addAction(QAction("Shift Down", self._legend_submenu))
        self._legend_submenu.addSeparator()
        self._legend_submenu.addAction(QAction("Remove Legend", self._legend_submenu))

        self.gridspec = gridspec
        self.figure = figure if figure else Figure()
        self.canvas = ContentCanvas(self.figure)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        if interactive:
            self._context_menu_position = QPoint(-1, -1)
            self._event_artist_queue = []
            self._event_modifier_queue = []
            self._event_ind_queue = []
            self.timer = self.figure.canvas.new_timer(interval=100)
            self.timer.add_callback(self.update_pos)
            self.timer.start()

    def connect_signals(self):
        self.customContextMenuRequested.connect(self.show_context_menu)

        actions = self._artist_submenu.actions()
        actions[0].triggered.connect(self.send_artist_to_front)
        actions[1].triggered.connect(self.send_artist_forward)
        actions[2].triggered.connect(self.send_artist_backward)
        actions[3].triggered.connect(self.send_artist_to_back)
        actions[5].triggered.connect(self.hide_artist)

        actions = self._legend_submenu.actions()
        actions[0].triggered.connect(self.add_legend)
        actions[1].triggered.connect(self.add_legend_here)
        actions[3].triggered.connect(self.move_legend_left)
        actions[4].triggered.connect(self.move_legend_right)
        actions[5].triggered.connect(self.move_legend_up)
        actions[6].triggered.connect(self.move_legend_down)
        actions[8].triggered.connect(self.remove_legend)

        self.canvas.callbacks.connect('pick_event', self.on_pick)

    def disconnect_signals(self):
        self.customContextMenuRequested.disconnect()

        actions = self._artist_submenu.actions()
        actions[0].triggered.disconnect()
        actions[1].triggered.disconnect()
        actions[2].triggered.disconnect()
        actions[3].triggered.disconnect()
        actions[5].triggered.disconnect()

        actions = self._legend_submenu.actions()
        actions[0].triggered.disconnect()
        actions[1].triggered.disconnect()
        actions[3].triggered.disconnect()
        actions[4].triggered.disconnect()
        actions[5].triggered.disconnect()
        actions[6].triggered.disconnect()
        actions[8].triggered.disconnect()

        self.canvas.callbacks.disconnect('pick_event')

    def __getstate__(self, state=frozenset({})):
        # ### Manually save selected object PROPERTIES here ###
        state["figure"] = self.figure
        return state

    def __setstate__(self, state):
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        self.__init__(parent=self._parent, figure=state["figure"])

    def gcf(self):
        return self.figure

    def gctb(self):
        return self.toolbar

    def gca(self):
        return self.gcf().gca()

    def sca(self, ax):
        self.gcf().sca(ax)

    def scaid(self, gid):
        for ax in self.gcf().axes:
            if ax.get_gid() == gid:
                self.sca(ax)
                return ax
        return None

    def gcp(self):
        return self.gca()._artist

    def scpid(self, gid):
        for plt in self.gca().artists:
            if plt.get_gid() == gid:
                self.scp(plt)
                return plt
        return None

    def scp(self, plt):
        self.gca()._artist = plt

    def add_toolbar(self, coordinates=True, toolbar_menus=ToolbarMenus.ALL):
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=coordinates, toolbar_menus=toolbar_menus)
        self.layout().insertWidget(0, self.toolbar)

    def add_axes(self, fig_model, ax_id, ax_model, share_x=False, share_y=False):
        fig = self.gcf()
        # Shared Axis with Existing Axes
        if len(fig.axes) and share_x:
            ax_old = fig.gca()
            ax = ax_old.twinx()
            self.share_axis(ax, ax_old)
        elif len(fig.axes) and share_y:
            ax_old = fig.gca()
            ax = ax_old.twiny()
            self.share_axis(ax, ax_old)
        else:
            if ax_model.type == AxesType.Rectangular:
                ax = fig.add_subplot(GridSpec(*fig_model.gridspec)[ax_model.gridspec], picker=5)
            elif ax_model.type == AxesType.Polar:
                ax = fig.add_subplot(GridSpec(*fig_model.gridspec)[ax_model.gridspec], picker=5, projection="polar")
            elif ax_model.type == AxesType.Smith:
                ax = fig.add_subplot(GridSpec(*fig_model.gridspec)[ax_model.gridspec], picker=5)
                smith(smithR=1, chart_type='z', draw_labels=True, border=True, ax=ax,
                      ref_imm=Settings().z0, draw_vswr=[1.5, 2.0, 3.0, 5.0, 10.0])
            else:
                raise ValueError("Unknown ax_model type")
        try:
            fig.tight_layout(pad=plot_pad["pad"], w_pad=plot_pad["w_pad"], h_pad=plot_pad["h_pad"])
        except np.linalg.LinAlgError:
            logger.warning("Figure: Cannot resize using fig.tight_layout()")
        ax.type = ax_model.type
        if not (share_x or share_y):
            ax.set_title(ax_model.title)
        ax.set_gid(ax_id)
        fig_model[ax_id] = ax_model

    def set_axes(self, index):
        fig = self.gcf()
        if index > 0:
            self.sca(fig.axes[index - 1])
            fig.axes[index - 1].set_facecolor(to_rgba("#0000FF0F"))
        for ax in fig.get_axes():
            if index == 0 or ax != self.gca():
                ax.set_facecolor(to_rgba(mpl.rcParams['axes.facecolor']))

    def remove_axes(self, index):
        fig = self.gcf()
        ax = self.gca()
        if index > 0:
            fig.delaxes(ax)

    def add_plot(self, fig_model, ax_id, ax_model, plt_id, plt_model):
        ax_model[plt_id] = plt_model

    @QtCore.Slot()
    def set_plot(self, fig_model, ax_id, ax_model, plt_id, plt_model, x, y, options):
        """Update the plot.
        """
        ax = self.scaid(ax_id)
        fig_model[ax_id] = ax_model
        fig_model[ax_id][plt_id] = plt_model
        axes_model = fig_model[ax_id]
        plt_model = axes_model[plt_id]

        custom_options = options
        options = options_map[plt_model.type].copy()
        options.update(custom_options)
        if isinstance(x, th.Tensor):
            x = x.detach().numpy()
        if isinstance(y, th.Tensor):
            y = y.detach().numpy()
        if plt_model.type == PlotType.Scatter:
            options.pop("marker")
            if "c" not in options:
                options["c"] = next(ax_model.color_cycle)
            plt = ax.scatter(x, y, s=plt_model.marker_size, marker=plt_model.marker_style, **options)
        elif plt_model.type == PlotType.Line:
            segs = np.zeros((y.shape + (2,)))
            segs[:, :, 0] = x
            segs[:, :, 1] = y
            if plt_model.line_enable:
                if len(plt_model.line_style):
                    line_styles = [plt_model.line_style]*segs.shape[0]
                else:
                    line_cycle = cycle(Settings().line_order)
                    line_styles = [next(line_cycle) for i in range(segs.shape[0])]
            else:
                line_styles = ["None"]*segs.shape[0]
            if "colors" not in options:
                options["colors"] = next(ax_model.color_cycle)
            plt = LineCollection(segs, linestyles=line_styles, **options)
            ax.add_collection(plt)
        elif plt_model.type == PlotType.Contour:
            plt = contour_plot(fig, ax, x, y, **options)
        elif plt_model.type == PlotType.Contourf:
            plt = contour_plot(fig, ax, x, y, **options)
        else:
            raise ValueError("Unknown Plot Type")
        plt.set_gid(plt_id)
        plt.set_label(plt_model.title)
        if axes_model.autoscale and axes_model.type in (AxesType.Rectangular, AxesType.Polar):
            self.update_axis(axes_model, xlabel=plt_model.x_label, ylabel=plt_model.y_label,
                             xlim=(x.min(), x.max()), ylim=(y.min(), y.max()))
        ax.add_artist(plt)
        if axes_model.type in (AxesType.Rectangular, AxesType.Polar):
            self.set_grid(ax, *ax_model.grid)
        self.sca(ax)
        self.scp(plt)
        self.gcf().canvas.draw()
        return plt

    def share_axis(self, ax, ax_old):
        ax.type = ax_old.type
        ax.set_xlim(ax_old.get_xlim())
        ax.set_ylim(ax_old.get_ylim())
        if ax.type == AxesType.Smith:
            ax.yaxis.set_ticks([])
            ax.xaxis.set_ticks([])
            for loc, spine in ax.spines.items():
                spine.set_color('none')

    def set_grid(self, ax, major_grid, minor_grid):
        if not major_grid and not minor_grid:
            ax.grid(b=False)
        elif major_grid:
            ax.grid(b=True, which='major', linestyle='-')
            nbins, steps = "auto", [1, 2, 2.5, 5, 10]
            ax.xaxis.set_major_locator(MaxNLocator(nbins=nbins, steps=steps))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=nbins, steps=steps))
        elif minor_grid:
            ax.grid(b=True, which='minor', linestyle='--')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.yaxis.set_minor_locator(AutoMinorLocator())

    @QtCore.Slot(QPoint)
    def show_context_menu(self, pos):
        """Display the "right-click" context menu
        """
        layout = self.layout()
        x_offset, y_offset, _, _ = layout.getContentsMargins()
        self._context_menu_position = (pos.x() - x_offset, self.height() - pos.y() - y_offset)
        self._context_menu.exec_(self.mapToGlobal(pos))

    @QtCore.Slot()
    def add_legend(self):
        if len(self.figure.axes) == 0:
            return
        ax = self.gca()
        self.addLegend.emit(ax, None)
        self.update()

    @QtCore.Slot()
    def add_legend_here(self):
        xy_points = self._context_menu_position
        if len(self.figure.axes) == 0:
            return
        ax = self.gca()
        inv_axes = ax.transAxes.inverted()
        xy_axes = inv_axes.transform((xy_points[0], xy_points[1]))
        self.addLegend.emit(ax, xy_axes)
        self.update()

    @QtCore.Slot()
    def move_legend_left(self):
        if len(self.figure.axes) == 0:
            return
        ax = self.gca()
        if ax.legend_:
            bb = ax.legend_.get_bbox_to_anchor().inverse_transformed(ax.transAxes)
            x_offset = -0.1
            bb.x0 += x_offset
            bb.x1 += x_offset
            ax.legend_.set_bbox_to_anchor(bb, transform=ax.transAxes)
            self.update()

    @QtCore.Slot()
    def move_legend_right(self):
        if len(self.figure.axes) == 0:
            return
        ax = self.gca()
        if ax.legend_:
            bb = ax.legend_.get_bbox_to_anchor().inverse_transformed(ax.transAxes)
            x_offset = 0.1
            bb.x0 += x_offset
            bb.x1 += x_offset
            ax.legend_.set_bbox_to_anchor(bb, transform=ax.transAxes)
            self.update()

    @QtCore.Slot()
    def move_legend_up(self):
        if len(self.figure.axes) == 0:
            return
        ax = self.gca()
        if ax.legend_:
            bb = ax.legend_.get_bbox_to_anchor().inverse_transformed(ax.transAxes)
            y_offset = 0.1
            bb.y0 += y_offset
            bb.y1 += y_offset
            ax.legend_.set_bbox_to_anchor(bb, transform=ax.transAxes)
            self.update()

    @QtCore.Slot()
    def move_legend_down(self):
        if len(self.figure.axes) == 0:
            return
        ax = self.gca()
        if ax.legend_:
            bb = ax.legend_.get_bbox_to_anchor().inverse_transformed(ax.transAxes)
            y_offset = -0.1
            bb.y0 += y_offset
            bb.y1 += y_offset
            ax.legend_.set_bbox_to_anchor(bb, transform=ax.transAxes)
            self.update()

    @QtCore.Slot()
    def remove_legend(self):
        if len(self.figure.axes) == 0:
            return
        ax = self.gca()
        self.removeLegend.emit(ax)
        self.update()

    @QtCore.Slot()
    def hide_artist(self):
        if self._context_artist:
            self._context_artist.setVisible(False)
            self.update()

    @QtCore.Slot()
    def send_artist_to_front(self):
        if self._context_artist:
            self._context_artist.set_zorder(3)
            self.update()

    @QtCore.Slot()
    def send_artist_forward(self):
        if self._context_artist:
            self._context_artist.set_zorder(self._context_artist.get_zorder() + 1)
            self.update()

    @QtCore.Slot()
    def send_artist_backward(self):
        if self._context_artist:
            self._context_artist.set_zorder(self._context_artist.get_zorder() + -1)
            self.update()

    @QtCore.Slot()
    def send_artist_to_back(self):
        if self._context_artist:
            self._context_artist.set_zorder(0)
            self.update()

    def update_axis(self, ax_model, xlabel="", ylabel="", xlim=(), ylim=()):
        ax = self.gca()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        # Auto-scale
        if ax_model.autoscale:
            epsilon = si_eps_map[SI.I]
            xlim = ax.get_xlim() if len(xlim) == 0 else xlim
            ylim = ax.get_ylim() if len(ylim) == 0 else ylim
            if ax_model.type == AxesType.Rectangular:
                if ax_model.axis == AxisType.Linear:
                    y_max = max(max(abs(ylim[0]), abs(ylim[1])), epsilon)
                    y_max = 10 ** mt.ceil(mt.log10(y_max))
                    y_min = -y_max
                else:
                    y_min = max(ylim[0], float(rU2dBU(th.as_tensor(epsilon))))
                    y_min = float(rU2dBU(th.as_tensor(epsilon))) if mt.isnan(y_min) else y_min
                    y_min = int(mt.floor(y_min/10.0))*10 - 10
                    y_max = max(ylim[1], float(rU2dBU(th.as_tensor(epsilon))))
                    y_max = float(rU2dBU(th.as_tensor(epsilon))) if mt.isnan(y_max) else y_max
                    y_max = int(mt.ceil(y_max/10.0))*10 + 10
                ax.set_xlim(xlim[0] - epsilon, xlim[1] + epsilon)
                ax.set_ylim(y_min, y_max)
                # ax.set_yticks(np.linspace(y_min, y_max, 11))
            if ax_model.type == AxesType.Polar:
                r_max = max(max(abs(xlim[1]), abs(ylim[1])), epsilon)
                r_max = 10 ** mt.ceil(mt.log10(r_max))
                ax.set_rmax(r_max)
                # ax.set_rticks(np.linspace(0, r_max, 6))
                ax.set_thetagrids(list(range(0, 300, 60)))
            if ax_model.type == AxesType.Smith:
                pass

            if self.canvas.cursor:
                self.canvas.callbacks.disconnect('motion_notify_event')
                self.canvas.cursor = Cursor(self.axes)
                self.canvas.callbacks.connect('motion_notify_event', self.canvas.cursor.mouse_move)

    def update_pos(self):
        while len(self._event_ind_queue) != 0:
            self.timer.stop()
            try:
                index = len(self._event_ind_queue) - 1 - np.argmin(self._event_ind_queue.reverse())
                artist = self._event_artist_queue[index]
                modifier = self._event_modifier_queue[index]
                ind = self._event_ind_queue[index]
                if isinstance(artist, mpl.lines.Line2D):
                    if modifier == Qt.NoModifier:
                        default, selected = mpl.rcParams['lines.linewidth'], 2 * mpl.rcParams['lines.linewidth']
                        getter, setter = artist.get_linewidth, artist.set_linewidth
                        setter(selected) if getter() == default else setter(default)
                    elif modifier == Qt.ControlModifier:
                        artist.set_visible(False)
                    else:
                        pass
                elif isinstance(artist, mpl.axes.Axes):
                    if modifier == Qt.NoModifier:
                        self.axesSelected.emit(self.figure.axes.index(artist))
                    else:
                        pass
            finally:
                self._event_artist_queue.clear()
                self._event_modifier_queue.clear()
                self._event_ind_queue.clear()
                self.update()
                self.timer.start()

    @QtCore.Slot(object)
    def on_pick(self, event):
        """Bold the selected line.
        """
        self._context_artist = event.artist
        if event.guiEvent:
            if event.guiEvent.button() == Qt.LeftButton and event.artist.get_visible():
                # Save closest point pick
                ind = event.ind if hasattr(event, "ind") else [mt.inf]
                if len(ind) > 1:
                    datax, datay = event.artist.get_data()
                    datax, datay = [datax[i] for i in ind], [datay[i] for i in ind]
                    msx, msy = event.mouseevent.xdata, event.mouseevent.ydata
                    dist = np.sqrt((np.array(datax) - msx) ** 2 + (np.array(datay) - msy) ** 2)
                    ind = [ind[np.argmin(dist)]]
                self._event_artist_queue.append(event.artist)
                self._event_modifier_queue.append(event.guiEvent.modifiers())
                self._event_ind_queue.append(ind)

    def update(self):
        self.canvas.draw()
