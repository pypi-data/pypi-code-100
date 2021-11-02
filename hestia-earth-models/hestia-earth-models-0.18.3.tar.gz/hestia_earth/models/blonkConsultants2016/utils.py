from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import debugMissingLookup, logger
from hestia_earth.models.utils.crop import get_crop_grouping_faostat
from . import MODEL


def get_emission_factor(cycle: dict, factor: str):
    site = cycle.get('site', {})
    country_id = site.get('country', {}).get('@id')
    product = find_primary_product(cycle) or {}
    product_id = product.get('term', {}).get('@id')
    crop_grouping = get_crop_grouping_faostat(product.get('term', {}))

    logger.debug('model=%s, country=%s, product=%s, crop grouping=%s', MODEL, country_id, product_id, crop_grouping)

    lookup_name = f"region-crop-cropGroupingFAOSTAT-{factor}.csv"
    lookup = download_lookup(lookup_name)
    value = get_table_value(lookup, 'termid', country_id, column_name(crop_grouping)) if crop_grouping else None
    debugMissingLookup(lookup_name, 'termid', country_id, crop_grouping, value)

    data = safe_parse_float(value, None)
    # fallback to site.siteType data if possible
    return data if data is not None else safe_parse_float(
        extract_grouped_data(
            get_table_value(lookup, 'termid', country_id, column_name('NONE')), site.get('siteType')), None)
