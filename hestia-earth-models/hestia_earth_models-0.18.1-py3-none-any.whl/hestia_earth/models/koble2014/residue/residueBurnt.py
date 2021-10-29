from hestia_earth.utils.lookup import get_table_value, download_lookup, column_name
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import debugRequirements
from hestia_earth.models.utils.crop import get_crop_lookup_value
from .. import MODEL

TERM_ID = 'residueBurnt'


def _get_default_percent(term_id: str, country_id: str):
    crop_grouping = get_crop_lookup_value(term_id, 'cropGroupingResidue')
    lookup = download_lookup('region-crop-cropGroupingResidue-burnt.csv', True)
    percent = safe_parse_float(
        get_table_value(lookup, 'termid', country_id, column_name(crop_grouping)) if crop_grouping else None, None
    )
    comb_factor = safe_parse_float(get_crop_lookup_value(term_id, 'combustion_factor_crop_residue'))
    debugRequirements(model=MODEL, term=TERM_ID,
                      crop_grouping=crop_grouping,
                      country_id=country_id,
                      percent=percent,
                      comb_factor=comb_factor)
    return percent if comb_factor is None or percent is None else percent * comb_factor


def run(cycle: dict, primary_product: dict):
    term_id = primary_product.get('term', {}).get('@id', '')
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    value = _get_default_percent(term_id, country_id)
    return None if value is None else value * 100
