# These namespaces are the most commonly used in digital publishing workflows.
# (Additional namespaces may be defined on individual document types, such as DOCX.)

NAMESPACES = {
    # XML base
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    # XHTML, EPUB, and related
    'html': 'http://www.w3.org/1999/xhtml',
    'opf': 'http://www.idpf.org/2007/opf',
    'container': 'urn:oasis:names:tc:opendocument:xmlns:container',
    'epub': 'http://www.idpf.org/2007/ops',
    'ncx': 'http://www.daisy.org/z3986/2005/ncx/',
    # Dublin Core and related
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'dcmitype': 'http://purl.org/dc/dcmitype/',
    # MathML and DocBook
    'math': 'http://www.w3.org/1998/Math/MathML',
    'db': 'http://docbook.org/ns/docbook',
    # InDesign XML
    'aid': 'http://ns.adobe.com/AdobeInDesign/4.0/',
    'aid5': 'http://ns.adobe.com/AdobeInDesign/5.0/',
    # Microsoft
    'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
    # Publishing XML
    'pub': 'http://publishingxml.org/ns',
    # EXSLT
    're': 'http://exslt.org/regular-expressions',
}

# Provide a mapping from namespace values to their commonly-used prefixes.

NAMESPACE_PREFIXES = {val: key for key, val in NAMESPACES.items()}
