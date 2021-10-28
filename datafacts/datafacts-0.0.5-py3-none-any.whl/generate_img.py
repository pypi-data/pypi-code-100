import os
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageOps


def get_text_size(txt, font):
    """
    Measures the width and height of arbitrary text for a given font

    :param txt: str - The text to measure width and height
    :param font: PIL.ImageFont - Either a truetype or opentype font
    :return: A tuple of (width, height)
    """

    test_img = Image.new('RGB', (1, 1))
    test_draw = ImageDraw.Draw(test_img)
    text_size = test_draw.textsize(txt, font)

    return text_size


def generate_img(df,
                 save_path,
                 width=400,
                 padding=6,
                 summary_description=None,
                 cols=None,
                 sections=None,
                 header_title='Data Facts',
                 summary_title='Descriptive summary',
                 population_title='Population composition',
                 font_color='#525252',
                 thick_bar_color='black',
                 thin_bar_color='#cfcfcf',
                 border_color='black',
                 background_color='white'):

    y = 0

    img = Image.new('RGBA', (width, 10000), background_color)
    draw = ImageDraw.Draw(img)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    h1_font = ImageFont.truetype(os.path.join(dir_path, 'fonts/OpenSans-Bold.ttf'), 36)
    h2_font = ImageFont.truetype(os.path.join(dir_path, 'fonts/OpenSans-Bold.ttf'), 16)
    h3_font = ImageFont.truetype(os.path.join(dir_path, 'fonts/OpenSans-Medium.ttf'), 16)

    draw.text((10, 10), header_title, font_color, font=h1_font)
    y += 40 + padding + 10

    draw.rectangle((10, y, width-10, y+8), fill=thick_bar_color)
    y += 8 + padding

    if summary_description:

        draw.text((10, y), summary_title, font_color, font=h2_font)
        y += 20 + padding

        draw.rectangle((10, y, width-10, y), fill=thin_bar_color)
        y += 1 + padding/2

        wrapped_list = textwrap.wrap(summary_description, width=45)
        wrapped_text = "\n".join(wrapped_list)

        draw.text((30, y), wrapped_text, font_color, font=h3_font)
        y += 22*len(wrapped_list) + padding

        draw.rectangle((10, y, width-10, y+8), fill=thick_bar_color)
        y += 8 + padding

    if sections:
        for key, value in sections.items():

            draw.text((10, y), key, font_color, font=h2_font)
            y += 20 + padding

            draw.rectangle((10, y, width-10, y), fill=thin_bar_color)
            y += 1 + padding / 2

            if type(value) is str:
                draw.text((30, y), value, font_color, font=h3_font)
                y += 20 + padding

                draw.rectangle((10, y, width-10, y), fill=thin_bar_color)
                y += 1 + padding/2

            elif type(value) is dict:

                for k, v in value.items():

                    text_size = get_text_size(v, h2_font)

                    wrapped_list = textwrap.wrap(k, width=36)
                    wrapped_key = "\n".join(wrapped_list)

                    draw.text((30, y), wrapped_key, font_color, font=h3_font)
                    draw.text((width-10-text_size[0], y), v, font_color, font=h2_font)
                    y += 20 * len(wrapped_list) + padding

                    draw.rectangle((10, y, width - 10, y), fill=thin_bar_color)
                    y += 1 + padding / 2

            else:
                raise ValueError('Value for sections must be str or dict!')

    if cols:

        draw.text((10, y), population_title, font_color, font=h2_font)
        y += 20 + padding

        draw.rectangle((10, y, width-10, y), fill=thin_bar_color)
        y += 1 + padding / 2

        for col in cols:

            draw.text((30, y), col, font_color, font=h3_font)
            y += 20 + padding

            draw.rectangle((10, y, width-10, y), fill=thin_bar_color)
            y += 1 + padding / 2

            data = df[col].value_counts(normalize=True)

            for value, relative_frequency in data.iteritems():

                formatted_count = f'{int(round(100*relative_frequency, 0))}%'

                text_size = get_text_size(formatted_count, h2_font)

                wrapped_list = textwrap.wrap(value, width=36)
                wrapped_value = "\n".join(wrapped_list)

                draw.text((50, y), wrapped_value, font_color, font=h3_font)
                draw.text((width-10-text_size[0], y), formatted_count, font_color, font=h2_font)
                y += 20*len(wrapped_list) + padding

                draw.rectangle((10, y, width-10, y), fill=thin_bar_color)
                y += 1 + padding / 2

    img = img.crop((0, 0, width, int(y+10)))
    img = ImageOps.expand(img, border=2, fill=border_color)
    img = ImageOps.expand(img, border=10, fill=background_color)

    img.save(save_path)
