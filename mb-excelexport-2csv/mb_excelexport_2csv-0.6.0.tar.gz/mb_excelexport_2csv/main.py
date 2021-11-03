import xml.dom.minidom
import click

@click.group('main')
def main():
    pass

@main.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
def cmd(input_file, output_file): 
    csv = convert(input_file)
    output_file.write(csv)

def convert(input_file, delim=','):
    output = []
    dom = xml.dom.minidom.parse(input_file)
    rows = dom.getElementsByTagName('Row')
    for row in rows:
        output_row = []
        cells = row.getElementsByTagName('Cell')
        for cell in cells:
            datum = cell.getElementsByTagName('Data')
            if 'ss:MergeAcross' in cell.attributes:
                multiplier = int(cell.attributes['ss:MergeAcross'].value)
            else:
                multiplier = 0
            for data in datum:
                first = data.firstChild
                if first:
                    # XML can have newline chracters in the data value area, which would mess up the formatting in GSheets
                    value_ = first.nodeValue.replace("\n", " ")
                    output_row.append(f'"{value_}"')
                else:
                    output_row.append('')
                if multiplier > 0:
                    output_row.extend([''] * multiplier)
        output.append(delim.join(output_row))

    return '\n'.join(output)

@main.command()
def gui():
    from .gui_model import gui_main
    gui_main(convert)