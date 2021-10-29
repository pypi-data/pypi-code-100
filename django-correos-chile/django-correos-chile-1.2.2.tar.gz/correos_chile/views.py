import logging
from django.http import HttpResponse
from correos_chile.utils import generate_barcode_c128

logger = logging.getLogger(__name__)


def get_c128_barcode(request, ccl_enc, shipping_nbr, slip):
    barcode = generate_barcode_c128(ccl_enc, shipping_nbr, slip)
    return HttpResponse(barcode, content_type='image/svg+xml')
