from typing import Optional, Union, Dict, List

from quickstats.plots.template import single_frame, parse_styles, parse_analysis_label_options

class AbstractPlot:
    
    COLOR_PALLETE = {}
    COLOR_PALLETE_SEC = {}
    
    def __init__(self, color_pallete:Optional[Dict]=None,
                 color_pallete_sec:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None):
        
        if color_pallete is None:
            self.color_pallete     = self.COLOR_PALLETE
        else:
            self.color_pallete = color_pallete
            
        if color_pallete_sec is None:
            self.color_pallete_sec = self.COLOR_PALLETE_SEC
        else:
            elf.color_pallete_sec = color_pallete_sec
            
        self.styles = parse_styles(styles)
        
        if analysis_label_options is None:
            self.analysis_label_options = None
        else:
            self.analysis_label_options = parse_analysis_label_options(analysis_label_options)
            