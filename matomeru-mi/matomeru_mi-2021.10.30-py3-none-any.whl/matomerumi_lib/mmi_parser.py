################################################################################
# MMI v2.0
# Codename: Fir
# Copyright 2021 Fe-Ti
################################################################################
# Parser and essential classes
# i.e. text, lists, pictures and other structure stuff
#
import sys
import hashlib
import mimetypes as mts
import zipfile as z

from . import mmi_odtgenlib as ogl
from . import mmi_auto_styles as ast
from .mmi_config import MMIC
from .mmi_path_handler import PathHandler

# Logging function
def log(self, string):
    if self.debug:
        print(string)

################################################################################
# Constants
#
OOBJ_TYPE = "OObject"
HEAD_TYPE = "Heading"
TEXT_TYPE = "TextBody"
CODE_TYPE = "Code"
LIST_TYPE = "List"
BUL_LIST_TYPE = "ListBulleted"
NUM_LIST_TYPE = "ListNumbered"
PIC_TYPE = "Picture"
PAGE_BREAK_TYPE = "PageBreak"
SPACE = ' '
################################################################################
# Functions
#


def is_heading(mmic, line):
    if mmic.heading_trig in line:
        trig_pos = line.find(mmic.heading_trig)
        trig_end = mmic.heading_trig + SPACE
        char_after_trig = line[line.find(trig_end , trig_pos) + len(mmic.heading_trig)]
        if (line[0:trig_pos].isspace() or trig_pos == 0) and char_after_trig.isspace():
            return True
    return False


def is_picture(mmic, line): # if some trigger isn't found then we're searching from -1
    b_trig_pos = line.find(mmic.pic_b_trig)
    sl = line.find(mmic.pic_e_trig, line.find(mmic.pic_m_trig,
                                            b_trig_pos)) + len(mmic.pic_e_trig)
    # finally adding pic_e_trig length
    prefix = line[:b_trig_pos]
    if sl > mmic.pic_trig_len and prefix.isspace() or prefix == '':
        return True         # Even if len() of m_trig and b_trig is equal to 0
    return False            #   pic_trig_len is greater than sl.
                            # So we consider line to be a picture
                            #   only if we've found picture trigger, i.e. ![]( )


def is_page_break(mmic, line):
    counter = 0
    for ch in line.replace(' ',''):
        if ch != mmic.page_break_trig[0]:   #As we're immitating Md we just need
            return False                    # to check only one character and if
                                            #  it's unexpected there is no PB
        else:
            counter += 1
            if counter >= len(mmic.page_break_trig):
                # If there are enough symbols say OK. That leads to smth like:
                return True # -- -- -lol i'm page break
                            # But who cares
    return False


def is_bulleted_list_item(mmic, line):
    trig_pos = line.find(mmic.bul_list_trig)
    return (line[0:trig_pos].isspace() or trig_pos == 0)


def is_numbered_list_item(mmic, line):
    return (line[0:line.find(mmic.num_list_trig)].lstrip().isdigit())


def is_indented(mmic, line):
    return (line[:mmic.tab_size].isspace())


def get_indent_lvl(mmic, line): # slow but steady
    counter = 0
    while line[:mmic.tab_size].isspace():
        line = line[mmic.tab_size:]
        counter += 1
    return counter


def get_heading_lvl(mmic, trig_streak):
    return 1 + mmic.heading_lvl.index(trig_streak)


def rm_trig(line, trig, count=1):
    return line.replace(trig, '', count)

def save_spacing(line):
    counter = 0
    i = 0
    b_pos = i
    line = line.rstrip()
    while i < len(line):
        if line[i] == ' ':
            if counter == 0:
                b_pos = i
            counter += 1
        else:
            if counter > 1:
                line = line[:b_pos] + f'<text:s text:c="{counter}"/>' + line[b_pos + counter:]
                i = 0
            elif counter > 0 and b_pos == 0:
                line = line[:b_pos] + '<text:s/>' + line[b_pos + counter:]
                i = 0
            counter = 0
        i += 1
    return line

def replace_special_characters(mmic, line, escape_char = '\\'):
    line = line.replace(escape_char+'<','&lt;')
    line = line.replace(escape_char+'>','&gt;')
    return line

