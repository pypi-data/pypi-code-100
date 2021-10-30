################################################################################
# MMI v2.0
# Codename: Fir
# Copyright 2021 Fe-Ti
################################################################################
# Automatic styles lib
#

##### INTERNAL STUFF ###########################################################
# List templates section
num_list_lvl_style_template = '''
<text:list-level-style-number text:level="{self.lvl}" text:style-name="Numbering_Symbols" style:num-format="{self.num_format}" text:display-levels="{self.lvl}">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
        <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="{self.list_offset}cm" fo:text-indent="{self.list_indent}cm" fo:margin-left="{self.list_offset}cm"/>
    </style:list-level-properties>
</text:list-level-style-number>'''

num_with_suffix_list_lvl_style_template = '''
<text:list-level-style-number text:level="{self.lvl}" text:style-name="Numbering_Symbols" style:num-suffix="{self.num_suffix}" style:num-format="{self.num_format}">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
        <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="{self.list_offset}cm" fo:text-indent="{self.list_indent}cm" fo:margin-left="{self.list_offset}cm"/>
    </style:list-level-properties>
</text:list-level-style-number>'''

bul_list_lvl_style_template = '''
<text:list-level-style-bullet text:level="{self.lvl}" text:style-name="Bullet_Symbols" text:bullet-char="{self.bullet_char}">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
        <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="{self.list_offset}cm" fo:text-indent="{self.list_indent}cm" fo:margin-left="{self.list_offset}cm"/>
    </style:list-level-properties>
    <style:text-properties style:font-name="{self.font_name}"/>
</text:list-level-style-bullet>'''

list_wrap_style_template = '''
<text:list-style style:name="{self.name}">
    {string}
</text:list-style>'''

##### INTERNAL STUFF ###########################################################
# List classes section
#

class NListLevelAutoStyle:
    lvl = 1
    num_format = 1
    num_suffix = ')'
    font_name = ''
    list_offset = 0
    list_indent = 0
    has_suffix = True
    
    def __init__(self, lvl, list_offset, list_indent,  num_format=1, num_suffix=')', has_suffix=True):
        #print(self, lvl, list_offset, list_indent,  num_format, num_suffix, has_suffix)
        self.lvl = lvl
        self.num_format = num_format
        self.num_suffix = num_suffix
        self.list_offset = list_offset
        self.list_indent = list_indent
        self.has_suffix = has_suffix
        #print(self)
    def __str__(self):
        if not self.has_suffix: # if there is no suffix  then we need
                                # some elements to make the list visible
            return num_list_lvl_style_template.format(self=self)
        else:
            return num_with_suffix_list_lvl_style_template.format(self=self)


class BListLevelAutoStyle:
    lvl = 1
    bullet_char = '-'
    font_name = ''
    list_offset = 0
    list_indent = 0
    
    def __init__(self, lvl, font_name, list_offset, list_indent, bullet_char = '-'):
        self.lvl = lvl
        self.bullet_char = bullet_char
        self.font_name = font_name
        self.list_offset = list_offset
        self.list_indent = list_indent
    
    def __str__(self):
        return bul_list_lvl_style_template.format(self=self)

class NListAutoStyle:
    level_styles=[]
    name = ''
    has_suffix = True
    
    def __init__(self, name, styledict, has_suffix=True):
        level_styles = list()
        for i in range(10):
            self.level_styles.append(
                                    NListLevelAutoStyle(
                                        i+1,
                                        styledict['list_offset']- i*styledict['list_indent'], 
                                        styledict['list_indent'],
                                        styledict['num_format'],
                                        styledict['num_suffix'],
                                        has_suffix
                                        )
                                    )
        self.name = name
        self.has_suffix = has_suffix
        
    def __str__(self):
        string = ''
        for i in self.level_styles:
            string += str(i)
        return list_wrap_style_template.format(self=self,string=string)

class BListAutoStyle:
    level_styles=[]
    name = ''
    
    def __init__(self, name, styledict):
        level_styles = list()
        for i in range(10):
            self.level_styles.append(
                                    BListLevelAutoStyle(
                                        i+1,
                                        styledict['font'],
                                        styledict['list_offset']- i*styledict['list_indent'],
                                        styledict['list_indent'],
                                        styledict['bullet_char']
                                        )
                                    )
        self.name = name
        
    def __str__(self):
        string = ''
        for i in self.level_styles:
            string += str(i)
        return list_wrap_style_template.format(self=self,string=string)

################################################################################
## API STUFF                                                                   #
################################################################################
# Functions
#
# TODO: more flexible templates (or maybe not 'TODO')

def mkframe_style(frame_stylename):
    return f'''<style:style style:name="{frame_stylename}" style:family="graphic" style:parent-style-name="Frame">
<style:graphic-properties style:vertical-pos="top" style:vertical-rel="paragraph-content" style:horizontal-pos="center" style:horizontal-rel="paragraph-content" fo:border="none"/>
</style:style>'''

def mkpic_style(pic_stylename):
    return f'''
<style:style style:name="{pic_stylename}" style:family="graphic" style:parent-style-name="Graphics">
<style:graphic-properties style:mirror="none" fo:clip="rect(0cm, 0cm, 0cm, 0cm)" draw:luminance="0%" draw:contrast="0%" draw:red="0%" draw:green="0%" draw:blue="0%" draw:gamma="100%" draw:color-inversion="false" draw:image-opacity="100%" draw:color-mode="standard" loext:rel-width-rel="paragraph"/>
</style:style>'''
        
def mkbul_list_style(bul_list_stylename, list_props):
    return str(BListAutoStyle(bul_list_stylename, list_props))
    
def mknum_list_style(num_list_stylename, list_props):
    return str(NListAutoStyle(num_list_stylename, list_props))


###for future
# ~ def mkpbpar_style(parent_stylename):
    # ~ return f'''<style:style style:name="{parent_stylename}{mmic.pb_suffix}" style:family="paragraph" style:parent-style-name="{parent_stylename}">
# ~ <style:paragraph-properties fo:break-before="page"/>
# ~ </style:style>'''
