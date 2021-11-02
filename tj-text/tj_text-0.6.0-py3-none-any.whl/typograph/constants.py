from .chars import NBHYPHEN

RU_LONG_PREPOSITIONS = (
    'без',
    'перед',
    'при',
    'через',
    'над',
    'под',
    'про',
    'для',
    'около',
    'среди',
    'из-под',
    'из-за',
    'по-над',
)
RU_VERBOSE_PREPOSITIONS = ('несмотря на', 'в отличие от', 'в связи с')
RU_PARTICLES = ('же', 'ли', 'бы', 'б', 'уж')
RU_CUSTOM_REPLACEMENTS = (('когда-нибудь', f'когда{NBHYPHEN}нибудь'),)
