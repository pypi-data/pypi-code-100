class MuzzleError(Exception):
    """
    General muzzle error class to provide a superclass for all other errors
    """


class XMLParserError(MuzzleError):
    """
    Error when parsing XML
    """