def prepare_text(mmic, line, is_code = False):
    '''
    Here the string is prepared, i.e. double quotes and special chars are
    replaced (if the line is not a code block, the special characters
    need to be escaped).
    '''
    line = line.replace('&','&amp;') # we'll not support any html codes
    if not is_code:
        line = replace_special_characters(mmic, line)
        line = line.strip()
        if mmic.replace_hyphens:
            line = line.replace(' - ', mmic.hyphenrpl)
        if mmic.replace_dquotes:    # Replacing double quotes
            d = 1
            while mmic.dquote in line:
                if d > 0:
                    line = line.replace(mmic.dquote, mmic.ldquoterpl, 1)
                else:
                    line = line.replace(mmic.dquote, mmic.rdquoterpl, 1)
                d *= -1
    else:
        line = replace_special_characters(mmic, line, escape_char='')
        if mmic.save_code_spaces:
            line = save_spacing(line)
    return line

################################################################################
# Classes
#

class InvalidArgument(Exception):

    def __init__(self, message):
        self.message = message


class OObject: # abstract class
    lvl = 0
    obj_type = OOBJ_TYPE
    debug = True

    def __init__(self, mmic, nested_items = list()):
        self.nested_items = list()
        self.mmic = mmic # MMI config reference
        #print(nested_items)
        if type(nested_items) == type(list()):
            self.nested_items = nested_items[:]
        elif type(nested_items) == type(str()) and nested_items != "":
            self.nested_items.append(ArbitraryText(self.mmic, nested_items))
        else:
            self.nested_items.append(nested_items)

    def __str__(self):
        string = ""
        #print(self.obj_type, self.nested_items)
        for i in self.nested_items:
            string += str(i)
        return string

    def obj_type(self):
        return self.obj_type

    def add_item(self, line, type_of_list, lvl):
        pass # this is only defined for lists

    def append_paragraph(self, line):
        pass # this is only defined for lists

    def append_line(self, line):
        if not self.nested_items:
            self.nested_items.append(ArbitraryText(self.mmic, line))
        else:
            self.nested_items[-1].append_line(line)

class ArbitraryText(OObject):   # Whatever text in p, h, span & other elements
                                # There is only text with no nested items
                                # This is just for a case of transition to C++


    def __init__(self, mmic, text = "", is_code = False):
        self.mmic = mmic
        self.text = prepare_text(self.mmic, text, is_code)

    def __str__(self):
        return self.text

    # is_code == True only if parent is a CodeBlock instance, but those're equal
    # to one line paragraph, so we do not need to think about them in this fnc.
    def append_line(self, line):
        self.text = self.text + ' ' + prepare_text(self.mmic, line)

class TextParagraph(OObject):
    obj_type = TEXT_TYPE
    def __init__(self, mmic, nested_items = list()): # TODO: add parsing of embedded items
        self.stylename = mmic.text_body_stylename
        super().__init__(mmic, nested_items)
        
    def __str__(self):
        string = super().__str__()
        if not string:
            return ogl.mkemptytextp(self.stylename)
        else:
            return ogl.mktextp(self.stylename, string)


class CodeBlock(TextParagraph):
    obj_type = CODE_TYPE
    

    def __init__(self, mmic, nested_items):
        self.nested_items = list()
        self.stylename = mmic.code_stylename
        self.mmic = mmic
        self.nested_items.append(ArbitraryText(self.mmic, nested_items, is_code=True))


class PageBreak(TextParagraph): # TODO: make PB from automatic styles
    obj_type = PAGE_BREAK_TYPE

    def __init__(self, mmic):
        self.stylename = mmic.page_break_stylename

    def __str__(self):
        return ogl.mkemptytextp(self.stylename)


class Heading(OObject):
    obj_type = HEAD_TYPE

    def __init__(self, mmic, line):
        trig_pos = line.find(mmic.heading_trig)
        trig_end = mmic.heading_trig + SPACE
        trig_end_pos = line.find(trig_end, trig_pos) + len(mmic.heading_trig)
        trig_streak = line[trig_pos:trig_end_pos]
        self.lvl = get_heading_lvl(mmic, trig_streak)
        self.stylename = mmic.heading_stylename_template.format(lvl=self.lvl)
        super().__init__(mmic, line[trig_end_pos:])

    def __str__(self):
        return ogl.mktexth(self.lvl, self.stylename, super().__str__())


