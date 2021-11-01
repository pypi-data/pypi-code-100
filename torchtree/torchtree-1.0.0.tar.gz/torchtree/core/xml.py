import xml.etree.ElementTree as ET

from torchtree.core.utils import JSONParseError, get_class

xml_to_type = {
    'alignment': 'torchtree.evolution.Alignment',
    'patterns': 'torchtree.evolution.SitePattern',
    'taxa': 'torchtree.evolution.Taxa',
    'taxon': 'torchtree.evolution.Taxon',
}


def process_objects(data: ET.Element, dic: dict):
    if isinstance(data, list):
        return [process_object(obj, dic) for obj in data]
    else:
        return process_object(data, dic)


def process_object(data: ET.Element, dic: dict):
    if isinstance(data, ET.Element):
        if 'idref' in data.attrib:
            return dic[data.attrib['id']]

        id_ = data.attrib['id']
        if id_ in dic:
            raise JSONParseError('Object with ID `{}\' already exists'.format(id_))
        # if 'type' not in data:
        #     raise JSONParseError(
        #         'Object with ID `{}\' does not have a type'.format(id_)
        #     )

        try:
            klass = get_class(xml_to_type[data.tag])
        except ModuleNotFoundError as e:
            raise JSONParseError(str(e) + " in object with ID '" + id_ + "'") from None
        except AttributeError as e:
            raise JSONParseError(str(e) + " in object with ID '" + id_ + "'") from None

        obj = klass.from_xml_safe(data, dic)
        dic[id_] = obj
    else:
        raise JSONParseError(
            'Object is not valid (should be str or object)\nProvided: {}'.format(data)
        )
    return obj


# should got in utils
# @classmethod
# @abc.abstractmethod
# def from_xml(cls, data, dic):
#     ...
#
# @classmethod
# def from_xml_safe(cls, data, dic):
#     try:
#         return cls.from_xml(data, dic)
#     except JSONParseError as e:
#         logging.error(e)
#         raise JSONParseError("Calling object with ID '{}'".format(data['id']))
