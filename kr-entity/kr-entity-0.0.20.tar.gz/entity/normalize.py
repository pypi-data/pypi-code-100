
from urllib.parse import urlparse
import email_normalize
from url_normalize import url_normalize
import phonenumbers
from cleanco import prepare_terms, basename
import pycountry
import distutils
import distutils.util




def url( value):
    """ FUNCTION DESCRIPTION
    """
    try:
        return url_normalize(value)


    except:
        print('error')
        return None


def email( value):

    try: 
        return email_normalize.normalize(value).normalized_address
    except:
        return None


def phone( value):
    
    try:
        x = phonenumbers.parse(value, "CA")

        if phonenumbers.is_valid_number(x):
            return phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            return None

    except:
        None


def address( value):

    return


def organization( value = None):

    terms = prepare_terms()
    return basename(value, terms, prefix=False, middle=False, suffix=True)

    
def country( value = None):


    if not isinstance(value, str):
        return None

    if len(value) == 2:
        country = pycountry.countries.get(alpha_2=value)
        if country:
            return country.alpha_2

    elif len(value) == 3:
        country = pycountry.countries.get(alpha_3=value)
        if country:
            return country.alpha_2

    else:
        country = pycountry.countries.get(name=value)
        if country:
            return country.alpha_2  

    return None


def bool( value = None):
    if value:
        value = value
    
    try:
        value = bool(distutils.util.strtobool(value))
    except:
        pass

    if not isinstance(value, bool):
        value = None

    return value

def date(value = None):

    return value