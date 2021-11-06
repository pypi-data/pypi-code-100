from typing import Optional, Union, Dict, List

import matplotlib.patches as patches
import matplotlib.lines as lines
import pandas as pd
import ROOT

import atlas_mpl_style as ampl

from quickstats.plots.template import single_frame, parse_styles, format_axis_ticks, draw_atlas_label
from quickstats.plots import AbstractPlot

class UpperLimitPlot(AbstractPlot):
    
    COLOR_PALLETE = {
        '2sigma': '#FDC536',
        '1sigma': '#4AD9D9',
        'expected': 'k',
        'observed': 'k'
    }
    
    COLOR_PALLETE_SEC = {
        '2sigma': '#FDC536',
        '1sigma': '#4AD9D9',
        'expected': 'r',
        'observed': 'r'
    }
    
    LABELS = {
        '2sigma': 'Expected limit $\pm 2\sigma$',
        '1sigma': 'Expected limit $\pm 1\sigma$',
        'expected': 'Expected limit (95% CL)',
        'observed': 'Observed limit (95% CL)'
    }
    
    LABELS_SEC = {
        '2sigma': 'Expected limit $\pm 2\sigma$',
        '1sigma': 'Expected limit $\pm 1\sigma$',
        'expected': 'Expected limit (95% CL)',
        'observed': 'Observed limit (95% CL)'
    }
    
    CONFIG = {
        'primary_hatch'  : '\\\\\\',
        'secondary_hatch': '///',
        'primary_alpha'  : 0.9,
        'secondary_alpha': 0.8,
    }
    
    def __init__(self, data, data_sec=None,
                 color_pallete:Optional[Dict]=None,
                 color_pallete_sec:Optional[Dict]=None,
                 labels:Optional[Dict]=None,
                 labels_sec:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]='limit',
                 analysis_label_options:Optional[Union[Dict, str]]='default'):
        super().__init__(color_pallete=color_pallete,
                         color_pallete_sec=color_pallete_sec,
                         styles=styles,
                         analysis_label_options=analysis_label_options)
        self.data     = data
        # secondary data
        self.data_sec = data_sec
        
        if labels is None:
            self.labels = self.LABELS
        else:
            self.labels = labels
            
        if labels_sec is None:
            self.labels_sec = self.LABELS_SEC
        else:
            self.labels_sec = labels_sec
            
        self.config = self.CONFIG
        
    def draw_single_data(self, ax, data, log:bool=False, 
                         draw_observed:bool=True,
                         color_pallete:Optional[Dict]=None,
                         labels:Optional[Dict]=None,
                         observed_marker:Optional[str]='o', 
                         sigma_band_hatch:Optional[str]=None,
                         alpha:float=1.):
        
        if color_pallete is None:
            color_pallete = self.COLOR_PALLETE
        if labels is None:
            labels = self.LABELS
            
        indices = data.index.astype(float).values
        exp_limits = data['0'].values
        n1sigma_limits = data['-1'].values
        n2sigma_limits = data['-2'].values
        p1sigma_limits = data['1'].values
        p2sigma_limits = data['2'].values 
        
        # draw +- 1, 2 sigma bands 
        handle_2sigma = ax.fill_between(indices, n2sigma_limits, p2sigma_limits, 
                                        facecolor=color_pallete['2sigma'],
                                        label=labels['2sigma'],
                                        hatch=sigma_band_hatch,
                                        alpha=alpha)
        handle_1sigma = ax.fill_between(indices, n1sigma_limits, p1sigma_limits, 
                                        facecolor=color_pallete['1sigma'],
                                        label=labels['1sigma'],
                                        hatch=sigma_band_hatch,
                                        alpha=alpha)
        
        if log:
            draw_fn = ax.semilogy
        else:
            draw_fn = ax.plot
        
        
        if draw_observed:
            obs_limits = data['obs'].values
            handle_observed = draw_fn(indices, obs_limits, color=color_pallete['observed'], 
                                      label=labels['observed'], 
                                      marker=observed_marker,
                                      alpha=alpha)
            handle_expected = draw_fn(indices, exp_limits, color=color_pallete['expected'],
                                      linestyle='--',
                                      label=labels['expected'],
                                      alpha=alpha)
        else:
            handle_observed = None
            handle_expected = draw_fn(indices, exp_limits, color=color_pallete['expected'],
                                      label=labels['expected'],
                                      alpha=alpha)
            
        return handle_observed[0], handle_expected[0], handle_1sigma, handle_2sigma
            
    def draw(self, xlabel:str="", ylabel:str="", ylim=None, xlim=None,
             log:bool=False, draw_observed:bool=True, observed_marker:Optional[str]='o'):
        
        ax = single_frame(styles=self.styles)

        if self.data_sec is not None:
            h_obs_sec, h_exp2_sec, h_1sig2_sec, h_2sig_sec = self.draw_single_data(ax, self.data_sec, log=log, 
                                                                 draw_observed=draw_observed,
                                                                 color_pallete=self.color_pallete_sec,
                                                                 labels=self.labels_sec,
                                                                 observed_marker=observed_marker, 
                                                                 sigma_band_hatch=self.config['secondary_hatch'],
                                                                 alpha=self.config['secondary_alpha'])
            sigma_band_hatch = self.config['primary_hatch']
            alpha = self.config['primary_alpha']
        else:
            sigma_band_hatch = None
            alpha = 1.
        
        h_obs, h_exp, h_1sig, h_2sig = self.draw_single_data(ax, self.data, log=log, 
                                                             draw_observed=draw_observed,
                                                             color_pallete=self.color_pallete,
                                                             labels=self.labels,
                                                             observed_marker=observed_marker, 
                                                             sigma_band_hatch=sigma_band_hatch,
                                                             alpha=alpha)
        
        
        ax.set_xlabel(xlabel, **self.styles['xlabel'])
        ax.set_ylabel(ylabel, **self.styles['ylabel'])
        format_axis_ticks(ax, **self.styles['axis'])
        
        if ylim is not None:
            ax.set_ylim(*ylim)
        if xlim is not None:
            ax.set_xlim(*xlim)
        
        if self.analysis_label_options is not None:
            draw_atlas_label(ax, dy=0.05, text_options=self.styles['text'], **self.analysis_label_options)

        # border for the legend
        border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)
        
        handles, labels = ax.get_legend_handles_labels()
        
        if draw_observed:
            primary_handles = [h_obs, h_exp, (h_1sig, border_leg), (h_2sig, border_leg)]
            primary_labels  = [labels[handles.index(h)] for h in [h_obs, h_exp, h_1sig, h_2sig]]
        else:
            primary_handles = [h_exp, (h_1sig, border_leg), (h_2sig, border_leg)]
            primary_labels  = [labels[handles.index(h)] for h in [h_exp, h_1sig, h_2sig]]
        
        if self.data_sec is not None:
            secondary_handles = [h_obs_sec, h_exp2_sec, (h_1sig2_sec, border_leg), (h_2sig_sec, border_leg)]
            secondary_labels  = [labels[handles.index(h)] for h in [h_obs_sec, h_exp2_sec, h_1sig2_sec, h_2sig_sec]]
        else:
            secondary_handles = []
            secondary_labels = []
            
        all_handles = primary_handles + secondary_handles
        all_labels = primary_labels + secondary_labels

        ax.legend(all_handles, all_labels, **self.styles['legend'])
        return ax