class Frame(OObject):
    content = ""
    stylename = ""
    number = 0
    anchor_type = "char"
    xsize = 0
    ysize = 0
    def __str__(self):
        return ogl.mkframe(self.content,
                            self.stylename,
                            self.mmic.frame_stylename,
                            self.number,
                            self.anchor_type,
                            self.mmic.paragraph_width,
                            self.ysize)


class Picture(Frame): # TODO: improve picture handling
    obj_type = PIC_TYPE
    
    def __init__(self, mmic, line, number, md_source):
        self.mmic = mmic
        self.nested_items = list()
        self.separator = mmic.pic_prefix_separator
        self.stylename = mmic.pic_caption_stylename
        
        trig_b = line.find(mmic.pic_b_trig)
        trig_m = line.find(mmic.pic_m_trig, trig_b)
        trig_e = line.find(mmic.pic_e_trig, trig_m)

        self.path = PathHandler(line[trig_m + len(mmic.pic_m_trig):trig_e], md_source)
        self.name = self.path.path.name
        self.caption = prepare_text(mmic, line[trig_b + len(mmic.pic_b_trig):trig_m])

        self.number = number
        self.mimetype = mts.guess_type(str(self.path))[0]

        with open(str(self.path), 'rb') as imgfile:
            if self.mmic.picture_name_is_hash:
                img = imgfile.read()
                name = hashlib.sha256(img).hexdigest() + self.path.path.suffix
            else:
                img = imgfile.read(32) # Just an arbitrary number (> 24)

        line_residue = line[trig_e + len(mmic.pic_e_trig):]
        if mmic.aspect_ratio_separator not in line_residue:
            # only PNG is supported when guessing image dimensions
            # others can become broken
            xpx = int.from_bytes(img[16:20], 'big')
            ypx = int.from_bytes(img[20:24], 'big')
            self.xsize, self.ysize = self.guess_dim(list((xpx,ypx)))
        else:
            aspect_ratio = line_residue.split(mmic.aspect_ratio_separator)
            self.xsize, self.ysize = self.guess_dim(aspect_ratio)

    def guess_dim(self, ar):
        xsize = 0
        ysize = 0
        ar[0] = int(ar[0])
        ar[1] = int(ar[1])
        #print (ar, ppcm)
        if len(ar) > 2:
            if ar[2] == cm_dim:
                xsize = ar[0]
                ysize = ar[1]
            elif ar[2] == px_dim:
                #print (ar, ppcm)
                xsize = ar[0] / self.mmic.ppcm
                ysize = ar[1] / self.mmic.ppcm
        else:
            xsize = self.mmic.paragraph_width * (ar[0]/(ar[0]+ar[1]))
            ysize = self.mmic.paragraph_width * (ar[1]/(ar[0]+ar[1]))
        return xsize, ysize

    def __str__(self):
        string = ""
        for i in self.nested_items:
            string += str(i)
        self.content = ogl.mkpicture(self.name,
                                self.mimetype,
                                self.caption,
                                self.mmic.pic_stylename,
                                self.number,
                                self.separator,
                                self.mmic.pic_caption_prefix,
                                self.anchor_type,
                                self.xsize,
                                self.ysize)
        return super().__str__() + string

class ListItem(OObject): # just a wrapper for better understanding
    pass

