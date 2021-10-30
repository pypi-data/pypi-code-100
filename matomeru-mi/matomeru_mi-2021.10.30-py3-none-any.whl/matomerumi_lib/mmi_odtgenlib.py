################################################################################
# MMI v2.0
# Codename: Fir
# Copyright 2021 Fe-Ti
################################################################################
# ODT generation library
#

def mkcontent_xml(styles, doc_body):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:officeooo="http://openoffice.org/2009/office" xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rpt="http://openoffice.org/2005/report" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:drawooo="http://openoffice.org/2010/draw" xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:xforms="http://www.w3.org/2002/xforms" office:version="1.3">
    <office:font-face-decls>
        <style:font-face style:name="Times New Roman" svg:font-family="&apos;Times New Roman&apos;" style:font-adornments="Обычный" style:font-family-generic="roman"/>
        <style:font-face style:name="Liberation Mono" svg:font-family="&apos;Liberation Mono&apos;" style:font-family-generic="modern" style:font-pitch="fixed"/>
        <style:font-face style:name="Times New Roman1" svg:font-family="&apos;Times New Roman&apos;" style:font-adornments="Обычный" style:font-family-generic="roman" style:font-pitch="variable"/>
    </office:font-face-decls>
    {styles}
    {doc_body}
</office:document-content>
'''

def mkdocbody(body):
    return f'''
<office:body>
<office:text text:use-soft-page-breaks="false">
<text:sequence-decls>
<text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
<text:sequence-decl text:display-outline-level="0" text:name="Table"/>
<text:sequence-decl text:display-outline-level="0" text:name="Text"/>
<text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
<text:sequence-decl text:display-outline-level="0" text:name="Figure"/>
</text:sequence-decls>
{body} 
</office:text> 
</office:body>'''

def mktextp(stylename, text):
    return f'\n<text:p text:style-name="{stylename}">{text}</text:p>'


def mktexth(header_lvl, stylename, text):
    return f'\n<text:h text:outline-level="{header_lvl}" text:style-name="{stylename}">{text}</text:h>'


def mkemptytextp(stylename):
    return f'\n<text:p text:style-name="{stylename}"/>'


def wrap_list_item(item):
    return f'\n<text:list-item>{item}</text:list-item>'


def mklist(list_id, stylename, items):
    wrapped_items = ''
    for i in items:
        wrapped_items += wrap_list_item(i)
    return f'\n<text:list xml:id="list{list_id}" text:style-name="{stylename}">{wrapped_items}</text:list>'


def mkminlist(stylename, items):
    wrapped_items = ''
    for i in items:
        wrapped_items += wrap_list_item(i)
    return f'\n<text:list text:style-name="{stylename}">{wrapped_items}</text:list>'


def mkframe(content, stylename, frame_style, frame_num, anchor_type, xsize, ysize):
    return f'''
<draw:frame draw:style-name="{frame_style}" draw:name="Frame{frame_num}" text:anchor-type="{anchor_type}" svg:width="{xsize:3}cm" draw:z-index="0">
<draw:text-box fo:min-height="5%">
<text:p text:style-name="{stylename}">
{content}
</text:p>
</draw:text-box>
</draw:frame>'''


def mkpicture(pic_name, pic_mimetype, pic_caption, pic_style, pic_num, separator, caption_type, anchor_type, xsize, ysize):
    return f'''
<draw:frame draw:style-name="{pic_style}" draw:name="Picture{pic_num}" text:anchor-type="{anchor_type}" svg:width="{xsize:3}cm" svg:height="{ysize:3}cm" draw:z-index="1">
<draw:image xlink:href="Pictures/{pic_name}" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad" draw:mime-type="{pic_mimetype}"/>
</draw:frame>
{caption_type} {pic_num}{separator}{pic_caption}
'''
