import shutil
import sys
import os
import re
from subprocess import Popen
from PIL import Image
from lxml import etree


here = os.path.abspath(os.path.dirname(__file__))
root = here


def system_cmd(command, wait=True, cwd=root):
    command = command if isinstance(command, str) else " ".join(command)
    print(command)
    process = Popen(command, shell=True, stdout=sys.stdout, cwd=cwd)
    if wait:
        process.wait()
    return process


def camel2underscore(camel):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def format_file(src, dest, ext):
    keep_trying = True
    modifier_str = ""
    modifier_num = 1
    while keep_trying:
        try:
            os.rename(src + ext, dest + modifier_str + ext)
        except:
            modifier_num += 1
            modifier_str = str(modifier_num)
            keep_trying = True
        else:
            keep_trying = False
    tree = etree.parse(dest + ext)
    root = tree.find('.')
    root.set('width', '64px')
    root.set('height', '64px')
    tree.write(dest + ext)

def format_files(directory):
    file_names = [os.path.splitext(f)[0] for f in os.listdir(directory) if not f.startswith('.')]
    [format_file(directory + os.sep + f, directory + os.sep + camel2underscore(re.sub(r'[\d]+[\s\-]+(.*)', r'\1', f)), ".svg")
     for f in file_names]

def change_file_color(src, dest, color_code):
    with open(dest, "wt") as fout:
        with open(src, "rt") as fin:
            contents = fin.read()
            contents = re.sub(r'fill=\"\#[fF]+\"','fill:@ffffff', contents)
            contents = re.sub(r'fill\:\#[fF]+','fill:@ffffff', contents)
            contents = re.sub(r'stroke=\"\#[fF]+\"','stroke:@ffffff', contents)
            contents = re.sub(r'stroke\:\#[fF]+','stroke:@ffffff', contents)
            contents = re.sub(r'fill=\"\#[^\"]+\"','fill="' + color_code + '"', contents)
            contents = re.sub(r'fill\:\#[0-9a-fA-F]+','fill:' + color_code, contents)
            contents = re.sub(r'stroke=\"\#[^\"]+\"','stroke="' + color_code + '"', contents)
            contents = re.sub(r'stroke\:\#[0-9a-fA-F]+','stroke:' + color_code, contents)
            contents = re.sub(r'fill\:\@[fF]+','fill:#ffffff', contents)
            contents = re.sub(r'stroke\:\@[fF]+','stroke:#ffffff', contents)
            fout.write(contents)

def change_color(src_directory, dest_directory, color_code):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    file_names = [f for f in os.listdir(src_directory) if not f.startswith('.')]
    [change_file_color(src_directory + os.sep + f, dest_directory + os.sep + f, color_code) for f in file_names]

def svg2png(src_directory, dest_directory):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    file_names = [os.path.splitext(f)[0] for f in os.listdir(src_directory) if not f.startswith('.')]
    [cairosvg.svg2png(url=src_directory + os.sep + f + '.svg', write_to=dest_directory + os.sep + f + '.png') for f in file_names]

def resizepng(src_directory, dest_directory, width=32, height=32):
    if not os.path.exists(dest_directory):
        os.mkdir(dest_directory)
    file_names = [f for f in os.listdir(src_directory) if f.endswith('.png')]
    [resizefile(src_directory + os.sep + f, dest_directory + os.sep + f, width=width, height=height) for f in file_names]

def resizefile(src, dest, width=32, height=32):
    img_org = Image.open(src)
    img_anti = img_org.resize((width, height), Image.ANTIALIAS)
    img_anti.save(dest)

def print_qrc(directory):
    directory_parts = directory.split(os.sep)
    qrc_filename = os.sep.join((root, "_".join(directory_parts[-2::]) + ".qrc"))
    qrc_directory = "    <file>" + os.sep.join((directory_parts[-3:]))
    prefix = '<!DOCTYPE RCC><RCC version="1.0">\n<qresource>\n'
    postfix = '</qresource>\n</RCC>'
    with open(qrc_filename, "wt") as fout:
        fout.write(prefix)
        [fout.write(os.sep.join((qrc_directory, f + "</file>\n"))) for f in os.listdir(directory) if not f.startswith('.')]
        fout.write(postfix)

def qrc2py(directory):
    directory_parts = directory.split(os.sep)
    qrc_filename = os.sep.join((root, "_".join(directory_parts[-2::])))
    system_cmd('pyside2-rcc -o %s %s -py3' % (qrc_filename + "_rc.py", qrc_filename + '.qrc'))


if __name__ == "__main__":
    import cairosvg

    color_list = (('white', '#FFFFFF'),
                  ('green', '#859900'),
                  ('cyan', '#2aa198'),
                  ('blue', '#268bd2'),
                  ('violet', '#6c71c4'),
                  ('magenta', '#d33682'),
                  ('red', '#dc322f'),
                  ('orange', '#cb4b16'),
                  ('yellow', '#b58900'))
    size_list = [32, 64]

    format_files(os.sep.join([root, 'SVG', 'black']))
    for color, code in color_list:
        print('Creating ' + os.sep.join([root, 'SVG', color]))
        change_color(os.sep.join([root, 'SVG', 'black']), os.sep.join([root, 'SVG', color]), code)

    # Black Icons
    color = "black"
    print('Creating ./PNG/' + color + '/raw')
    svg2png(os.sep.join([root, 'SVG', color]), os.sep.join([root, 'PNG', color, 'raw']))
    for size in size_list:
        print('Creating ' + os.sep.join([root, 'PNG', color, str(size)]))
        resizepng(os.sep.join([root, 'PNG', color, 'raw']), os.sep.join([root, 'PNG', color, str(size)]), width=size, height=size)
        print_qrc(os.sep.join([root, 'PNG', color, str(size)]))
        qrc2py(os.sep.join([root, 'PNG', color, str(size)]))

    # Color Icons
    for color, code in color_list:
        print('Creating ' + os.sep.join([root, 'PNG', color, 'raw']))
        svg2png(os.sep.join([root, 'SVG', color]), os.sep.join([root, 'PNG', color, 'raw']))
        for size in size_list:
            if size != 64 or color == "white":
                print('Creating ' + os.sep.join([root, 'PNG', color, str(size)]))
                resizepng(os.sep.join([root, 'PNG', color, 'raw']), os.sep.join([root, 'PNG', color, str(size)]), width=size, height=size)
                print_qrc(os.sep.join([root, 'PNG', color, str(size)]))
                qrc2py(os.sep.join([root, 'PNG', color, str(size)]))
        shutil.rmtree(os.sep.join([root, 'PNG', color, 'raw']))
    if color != "black":
        shutil.rmtree(os.sep.join([root, 'SVG', color]))

    # Other Resources
    system_cmd('pyside2-rcc -o %s %s -py3' % ("transforms" + "_rc.py", "transforms" + '.qrc'))
    system_cmd('pyside2-rcc -o %s %s -py3' % ("markers" + "_rc.py", "markers" + '.qrc'))