class List(OObject): # abstract class
    obj_type = LIST_TYPE
    trigger = ''
    lvl = 1
    stylename = ''

    def __init__(self, mmic, line='', lvl=1):
        self.mmic = mmic
        self.nested_items = list()
        self.lvl = lvl
        line = rm_trig(line, self.trigger)
        self.nested_items.append(ListItem(self.mmic, TextParagraph(self.mmic, line)))
    
    def is_item_of_this_list(self, line, type_of_list, lvl):
        return type_of_list == self.obj_type and lvl == self.lvl
        
    def last_nested_obj(self):
        return self.nested_items[-1].nested_items[-1]

    def get_last_nested_type(self): # get type of the last nested item in the list
        if not self.nested_items:
            return ""
        return self.last_nested_obj().obj_type

    def get_last_nested_lvl(self): # get level
        if not self.nested_items:
            return ""
        return self.last_nested_obj().lvl

    def add_new_nested_list(self, line, type_of_list, lvl):
        if type_of_list == BUL_LIST_TYPE:
            self.nested_items.append(ListItem(ListBulleted(self.mmic, line, lvl)))
        elif type_of_list == NUM_LIST_TYPE:
            self.nested_items.append(ListItem(ListNumbered(self.mmic, line, lvl)))


    def add_item(self, line, type_of_list, lvl):
        if self.is_item_of_this_list(line, type_of_list, lvl):
#            log(self, f"Before removing trigger {self.trigger}:\n" + line)
            line = rm_trig(line, self.trigger)
#            log(self, f"After removing trigger {self.trigger}:\n" + line)
        last_type = self.get_last_nested_type()
        if lvl > self.lvl:
            if type_of_list == last_type or (self.get_last_nested_lvl() < lvl
                                        and last_type.startswith(LIST_TYPE)):
                self.last_nested_obj().add_item(line, type_of_list, lvl)
            else:
                self.add_new_nested_list(line, type_of_list, lvl)
        else:
            self.nested_items.append(ListItem(self.mmic, TextParagraph(self.mmic, line)))


    def append_paragraph(self, line):
        if self.get_last_nested_type() == TEXT_TYPE:
            self.nested_items[-1].nested_items.append(TextParagraph(self.mmic, line))
        else:
            self.nested_items[-1].nested_items[-1].append_paragraph(line)

    def __str__(self):
        return ogl.mkminlist(self.stylename, self.nested_items)

class ListBulleted(List):
    obj_type = BUL_LIST_TYPE
    def __init__(self, mmic, line='', lvl=1):
        self.trigger = mmic.bul_list_trig
        self.stylename = mmic.bul_list_stylename
        super().__init__(mmic, line, lvl)


class ListNumbered(List):
    obj_type = NUM_LIST_TYPE
    
    def __init__(self, mmic, line='', lvl=1):
        self.trigger = mmic.num_list_trig
        self.stylename = mmic.num_list_stylename
        if line.find(self.trigger) > 0:
            line = line[line.find(self.trigger):]
        super().__init__(mmic, line, lvl)

    def add_item(self, line, type_of_list, lvl):
        if self.is_item_of_this_list(line, type_of_list, lvl):
#            log(self, f"Before removing trigger in List N:\n{line}")
            line = line[line.find(self.trigger):]
#            log(self, f"After removing trigger in List N:\n{line}")
        super().add_item(line, type_of_list, lvl)


