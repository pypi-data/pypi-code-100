import barcode
import logging

logger = logging.getLogger(__name__)

render_options = {
    'module_width': 0.5, 'module_height': 25.0, 'quiet_zone': 6.5, 'font_size': 10,
    'text_distance': 5.0, 'background': 'white', 'foreground': 'black',
    'write_text': True, 'text': ''
}

def generate_barcode_c128(ccl_enc, shipping_nbr, slip):
    try:
        code = f'{ccl_enc}{shipping_nbr}{slip}'
        c128 = barcode.get_barcode_class('code128')
        code = c128(code)
        return code.render(writer_options=render_options)
    except Exception:
        logger.error(Exception)
        return False