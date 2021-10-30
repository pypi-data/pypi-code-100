################################################################################
# MMI v2.0
# Codename: Fir
# Copyright 2021 Fe-Ti
################################################################################
# Classes which run all stages of ODT generation
# Can be used as a standalone script.
#

from pathlib import Path
import sys
import shutil
import os
import datetime

from .mmi_parser import *
from .mmi_templates import *
# manifest_item, manifest_xml, manifest_rdf, meta_xml, styles_xml and mimetype

xml_mimetype = 'application/xml'
xmlrdf_mimetype = 'application/rdf+xml'

def parse_cmd(argc, argv):
    '''
    Parses the command line parameters.
    '''
    #print (argv)
    mmi_config = MMIC()
    ifile = ''
    ofile = ''
    i = 1
    while i < argc:
        #print (argv[i], argv[i + 1])
        if argv[i] == '-if' or argv[i] == '--input-file':
            ifile = PathHandler(argv[i + 1])
            i+=1    
        elif argv[i] == '-of' or argv[i] == '--output-file':
            ofile = PathHandler(argv[i + 1])
            i+=1
        elif argv[i] == '--template-dir' or argv[i] == '-tld':
            mmi_config.template_dir = PathHandler(argv[i + 1])
            i+=1
        elif argv[i] == '--tmp-dir' or argv[i] == '-tmp':
            mmi_config.tmp_dir = PathHandler(argv[i + 1])
            i+=1
        elif argv[i] == '--config' or argv[i] == '-c':
            mmi_config.update_cfg(argv[i + 1])
            i+=1
        elif argv[i] == '--config-file' or argv[i] == '-cf':
            try:
                mmi_config.update_cfg_from_file(PathHandler(argv[i + 1]))
            except:
                sys.exit("Can't read file: " + argv[i + 1])
            i+=1
        elif argv[i] == '--verbose':
            mmi_config.debug = True
        elif argv[i] == '--hash-images' or argv[i] == '-hi':
            mmi_config.picture_name_is_hash = True
        else:
            print('Unknown parameter:', argv[i])
        i+=1
    # checking mandatory parameters
    if ifile == '' or ofile=='':
        sys.exit(mmi_config.usage_help)
    return ifile, ofile, mmi_config


###############
# Zip Archiver 
# Begin Section
class Zipper:
    def __init__(self, arcname, filestrings = dict(), compresslevel=9):
        self.arcname = arcname
        self.filestrings = filestrings # a list of tuples
        self.comprlvl = compresslevel

    def add_file(self, filestring):
        self.filestrings[filestring[0]] = (filestring[1],filestring[2])

    def compress(self, verbose=False):
        try: # try to use zlib
            arc = z.ZipFile(str(self.arcname),
                                mode='w',
                                compression=z.ZIP_DEFLATED,
                                compresslevel=self.comprlvl)
        except RuntimeError:
            arc = z.ZipFile(str(self.arcname), mode='w') # fallback

        for i in self.filestrings:
            if verbose:
                print(i, self.filestrings[i][0], self.filestrings[i][1])
            arc.writestr(i, self.filestrings[i][0])
# End Section

class MMI:
    def __init__(self, ifile, ofile, mmic):
        self.ifile = ifile
        self.ofile = ofile
        self.debug = mmic.debug
        self.mmic = mmic
        self.filestrings = dict()   # a dict of tuples used by Zipper class looks
                                    # like {'filename':(filestring, mimetype)}

    def make_content_xml(self):
        parser = MdParser(self.mmic, self.ifile, self.debug)
        parser.parse_file()
        self.embedded_pictures = parser.embedded_pictures[:]
        return parser.compose_xml()

    def make_manifest_xml(self):
        string = ''
        for i in self.filestrings:
            string += manifest_item.format(name=i, mediatype=self.filestrings[i][1])
        string+= manifest_item.format(name='META-INF/manifest.xml', mediatype=xml_mimetype)
        return manifest_xml.format(string=string)
 
    def make_file_list(self):
        self.filestrings.clear()
        self.filestrings['content.xml'] = (self.make_content_xml(), xml_mimetype)
        self.filestrings['styles.xml'] = (styles_xml, xml_mimetype)
        self.filestrings['manifest.rdf'] = (manifest_rdf, xmlrdf_mimetype)
        datestring = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        self.filestrings['meta.xml'] = (meta_xml.format(
                                            datetimestring=datestring
                                            ), xml_mimetype)
        picbytes = bytes()
        for path, name in self.embedded_pictures:
            with open(str(path), 'rb') as picture:
                picbytes = picture.read()
            self.filestrings['Pictures/' + name] = (picbytes, mts.guess_type(str(path))[0])
            log(self, 'Added picture:' + name)
        self.filestrings['META-INF/manifest.xml'] = (self.make_manifest_xml(),
                                                                xml_mimetype)
        self.filestrings['mimetype'] = (mimetype, "mimetype_spec")

    def compress_list_into_odt(self):
        # compressing
        archiver = Zipper(self.ofile, self.filestrings)
        archiver.compress(self.debug)

    def run(self):
        self.make_file_list()
        self.compress_list_into_odt()