class MdParser:
    chunks = list()         # document chunks
    embedded_pictures = list() # a list of pictures used in the document

    prev_type = ""

    bl_line_flag = True     # blank line flag
    
    # sort of a kludge
    skip_next_bl = False    # I like MD, but some stuff is annoying 
    
    #pb_line_flag = False    # page break flag
    is_code_flag = False
    #is_ttpg_flag = False    # title page flag

    style_flags = { # for generating automatic styles
    'has_bul_list'  : False,
    'has_num_list'  : False,
    'has_frame'     : False,
    'has_picture'   : False,
    }
    
    def __init__(self, mmic, filename, debug = True):
        self.mmic = mmic
        self.filename = PathHandler(filename)
        self.debug = debug

    def get_last_chunk_type(self):
        if not self.chunks: # if chunks is empty say nothing
            return ""
        return self.chunks[-1].obj_type # or get the previous obj. type

    def parse_file(self):
        with open(str(self.filename)) as ifile:
            for line in ifile:
                if line.startswith(self.mmic.switch_trig):
                    self.set_flags(line)
                elif self.is_code_flag:
                    self.chunks.append(CodeBlock(self.mmic, line))
                else:
                    self.parse_elements(line)

    def set_flags(self, line): # TODO: make title page, raw xml and code blocks
        #line = rm_trig(line, mmic.switch_trig)
        self.is_code_flag = not self.is_code_flag


    def parse_elements(self, line):
        if line.isspace():
            if self.bl_line_flag and self.mmic.allow_empty_paragraphs:
                self.chunks.append(TextParagraph(self.mmic, line))
            if not self.skip_next_bl:
                self.bl_line_flag = True
            else:
                self.skip_next_bl = False
        else:
            self.skip_next_bl = False
            if self.debug:
                log(self, f"Line is:\n{line}")
            line = line.expandtabs(tabsize=self.mmic.tab_size)
            if is_heading(self.mmic, line):
                self.chunks.append(Heading(self.mmic, line))
            elif is_page_break(self.mmic, line):
                self.chunks.append(PageBreak(self.mmic))
            elif is_picture(self.mmic, line):
                self.style_flags['has_frame'] = True
                self.style_flags['has_picture'] = True
                if self.mmic.pic_md_compat:
                    self.skip_next_bl = True # skip next blank line (MD compatibility issue)
                self.add_picture(line)
            elif is_bulleted_list_item(self.mmic, line):
                self.style_flags['has_bul_list'] = True
                self.add_list_item(line, BUL_LIST_TYPE)
            elif is_numbered_list_item(self.mmic, line):
                self.style_flags['has_num_list'] = True
                self.add_list_item(line, NUM_LIST_TYPE)
            else:
                self.append_text(line)
            self.bl_line_flag = False
           # self.pb_line_flag = False
    
    def add_picture(self, line):
        try:
            self.chunks.append(TextParagraph(self.mmic, [Picture(self.mmic, line, len(self.embedded_pictures) + 1, self.filename)]))
            # note: embedded_pictures contains tuples of length == 2
            self.embedded_pictures.append((self.chunks[-1].nested_items[0].path,
                                            self.chunks[-1].nested_items[0].name))
        except FileNotFoundError:
            print(f"Can't open picture from '{line.strip()}'")
           
    def add_list_item(self, line, type_of_list):
        last_chunk_type = self.get_last_chunk_type()
        lvl = get_indent_lvl(self.mmic, line) + 1 # counting from 1
        
        # if (line is the same list type
        # or we have a list embedded into another one)
        # then we add new list item
        # else we create new list
        if (last_chunk_type == type_of_list
                or (last_chunk_type.startswith(LIST_TYPE)
                        and lvl > self.chunks[-1].lvl)):
            self.chunks[-1].add_item(line, type_of_list, lvl)
        else:
            if type_of_list == BUL_LIST_TYPE:
                self.chunks.append(ListBulleted(self.mmic, line, lvl))
            elif type_of_list == NUM_LIST_TYPE:
                self.chunks.append(ListNumbered(self.mmic, line, lvl))

    def append_text(self, line):
        last_chunk_type = self.get_last_chunk_type()
        if last_chunk_type == TEXT_TYPE and not self.bl_line_flag:
            self.chunks[-1].append_line(line)
        elif last_chunk_type.startswith(LIST_TYPE) and (not self.bl_line_flag
                                                            or is_indented(line)):
            if self.bl_line_flag:
                self.chunks[-1].append_paragraph(line)
            else:
                self.chunks[-1].append_line(line)
        else:
            self.chunks.append(TextParagraph(self.mmic, line))
    
    def make_astyles(self):
        string = ''
        if self.style_flags['has_frame']:
            string += ast.mkframe_style(self.mmic.frame_stylename)
        if self.style_flags['has_picture']:
            string += ast.mkpic_style(self.mmic.pic_stylename)
        if self.style_flags['has_bul_list']:
            string += ast.mkbul_list_style(self.mmic.bul_list_stylename, self.mmic.list_props)
        if self.style_flags['has_num_list']:
            string += ast.mknum_list_style(self.mmic.num_list_stylename, self.mmic.list_props)
        return f'<office:automatic-styles>{string}</office:automatic-styles>'
        
    def compose_xml(self):
        #print(self.chunks)
        styles = self.make_astyles()
        xml_content = ''
        for i in self.chunks:
            xml_content += str(i)
        xml_content = ogl.mkdocbody(xml_content)
        return ogl.mkcontent_xml(styles, xml_content)

