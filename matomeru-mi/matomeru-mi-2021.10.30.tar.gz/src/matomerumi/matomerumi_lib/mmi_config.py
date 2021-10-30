################################################################################
# MMI v2.0
# Codename: Fir
# Copyright 2021 Fe-Ti
################################################################################
# Configuration class and defaults
import json

from .mmi_path_handler import PathHandler
###TODO
# pb_suffix = '_pb' # suffix for automatic page fo:break-before styles

class MMIC:
    ################################################################################
    # General settings
    tmp_dir = str(PathHandler('/tmp/tmpMMI/'))   # tmp dir
    template_dir = str(PathHandler(__file__).path.parent / 'template')
    remove_tmp = True
    debug = False
    usage_help = '''Usage:  python3 -m matomerumi -if <input file> -of <output file>

    Optional:
    --template-dir or -tld  -   use specified directory as a template
    --tmp-dir or -tmp       -   use specified directory as a tmp directory
    --config or -c          -   use specified string to override defaults
    --config-file or -cf    -   use specified file as a config (similar to -c)
    -hi or --hash-images    -   use image hashes as their names
    --verbose               -   be verbose
    '''

    ################################################################################
    # Text properties
    #

    tab_size = 4
    dir_name_separator = '/'
    replace_dquotes = True
    dquote = '"'
    ldquoterpl = '«' # replacements for double quotes
    rdquoterpl = '»'
    replace_hyphens = True
    hyphenrpl = ' – ' # replacement for hyphens
    replace_amp = True
    save_code_spaces = True
    allow_empty_paragraphs = False #True 
                                  # A sequence of n blank lines is considered to be 
                                  # a sequence of n-1 blank paragraphs (if True)
                                  
    pic_md_compat = True # Markdown requires a f*cking blank line after a picture
                         # But we do not... so here is some sort of a kludge

    # Image processing stuff
    picture_name_is_hash = True
    pic_caption_prefix = 'Рисунок'
    pic_prefix_separator = ' – '
    aspect_ratio_separator = ':'
    px_dim = 'px'       # Pixel dimension trigger
    cm_dim = 'cm'       # Cantimeter dimension trigger

    ppi = 96            # Pixel per inch
    ppcm = ppi * 2.54   # Pixel per cm
    page_x = 21
    page_y = 29.7
    margin_top = 2
    margin_bottom = 2
    margin_left = 3
    margin_right = 1.5
    paragraph_width = page_x - margin_left - margin_right

    # monospace_page_h = 32 # lines
    # monospace_page_w = 54 # char
    # Switches
    switch_trig = '```'

    # switches currently not implemented
         #title_page_trig = 'title page' 
         #raw_xml_trig = 'xml raw' # a way to add tables

    # Triggers
    heading_trig = '#'
    page_break_trig = '----' #startswith#
    num_list_trig = '. ' #') ' # numbered list trigger
    bul_list_trig = '- ' # bulleted list trigger

    pic_b_trig = '![' # pic_b_trig<picture name>pic_m_trig<path to file>pic_e_trig
    pic_m_trig = '](' 
    pic_e_trig = ')'  
    pic_trig_len = len(pic_b_trig + pic_m_trig + pic_e_trig)

    # ['# ', '## ',...] list compr.
    heading_lvl = [ i*'#' for i in range(1, 11) ]

    # Styles
    page_break_stylename = "PageBreak" # page break style
    code_stylename = "CodeBlock" # code style
    pic_caption_stylename = "Drawing" # image name style

    text_body_stylename = 'Text_Body'
    heading_stylename_template = 'Heading_{lvl}'

    ################################################################################
    # List properties

    list_props = {
        'font' : 'Times New Roman',
        'bullet_char' : '–',
        'num_format' : '1',
        'num_suffix' : ')',
        'list_offset' : 1.27,
        'list_indent' : -0.635
        }

    bul_list_stylename = 'L1'
    num_list_stylename = 'L2'

    frame_stylename = 'fr1'
    pic_stylename = 'fr2'

    def __init__(self, path = ""):
        if str(path) == "":
            return
        else:
            self.update_cfg_from_file(path)

    def get_cfg_from_file(self, path):
        with open(str(path)) as cfgfile:
            string = cfgfile.read()
        return string

    def update_cfg(self, string):
        cfg = json.loads(string)
        for i in cfg:
            setattr(self, i, cfg[i])

    def update_cfg_from_file(self, path):
        self.update_cfg(self.get_cfg_from_file(path))
